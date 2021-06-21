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

import json
from datetime import datetime
from collections import OrderedDict

import implementation
from implementation.problems.MTO_benchmark import *
from implementation.MT_SBMS import MT_SBMS

tasks = [CIHS(), CIMS(), CILS(), PIHS(), PIMS(), PILS(), NIHS(), NIMS(), NILS()]
names = ["CIHS", "CIMS", "CILS", "PIHS", "PIMS", "PILS", "NIHS", "NIMS", "NILS"]

with open("setting.json") as f:
    params = json.load(f, object_pairs_hook=OrderedDict)

path = F'mig_all_a={str(params["alpha"])}_b={str(params["beta"])}'
os.makedirs(path, exist_ok = True)
print(path)

results = np.empty((len(tasks), 2, 2))

for t, n, task_no in zip(tasks, names, range(len(tasks))):

    path_task = [path + "/" + n + "_task1", path + "/" + n + "_task2"]
    os.makedirs(path_task[0], exist_ok = True)
    os.makedirs(path_task[1], exist_ok = True)

    igd = np.empty([2, params["n_trial"]])

    p = t.get_tasks()

    params.update({"start_time": datetime.now().isoformat()})

    solver = MT_SBMS(params, p)

    for trial in range(params["n_trial"]):

        solver.init_pop()
        solver.execute(params["n_gen"])

        for idx in range(2):

            igd[idx][trial] = p[idx].calc_IGD(solver.algs[idx].pop["objectives"])

    for idx in range(2):

        results[task_no, idx, 0] = igd[idx].mean()
        results[task_no, idx, 1] = igd[idx].std()

        np.savetxt(path_task[idx] + "/all_IGDs.csv", igd[idx], delimiter = ',')

    params.update({"end_time": datetime.now().isoformat()})

    with open(F'{path}/setting_log.json', 'w') as f:
        json.dump(params, f, indent = 0)
    print("\n" + n +" Finished\n")

np.savetxt(path + "/all_results.csv", results.reshape([-1, 2]), delimiter = ',')