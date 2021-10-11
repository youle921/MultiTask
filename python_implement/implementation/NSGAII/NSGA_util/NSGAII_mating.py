# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 16:50:13 2020

@author: t.urita
"""
import numpy as np

def mating(pr, cd, num):

    cost = pr + 1/(1 + cd)
    rank = cost.argsort()

    rand_idx = np.random.randint(pr.shape[0], size = [num, 2])
    idx = rank[rand_idx].argmin(axis = 1)

    return rand_idx[range(rand_idx.shape[0]), idx]