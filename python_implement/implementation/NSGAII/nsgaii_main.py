# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 22:04:37 2020

@author: t.urita
"""
import numpy as np
import matplotlib.pyplot as plt

from ..operator import *
from .NSGA_util import NDsorting, calc_cd, mating

class NSGAII:

    def __init__(self, ndim, nobj, npop, noff, problem, code):

        self.pop = {}
        self.pop["variables"] = np.zeros([npop, ndim])
        self.pop["objectives"] = np.zeros([npop, nobj])
        self.pop["pareto_rank"] = np.zeros(npop)
        self.pop["crowding_distance"] = np.zeros(npop)

        self.problem = problem

        self.neval = 0
        self.noff = noff

        self.code = code

        if code == "real":
            self.crossover = SBX
            self.mutation = PM
        elif code == "bin":
            self.crossover = uniform_crossover
            self.mutation = bitflip_mutation

    def import_pop(self, task_name, task_no, trial):

        self.pop["variables"] = np.loadtxt("D:/research/MultiTask/code/result/実験結果/result/NSGA2/" + task_name + "/Task" + str(task_no) + "/InitialVAR/InitialVAR" + str(trial) + ".dat")
        self.pop["objectives"] = self.problem.evaluate(self.pop["variables"])
        self.init_eval()

        self.neval = self.pop["variables"].shape[0]

    def init_pop(self):

        if self.code == "real":
            self.pop["variables"] = np.random.rand(*self.pop["variables"].shape,)
        elif self.code == "bin":
            self.pop["variables"] = np.random.randint(2, size = self.pop["variables"].shape)

        self.pop["objectives"] = self.problem.evaluate(self.pop["variables"])
        self.init_eval()

        self.neval = self.pop["variables"].shape[0]

    def init_eval(self):

        r = NDsorting(self.pop["objectives"], self.pop["objectives"].shape[0])
        self.pop["pareto_rank"] = r

        for i in range(max(r) + 1):

            self.pop["crowding_distance"][r == i] = calc_cd(self.pop["objectives"][r == i])

    def execute(self, max_eval):

        offs = {}
        offs["variables"] = np.zeros([self.noff, self.pop["variables"].shape[1]])
        offs["objectives"] = np.zeros([self.noff, self.pop["objectives"].shape[1]])

        n, mod= divmod(max_eval - self.neval, self.noff)

        # rep = np.empty(n)

        for i in range(n):

            # old_pop = self.pop["variables"].copy()

            parents = self.selection()

            offs["variables"] = self.mutation(self.crossover(parents, pc = 0.8))
            offs["objectives"] = self.problem.evaluate(offs["variables"])
            self.update(offs)

            # visualize objective space
            # plt.cla()
            # plt.scatter(*self.pop["objectives"].T,)
            # plt.pause(0.01)

            # rep[i] = self.noff - np.sum((self.pop["variables"][:, None, :] == old_pop[None, :, :]).sum(axis = 2) == self.pop["variables"].shape[1])

        if mod != 0:

            parents = []
            parents.append(self.pop["variables"][self.selection()])
            parents.append(self.pop["variables"][self.selection()])

            offs["variables"] = self.mutation(self.crossover(parents))
            offs["objectives"][:mod] = self.problem.evaluate(offs["variables"][:mod])
            offs["objectives"][mod:] = 0
            self.update(offs)

        self.neval = max_eval

        # return rep

    def selection(self):

        parents = []
        parent1 = mating(self.pop["pareto_rank"], self.pop["crowding_distance"], \
                         int(self.noff/2))
        parent2 = mating(self.pop["pareto_rank"], self.pop["crowding_distance"], \
                         int(self.noff/2))

        parents.append(self.pop["variables"][parent1])
        parents.append(self.pop["variables"][parent2])

        return parents

    def update(self, offs):

        pop_size = self.pop["objectives"].shape

        union = {}
        # union["variables"] = np.vstack((self.pop["variables"] ,offs["variables"]))
        # union["objectives"] = np.vstack((self.pop["objectives"], offs["objectives"]))
        union["variables"], idx = np.unique(np.vstack((self.pop["variables"] ,offs["variables"])),\
                                              axis = 0, return_index = True)
        union["objectives"] = np.vstack((self.pop["objectives"], offs["objectives"]))[idx]

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