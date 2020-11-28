# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 16:50:13 2020

@author: t.urita
"""
import numpy as np

def mating(pr, cd, num):

    rand_idx = np.random.randint(pr.shape[0], size = [num, 2])

    idx = np.argmin([pr[rand_idx[:, 0]], pr[rand_idx[:, 1]]], axis = 0)
    same_pr = pr[rand_idx[:, 0]] == pr[rand_idx[:, 1]]
    idx[same_pr] = np.argmax([cd[rand_idx[same_pr, 0]],\
                              cd[rand_idx[same_pr, 1]]], axis = 0)

    return rand_idx[range(rand_idx.shape[0]), idx]