"""
Created on Fri Apr 17 22:30:08 2020

@author: youle
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
from implementation.problems.reproblems_master import *
from implementation.MOMFEA import MOMFEA

tasks = get_prob_pairs()
names = [f'Problem Set{i + 1}' for i in range(len(tasks))]

with open("setting.json") as f:
    params = json.load(f, object_pairs_hook=OrderedDict)

path = datetime.today().strftime("%m%d")
os.makedirs(path, exist_ok = True)
print(path)

results = np.empty((len(tasks), 2, 2))

for t, n, task_no in zip(tasks, names, range(len(tasks))):

    path_task = [f'{path}/{n}_{task.problem_name}' for task in t.get_tasks()]
    os.makedirs(path_task[0], exist_ok = True)
    os.makedirs(path_task[1], exist_ok = True)

    p = t.get_tasks()

    params.update({"start_time": datetime.now().isoformat()})
    solver = MOMFEA(params, p)

    igd = np.zeros([2, params["n_trial"]])

    for trial in range(params["n_trial"]):

        np.random.seed(trial)
        solver.init_pop()
        solver.execute(params["n_eval"])

        for idx in range(2):

            igd[idx][trial] = p[idx].calc_IGD(solver.pops["objectives"][idx])

    params.update({"end_time": datetime.now().isoformat()})
    
    results[task_no, :, 0] = np.median(igd, axis = 1)
    results[task_no, :, 1] = igd.std(axis = 1)

    for idx in range(2):

        np.savetxt(path_task[idx] + "/all_IGDs.csv", igd[idx], delimiter = ',')
        with open(F'{path_task[idx]}/setting_log.json', 'w') as f:
            json.dump(params, f, indent = 0)

    print("\n" + n +" Finished\n")

np.savetxt(path + "/all_results.csv", results.reshape([-1, 2]), delimiter = ',')