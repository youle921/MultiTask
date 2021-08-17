# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:54:46 2020

@author: youle
"""
from .nsgaii_for_migration import nsgaii_for_all_migration

class MT_all_mig:

    def __init__(self, params, problem_list):

        self.algs = []
        ndim = max([p.ndim for p in problem_list])
        for task in problem_list:
            self.algs.append(nsgaii_for_all_migration(params, task, ndim = ndim))

    def init_pop(self):

        for alg in self.algs:
            alg.init_pop()

    def execute(self, max_gen):

        n_tasks = len(self.algs)

        for g in range(max_gen):

            [*map(lambda alg: alg.execute(1), self.algs)]

            for i in range(n_tasks):

                self.algs[i].migration(self.algs[n_tasks - i - 1].offs)

        return