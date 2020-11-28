# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:59:15 2020

@author: t.urita
"""
import numpy as np

class populations:

    def __init__(self, nprob, npop, ndim, nobj):

        self.variables = np.zeros([nprob, npop, ndim])
        self.objectives = np.zeros([nprob, npop, nobj])
        self.pareto_rank = np.zeros([nprob, npop])
        self.crowding_distance = np.zeros([nprob, npop])