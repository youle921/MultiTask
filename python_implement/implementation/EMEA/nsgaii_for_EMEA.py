# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 22:04:37 2020

@author: t.urita
"""
import numpy as np

from ..NSGAII.nsgaii_main import NSGAII
from ..NSGAII.NSGA_util import calc_cd, NDsorting

class NSGAII_EMEA(NSGAII):

    def __init__(self, ndim, nobj, npop, noff, problem, code, maxeval):

        super().__init__(ndim, nobj, npop, noff, problem, code)

        self.maxeval = maxeval
        self.offs = {}
        self.parents = [np.empty([noff, ndim]), np.empty([noff, ndim])]

    def execute(self, ngen):

        for i in range(ngen):

            parents = self.selection()

            self.offs["variables"] = self.mutation(self.crossover(parents))
            self.offs["objectives"] = self.problem.evaluate(self.offs["variables"])
            self.update(self.offs)

    def migration_gen(self, mig):

        injected_pop = {}
        nmig = mig.shape[0]
        injected_pop["variables"] = np.clip(mig, self.problem.lower, self.problem.upper)
        injected_pop["objectives"] = self.eval_method(injected_pop["variables"])

        self.injection(self, injected_pop)

        parents = self.selection()

        self.offs["variables"] = self.mutation(self.crossover(parents))[nmig:]
        self.offs["objectives"] = self.problem.evaluate(self.offs["variables"])
        self.update(self.offs)

    def injection(self, injected_pop):

        union = self.concat_pops(injected_pop)

        r = NDsorting(union["objectives"], union["objecives"].shape[0])

        offset = 0
        for i in range(max(r) + 1):

            n = sum(r == i)

            self.pop["objectives"][offset:offset + n] = union["objectives"][r == i]
            self.pop["variables"][offset:offset + n] = union["variables"][r == i]
            self.pop["pareto_rank"][offset:offset + n] = i
            self.pop["crowding_distance"][offset:offset + n] = calc_cd(union["objectives"][r == i])

            offset +=n