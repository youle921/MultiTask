# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 15:58:18 2019

@author: y5ule
"""

import numpy as np
import itertools

first = ["CI", "PI", "NI"]
last = ["HS", "MS", "LS"]
resultname = ["mean", "stdev"]

result = np.empty([len(first) * len(last) * 2, 2])
names = itertools.product(first, last)

for n, name in zip(range(len(first) * len(last)), names):

    for i in range(2):

        d = np.loadtxt(name[0] + name[1] + str(i + 1) + "_IGD.csv", delimiter = ",", usecols =[0])
        result[n * 2 + i, 0] = d.mean()
        result[n * 2 + i, 1] = d.std()
        
np.savetxt('result_NSGAII.csv', result, delimiter = ',')