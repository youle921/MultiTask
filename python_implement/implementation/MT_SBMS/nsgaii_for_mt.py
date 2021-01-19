# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 22:04:37 2020

@author: t.urita
"""
import numpy as np
import matplotlib.pyplot as plt

from ..NSGAII.nsgaii_main import NSGAII
from ..operator import *
from ..NSGAII.NSGA_util import NDsorting, calc_cd, mating

class nsgaii_SBMS_for_mt(NSGAII):

    def __init__(self, ndim, nobj, npop, noff, problem, code, t_num_alpha, t_num_beta):

        super().__init__(ndim, nobj, npop, noff, problem, code)

        # 目的関数空間上で選択する解の個数
        self.alpha = t_num_alpha
        # 決定変数空間上で選択する解の個数
        self.beta = t_num_beta

    def execute(self, gen):

        offs = {}

        for i in range(gen):

            parents = self.selection()

            offs["variables"] = self.mutation(self.crossover(parents))
            offs["objectives"] = self.problem.evaluate(offs["variables"])
            self.update(offs)

    def migration_gen(self, base, mig):

        parents = []

        size = self.noff - base.shape[0]
        idx1 = mating(self.pop["pareto_rank"], self.pop["crowding_distance"], \
                         size)
        parents.append(np.vstack((base, self.pop["variables"][idx1])))

        idx2 = mating(self.pop["pareto_rank"], self.pop["crowding_distance"], \
                         size)
        parents.append(np.vstack((mig, self.pop["variables"][idx2])))

        offs = {}

        offs["variables"] = self.mutation(self.crossover(parents))
        offs["objectives"] = self.problem.evaluate(offs["variables"])

        self.update(offs)

    def selection(self):

        parents = []

        parents.append(self.select_parent_a())
        parents.append(self.select_parent_b(parents[0]))

        return parents

    def select_parent_a(self):

        idx = mating(self.pop["pareto_rank"], self.pop["crowding_distance"], \
                     int(self.noff/2) * self.alpha).reshape([-1, self.alpha])

        candidate = self.pop["objectives"][idx]
        center = candidate.mean(axis = 1)
        dist = ((candidate - center[:, None, :])**2).sum(axis = 2)

        parents = idx[range(idx.shape[0]), dist.argmax(axis = 1)]

        return self.pop["variables"][parents]

    def select_parent_b(self, parent_a):

        idx = mating(self.pop["pareto_rank"], self.pop["crowding_distance"], \
                     parent_a.shape[0] * self.beta).reshape([-1, self.beta])

        dist = ((self.pop["variables"][idx] - parent_a[:, None, :])**2).sum(axis = 2)

        parents = idx[range(idx.shape[0]), dist.argmin(axis = 1)]

        return self.pop["variables"][parents]

    def select_parent(self, size):

        parent = mating(self.pop["pareto_rank"], self.pop["crowding_distance"], \
                         size)

        return self.pop["variables"][parent]
