# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:54:46 2020

@author: t.urita
"""
from .nsgaii_for_mt import nsgaii_SBMS_for_mt

class MT_SBMS:

    def __init__(self, ndim, nobj, npop, noff, problem_list, code, alpha, beta, m_size, interval):

        self.algs = []
        for task in problem_list:
            self.algs.append(nsgaii_SBMS_for_mt(ndim, nobj, npop, noff, task, code, alpha, beta))

        self.migration_size = m_size
        self.interval = interval

    def init_pop(self):

        for alg in self.algs:
            alg.init_pop()

    def execute(self, max_gen):

        [*map(lambda alg: alg.execute(self.interval - 2), self.algs)]
        self.migration()

        itr = int(max_gen / self.interval)
        for i in range(itr - 1):

            [*map(lambda alg: alg.execute(self.interval - 1), self.algs)]
            self.migration()

        return

    def execute_nn(self, max_gen):

        [*map(lambda alg: alg.execute(self.interval - 2), self.algs)]
        self.migration_nn()

        itr = int(max_gen / self.interval)
        for i in range(itr - 1):

            [*map(lambda alg: alg.execute(self.interval - 1), self.algs)]
            self.migration_nn()

        return
    
    def execute_custom_migration(self, max_gen, num):

        [*map(lambda alg: alg.execute(self.interval - 2), self.algs)]
        self.custom_migration(num)

        itr = int(max_gen / self.interval)
        for i in range(itr - 1):

            [*map(lambda alg: alg.execute(self.interval - 1), self.algs)]
            self.custom_migration(num)

        return

    def migration(self):

        base_pops = [*map(lambda alg: alg.select_parent(self.migration_size), self.algs)]
        migrated_pops = [*map(lambda alg, p, beta:alg.select_parent_b(p, beta), reversed(self.algs), base_pops, self.algs.beta)]

        [*map(lambda alg, base_p, mig_p: alg.migration_gen(base_p, mig_p), self.algs, base_pops, migrated_pops)]

    def migration_nn(self):

        base_pops = [*map(lambda alg: alg.select_parent(self.migration_size), self.algs)]
        migrated_pops = [*map(lambda alg, p:alg.select_nn_parent(p), reversed(self.algs), base_pops)]

        [*map(lambda alg, base_p, mig_p: alg.migration_gen(base_p, mig_p), self.algs, base_pops, migrated_pops)]

    def custom_migration(self, size):
        
        base_pops = [*map(lambda alg: alg.select_parent(self.migration_size), self.algs)]
        migrated_pops = [*map(lambda alg, p:alg.select_parent_b(p, size), reversed(self.algs), base_pops)]

        [*map(lambda alg, base_p, mig_p: alg.migration_gen(base_p, mig_p), self.algs, base_pops, migrated_pops)]
