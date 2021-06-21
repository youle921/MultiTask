# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 22:04:37 2020

@author: t.urita
"""
import numpy as np

from ..NSGAII.nsgaii_main import NSGAII
# from ..operator import *
# from ..NSGAII.NSGA_util import NDsorting, calc_cd, mating
from ..NSGAII.NSGA_util import mating

class nsgaii_SBMS_eval_base(NSGAII):

    def __init__(self, ndim, nobj, npop, noff, problem, code, maxeval):

        super().__init__(ndim, nobj, npop, noff, problem, code)

        self.maxeval = maxeval
        self.offs = {}
        self.parents = [np.empty([noff, ndim]), np.empty([noff, ndim])]

    def execute(self):

        n_eval = self.pop["objectives"].shape[0]
        if self.neval
        for i in range(gen):

            parents = self.selection()

            self.offs["variables"] = self.mutation(self.crossover(parents))
            self.offs["objectives"] = self.problem.evaluate(self.offs["variables"])
            self.update(self.offs)

    def migration_gen(self, base, mig):

        size = self.noff - base.shape[0]
        self.parents[0][:base.shape[0]] = base
        self.parents[1][:base.shape[0]] = mig

        for i in range(2):
            self.parents[i][base.shape[0]:] = self.select_parent(size)

        self.offs["variables"] = self.mutation(self.crossover(self.parents))[:self.noff]
        self.offs["objectives"] = self.problem.evaluate(self.offs["variables"])

        self.update(self.offs)

    def select_parent(self, size):

        parent = mating(self.pop["pareto_rank"], self.pop["crowding_distance"], \
                         size)

        return self.pop["variables"][parent]