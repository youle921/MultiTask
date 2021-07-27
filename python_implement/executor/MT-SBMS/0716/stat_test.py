# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 22:31:07 2021

@author: youle
"""
from collections import OrderedDict

import numpy as np
from scipy import stats

import scikit_posthocs as sp

import Orange
import matplotlib.pyplot as plt

n_trial = 31

size = [1,5,10,20,30,40,50,60]
# size = [2,5,10,20,30]

dir_names = [f'm_size={i}_a=10_b=2' for i in size]

names = ["CIHS", "CIMS", "CILS", "PIHS", "PIMS", "PILS", "NIHS", "NIMS", "NILS"]
names_ = [f'{n}_{t}' for n in names for t in ["task1", "task2"]]

filename = "all_IGDs.csv"

results = OrderedDict()

graph_names = [f's = {s}' for s in size]

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

        averank = stats.rankdata(testing_data, axis = 0).mean(axis = 1)
        cd = Orange.evaluation.compute_CD(averank, testing_data.shape[1])
        Orange.evaluation.graph_ranks(averank, graph_names, cd = cd)
        plt.show()
        plt.savefig(f'{n}_cd_diagram.svg')
    else:
        print("not Significance\n")


