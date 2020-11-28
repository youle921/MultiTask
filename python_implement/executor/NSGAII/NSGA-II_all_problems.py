# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 22:30:08 2020

@author: t.urita
"""
import sys
import os

sys.path.append(os.pardir)

from nsgaii_main import NSGAII

import numpy as np
import matplotlib.pyplot as plt

from problems.MTO_benchmark import *

tasks = [CIHS(), CIMS(), CILS(), PIHS(), PIMS(), PILS(), NIHS(), NIMS(), NILS()]
names = ["CIHS", "CIMS", "CILS", "PIHS", "PIMS", "PILS", "NIHS", "NIMS", "NILS"]

n_trial = 31
results = np.empty((len(tasks), 2, 2))

for t, n, task_no in zip(tasks, names, range(len(tasks))):

    for idx in range(2):

        print(n + " Task" + str(idx + 1))

        p = t.get_tasks()[idx]
        solver = NSGAII(50, 2, 100, 100, p, 'real')

        igd = np.zeros(n_trial)

        for i in range(n_trial):
            solver.import_pop(n, idx + 1, i + 1)
            # solver.init_pop()
            solver.execute(100000)

            igd[i] = p.calc_IGD(solver.pop["objectives"])

        np.savetxt("SBX_java_result/" + n + "_Task" + str(idx + 1) + "IGD.csv", igd, delimiter = ",")

        print("---------mean IGD---------")
        results[task_no, idx, 0] = igd.mean()
        print(results[task_no, idx, 0])

        print("----standard deviation----")
        results[task_no, idx, 1] = igd.std()
        print(results[task_no, idx, 1])

    print("\n" + n +" Finished\n")