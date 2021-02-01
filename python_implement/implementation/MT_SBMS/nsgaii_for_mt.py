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

class nsgaii_SBMS_for_mt(NSGAII):

    def __init__(self, ndim, nobj, npop, noff, problem, code, t_num_alpha, t_num_beta):

        super().__init__(ndim, nobj, npop, noff, problem, code)

        # 目的関数空間上で選択する解の個数
        self.alpha = t_num_alpha
        # 決定変数空間上で選択する解の個数
        self.beta = t_num_beta

        self.offs = {}
        self.parents = [np.empty([noff, ndim]), np.empty([noff, ndim])]

    def execute(self, gen):

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

    def selection(self):

        parents = []

        parents.append(self.select_parent_a(self.alpha))
        parents.append(self.select_parent_b(parents[0], self.beta))

        return parents

    def select_parent_a(self, size):

        idx = mating(self.pop["pareto_rank"], self.pop["crowding_distance"], \
                     int(self.noff/2) * size).reshape([-1, size])

        candidate = self.pop["objectives"][idx]
        center = candidate.mean(axis = 1)
        dist = ((candidate - center[:, None, :])**2).sum(axis = 2)

        parent = idx[range(idx.shape[0]), dist.argmax(axis = 1)]

        return self.pop["variables"][parent]

    def select_parent_b(self, parent_a, size):

        idx = mating(self.pop["pareto_rank"], self.pop["crowding_distance"], \
                     parent_a.shape[0] * size).reshape([-1, size])

        dist = ((self.pop["variables"][idx] - parent_a[:, None, :])**2).sum(axis = 2)

        parent = idx[range(idx.shape[0]), dist.argmin(axis = 1)]

        return self.pop["variables"][parent]

    def select_parent(self, size):

        parent = mating(self.pop["pareto_rank"], self.pop["crowding_distance"], \
                         size)

        return self.pop["variables"][parent]

    def select_nn_parent(self, parent_a):

        """
        todo parent_aと最近傍の個体を探索
        各個体と最近傍のbを親個体としてreturn
        """
        idx = ((parent_a[:, None, :] - self.pop["variables"][None, :, : ])**2).sum(axis = 2).argmax(axis = 1)

        return self.pop["variables"][idx]
