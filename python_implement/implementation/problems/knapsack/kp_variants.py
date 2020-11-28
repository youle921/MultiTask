# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 23:59:14 2020

@author: t.urita
"""
import os
import sys
sys.path.append(os.path.dirname(__file__))

from class_kp import knapsack

class kp_inversion(knapsack):

    def __init__(self, ir):
        super().__init__()
        inversion_num = int(ir * self.items.shape[0])
        self.items[:inversion_num, 0, 1] = 110 - self.items[:inversion_num, 0, 1]

class kp_scaling(knapsack):

    def __init__(self, sf):
        super().__init__()
        self.size *= sf

class kp_bitflip(knapsack):

    def __init__(self, br):

        super().__init__()
        self.flip_num = int(br*self.items.shape[0])

    def evaluate(self, solutions):

        flip_mask = np.zeros_like(solutions)
        flip_mask[:, :self.flip_num] = 1

        self.repair(solutions, flip_mask)
        f = np.dot((flip_mask - solutions), self.items[:, 0, :])

        return -f

    def repair(self, solutions):

        flip_mask = np.zeros_like(solutions)
        flip_mask[:, :self.flip_num] = 1

        w = np.dot(solutions, self.items[:, 1, :])

        mask = np.sum(w > self.size, axis = 1) > 0
        util = solutions * self.utility
        util[util == 0] = np.inf

        while(np.sum(mask) != 0):

            idx = np.argmin(util, axis = 1)[mask]

            solutions[mask, idx] = 0
            util[mask, idx] = np.inf

            mask = np.sum(np.dot(solutions, self.items[:, 1, :]) > self.size, axis = 1) > 0
