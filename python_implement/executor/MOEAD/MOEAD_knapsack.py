# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 19:41:45 2020

"""
import numpy as np

import json
from datetime import datetime
from collections import OrderedDict

import sys
import os
sys.path.append(os.path.join(os.pardir, '..'))

import implementation
from implementation.problems.knapsack import *
from implementation.MOEAD import MOEAD

dirname = "final_pops_PBI_"
os.makedirs(dirname, exist_ok = True)

with open("setting.json") as f:
    params = json.load(f, object_pairs_hook=OrderedDict)

p = class_kp.knapsack(objective = params["nobj"])
solver = MOEAD(params, p)

params.update({"start_time": datetime.now().isoformat()})

for i in range(params["ntrial"]):

    np.random.seed(i)
    solver.init_pop()
    solver.execute(params["neval"])

    np.savetxt(F'{dirname}/pops{i}.dat', solver.get_NDsolution())

    print(F'trial {i + 1} finished')

params.update({"end_time": datetime.now().isoformat()})

with open(F'{dirname}/setting_log.json', 'w') as f:
    json.dump(params, f, indent = 0)