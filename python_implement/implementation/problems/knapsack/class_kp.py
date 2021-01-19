# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 23:30:13 2019

@author: t.urita
"""
import numpy as np
import os

class knapsack:

    def __init__(self, objective = 2, items = 500, lower = 10, upper = 100, load = True):

        self.objective = objective
        self.pf = None

        if load:
            path = os.path.dirname(__file__)
            self.items = np.empty([objective, items, 2])
            for i in range(objective):
                load_item = np.loadtxt(path + "/items/knapsack_500_profit" + str(i + 1) + ".csv")
                self.items[i, :, 0] = load_item[:items]
                load_weight = np.loadtxt(path + "/items/knapsack_500_weight" + str(i + 1) + ".csv")
                self.items[i, :, 1] = load_weight[:items]

        else:
            self.items = np.random.randint(lower, high = upper + 1, size = (items, 2, objective))

        self.utility = (self.items[0:2, :, 0] / self.items[0:2, :, 1]).max(axis = 0)

        self.size = np.sum(self.items[:, :, 1], axis = 1) / 2
        if objective > 2:
            self.size[2:] *= 2

        self.original_size = self.size
        self.repair_order = (self.items[0:2, :, 0] / self.items[0:2, :, 1])

    def get_pf(self):

        if self.pf is None:
            path = os.path.dirname(__file__)
            self.pf = np.loadtxt(path + "/pf/knapsack_500_pf.dat")

        return self.pf

    def evaluate(self, solutions):

        self.repair(solutions)
        f = np.dot(solutions, self.items[:, :, 0].T)

        return -f

    def evaluate_with_violation(self, solutions):

        f = np.dot(solutions, self.items[:, :, 0].T)
        w = np.dot(solutions, self.items[:, :, 1].T)

        return [-f, np.clip(w - self.size, 0, None)]

    def repair(self, solutions):

        w = np.dot(solutions, self.items[:, :, 1].T)

        mask = np.sum(w > self.size, axis = 1) > 0
        util = solutions * self.utility
        util[util == 0] = np.inf

        while(np.sum(mask) != 0):

            idx = np.argmin(util[mask], axis = 1)

            solutions[mask, idx] = 0
            util[mask, idx] = np.inf

            mask = np.sum(np.dot(solutions, self.items[:, :, 1].T) > self.size, axis = 1) > 0

if __name__ == "__main__":

    kp = knapsack(objective = 2)
    sol = np.random.randint(0, 2, size = (200, 500))
    sol_ = sol.copy()
    f = kp.evaluate(sol)
    f_const, g = kp.evaluate_with_violation(sol_)