# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 19:41:45 2020

@author: t.urita
"""
import sys
import os
sys.path.append(os.path.join(os.pardir, '..'))

import numpy as np

import implementation
from implementation.problems.knapsack import *
from implementation.NSGAII import NSGAII

n_trial = 1
n_eval = 10000
n_obj = 2

p = class_kp.knapsack(objective = n_obj)
solver = NSGAII(500, n_obj, 100, 100, p, 'bin')

ratio = np.empty(n_trial)
os.makedirs("final_pops", exist_ok = True)

for i in range(n_trial):

    solver.init_pop()
    solver.execute(n_eval)

    sol = solver.pop["objectives"][solver.pop["pareto_rank"] == 0]
    # np.savetxt("final_pops/pops" + str(i) + ".dat", sol)

    print("trial " + str(i + 1) + " finished")