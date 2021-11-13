# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 00:13:59 2021

@author: youle
"""
import numpy as np

class IGD:
    def __init__(self, ref):
        self.ref = ref

    def compute(self, objective, power = 1):

        dist = np.sqrt(np.sum((self.ref[:, None, :] - objective[None, :, :])**2, axis = 2))
        min_dist = np.min(dist, axis = 1)
        dist_sum =  ((min_dist**power).sum())**(1/power)

        return dist_sum/self.ref.shape[0]