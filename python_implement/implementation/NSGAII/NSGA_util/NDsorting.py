# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 00:19:23 2020

@author: t.urita
"""
import numpy as np

def NDsorting(union, num):

    r = 0
    rank = -np.ones(union.shape[0], dtype = int)

    # for minmization problem(compalator: >)
    is_dominated = (union[:, None, :] >= union[None, :, :]).prod(axis = 2) * \
        (union[:, None, :] > union[None, :, :]).max(axis = 2)

    while(np.sum(rank != -1) < num):

        NDsolution = is_dominated.max(axis = 1) == 0
        rank[NDsolution] = r
        r += 1

        is_dominated[:, NDsolution] = 0
        is_dominated[NDsolution] = 1

    return rank