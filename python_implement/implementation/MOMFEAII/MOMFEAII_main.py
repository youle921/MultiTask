# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:54:46 2020

@author: t.urita
"""
import numpy as np

import scipy.optimize as opt

from ..MOMFEA import MOMFEA

def norm_dist(x, mu, var, eps = 1e-8):

    return (1 / (np.sqrt(2 * np.pi * var + eps))) * np.exp(-1 * ((x - mu)**2 / (2 * var + eps)))

def loglik(rmp, probmatrix):

    ntasks = probmatrix.shape[2]

    factor = np.full([ntasks, ntasks], 0.5 * (ntasks - 1) * rmp / ntasks)
    factor[np.diag_indices(ntasks)] = 1 - factor[np.diag_indices(ntasks)]

    f = (-np.log((probmatrix * factor[:, None, :]).sum(axis = 2)).sum())

    return f

class MOMFEAII(MOMFEA):

    def execute(self, max_eval):

        n, mod= divmod(max_eval - self.neval, self.noff * self.ntask)

        offs = {}
        assigned_offs = {}

        parents = np.empty([2, int(self.noff * self.ntask * 0.5), self.pops["variables"].shape[2]])
        skill_factor = np.empty(parents.shape[:2], dtype = int)
        p_idx = np.empty_like(skill_factor)

        for gen in range(n):

            self._learn_rmp()

            for t_idx in range(2):

                p_idx[t_idx], skill_factor[t_idx]= self._mfea_selection()
                parents[t_idx] = self.pops["variables"][skill_factor[t_idx], p_idx[t_idx]]

            offs["variables"], offs["skill_factor"] = self._mfea_crossover(p_idx, parents, skill_factor)

            for task_no, p in enumerate(self.problems):

                assigned_offs["variables"] = offs["variables"][offs["skill_factor"] == task_no]
                assigned_offs["objectives"] = p.evaluate(assigned_offs["variables"])

                self._update(assigned_offs, task_no)

            self._set_factorial_rank()

        # if mod != 0:

        #     parents = []
        #     parents.append(self.pops["variables"][self.selection()])
        #     parents.append(self.pops["variables"][self.selection()])

        #     offs["variables"] = self.mutation(self.crossover(parents))
        #     offs["objectives"][:mod] = self.problem.evaluate(offs["variables"][:mod])
        #     offs["objectives"][mod:] = 0
        #     self.update(offs)

        self.neval = max_eval

        return

    def _mfea_crossover(self, p_idx, parents, sf):

        offs = parents.copy()

        do_cross = (np.random.rand(*sf[0].shape,) < self.rmp) | (sf[0] == sf[1])
        no_cross = ~do_cross
        offs[:, do_cross] = np.split(self.crossover([parents[0][do_cross], parents[1][do_cross]]), 2)

        offs_sf = np.vstack([sf[0], sf[1]])

        inner_idx = np.random.randint(self.npop - 1, size = [2, no_cross.sum()])
        inner_idx[inner_idx >= p_idx[:, no_cross]] += 1
        inner_parent = self.pops["variables"][offs_sf[:, no_cross], inner_idx]

        offs[0, no_cross] = np.split(self.crossover([parents[0][no_cross], inner_parent[0]]), 2)[0]
        offs[1, no_cross] = np.split(self.crossover([parents[1][no_cross], inner_parent[1]]), 2)[0]

        offs = offs.reshape([np.prod(offs.shape[:2]), -1])

        mask = (np.random.rand(*offs_sf.shape,) < 0.5)[:, do_cross]

        offs_sf[0][do_cross][mask[0]] = sf[1][do_cross][mask[0]]
        offs_sf[1][do_cross][mask[1]] = sf[0][do_cross][mask[1]]

        return self.mutation(offs), offs_sf.reshape([-1])

    def _learn_rmp(self):

        noise = np.random.rand(2, int(self.pops["variables"].shape[1] * 0.1), self.pops["variables"].shape[2])

        mean = np.empty([self.ntask, self.pops["variables"].shape[2]])
        var = np.empty_like(mean)

        noise_pop1 = np.array([*self.pops["variables"][0], *noise[0]])
        noise_pop2 = np.array([*self.pops["variables"][1], *noise[1]])

        mean[0] = noise_pop1.mean(axis = 0)
        var[0] = noise_pop1.var(axis = 0, ddof = 1)

        mean[1] = noise_pop2.mean(axis = 0)
        var[1] = noise_pop2.var(axis = 0, ddof = 1)

        probmatrix = np.empty([2, self.npop, 2])

        probmatrix[0] = (norm_dist(self.pops["variables"][:1], mean[:, None, :], var[:, None, :])).prod(axis = 2).T
        probmatrix[1] = (norm_dist(self.pops["variables"][1:], mean[:, None, :], var[:, None, :])).prod(axis = 2).T

        rmp = opt.fminbound(loglik, 0, 1, args = ([probmatrix]))

        self.rmp = np.clip(rmp + np.random.randn() * 0.01, 0, 1)

        return
