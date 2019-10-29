# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 15:58:18 2019

@author: y5ule
"""

import numpy as np

first = ["CI", "NI", "PI"]
last = ["HS", "LS", "MS"]
resultname = ["mean", "stdev"]

result = np.empty([len(first) * len(last) * 2, 2])
names = [f + l for f in first for l in last]

for n, name in enumerate(names):

    for i in range(2):

        d = np.loadtxt(name + str(i + 1) + "_IGD.csv", delimiter = ",", usecols =[0])
        result[n * 2 + i, 0] = d.mean()
        result[n * 2 + i, 1] = d.std()

np.savetxt('result_NSGAII.csv', result, delimiter = ',')