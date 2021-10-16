# -*- coding: utf-8 -*-

import numpy as np
from .nsgaii_for_Island import NSGAII_Island

class Island_Model:

    def __init__(self, params, problem_list):

        self.interval = params["interval"]
        self.mig_size = params["migration_size"]

        self.algs = []
        ndim = max([p.ndim for p in problem_list])
        for task in problem_list:
            self.algs.append(NSGAII_Island(params, task, ndim))

    def init_pop(self):

        for alg in self.algs:
            alg.init_pop()

    def execute(self, max_gen):

        pop_size = self.algs[0].pop["variables"].shape[0]

        for g in range(1, max_gen):

            if g % self.interval != 0:
                [alg.execute(1) for alg in self.algs]

            else:
                inject_pop = [alg.pop["variables"][np.random.permutation(pop_size)[:self.mig_size]] for alg in self.algs]
                [self.algs[i].migration_gen(inject_pop[1 - i]) for i in range(len(self.algs))]

        return

    def get_objectives(self):

        return [alg.pop["objectives"] for alg in self.algs]

    def get_NDsolution(self):

        return [alg.pop.get_NDsolution() for alg in self.algs]

    def output_log(self, paths, trial):

        for p, alg in zip(paths, self.algs):
            alg.output_log(p, trial)