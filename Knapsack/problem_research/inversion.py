# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 22:59:42 2020

@author: t.urita
"""

from class_kp import Knapsack

class kp_inversion(Knapsack):

    def __init__(self, ir):
        super().__init__()
        inversion_num = int(ir * self.items.shape[0])
        self.items[:inversion_num, 0, 1] = 110 - self.items[:inversion_num, 0, 1]