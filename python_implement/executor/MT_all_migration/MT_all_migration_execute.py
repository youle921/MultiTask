# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 22:30:08 2020

@author: t.urita
"""
import sys
import os
sys.path.append(os.path.join(os.pardir, '..'))

import numpy as np
import matplotlib.pyplot as plt
import datetime

import implementation
from implementation.problems.MTO_benchmark import *
from implementation.MT_all_migration import MT_all_mig

tasks = [CIHS(), CIMS(), CILS(), PIHS(), PIMS(), PILS(), NIHS(), NIMS(), NILS()]
names = ["CIHS", "CIMS", "CILS", "PIHS", "PIMS", "PILS", "NIHS", "NIMS", "NILS"]

n_trial = 1
n_gen = 10

path = datetime.date.today().strftime("%m%d")
os.makedirs(path, exist_ok = True)
print(path)

results = np.empty((len(tasks), 2, 2))

for t, n, task_no in zip(tasks, names, range(len(tasks))):

    path_task = [path + "/" + n + "_task1", path + "/" + n + "_task2"]
    os.makedirs(path_task[0], exist_ok = True)
    os.makedirs(path_task[1], exist_ok = True)

    p = t.get_tasks()
    solver = MT_all_mig(50, 2, 100, 100, p, 'real')

    igd = np.zeros([2, n_trial])

    for trial in range(n_trial):

        solver.init_pop()
        solver.execute(n_gen)

        for idx in range(2):

            igd[idx][trial] = p[idx].calc_IGD(solver.algs[idx].pop["objectives"])

    for idx in range(2):

        results[task_no, idx, 0] = igd[idx].mean()
        results[task_no, idx, 1] = igd[idx].std()

        np.savetxt(path_task[idx] + "/all_IGDs.csv", igd[idx], delimiter = ',')

    print("\n" + n +" Finished\n")

np.savetxt(path + "/all_results.csv", results.reshape([-1, 2]), delimiter = ',')