# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import numpy as np

class MT_Algorithm(metaclass=ABCMeta):

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

        output_pop = []

        for t in range(self.ntask):

            is_feasible = np.ones_like(self.pops["crowding_distance"][t], dtype = bool)
            if "violations" in self.pops:
                is_feasible[...] = self.pops["violations"][t].sum(axis = 1) == 0
            feasible_sol = self.pops["objectives"][t][is_feasible]

            # for minmization problem(compalator: >)
            is_dominated = (feasible_sol[:, None, :] >= feasible_sol[None, :, :]).prod(axis = 2) & \
                (feasible_sol[:, None, :] > feasible_sol[None, :, :]).max(axis = 2)

            NDsolution = is_dominated.max(axis = 1) == 0

            output_pop.append(self.pops["objectives"][t][is_feasible][NDsolution])

        return output_pop

    def get_objectives(self):

        return self.pops["objectives"]

    def set_datalogger(self, save_list):

        self.saved_data = {}

        for key in save_list:
            self.saved_data[key] = [[] for _ in range(self.ntask)]

        self.logger = self.datalogger

    def datalogger(self):

        for key in self.saved_data:
            for i, d in enumerate(self.pops[key]):
                self.saved_data[key][i].append(d.copy())

    def output_log(self, paths, trial):

        if "saved_data" in dir(self):
            for key in self.saved_data:
                for p, data in zip(paths, self.saved_data[key]):
                    np.savez_compressed(f'{p}/trial{trial}_{key}', data)
                    data.clear()