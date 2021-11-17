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

class normalized_IGD:
    def __init__(self, ref):

        self.ideal = ref.min(axis = 0)
        self.nadir = ref.max(axis = 0)

        self.ref = (ref - self.nadir) / (self.ideal - self.nadir)

    def compute(self, objective, power = 1):

        norm_obj = (objective - self.nadir) / (self.ideal - self.nadir)
        dist = np.sqrt(np.sum((self.ref[:, None, :] - norm_obj[None, :, :])**2, axis = 2))
        min_dist = np.min(dist, axis = 1)
        dist_sum =  ((min_dist**power).sum())**(1/power)

        return dist_sum/self.ref.shape[0]