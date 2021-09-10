# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 22:30:08 2020

@author: youle
"""

import sys
import os
sys.path.append(os.path.join(os.pardir, '..'))

import numpy as np

import json
from datetime import datetime
from collections import OrderedDict

import implementation
from implementation.problems.MTO_benchmark import *
from implementation.NSGAII import NSGAII

tasks = task_list
names = name_list

with open("setting.json") as f:
    params = json.load(f, object_pairs_hook=OrderedDict)

path_parent = datetime.today().strftime("%m%d")
os.makedirs(path_parent, exist_ok = True)

results = np.empty((len(tasks), 2, 2))

for t, n, task_no in zip(tasks, names, range(len(tasks))):

    for idx in range(2):

        print(f'{n} Task {idx + 1}')

        path = f'{path_parent}/{n}_Task{idx + 1}'
        os.makedirs(path, exist_ok = True)

        p = t.get_tasks()[idx]

        params.update({"start_time": datetime.now().isoformat()})
        solver = NSGAII(params, p)

        igd = np.zeros(params["ntrial"])

        for i in range(params["ntrial"]):

            np.random.seed(i)

            solver.init_pop()
            solver.execute(params["neval"])

            igd[i] = p.calc_IGD(solver.pop["objectives"])

        params.update({"end_time": datetime.now().isoformat()})
        with open(F'{path}/setting_log.json', 'w') as f:
            json.dump(params, f, indent = 0)

        print("---------mean IGD---------")
        results[task_no, idx, 0] = igd.mean()
        print(results[task_no, idx, 0])

        print("----standard deviation----")
        results[task_no, idx, 1] = igd.std()
        print(results[task_no, idx, 1])

        np.savetxt(f'{path}/all_IGDs.csv', igd, delimiter = ",")

    print("\n" + n +" Finished\n")

np.savetxt(f'{path_parent}/all_results.csv', results.reshape([-1, 2]), delimiter = ",")