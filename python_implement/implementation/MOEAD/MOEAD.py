# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 16:02:30 2021

@author: youle
"""

import numpy as np
import matplotlib.pyplot as plt
import itertools

from ..base_class.EMOA_base import Algorithm
from ..operator import *
from .MOEAD_util import *

class MOEAD(Algorithm):

    def __init__(self, params, problem):

        self.pop = {}
        self.pop["variables"] = np.empty([params["npop"], problem.ndim])
        self.pop["objectives"] = np.empty([params["npop"], problem.nobj])

        self.weight_vector, self.neighbor = generate_weight_vector\
            (problem.nobj, params["divide"], params["neighbor_size"])
        self.npop = self.weight_vector.shape[0]

        self.code = problem.code
        self.eval_method = problem.evaluate

        self.neval = 0

        if self.code == "real":
            self.crossover = SBX
            self.mutation = PM
        elif self.code == "bin":
            self.crossover = uniform_crossover
            self.mutation = bitflip_mutation

        if params["type"] in [1, "tch", "tchebycheff"]:
            self.scalarizing_function = tchebycheff
        elif params["type"] in [2, "PBI"]:
            self.scalarizing_function = PBI

    def init_pop(self):

        if self.code == "real":
            self.pop["variables"] = np.random.rand(*self.pop["variables"].shape,)
        elif self.code == "bin":
            self.pop["variables"] = np.random.randint(2, size = self.pop["variables"].shape)

        self.pop["objectives"] = self.eval_method(self.pop["variables"])
        self.z = self.pop["objectives"].min(axis = 0)

        self.neval = self.npop

    def execute_genbase(self, max_eval):

        n, mod= divmod(max_eval - self.neval, self.npop)

        indices = np.random.permutation(self.weight_vector.shape[0])

        for gen in range(n):

            for idx in indices:

                off = dict(variables = self.generate_offspring(idx))
                off["objectives"] = self.eval_method(off["variables"])

                self.z = np.min([self.z, off["objectives"][0]], axis = 0)

                self.update(idx, off)

            indices = np.random.permutation(self.weight_vector.shape[0])

        for remain_idx in indices[:mod]:

            off = dict(variables = self.generate_offspring(remain_idx))
            off["objectives"] = self.eval_method(off["variables"])

            self.z = np.min([self.z, off["objectives"][0]], axis = 0)

            self.update(remain_idx, off)

    def execute(self, max_eval):

        remain_eval = max_eval -self.neval
        nrep = np.ceil(remain_eval / self.npop)
        indices = np.array([np.random.permutation(self.weight_vector.shape[0]) for _ in range(int(nrep))])\
            .flatten()[:remain_eval]

        for idx in indices:

            off = dict(variables = self.generate_offspring(idx))
            off["objectives"] = self.eval_method(off["variables"])

            self.z = np.min([self.z, off["objectives"][0]], axis = 0)

            self.update(idx, off)

    def generate_offspring(self, idx):

        parents_idx = np.random.choice(self.neighbor[idx], 2, replace = False)

        parents = [*map(lambda p_idx: self.pop["variables"][p_idx: p_idx + 1], parents_idx)]
        offspring = self.mutation(self.crossover(parents)[:1])

        return offspring

    def update(self, idx, off):

        neighbor = self.neighbor[idx]
        candidate_vec = self.weight_vector[neighbor]

        off["scalar_objectives"] = self.scalarizing_function(off["objectives"], candidate_vec, self.z)
        parents_scalar_objectives = self.scalarizing_function\
            (self.pop["objectives"][neighbor], candidate_vec, self.z)
        replace_mask = off["scalar_objectives"] < parents_scalar_objectives
        replace_pos = neighbor[replace_mask]

        self.pop["variables"][replace_pos] = off["variables"]
        self.pop["objectives"][replace_pos] = off["objectives"]