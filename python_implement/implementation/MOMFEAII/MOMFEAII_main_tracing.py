# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:54:46 2020

@author: t.urita
"""
import numpy as np

import scipy.optimize as opt

from . import MOMFEAII
from ..NSGAII.NSGA_util import NDsorting, calc_cd

def norm_dist(x, mu, var, eps = 1e-8):

    return (1 / (np.sqrt(2 * np.pi * var + eps))) * np.exp(-1 * ((x - mu)**2 / (2 * var + eps)))

def loglik(rmp, probmatrix):

    ntasks = probmatrix.shape[2]

    factor = np.full([ntasks, ntasks], 0.5 * (ntasks - 1) * rmp / ntasks)
    factor[np.diag_indices(ntasks)] = 1 - factor[np.diag_indices(ntasks)]

    f = (-np.log((probmatrix * factor[:, None, :]).sum(axis = 2)).sum())

    return f

class MOMFEAII_tracing(MOMFEAII):

    def execute(self, max_eval):

        self.logger()

        n, mod= divmod(max_eval - self.neval, self.noff * self.ntask)
        trace_log = np.empty([2, n, self.npop], dtype = int)

        self.offs = dict(
                         variables = np.empty([self.noff * self.ntask,
                                               self.pops["variables"].shape[-1]]),
                         skill_factor = np.empty([self.noff * self.ntask])
                         )

        assigned_offs = {}

        parents = np.empty([2, int(self.noff * self.ntask * 0.5), self.pops["variables"].shape[2]])
        skill_factor = np.empty(parents.shape[:2], dtype = int)
        p_idx = np.empty_like(skill_factor)

        for gen in range(n):

            self._learn_rmp()
            self._set_factorial_rank()

            for t_idx in range(2):

                p_idx[t_idx], skill_factor[t_idx]= self._mfea_selection()
                parents[t_idx] = self.pops["variables"][skill_factor[t_idx], p_idx[t_idx]]

            self.offs["variables"][...], self.offs["skill_factor"][...], inter_cross = self._mfeaii_crossover(p_idx, parents, skill_factor)

            for task_no, p in enumerate(self.problems):

                assigned_offs["variables"] = self.offs["variables"][self.offs["skill_factor"] == task_no]
                assigned_offs["objectives"] = p.evaluate(assigned_offs["variables"])

                trace_log[task_no, gen] = self._update(assigned_offs, task_no, inter_cross[self.offs["skill_factor"] == task_no])

            self.logger()

        if mod != 0:

            for t_idx in range(2):

                p, skill_factor[t_idx] = self._mfea_selection()
                parents[t_idx] = self.pops["variables"][skill_factor[t_idx], p]

            self.offs["variables"][...], self.offs["skill_factor"][...] = self._mfeaii_crossover(p_idx, parents, skill_factor)
            self.offs["skill_factor"][mod:] = -1

            for task_no, p in enumerate(self.problems):
                assigned_offs["variables"] = self.offs["variables"][self.offs["skill_factor"] == task_no]
                assigned_offs["objectives"] = p.evaluate(assigned_offs["variables"])

                self._update(assigned_offs, task_no)

            self.logger()

        self.neval = max_eval

        return trace_log

    def _mfeaii_crossover(self, p_idx, parents, sf):

        offs = np.empty_like(parents)

        do_cross = (np.random.rand(*sf[0].shape,) < self.rmp) | (sf[0] == sf[1])
        no_cross = ~do_cross
        offs[:, do_cross] = np.split(self.crossover(parents[:, do_cross]), 2)

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

        inter_cross = np.ones_like(offs_sf)
        inter_cross[:, (sf[0] != sf[1]) & do_cross] = 2

        return self.mutation(offs), offs_sf.reshape(-1), inter_cross.reshape(-1)
    
    def _update(self, offs, sf, inter_cross):

        union = self.concat_pops({"variables":self.pops["variables"][sf], "objectives":self.pops["objectives"][sf]}, offs)
        tmp = np.hstack([[0] * self.npop, inter_cross])
        trace = np.empty(self.npop, dtype = int)
        r = NDsorting(union["objectives"], self.npop)

        offset = 0
        for i in range(max(r)):

            n = sum(r == i)

            self.pops["objectives"][sf][offset:offset + n] = union["objectives"][r == i]
            self.pops["variables"][sf][offset:offset + n] = union["variables"][r == i]
            self.pops["pareto_rank"][sf][offset:offset + n] = i
            self.pops["crowding_distance"][sf][offset:offset + n] = calc_cd(union["objectives"][r == i])
            trace[offset:offset + n] = tmp[r == i]
            offset +=n

        cd = calc_cd(union["objectives"][r == max(r)])
        remain = np.argsort(-cd)[:self.npop - offset]

        self.pops["objectives"][sf][offset:] = union["objectives"][r == max(r)][remain]
        self.pops["variables"][sf][offset:] = union["variables"][r == max(r)][remain]
        self.pops["pareto_rank"][sf][offset:] = max(r)
        self.pops["crowding_distance"][sf][offset:] = calc_cd(self.pops["objectives"][sf][offset:])
        trace[offset:] = tmp[r == max(r)][remain]

        return trace

