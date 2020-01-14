# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 02:18:29 2020

@author: t.urita
"""

import numpy as np

def min_hamming(data, datasets):
    dist = np.logical_xor(data, datasets)

    return min(np.sum(dist, axis = 1))

base = "result_moead_1.0/MOEAD/pops_"
comp = "result_moead_1.4/MOEAD/pops_"
ext = "gen.csv"

dist_list = np.zeros([500, 1])

for i in range(1, 501):

    d1 = np.loadtxt(comp + str(i) + ext, delimiter = ',')
    base_data = np.loadtxt(base + str(i) + ext, delimiter = ',')
    for n in range(200):
        dist_list[i - 1] += min_hamming(d1[n, :], base_data)

avr_dist = dist_list / 200

