# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 22:04:34 2019

@author: t.urita
"""

import numpy as np

data = np.loadtxt("knapsack_2_500to8.txt", skiprows = 2)
ext = ".csv"

for i in range(8):
    kp = data[i * 1001 + 1: (i + 1) * 1001]
    kp_weight = kp[0::2]
    kp_profit = kp[1::2]

    np.savetxt("knapsack_500_weight" + str(i + 1) + ext, kp_weight, delimiter = ',')
    np.savetxt("knapsack_500_profit" + str(i + 1) + ext, kp_profit, delimiter = ',')
