# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 00:22:37 2020

@author: t.urita
"""
import numpy as np
import matplotlib.pyplot as plt

import sys, os
sys.path.append(os.pardir)

from NSGAII.nsgaii_main import NSGAII
from MOMFEA.MOMFEA_main import MOMFEA

from problems.knapsack.class_kp import knapsack
from problems.knapsack.kp_variants import *

def get_runnning_average(data, n):

    fil = np.ones(n)/n

    return np.convolve(data, fil, mode = 'same')

base = knapsack()
scaling = kp_scaling(1.1)
inversion = kp_inversion(0.1)

p1 = [base, scaling]
p2 = [base, inversion]
n_eval = 100000

solver1 = NSGAII(500, 2, 100, 100, base, 'bin')

mt_solver1 = MOMFEA(500, 2, 100, 100, p1, 'bin')
mt_solver2 = MOMFEA(500, 2, 100, 100, p2, 'bin')

solver1.init_pop()
t1_nsga_data = solver1.execute(n_eval)

mt_solver1.init_pop()
mt_data1 = mt_solver1.execute(n_eval * len(p1))

mt_solver2.init_pop()
mt_data2 = mt_solver2.execute(n_eval * len(p2))

mean_num = 5

t1_nsga_mean = get_runnning_average(t1_nsga_data, mean_num)

t1_mt_mean = get_runnning_average(mt_data1[0], mean_num)
t1_mt_mean2 = get_runnning_average(mt_data2[0], mean_num)

plt.figure(1)
plt.plot(t1_nsga_mean, label = "NSGA-II")
plt.plot(t1_mt_mean, label = "MOMFEA_scaling")
plt.plot(t1_mt_mean2, label = "MOMFEA_inversion")
plt.legend(fontsize = 16)
plt.tick_params(labelsize = 14)

plt.show()