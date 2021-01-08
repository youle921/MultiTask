# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 22:11:12 2021

@author: t.urita
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 22:04:37 2020

@author: t.urita
"""
import numpy as np
import matplotlib.pyplot as plt

from ..operator import *
from ..NSGAII.NSGA_util import calc_cd, mating
from ..constraint_handling.NDsorting_CDP import NDsorting_CDP

class NSGAII_CDP:

    def __init__(self, ndim, nobj, nvio, npop, noff, problem, code):

        self.pop = {}
        self.pop["variables"] = np.zeros([npop, ndim])
        self.pop["objectives"] = np.zeros([npop, nobj])
        self.pop["violations"] = np.zeros([npop, nvio])
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

        self.pop["objectives"], self.pop["violations"] = \
            self.problem.evaluate_with_violation(self.pop["variables"])
        self.init_eval()

        self.neval = self.pop["variables"].shape[0]

    def init_eval(self):

        self.pop["pareto_rank"] = NDsorting_CDP(self.pop["objectives"], self.pop["violations"], self.pop["objectives"].shape[0])

        max_pr = (self.pop["pareto_rank"] < 1000).max()
        for i in range(max_pr + 1):

            self.pop["crowding_distance"][self.pop["pareto_rank"] == i] = \
                calc_cd(self.pop["objectives"][self.pop["pareto_rank"] == i])

    def execute(self, max_eval):

        offs = {}
        offs["variables"] = np.zeros([self.noff, self.pop["variables"].shape[1]])
        offs["objectives"] = np.zeros([self.noff, self.pop["objectives"].shape[1]])

        n, mod= divmod(max_eval - self.neval, self.noff)

        rep = np.empty(n)

        for i in range(n):

            # old_pop = self.pop["variables"].copy()

            parents = self.selection()

            offs["variables"] = self.mutation(self.crossover(parents, pc = 0.8))
            offs["objectives"], offs["violations"] = self.problem.evaluate_with_violation(offs["variables"])
            self.update(offs)

            # visualize objective space
            # plt.cla()
            # plt.scatter(*self.pop["objectives"].T,)
            # plt.pause(0.01)

            # rep[i] = self.noff - np.sum((self.pop["variables"][:, None, :] == old_pop[None, :, :]).sum(axis = 2) == self.pop["variables"].shape[1])

        if mod != 0:

            parents = self.selection()

            offs["variables"] = self.mutation(self.crossover(parents))
            offs["objectives"][:mod], offs["violations"][:mod] = self.problem.evaluate_with_violation(offs["variables"][:mod])
            offs["objectives"][mod:] = 0
            offs["violations"][mod:] = 1.0e+7
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
        # union["violations"] = np.vstack((self.pop["violations"], offs["violations"]))
        union["variables"], idx = np.unique(np.vstack((self.pop["variables"] ,offs["variables"])),\
                                              axis = 0, return_index = True)
        union["objectives"] = np.vstack((self.pop["objectives"], offs["objectives"]))[idx]
        union["violations"] = np.vstack((self.pop["violations"], offs["violations"]))[idx]

        r = NDsorting_CDP(union["objectives"], union["violations"], pop_size[0])
        max_pr = r[(-1 < r) & (r < 1000)].max()

        offset = 0

        if np.all(r < 1000):

            for i in range(max_pr):

                n = sum(r == i)

                self.pop["objectives"][offset:offset + n] = union["objectives"][r == i]
                self.pop["variables"][offset:offset + n] = union["variables"][r == i]
                self.pop["violations"][offset:offset + n] = 0
                self.pop["pareto_rank"][offset:offset + n] = i
                self.pop["crowding_distance"][offset:offset + n] = calc_cd(union["objectives"][r == i])

                offset +=n

            cd = calc_cd(union["objectives"][r == max_pr])
            remain = np.argsort(-cd)[:pop_size[0] - offset]
            self.pop["objectives"][offset:] = union["objectives"][r == max_pr][remain]
            self.pop["variables"][offset:] = union["variables"][r == max_pr][remain]
            self.pop["violations"][offset:] = 0
            self.pop["pareto_rank"][offset:] = max_pr
            self.pop["crowding_distance"][offset:] = calc_cd(self.pop["objectives"][offset:])

        else:
            for i in range(max_pr + 1):

                n = sum(r == i)

                self.pop["objectives"][offset:offset + n] = union["objectives"][r == i]
                self.pop["variables"][offset:offset + n] = union["variables"][r == i]
                self.pop["violations"][offset:offset + n] = 0
                self.pop["pareto_rank"][offset:offset + n] = i
                self.pop["crowding_distance"][offset:offset + n] = calc_cd(union["objectives"][r == i])

                offset +=n

            infeasible = union["violations"].sum(axis = 1) > 0
            remain = np.argsort(union["violations"][infeasible].sum(axis = 1))[:pop_size[0] - offset]
            self.pop["objectives"][offset:] = union["objectives"][infeasible][remain]
            self.pop["variables"][offset:] = union["variables"][infeasible][remain]
            self.pop["violations"][offset:] = union["violations"][infeasible][remain]
            self.pop["pareto_rank"][offset:] = r[remain]
