# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 22:04:37 2020

@author: youle
"""
import numpy as np

from ..NSGAII.nsgaii_main import NSGAII

class nsgaii_for_all_migration(NSGAII):

    def __init__(self, params, problem):

        super().__init__(params, problem)

    def execute(self, gen):

        for i in range(gen):

            parents = self.selection()

            self.offs["variables"] = self.mutation(self.crossover(parents))
            self.offs["objectives"] = self.eval_method(self.offs["variables"])
            self.update(self.offs)

    def migration(self, migrated):

        mig_pop = {}

        mig_pop["variables"] = migrated["variables"].copy()
        mig_pop["objectives"] = self.eval_method(mig_pop["variables"])

        self.update(mig_pop)
