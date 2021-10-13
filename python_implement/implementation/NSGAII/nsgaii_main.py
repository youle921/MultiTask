# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 22:04:37 2020

@author: youle
"""
import numpy as np

from ..base_class.EMOA_base import Algorithm
from ..operator import *
from .NSGA_util import NDsorting, calc_cd, mating


class NSGAII(Algorithm):
    def __init__(self, params, problem, ndim=None):

        if ndim == None:
            ndim = problem.ndim

        self.pop = {}
        self.pop["variables"] = np.empty([params["npop"], ndim])
        self.pop["crowding_distance"] = np.empty(params["npop"])

        self.code = problem.code
        self.eval_method = problem.evaluate

        self.npop = params["npop"]
        self.noff = params["noff"]

        self.offs = {}

        if self.code == "real":
            self.crossover = SBX
            self.mutation = PM
            self.concat_pops = self.create_union

        elif self.code == "bin":
            self.crossover = uniform_crossover
            self.mutation = bitflip_mutation
            self.concat_pops = self.create_unique_union

    def init_pop(self):

        if self.code == "real":
            self.pop["variables"][...] = \
                np.random.rand(*self.pop["variables"].shape,)

        elif self.code == "bin":
            self.pop["variables"][...] = \
                np.random.randint(2, size=self.pop["variables"].shape)

        self.pop["objectives"] = self.eval_method(self.pop["variables"])
        self._init_eval()

        self.neval = self.npop

    def _init_eval(self):

        r = NDsorting(self.pop["objectives"], self.npop)
        self.pop["pareto_rank"] = r

        for i in range(max(r) + 1):

            self.pop["crowding_distance"][r == i] = calc_cd(
                self.pop["objectives"][r == i])

    def execute(self, max_eval):

        n, mod = divmod(max_eval - self.neval, self.noff)

        for i in range(n):

            parents = self._selection()

            self.offs["variables"] = self.mutation(self.crossover(parents))
            self.offs["objectives"] = self.eval_method(self.offs["variables"])
            self._update(self.offs)

        if mod != 0:

            parents = self._selection()

            self.offs["variables"] = self.mutation(self.crossover(parents[:mod]))
            self.offs["objectives"] = self.eval_method(self.offs["variables"])
            self._updata(self.offs)

        self.neval = max_eval

    def _selection(self):

        parents = [self.pop["variables"]\
                   [mating(self.pop["pareto_rank"],self.pop["crowding_distance"],
                           int(self.noff / 2))] for _ in range(2)]

        return parents

    def _update(self, offs):

        union = self.concat_pops(self.pop, offs)

        r = NDsorting(union["objectives"], self.npop)

        offset = 0
        for i in range(max(r)):

            n = sum(r == i)

            self.pop["objectives"][offset: offset + n] = union["objectives"][r == i]
            self.pop["variables"][offset: offset + n] = union["variables"][r == i]
            self.pop["pareto_rank"][offset: offset + n] = i
            self.pop["crowding_distance"][offset: offset + n] = calc_cd(union["objectives"][r == i])

            offset += n
        cd = calc_cd(union["objectives"][r == max(r)])
        remain = np.argsort(-cd)[: self.npop - offset]

        self.pop["objectives"][offset:] = union["objectives"][r ==max(r)][remain]
        self.pop["variables"][offset:] = union["variables"][r ==max(r)][remain]
        self.pop["pareto_rank"][offset:] = max(r)
        self.pop["crowding_distance"][offset:] = calc_cd(self.pop["objectives"][offset:])
