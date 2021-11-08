# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 22:04:37 2020

@author: youle
"""
import numpy as np

from ..NSGAII.nsgaii_main_tracing import NSGAII_tracing
from ..NSGAII.NSGA_util import calc_cd, NDsorting

class NSGAII_EMEA_traciing(NSGAII_tracing):

    def __init__(self, params, problem):

        super().__init__(params, problem)

        self.offs = {}

        problem.project_uss = False
        self.lb = problem.lower
        self.ub = problem.upper

    def init_pop(self):

        if self.code == "real":
            self.pop["variables"][...] = np.random.rand(*self.pop["variables"].shape,)\
                                       * (self.ub - self.lb)[None, :] + self.lb[None, :]
        elif self.code == "bin":
            self.pop["variables"][...] = np.random.randint(2, size = self.pop["variables"].shape)

        self.pop["objectives"] = self.eval_method(self.pop["variables"])
        self._init_eval()

        self.neval = self.npop

        self.tarce_log = []

    def execute(self, ngen):

        for _ in range(ngen):

            parents = self._selection()

            self.offs["variables"] = self.mutation(self.crossover(parents), \
                                                   lower = self.lb, upper = self.ub)
            self.offs["objectives"] = self.eval_method(self.offs["variables"])
            self.tarce_log.append(self._update(self.offs, np.ones(self.noff)))

    def migration_gen(self, mig):

        injected_pop = {}
        nmig = mig.shape[0]
        injected_pop["variables"] = np.clip(mig, self.lb, self.ub)
        injected_pop["objectives"] = self.eval_method(injected_pop["variables"])

        self._injection(injected_pop)

        parents = self._selection()
        inter_cross = np.isin(parents, injected_pop).min(axis = 2).max(axis = 0) + 1

        self.offs["variables"] = self.mutation(self.crossover(parents),\
                                               lower = self.lb, upper = self.ub)[nmig:]
        self.offs["objectives"] = self.eval_method(self.offs["variables"])

        self._split_injected_pop()
        self.offs = self.concat_pops(self.offs, injected_pop)

        self.tarce_log.append(self._update(self.offs, np.hstack([inter_cross, [3] * nmig])))
