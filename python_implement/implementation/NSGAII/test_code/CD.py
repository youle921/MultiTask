# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 21:54:35 2020

@author: t.urita
"""
import numpy as np
import matplotlib.pyplot as plt

def test_calc_cd(obj):

    size = obj.shape
    cd = np.zeros(size[0])
    for n in range(size[1]):
        idx = np.argsort(obj[:, n])
        cd[idx[[0, -1]]] += 1000000
        cd[1:size[0] - 1] += (obj[idx[2:], n] - obj[idx[:size[0] - 2], n])/(obj[idx[-1], n] - obj[idx[0], n])

    return cd

obj = np.random.rand(5, 2)
cd = test_calc_cd(obj)

plt.scatter(*obj.T,)