# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 22:04:37 2020

@author: t.urita
"""
import numpy as np
import matplotlib.pyplot as plt

from ..operator import *
from ..NSGAII.NSGA_util import NDsorting, calc_cd, mating
from ..constraint_handling.SP import modify_objective_function

def plot_kp_sols(i, sol, pf):

    plt.cla()

    plt.plot(*pf.T, c = 'gray', label = "Pareto Front")
    plt.scatter(*-sol[i].T, label = "population")

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.tight_layout()


class NSGAII_SP:

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

        self.analyzer_func = lambda t : None

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

        self.neval = self.pop["variables"].shape[0]

    def re_eval_population(self):

        self.feasible_ratio = (self.pop["violations"].sum(axis = 1) == 0).mean()
        self.pop["modified_obj"] = modify_objective_function\
            (self.pop["objectives"], self.pop["violations"], self.feasible_ratio)

        r = NDsorting(self.pop["modified_obj"], self.pop["objectives"].shape[0])
        self.pop["pareto_rank"] = r

        for i in set(r):

            self.pop["crowding_distance"][r == i] = calc_cd(self.pop["modified_obj"][r == i])

    def execute(self, max_eval):

        offs = {}
        n, mod= divmod(max_eval - self.neval, self.noff)

        # rep = np.empty(n)

        for i in range(n):

            # old_pop = self.pop["variables"].copy()

            self.re_eval_population()
            self.analyzer_func(i + 1)

            parents = self.selection()

            offs["variables"] = self.mutation(self.crossover(parents, pc = 0.8))
            offs["objectives"], offs["violations"] = self.problem.evaluate_with_violation(offs["variables"])
            self.update(offs)

            # visualize objective space
            # if i % 10 == 0:

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

        self.re_eval_population()
        self.analyzer_func(n + 1)

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
        union["violations"] = np.vstack((self.pop["violations"], offs["violations"]))[idx]
        union["modified_obj"] = modify_objective_function\
            (union["objectives"], union["violations"], self.feasible_ratio)

        r = NDsorting(union["modified_obj"], pop_size[0])

        offset = 0
        max_r = np.max(r)
        for i in range(max_r):

            n = sum(r == i)

            self.pop["objectives"][offset:offset + n] = union["objectives"][r == i]
            self.pop["variables"][offset:offset + n] = union["variables"][r == i]
            self.pop["violations"][offset:offset + n] = union["violations"][r == i]

            offset +=n

        cd = calc_cd(union["modified_obj"][r == max_r])
        remain = np.argsort(-cd)[:pop_size[0] - offset]
        self.pop["objectives"][offset:] = union["objectives"][r == max_r][remain]
        self.pop["variables"][offset:] = union["variables"][r == max_r][remain]
        self.pop["violations"][offset:] = union["violations"][r == max_r][remain]

    def get_NDsolution(self):

        is_feasible = self.pop["violations"].sum(axis = 1) == 0
        feasible_sol = self.pop["objectives"][is_feasible]

        # for minmization problem(compalator: >)
        is_dominated = (feasible_sol[:, None, :] >= feasible_sol[None, :, :]).prod(axis = 2) & \
            (feasible_sol[:, None, :] > feasible_sol[None, :, :]).max(axis = 2)

        NDsolution = is_dominated.max(axis = 1) == 0

        return self.pop["objectives"][is_feasible][NDsolution]

    def set_analyzer(self, save_list, dulation):

        self.saved_data = {}
        self.save_list = save_list
        self.dulation = dulation

        for key in self.save_list:
            self.saved_data[key] = []

        self.analyzer_func = self.analyzer

    def analyzer(self, gen):

        if gen % self.dulation == 0 or gen == 1:
            for key in self.save_list:
                self.saved_data[key].append(self.pop[key].copy())

    def visualize_optimization(self):

        from matplotlib.animation import FuncAnimation

        fig = plt.figure()
        a = self.problem.get_pf()

        anim = FuncAnimation(fig, plot_kp_sols, fargs = (self.saved_data["objectives"], self.problem.get_pf()),frames = len(self.saved_data["objectives"]),interval = 50, repeat = False)
        fig.show()

        return anim

        # 没案(軸の調整ができない)

        # fig, ax = plt.subplots()
        # fig.canvas.draw()

        # bg = fig.canvas.copy_from_bbox(ax.bbox)

        # scat = ax.scatter(*np.vstack((self.saved_data["objectives"][0], self.saved_data["objectives"][-1])).T,)
        # fig.show()

        # ds = self.saved_data["objectives"]

        # for d in self.saved_data["objectives"]:

        #     scat.set_offsets(d)
        #     fig.canvas.restore_region(bg)
        #     ax.draw_artist(scat)
        #     fig.canvas.blit(ax.bbox)

        #     fig.canvas.flush_events()

