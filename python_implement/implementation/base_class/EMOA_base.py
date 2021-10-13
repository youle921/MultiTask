# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import numpy as np

import matplotlib.pyplot as plt

class Algorithm(metaclass=ABCMeta):

    @abstractmethod
    def init_pop(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def _update(self):
        pass

    def create_union(self, pop, offs):

        union = {}

        for k in ["variables", "objectives"]:
            size_p, dim = pop[k].shape
            size_o = offs[k].shape[0]

            union[k] = np.empty([size_p + size_o, dim])
            union[k][:size_p] = pop[k]
            union[k][size_p:] = offs[k]

        return union

    def create_unique_union(self, pop, offs):

        union = {}

        union["variables"], idx = np.unique(np.vstack((pop["variables"] ,offs["variables"])),\
                                              axis = 0, return_index = True)
        union["objectives"] = np.vstack((pop["objectives"], offs["objectives"]))[idx]

        return union

    def get_NDsolution(self):

        is_feasible = np.ones_like(self.pop["crowding_distance"], dtype = bool)
        if "violations" in self.pop:
            is_feasible[...] = self.pop["violations"].sum(axis = 1) == 0
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

        self.analyst = self.analyzer

    def analyzer(self, gen):

        if gen % self.dulation == 0 or gen == 1:
            for key in self.save_list:
                self.saved_data[key].append(self.pop[key].copy())

# 以降の関数は未検証，たぶん動かない？
    def plot_kp_sols(i, sol, pf):

        plt.cla()

        plt.plot(*pf.T, c = 'gray', label = "Pareto Front")
        plt.scatter(*-sol[i].T, label = "population")

        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.tight_layout()

    def visualize_optimization(self):

        from matplotlib.animation import FuncAnimation
        fig = plt.figure()

        anim = FuncAnimation(fig, self.plot_kp_sols, fargs = (self.saved_data["objectives"], self.problem.get_pf()),frames = len(self.saved_data["objectives"]),interval = 50, repeat = False)
        fig.show()

        return anim