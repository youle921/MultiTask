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
from implementation.CNSGAII import NSGAII_SP

import matplotlib.animation as animation

n_trial = 31
n_eval = 400000
n_obj = 2

p = kp_scaling(1.2)
solver = NSGAII_SP(500, n_obj, n_obj, 100, 100, p, 'bin')

ratio = np.empty(n_trial)
os.makedirs("final_pops_scaling", exist_ok = True)

for i in range(n_trial):

    np.random.seed(i)
    solver.init_pop()
    solver.set_analyzer(["variables", "objectives"], dulation = 1)
    solver.execute(n_eval)

    sol = solver.get_NDsolution()

    #gif作るやつ 繰り返しoffにする方法が見つからない
    # anim = solver.visualize_optimization()
    # w = animation.PillowWriter(fps=20)
    # anim.save('animation_test.gif', writer=w)

    np.savetxt("final_pops_scaling/pops" + str(i) + ".dat", sol)

    ratio[i] = sol.shape[0] / 100
    print(ratio[i])
    print("trial " + str(i + 1) + " finished")