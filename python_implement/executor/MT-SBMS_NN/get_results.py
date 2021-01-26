# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 02:04:13 2021

@author: t.urita
"""

import numpy as np
from sklearn import preprocessing

params = [2,3,5,10,15,20,40]

dir_names = ["a=" + str(i) + "_b=" + str(j)for i in params for j in params]

names = ["CIHS", "CIMS", "CILS", "PIHS", "PIMS", "PILS", "NIHS", "NIMS", "NILS"]
results = {}

keys = [name + "_" + tasks for name in names for tasks in ["task1", "task2"]]
for k in keys:
    results[k] = np.zeros(len(dir_names))

for i, d in enumerate(dir_names):
    for k in keys:
        mean = np.loadtxt(d + "/" + k + "/all_IGDS.csv", delimiter = ",").mean()
        results[k][i] = mean

out = np.vstack([*map(preprocessing.minmax_scale, results.values())])

idx = out.sum(axis = 0).argmin()
best_params = dir_names[idx]
print("best paremeters is {}".format(best_params))