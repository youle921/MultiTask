# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 20:47:55 2020

@author: t.urita
"""
import numpy as np
import matplotlib.pyplot as plt

def test_NDsort(union, num):

    rank = -np.ones(union.shape[0], dtype = int)
    comp = (union[:, None, :] <= union[None, :, :]).sum(axis = 2)
    r = 0

    while(np.sum(rank != -1) < num):

        NDsolution = (comp != 0).min(axis = 1)
        rank[NDsolution] = r
        r += 1

        comp[:, NDsolution] = 1
        comp[NDsolution] = 0

    return rank

sol = np.random.randn(50, 2)

r = test_NDsort(sol, 50)

for i in range(max(r) + 1):
    plt.scatter(*sol[r == i].T,)