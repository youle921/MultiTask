# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 22:52:29 2020

@author: t.urita
"""

from class_kp import Knapsack

class kp_scaling(Knapsack):

    def __init__(self, sf):
        super().__init__()
        self.size *= sf