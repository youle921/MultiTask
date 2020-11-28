# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 22:30:08 2020

@author: t.urita
"""
import sys
import os

sys.path.append(os.pardir)

# from problems.MTO_benchmark.PIMS import PIMS
from nsgaii_main import NSGAII

import numpy as np
import matplotlib.pyplot as plt

from problems.MTO_benchmark import *

problems = [CIMS().get_tasks()[1], PIMS().get_tasks()[0], NIMS().get_tasks()[1]]
names = ["CIMS T2","PIMS T1", "NIMS T2"]

n_trial = 31
results = np.empty((len(problems), 2))

for p, n, idx in zip(problems, names, range(len(problems))):

    print(n)

    solver = NSGAII(50, 2, 100, 100, p, 'real')

    igd = np.zeros(n_trial)

    for i in range(n_trial):

        solver.init_pop()
        solver.execute(100000)

        igd[i] = p.calc_IGD(solver.pop["objectives"])
        print("Trial " + str(i+1).zfill(2) + ": " + str(igd[i]))

    print("---------mean IGD---------")
    results[idx, 0] = igd.mean()
    print(results[idx, 0])

    print("----standard deviation----")
    results[idx, 1] = igd.std()
    print(results[idx, 1])

    print("\n" + n +" Finished\n")