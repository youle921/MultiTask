# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 18:31:05 2020

@author: t.urita
"""

from pathlib import Path
import pandas as pd
import numpy as np

from scipy import stats

import matplotlib.pyplot as plt

Path("statistical_result").mkdir(exist_ok = "True")

base_hv_t1 = pd.read_csv("Knapsack_baseline/final_pops/hv.csv", header = None)
base_name = "Knapsack_"

dir_list = list(Path().glob("NSGA-II*"))
alg = ["momfea"]
alg.extend(list(map(str, dir_list)))

problems = ["bitflip", "scaling", "profitflip"]
sr = ["0.8", "0.9", "1.1", "1.2"]
fr = ["0.05", "0.1", "0.15", "0.2", "0.25"]
pfr = ["0.05", "0.1", "0.15", "0.2", "0.25"]

param_dict = {}
param_dict["bitflip"] = fr
param_dict["scaling"] = sr
param_dict["profitflip"] = pfr

for p in problems:

    for param in param_dict[p]:

        plot_data = [[], []]
        plot_data[0].append(base_hv_t1.to_numpy().flatten())
        save_data = np.zeros([2, 2, len(alg) + 1])

        footer = base_name + p + "_" + param
        path = Path(footer)
        base_hv_t2 = pd.read_csv(list(path.glob("**/hv.csv"))[0], header = None)
        plot_data[1].append(base_hv_t2.to_numpy().flatten())
        save_data[0, 0, 0] = base_hv_t1.median()
        save_data[1, 0, 0] = base_hv_t2.median()

        for i, a in enumerate(alg):

            path = Path(a + "/" + footer + "/base")
            cmp_hv_t1 = pd.read_csv(list(path.glob("**/hv.csv"))[0], header = None)
            path = Path(a + "/" + footer + "/" + p)
            cmp_hv_t2 = pd.read_csv(list(path.glob("**/hv.csv"))[0], header = None)

            save_data[0, 0, i + 1] = cmp_hv_t1.median()
            save_data[1, 0, i + 1] = cmp_hv_t2.median()

            _, p1 = stats.mannwhitneyu(base_hv_t1, cmp_hv_t1, alternative = 'two-sided')
            _, p2 = stats.mannwhitneyu(base_hv_t2, cmp_hv_t2, alternative = 'two-sided')

            # save reject(-1(NSGA-II win), 1(MTO win)) or not(0)
            if save_data[0, 0, 0] - save_data[0, 0, i + 1] > 0:
                save_data[0, 1, i + 1] = (p1 < 0.05) *-1
            else:
                save_data[0, 1, i + 1] = p1 < 0.05

            if save_data[1, 0, 0] - save_data[1, 0, i + 1] > 0:
                save_data[1, 1, i + 1] = (p2 < 0.05) *-1
            else:
                save_data[1, 1, i + 1] = p2 < 0.05

            plot_data[0].append(cmp_hv_t1.to_numpy().flatten())
            plot_data[1].append(cmp_hv_t2.to_numpy().flatten())

        fig, ax = plt.subplots(1, 1)
        ax.boxplot(plot_data[0])
        ax.set_title(p + param + " Task1")
        fig.show()

        fig, ax = plt.subplots(1, 1)
        ax.boxplot(plot_data[1])
        ax.set_title(p + param + " Task2")
        fig.show()

        # np.savetxt("statistical_result/" + p + param + "Task1.csv", save_data[0], delimiter = ',')
        # np.savetxt("statistical_result/" + p + param + "Task2.csv", save_data[1], delimiter = ',')

p = Path("statistical_result")
l = list(p.glob("*.csv"))
flag = np.zeros([len(l), 11])

for i, f in enumerate(l):

    flag[i] = pd.read_csv(f, header = None, skiprows = 1)
