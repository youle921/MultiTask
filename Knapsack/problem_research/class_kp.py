# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 23:30:13 2019

@author: t.urita
"""

import numpy as np

class Knapsack:

    def __init__(self, objective = 2, items = 500, lower = 10, upper = 100, load = True):

        self.objective = objective

        if load:
            self.items = np.empty([items, 2, objective])
            for i in range(objective):
                load_item = np.loadtxt("../KnapsackData/items/knapsack_500_profit" + str(i + 1) + ".csv")
                self.items[:, 0, i] = load_item[:items]
                load_weight = np.loadtxt("../KnapsackData/items/knapsack_500_weight" + str(i + 1) + ".csv")
                self.items[:, 1, i] = load_weight[:items]

        else:
            self.items = np.random.randint(lower, high = upper + 1, size = (items, 2, objective))

        self.utility = np.max(self.items[:, 0, 0 : 2] / self.items[:, 1, 0 : 2], axis = 1)

        self.size = np.sum(self.items[:, 1, :], axis = 0) / 2
        if objective > 3:
            self.size[2:] = np.inf

        self.original_size = self.size

    def evaluate(self, solutions):

        self.repair(solutions)
        f = np.dot(solutions, self.items[:, 0, :])

        return f

    def repair(self, solutions):

        w = np.dot(solutions, self.items[:, 1, :])

        mask = np.sum(w > self.size, axis = 1) > 0
        util = solutions * self.utility
        util[util == 0] = np.inf

        while(np.sum(mask) != 0):

            idx = np.argmin(util, axis = 1)[mask]

            solutions[mask, idx] = 0
            util[mask, idx] = np.inf

            mask = np.sum(np.dot(solutions, self.items[:, 1, :]) > self.size, axis = 1) > 0

    def shift_size(self, scale):

        self.size = self.original_size * scale

if __name__ == "__main__":

    kp = Knapsack(items = 20)
    sol = np.random.randint(0, 2, size = (10, 20))
    sol2 = sol.copy()
    f = kp.evaluate(sol)