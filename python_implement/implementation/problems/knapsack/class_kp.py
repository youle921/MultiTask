# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 23:30:13 2019

@author: t.urita
"""
import numpy as np
import os

class knapsack:

    def __init__(self, objective = 2, items = 500, lower = 10, upper = 100, load = True):

        self.nobj = objective
        self.ndim = items

        self.pf = None
        self.code = 'bin'

        if load:
            path = os.path.dirname(__file__)
            self.items = dict(profit = np.empty([objective, items]), weight = np.empty([objective, items]))
            for i in range(objective):
                load_item = np.loadtxt(path + "/items/knapsack_500_profit" + str(i + 1) + ".csv")
                self.items["profit"][i] = load_item[:items]
                load_weight = np.loadtxt(path + "/items/knapsack_500_weight" + str(i + 1) + ".csv")
                self.items["weight"][i] = load_weight[:items]

        else:
            self.items["profit"] = np.random.randint(lower, high = upper + 1, size = (objective, items))
            self.items["weight"] = np.random.randint(lower, high = upper + 1, size = (objective, items))

        self.utility = (self.items["profit"][0:2] / self.items["weight"][0:2]).max(axis = 0)

        self.size = np.sum(self.items["weight"], axis = 1) / 2
        if objective > 2:
            self.size[2:] *= 3

        self.original_size = self.size

        # for repair operation
        self.sort_idx = self.utility.argsort()[::-1]
        self.inv_sort_idx = self.sort_idx.argsort()

    def get_pf(self):

        if self.pf is None:
            path = os.path.dirname(__file__)
            self.pf = np.loadtxt(path + "/pf/knapsack_500_pf.dat")

        return self.pf

    def evaluate(self, solutions):

        self.repair(solutions)
        f = np.dot(solutions, self.items["profit"].T)

        return -f

    def evaluate_with_violation(self, solutions):

        f = np.dot(solutions, self.items["profit"].T)
        w = np.dot(solutions, self.items["weight"].T)

        return [-f, np.clip(w - self.size, 0, None)]

    # while削除バージョン，実行不可能解にのみ適用，思いつく限り最速
    def repair(self, solutions):

        w_ = solutions[None, :, :] * self.items["weight"][:, None, :]
        no_repair_pos = np.ones_like(solutions, dtype = bool)
        infeasible = np.logical_or(*w_.sum(axis = 2) > self.size[:, None])

        w_sorted = w_[:,infeasible][:, :, self.sort_idx]
        w_mask = w_sorted.cumsum(axis = 2) < self.size[:, None, None]
        no_repair_pos[infeasible] = np.logical_and(*w_mask,)[:, self.inv_sort_idx]

        solutions[~no_repair_pos] = 0

    def repair_2loop(self, solutions):
        for s in solutions:
            is_feasible = np.logical_and.reduce(np.dot(self.items["weight"], s) <= self.size)
            idx = 499
            while(not(is_feasible)):
                s[self.sort_idx[idx]] = 0
                is_feasible = np.logical_and.reduce(np.dot(self.items["weight"], s) <= self.size)
                idx -= 1

    # ベクトル対応・whileバージョン
    def repair_while(self, solutions):

        w = np.dot(solutions, self.items["weight"].T)

        mask = np.sum(w > self.size, axis = 1) > 0
        util = solutions * self.utility
        util[util == 0] = np.inf

        while(np.sum(mask) != 0):

            idx = np.argmin(util[mask], axis = 1)

            solutions[mask, idx] = 0
            util[mask, idx] = np.inf

            w[mask] -= self.items["weight"][:, idx].T

            mask = np.sum(w > self.size, axis = 1) > 0


    def repair_old(self, solutions):

        w = np.dot(solutions, self.items["weight"].T)

        mask = np.sum(w > self.size, axis = 1) > 0
        util = solutions * self.utility
        util[util == 0] = np.inf

        while(np.sum(mask) != 0):

            idx = np.argmin(util[mask], axis = 1)

            solutions[mask, idx] = 0
            util[mask, idx] = np.inf

            mask = np.sum(np.dot(solutions, self.items["weight"].T) > self.size, axis = 1) > 0

    # while削除バージョン，実行可能解にも適用するためちょっと遅い
    def repair_all(self, solutions):

        w_sorted = (solutions[None, :, :] * self.items["weight"][:, None, :])\
            [:, :, self.sort_idx]
        w_mask = w_sorted.cumsum(axis = 2) < self.size[:, None, None]
        w_pos = np.logical_and(*w_mask,)[:, self.inv_sort_idx]

        solutions[~w_pos] = 0

if __name__ == "__main__":

    np.random.seed(0)

    kp = knapsack(objective = 2)
    # sol = np.random.randint(0, 2, size = (200, 500))
    sol1 = np.where(np.random.rand(100, 500) < 0.5, 1, 0)
    sol2 = sol1.copy()
    sol3 = sol1.copy()
    sol4 = sol1.copy()

    kp.repair(sol1)
    f1, g1 = kp.evaluate_with_violation(sol1)

    kp.repair_old(sol2)
    f2, g2 = kp.evaluate_with_violation(sol2)

    kp.repair_while(sol3)
    f3, g3 = kp.evaluate_with_violation(sol3)

    kp.repair_2loop(sol4)
    f4, g4 = kp.evaluate_with_violation(sol4)
