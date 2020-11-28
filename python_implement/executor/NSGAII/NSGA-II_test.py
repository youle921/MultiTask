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
from implementation.NSGAII import NSGAII

# p = NIHS().get_tasks()[1]
# solver = NSGAII(50, 2, 100, 100, p, 'real')
# solver.init_pop()
# solver.execute(100000)

# sol = solver.pop["objectives"][solver.pop["pareto_rank"] == 0]
# var = solver.pop["variables"]
# np.savetxt("final_pops/pops" + str(11) + ".dat", sol)

# tasks = [CIHS(), CIMS(), CILS(), PIHS(), PIMS(), PILS(), NIHS(), NIMS(), NILS()]
# names = ["CIHS", "CIMS", "CILS", "PIHS", "PIMS", "PILS", "NIHS", "NIMS", "NILS"]
tasks = [CIMS(), PIMS(), NIMS()]
names = ["CIMS", "PIMS", "NIMS"]

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

            # sol = solver.pop["objectives"][solver.pop["pareto_rank"] == 0]
            # np.savetxt("final_pops/pops" + str(i) + ".dat", sol)

            igd[i] = p.calc_IGD(solver.pop["objectives"])
            print("Trial " + str(i+1).zfill(2) + ": " + str(igd[i]))

        print("---------mean IGD---------")
        results[task_no, idx, 0] = igd.mean()
        print(results[task_no, idx, 0])

        print("----standard deviation----")
        results[task_no, idx, 1] = igd.std()
        print(results[task_no, idx, 1])

    print("\n" + n +" Finished\n")