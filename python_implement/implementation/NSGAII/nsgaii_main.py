# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 22:04:37 2020

@author: t.urita
"""
import numpy as np
import matplotlib.pyplot as plt

from ..base_class.EMOA_base import Algorithm
from ..operator import *
from .NSGA_util import NDsorting, calc_cd, mating

class NSGAII(Algorithm):

    def __init__(self, params, problem):

        self.pop = {}
        self.pop["variables"] = np.empty([params["npop"], problem.ndim])
        self.pop["crowding_distance"] = np.zeros(params["npop"])

        self.code = problem.code
        self.eval_method = problem.evaluate

        self.noff = params["noff"]
        self.offs = {}

        if self.code == "real":
            self.crossover = SBX
            self.mutation = PM
            self.concat_pops = self.create_union
        elif self.code == "bin":
            self.crossover = uniform_crossover
            self.mutation = bitflip_mutation
            self.concat_pops = self.create_unique_union

    def import_pop(self, task_name, task_no, trial):

        self.pop["variables"] = np.loadtxt("D:/research/MultiTask/code/result/実験結果/result/NSGA2/" + task_name + "/Task" + str(task_no) + "/InitialVAR/InitialVAR" + str(trial) + ".dat")
        self.pop["objectives"] = self.eval_method(self.pop["variables"])
        self.init_eval()

        self.neval = self.pop["variables"].shape[0]

    def init_pop(self):

        if self.code == "real":
            self.pop["variables"] = np.random.rand(*self.pop["variables"].shape,)
        elif self.code == "bin":
            self.pop["variables"] = np.random.randint(2, size = self.pop["variables"].shape)

        self.pop["objectives"] = self.eval_method(self.pop["variables"])
        self.init_eval()

        self.neval = self.pop["variables"].shape[0]

    def init_eval(self):

        r = NDsorting(self.pop["objectives"], self.pop["objectives"].shape[0])
        self.pop["pareto_rank"] = r

        for i in range(max(r) + 1):

            self.pop["crowding_distance"][r == i] = calc_cd(self.pop["objectives"][r == i])

    def execute(self, max_eval):

        n, mod= divmod(max_eval - self.neval, self.noff)

        # rep = np.empty(n)

        for i in range(n):

            # old_pop = self.pop["variables"].copy()

            parents = self.selection()

            self.offs["variables"] = self.mutation(self.crossover(parents, pc = 0.9))
            self.offs["objectives"] = self.eval_method(self.offs["variables"])
            self.update(self.offs)

            # rep[i] = self.noff - np.sum((self.pop["variables"][:, None, :] == old_pop[None, :, :]).sum(axis = 2) == self.pop["variables"].shape[1])

        if mod != 0:

            parents = self.selection()

            self.offs["variables"] = self.mutation(self.crossover(parents[:mod]))
            self.offs["objectives"] = self.eval_method(self.offs["variables"])
            self.update(self.offs)

        self.neval = max_eval

        # return rep

    def selection(self):

        parents = [*map(lambda _:self.pop["variables"]\
                        [mating(self.pop["pareto_rank"], self.pop["crowding_distance"], int(self.noff/2))],range(2))]

        # parents = []
        # parent1 = mating(self.pop["pareto_rank"], self.pop["crowding_distance"], \
        #                   int(self.noff/2))
        # parent2 = mating(self.pop["pareto_rank"], self.pop["crowding_distance"], \
        #                   int(self.noff/2))

        # parents.append(self.pop["variables"][parent1])
        # parents.append(self.pop["variables"][parent2])

        return parents

    def update(self, offs):

        pop_size = self.pop["objectives"].shape
        union = self.concat_pops(self.offs)

        r = NDsorting(union["objectives"], pop_size[0])

        offset = 0
        for i in range(max(r)):

            n = sum(r == i)

            self.pop["objectives"][offset:offset + n] = union["objectives"][r == i]
            self.pop["variables"][offset:offset + n] = union["variables"][r == i]
            self.pop["pareto_rank"][offset:offset + n] = i
            self.pop["crowding_distance"][offset:offset + n] = calc_cd(union["objectives"][r == i])

            offset +=n

        cd = calc_cd(union["objectives"][r == max(r)])
        remain = np.argsort(-cd)[:pop_size[0] - offset]
        self.pop["objectives"][offset:] = union["objectives"][r == max(r)][remain]
        self.pop["variables"][offset:] = union["variables"][r == max(r)][remain]
        self.pop["pareto_rank"][offset:] = max(r)
        self.pop["crowding_distance"][offset:] = calc_cd(self.pop["objectives"][offset:])