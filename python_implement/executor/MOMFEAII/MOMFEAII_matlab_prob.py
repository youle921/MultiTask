# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 23:22:50 2020

@author: youle
"""

import sys
import os
sys.path.append(os.path.join(os.pardir, '..'))

import numpy as np

import json
from collections import OrderedDict

import implementation
from implementation.problems.MTO_benchmark import *
from implementation.MOMFEAII import MOMFEAII

task = [CIHS()]

with open("setting.json") as f:
    params = json.load(f, object_pairs_hook=OrderedDict)

for t in task:

    p = t.get_tasks()
    for i in range(2):
        p[i].ndim = 10
        p[i].lower = p[i].lower[:10]
        p[i].upper = p[i].upper[:10]

    solver = MOMFEAII(params, p)

    igd = np.zeros([params["n_trial"], 2])

    for trial in range(params["n_trial"]):

        np.random.seed(trial)
        solver.init_pop()
        solver.execute(20000)
        # solver.execute(params["n_eval"])

        for idx in range(2):

            igd[trial][idx] = p[idx].calc_IGD(solver.pops["objectives"][idx])