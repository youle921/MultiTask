# -*- coding: utf-8 -*-

import numpy as np
from .nsgaii_for_EMEA import NSGAII_EMEA

class EMEA:

    def __init__(self, params, problem_list):

        self.interval = params["interval"]
        self.mig_size = params["migration_size"]

        self.algs = []
        ndim = max([p.ndim for p in problem_list])
        for task in problem_list:
            self.algs.append(NSGAII_EMEA(params, task, ndim = ndim))

        self.matrix = [[] for i in range(len(problem_list))]

    def init_pop(self):

        for alg in self.algs:
            alg.init_pop()

        self.learn_matrix()

    def execute(self, max_gen):

        n_tasks = len(self.algs)
        gen = 1

        while gen < max_gen:

            for g in range(self.interval - 1):

                [*map(lambda alg: alg.execute(self.interval - 1), self.algs)]

                for i in range(n_tasks):

                    self.algs[i].migration(self.algs[n_tasks - i - 1].offs)

            injected_pop = []
            [self.algs[i].migration_gen(injected_pop[i]) for i in range(len(self.algs))]
            [*map(lambda alg: alg.migration_gen(self.interval - 1), self.algs)]

        return

    def learn_matrix(self):

        for alg_idx in range(len(self.algs)):
            for source_obj in range(self.algs[alg_idx].pop["objectives"].shape[1]):

                W_list = []

                for target_obj in range(self.algs[1 - alg_idx].pop["objectives"].shape[1]):

                    sorted_idx = self.algs[alg_idx].pop["objectives"][:, source_obj].argsort()
                    source_pop = self.algs[alg_idx].pop["variables"][sorted_idx]

                    sorted_idx = self.algs[1 - alg_idx].pop["objectives"][:, target_obj].argsort()
                    target_pop = self.algs[1 - alg_idx].pop["variables"][sorted_idx]

                    d1 = source_pop.shape[1]
                    d2 = target_pop.shape[1]

                    if d1 != d2:
                        if d1 > d2:
                            target_pop = self.padding_pop(target_pop, d1)
                        else:
                            source_pop = self.padding_pop(source_pop, d2)

                    xx = target_pop.T
                    noise = source_pop.T

                    d, n = xx.shape
                    xxb = np.ones(d + 1, n)
                    xxb[:d] = xx
                    noise_xb = np.ones_like(xxb)
                    noise_xb[:d] = noise

                    Q = np.dot(noise_xb, noise_xb.T)
                    P = np.dot(xxb , noise_xb.T)

                    reg = 1e-5 * np.eye(d + 1)
                    reg[-1, -1] = 0
                    W = np.dot(P, np.linalg.inv(Q + reg))

                    W_list.append(W[:d, :d])
                self.matrix[alg_idx].append(W_list)

        return

    def padding_pop(self, target, dim):

        padded_pop = np.zeros([target.shape[0], dim])
        padded_pop[:, :target.shape[1]] = target

        return padded_pop