# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:54:46 2020

@author: t.urita
"""
import numpy as np

from ..NSGAII.NSGA_util import NDsorting, calc_cd
from ..operator import *

class MOMFEA:

    def __init__(self, params, problem_list):

        ndim = max([p.ndim for p in problem_list])

        self.problems = problem_list
        self.ntask = len(problem_list)

        self.npop = params["npop"]
        self.noff = params["noff"]

        self.pops = dict(
                         variables = np.empty([self.ntask, self.npop, ndim]), \
                         objectives = [None] * self.ntask, \
                         pareto_rank = np.empty([self.ntask, self.npop]), \
                         crowding_distance = np.empty([self.ntask, self.npop]), \
                         factorial_rank = np.empty([self.ntask, self.npop])
                         )

        self.code = problem_list[0].code
        self.rmp = 0.9
        if "rmp" in params:
            self.rmp = params["rmp"]

        if self.code == "real":
            self.crossover = SBX
            self.mutation = PM
        elif self.code == "bin":
            self.crossover = uniform_crossover
            self.mutation = bitflip_mutation

    def init_pop(self):

        if self.code == "real":
            self.pops["variables"][...] = np.random.rand(*self.pops["variables"].shape,)
        elif self.code == "bin":
            self.pops["variables"][...] = np.random.randint(2, size = self.pops["variables"].shape)

        for i, p in enumerate(self.problems):

            self.pops["objectives"][i] = p.evaluate(self.pops["variables"][i])
            self._init_eval(i)

        self._set_factorial_rank()
        self.neval = self.npop* self.ntask

    def _init_eval(self, sf):

        r = NDsorting(self.pops["objectives"][sf], self.npop)
        self.pops["pareto_rank"][sf] = r

        for i in range(max(r) + 1):
            self.pops["crowding_distance"][sf][r == i] = calc_cd(self.pops["objectives"][sf][r == i])

    def execute(self, max_eval):

        n, mod= divmod(max_eval - self.neval, self.noff * self.ntask)

        offs = {}
        assigned_offs = {}

        parents = np.empty([2, int(self.noff * self.ntask * 0.5), self.pops["variables"].shape[2]])
        skill_factor = np.empty(parents.shape[:2], dtype = int)

        for gen in range(n):

            for t_idx in range(2):

                p, skill_factor[t_idx]= self._mfea_selection()
                parents[t_idx] = self.pops["variables"][skill_factor[t_idx], p]

            offs["variables"], offs["skill_factor"] = self._mfea_crossover(parents, skill_factor)

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

    def _set_factorial_rank(self):

        cost = self.pops["pareto_rank"] + 1/(1 + self.pops["crowding_distance"])
        idx = cost.argsort(axis = 1).flatten()
        self.pops["factorial_rank"][np.repeat(np.arange(cost.shape[0]), cost.shape[1]), idx] = np.tile(np.arange(cost.shape[1]), cost.shape[0])

        return

    def _mfea_selection(self):

        rand_idx, sf = np.divmod(np.random.randint(self.npop * self.ntask, size = [int(self.noff*self.ntask*0.5), 2]), self.ntask)
        idx = self.pops["factorial_rank"][sf, rand_idx].argmin(axis = 1)

        return rand_idx[range(sf.shape[0]), idx], sf[range(sf.shape[0]), idx]

    def _mfea_crossover(self, parents, sf):

        offs = parents.copy()

        do_cross = (np.random.rand(*sf[0].shape,) < self.rmp) | (sf[0] == sf[1])
        offs[:, do_cross] = np.split(self.crossover([parents[0][do_cross], parents[1][do_cross]]), 2)
        offs = offs.reshape([np.prod(offs.shape[:2]), -1])

        offs_sf = np.vstack([sf[0], sf[1]])

        mask = (np.random.rand(*offs_sf.shape,) < 0.5)[:, do_cross]

        offs_sf[0][do_cross][mask[0]] = sf[1][do_cross][mask[0]]
        offs_sf[1][do_cross][mask[1]] = sf[0][do_cross][mask[1]]

        return self.mutation(offs), offs_sf.reshape([-1])

    def _update(self, offs, sf):

        union = {}
        
        union["variables"] = np.vstack((self.pops["variables"][sf] ,offs["variables"]))
        union["objectives"] = np.vstack((self.pops["objectives"][sf], offs["objectives"]))

        r = NDsorting(union["objectives"], self.npop)

        offset = 0
        for i in range(max(r)):

            n = sum(r == i)

            self.pops["objectives"][sf][offset:offset + n] = union["objectives"][r == i]
            self.pops["variables"][sf][offset:offset + n] = union["variables"][r == i]
            self.pops["pareto_rank"][sf][offset:offset + n] = i
            self.pops["crowding_distance"][sf][offset:offset + n] = calc_cd(union["objectives"][r == i])

            offset +=n

        cd = calc_cd(union["objectives"][r == max(r)])
        remain = np.argsort(-cd)[:self.npop - offset]

        self.pops["objectives"][sf][offset:] = union["objectives"][r == max(r)][remain]
        self.pops["variables"][sf][offset:] = union["variables"][r == max(r)][remain]
        self.pops["pareto_rank"][sf][offset:] = max(r)
        self.pops["crowding_distance"][sf][offset:] = calc_cd(self.pops["objectives"][sf][offset:])
