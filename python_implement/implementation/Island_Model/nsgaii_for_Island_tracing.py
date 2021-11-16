# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 22:04:37 2020

@author: youle
"""
import numpy as np

from ..NSGAII.nsgaii_main_tracing import NSGAII_tracing
from ..NSGAII.NSGA_util import calc_cd, NDsorting, mating

class NSGAII_Island_tracing(NSGAII_tracing):

    def init_pop(self):

        super().init_pop()
        self.mating_pool = dict(
                        variables = np.empty_like(self.pop["variables"]),
                        objectives = np.empty_like(self.pop["objectives"]),
                        pareto_rank = np.empty_like(self.pop["pareto_rank"]),
                        crowding_distance = np.empty_like(self.pop["crowding_distance"])
                        )

        self.logger()
        self.offs = {}

        self.trace_log = []

    def execute(self, ngen):

        for _ in range(ngen):

            parents = self._selection()

            self.offs["variables"] = self.mutation(self.crossover(parents))
            self.offs["objectives"] = self.eval_method(self.offs["variables"])
            self.trace_log.append(self._update(self.offs, np.ones(self.noff)))

            self.logger()

    def migration_gen(self, mig):

        injected_pop = {}
        injected_pop["variables"] = mig
        injected_pop["objectives"] = self.eval_method(injected_pop["variables"])

        parents = self._selection_mig_gen(injected_pop)

        inter_cross = np.isin(parents, injected_pop["variables"]).min(axis = 2).reshape(-1) + 1

        self.offs["variables"] = self.mutation(self.crossover(parents))
        self.offs["objectives"] = self.eval_method(self.offs["variables"])

        self.offs = self.concat_pops(self.offs, injected_pop)

        self.trace_log.append(self._update(self.offs, np.hstack([inter_cross, [3] * mig.shape[0]])))

        self.logger()

    def _selection_mig_gen(self, mig):

        # create mating pool
        internal_size = self.npop - mig["objectives"].shape[0]

        rank = np.argsort(self.pop["pareto_rank"] + 1 / (1 + self.pop["crowding_distance"]))
        mask = rank < internal_size

        self.mating_pool["objectives"][:internal_size] = self.pop["objectives"][mask]
        self.mating_pool["variables"][:internal_size] = self.pop["variables"][mask]

        self.mating_pool["objectives"][internal_size:] = mig["objectives"]
        self.mating_pool["variables"][internal_size:] = mig["variables"]

        self.mating_pool["pareto_rank"] = NDsorting(self.mating_pool["objectives"], self.npop)
        for i in range(self.mating_pool["pareto_rank"].max() + 1):
            self.mating_pool["crowding_distance"][self.mating_pool["pareto_rank"] == i] = \
                calc_cd(self.mating_pool["objectives"][self.mating_pool["pareto_rank"] == i])

        # parent selection
        parents = [self.mating_pool["variables"]\
                   [mating(self.mating_pool["pareto_rank"],self.mating_pool["crowding_distance"],
                           int((self.noff - mig["objectives"].shape[0]) / 2))] for _ in range(2)]

        return parents