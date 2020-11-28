# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 23:58:59 2020

@author: t.urita
"""
import numpy as np

def calc_cd(obj):

    size = obj.shape
    cd = np.zeros(size[0])

    if size[0] < 3:
        cd[:] = 1000000 * size[1]

    else:
        for n in range(size[1]):

            idx = np.argsort(obj[:, n])
            cd[idx[[0, -1]]] += 1000000
            cd[idx[1:size[0] - 1]] += (obj[idx[2:], n] - obj[idx[:size[0] - 2], n])/(obj[idx[-1], n] - obj[idx[0], n])

    return cd