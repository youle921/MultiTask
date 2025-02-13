# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 22:04:37 2020

@author: youle
"""
import numpy as np

from ..NSGAII.nsgaii_main import NSGAII
from ..NSGAII.NSGA_util import calc_cd, NDsorting

class NSGAII_EMTIL(NSGAII):

    def __init__(self, params, problem, ndim):

        super().__init__(params, problem, ndim)

        self.offs = {}

    def execute(self, ngen):

        for _ in range(ngen):

            parents = self.selection()

            self.offs["variables"] = self.mutation(self.crossover(parents, lower = self.lb, upper = self.ub), \
                                                   lower = self.lb, upper = self.ub)
            self.offs["objectives"] = self.eval_method(self.offs["variables"])
            self.update(self.offs)

    def migration_gen(self, mig):

        nmig = mig.shape[0]
        
        injected_pop = {}
        injected_pop["variables"] = mig
        injected_pop["objectives"] = self.eval_method(injected_pop["variables"])

        self.injection(injected_pop)

        parents = self.selection()

        self.offs["variables"] = self.mutation(self.crossover(parents))[nmig:]
        # self.offs["variables"] = self.mutation(self.crossover(parents))
        self.offs["objectives"] = self.eval_method(self.offs["variables"])

        self.split_injected_pop()
        self.offs = self.concat_pops(self.offs, injected_pop)

        self.update(self.offs)

    def split_injected_pop(self):

        self.pop["objectives"] = self.pop["objectives"][:self.npop]
        self.pop["variables"] = self.pop["variables"][:self.npop]
        self.pop["pareto_rank"] = np.empty(self.npop)
        self.pop["crowding_distance"] = np.empty(self.npop)

    def injection(self, injected_pop):

        union = self.concat_pops(self.pop, injected_pop)
        n_union = union["objectives"].shape[0]

        self.pop["variables"] = union["variables"]
        self.pop["objectives"] = union["objectives"]

        r = NDsorting(union["objectives"], n_union)
        self.pop["pareto_rank"] = r

        self.pop["crowding_distance"] = np.empty_like(self.pop["pareto_rank"])

        for i in range(max(r) + 1):

            self.pop["crowding_distance"][r == i] = calc_cd(self.pop["objectives"][r == i])
