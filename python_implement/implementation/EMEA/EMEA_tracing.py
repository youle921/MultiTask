# -*- coding: utf-8 -*-

import numpy as np
from .nsgaii_for_EMEA_tracing import NSGAII_EMEA_tracing

from . import EMEA

class EMEA_tracing(EMEA):

    def __init__(self, params, problem_list):

        self.interval = params["interval"]
        self.mig_size = params["migration_size"]

        self.algs = []
        for task in problem_list:
            self.algs.append(NSGAII_EMEA_tracing(params, task))

        self.matrix = [[] for i in range(len(problem_list))]

    def execute(self, max_gen):

        for g in range(1, max_gen):

            if g % self.interval != 0:
                [alg.execute(1) for alg in self.algs]

            else:
                inject_pop = self._get_inject_pop()
                [self.algs[i].migration_gen(inject_pop[1 - i]) for i in range(len(self.algs))]

        return np.array([alg.trace_log for alg in self.algs])