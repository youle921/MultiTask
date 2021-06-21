# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:54:46 2020

@author: t.urita
"""
from .nsgaii_for_migration import nsgaii_for_all_migration

class MT_all_mig:

    def __init__(self, ndim, nobj, npop, noff, problem_list, code):

        self.algs = []
        for task in problem_list:
            self.algs.append(nsgaii_for_all_migration(ndim, nobj, npop, noff, task, code))

    def init_pop(self):

        for alg in self.algs:
            alg.init_pop()

    def execute(self, max_gen):

        for g in range(max_gen):

            n_tasks = len(self.algs)
            [*map(lambda alg: alg.execute(1), self.algs)]

            for i in range(n_tasks):

                self.algs[i].migration(self.algs[n_tasks - i - 1].pop)

        return