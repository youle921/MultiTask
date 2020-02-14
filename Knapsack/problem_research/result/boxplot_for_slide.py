# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 01:13:02 2020

@author: t.urita
"""
from pathlib import Path
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

base_hv_t1 = pd.read_csv("knapsack_baseline/final_pops/hv.csv", header = None)
base_name = "knapsack_"

problems = ["scaling", "profitflip"]
params= ["_1.1", "_0.1"]

alg = ["momfea", "NSGA-II-island_interval5_size10"]

label = ["NSGA-II", "MOMFEA", "島モデル"]

plt.rcParams["font.size"] = 20

for i in range(2):

    plot_data = [[], []]
    plot_data[0].append(base_hv_t1.to_numpy().flatten())

    footer = base_name + problems[i] + params[i]
    path = Path(footer)
    base_hv_t2 = pd.read_csv(list(path.glob("**/hv.csv"))[0], header = None)
    plot_data[1].append(base_hv_t2.to_numpy().flatten())

    for a in alg:

        path = Path(a + "/" + footer + "/base")
        cmp_hv_t1 = pd.read_csv(list(path.glob("**/hv.csv"))[0], header = None)
        path = Path(a + "/" + footer + "/" + problems[i])
        cmp_hv_t2 = pd.read_csv(list(path.glob("**/hv.csv"))[0], header = None)

        plot_data[0].append(cmp_hv_t1.to_numpy().flatten())
        plot_data[1].append(cmp_hv_t2.to_numpy().flatten())

    fig, ax = plt.subplots(1, 1)
    ax.boxplot(plot_data[0], labels = label)
    # ax.set_title(problems[i] + " Task1")
    fig.show()

    fig, ax = plt.subplots(1, 1)
    ax.boxplot(plot_data[1], labels = label)
    # ax.set_title(problems[i] + " Task2")
    fig.show()

        # np.savetxt("statistical_result/" + p + param + "Task1.csv", save_data[0], delimiter = ',')
        # np.savetxt("statistical_result/" + p + param + "Task2.csv", save_data[1], delimiter = ',')
