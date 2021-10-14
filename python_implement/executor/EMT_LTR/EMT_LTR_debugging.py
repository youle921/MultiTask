# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.join(os.pardir, '..'))

import numpy as np

import json
from datetime import datetime
from collections import OrderedDict

import implementation
from implementation.problems.MTO_benchmark import *
from implementation.EMT_LTR import EMTLTR

from implementation.indicator.IGD import IGD

task = CIHS()

with open("setting.json") as f:
    params = json.load(f, object_pairs_hook=OrderedDict)

p = task.tasks

solver = EMTLTR(params, p)

igd = np.zeros([2, params["n_trial"]])
metric_calc = [IGD(t.IGD_ref) for t in p]

for trial in range(params["n_trial"]):

    np.random.seed(trial)
    solver.init_pop()
    solver.execute(params["n_eval"])

    for idx in range(2):

        igd[idx][trial] = metric_calc[idx].compute(solver.pops["objectives"][idx])

