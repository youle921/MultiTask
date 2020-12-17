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

import implementation
from implementation.problems.MTO_benchmark import *
from implementation.NSGAII_SBMS import NSGAII_SBMS

tasks = [CIHS(), CIMS(), CILS(), PIHS(), PIMS(), PILS(), NIHS(), NIMS(), NILS()]
names = ["CIHS", "CIMS", "CILS", "PIHS", "PIMS", "PILS", "NIHS", "NIMS", "NILS"]

n_trial = 31
n_eval = 100000

alpha = [2,3,5,10,15,20,40]
beta = [2,3,5,10,15,20,40]

params = [[i, j]for i in alpha for j in beta]

for a, b in params:

    path = "a=" + str(a) + "_b=" + str(b)
    os.mkdir(path)
    print(path)

    results = np.empty((len(tasks), 2, 2))

    for t, n, task_no in zip(tasks, names, range(len(tasks))):

        for idx in range(2):

            path_task = path + "/" + n + "_task" + str(idx + 1)
            os.mkdir(path_task)

            p = t.get_tasks()[idx]
            solver = NSGAII_SBMS(50, 2, 100, 100, p, 'real', t_num_alpha = a, t_num_beta = b)

            igd = np.zeros(n_trial)

            for i in range(n_trial):

                solver.init_pop()
                solver.execute(100000)

                igd[i] = p.calc_IGD(solver.pop["objectives"])

            results[task_no, idx, 0] = igd.mean()
            results[task_no, idx, 1] = igd.std()

            np.savetxt(path_task + "/all_IGDs.csv", igd, delimiter = ',')

        print("\n" + n +" Finished\n")

    np.savetxt(path + "/all_results.csv", results.reshape([-1, 2]), delimiter = ',')