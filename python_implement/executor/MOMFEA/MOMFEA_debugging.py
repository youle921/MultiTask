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
from implementation.MOMFEA import MOMFEA

task = [PIHS(), PILS()]

with open("setting.json") as f:
    params = json.load(f, object_pairs_hook=OrderedDict)

for t in task:
    p = t.get_tasks()

    solver = MOMFEA(params, p)

    igd = np.zeros([2, params["n_trial"]])

    for trial in range(params["n_trial"]):

        np.random.seed(trial)
        solver.init_pop()
        solver.execute(params["n_eval"])

        for idx in range(2):

            igd[idx][trial] = p[idx].calc_IGD(solver.pops["objectives"][idx])