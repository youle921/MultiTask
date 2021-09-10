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
        self.neval =  self.npop* self.ntask

    def _init_eval(self, sf):

        r = NDsorting(self.pops["objectives"][sf], self.npop)
        self.pops["pareto_rank"][sf] = r

        for i in range(max(r) + 1):
            self.pops["crowding_distance"][sf][r == i] = calc_cd(self.pops["objectives"][sf][r == i])

    def execute(self, max_eval):


        n, mod= divmod(max_eval - self.neval, self.noff * self.ntask)

        offs = {}
        for gen in range(n):

            parents = []
            skill_factor = []

            for t_size in range(2):
                p, sf = self._mfea_selection()
                parents.append(self.pops["variables"][sf, p])
                skill_factor.append(sf)

            offs["variables"], offs["skill_factor"]= self._mfea_crossover(parents, skill_factor)

            for task_no, p in enumerate(self.problems):

                off = {}
                mask = offs["skill_factor"] == task_no
                off["variables"] = offs["variables"][mask]
                off["objectives"] = p.evaluate(off["variables"])
                self._update(off, task_no)

            self._set_factorial_rank()

        if mod != 0:

            parents = []
            parents.append(self.pops["variables"][self.selection()])
            parents.append(self.pops["variables"][self.selection()])

            offs["variables"] = self.mutation(self.crossover(parents))
            offs["objectives"][:mod] = self.problem.evaluate(offs["variables"][:mod])
            offs["objectives"][mod:] = 0
            self.update(offs)

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

        inner_cross = sf[0] == sf[1]
        inter_cross = ~inner_cross & (np.random.rand(parents[0].shape[0]) < self.rmp)
        inter_mu = ~inner_cross != inter_cross

        inner_offs = np.split(self.crossover([parents[0][inner_cross], parents[1][inner_cross]]), 2)
        inter_offs = np.split(self.crossover([parents[0][inter_cross], parents[1][inter_cross]]), 2)
        no_cross = [parents[0][inter_mu], parents[1][inter_mu]]

        offs = np.vstack([inner_offs[0], inter_offs[0], no_cross[0], \
                          inner_offs[1], inter_offs[1], no_cross[1]])

        offs_sf = np.vstack([sf[0], sf[1]])

        no_cross_len = no_cross[0].shape[0]
        mask = (np.random.rand(*offs_sf.shape,) < 0.5)[:, :-no_cross_len]

        offs_sf[0][:-no_cross_len][mask[0]] = sf[1][:-no_cross_len][mask[0]]
        offs_sf[1][:-no_cross_len][mask[1]] = sf[0][:-no_cross_len][mask[1]]

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
