# -*- coding: utf-8 -*-

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
from implementation.EMEA import EMEA

task = NILS()

with open("setting.json") as f:
    params = json.load(f, object_pairs_hook=OrderedDict)

p = task.get_tasks()

solver = EMEA(params, p)

igd = np.zeros([2, params["n_trial"]])

for trial in range(params["n_trial"]):

    np.random.seed(trial)
    solver.init_pop()
    solver.execute(params["n_gen"])

    for idx in range(2):

        igd[idx][trial] = p[idx].calc_IGD(solver.algs[idx].pop["objectives"])

