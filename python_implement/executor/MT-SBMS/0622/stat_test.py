# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 22:31:07 2021

@author: youle
"""
from collections import OrderedDict

import numpy as np
from scipy import stats

import scikit_posthocs as sp

n_trial = 31

size = [1,2,3,5,7,10,15,20,30]
# size = [2,5,10,20,30]

dir_names = [f'm_size={i}_a=10_b=2' for i in size]

names = ["CIHS", "CIMS", "CILS", "PIHS", "PIMS", "PILS", "NIHS", "NIMS", "NILS"]
names_ = [f'{n}_{t}' for n in names for t in ["task1", "task2"]]

filename = "all_IGDs.csv"

results = OrderedDict()

for n in names_:
    print(f'----Testing Task: {n}----\n')
    testing_data = np.empty([len(size), n_trial])
    for i, d in enumerate(dir_names):
        testing_data[i] = np.loadtxt(f'{d}/{n}/{filename}', delimiter = ",")

    _, p = stats.friedmanchisquare(*testing_data,)

    print(f'p value: {p}')
    if p < 0.05:
        print("Significance\n")
        nemenyi_result = sp.posthoc_nemenyi_friedman(testing_data.T)
        result_str = nemenyi_result.astype("str")
        results[n] = np.triu(np.where(nemenyi_result > 0.05, result_str, "*" + result_str), k = 1)
    else:
        print("not Significance\n")


