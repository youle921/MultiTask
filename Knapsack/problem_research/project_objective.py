# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 20:04:00 2020

@author: t.urita
"""
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

import subprocess
import os

from class_kp import Knapsack

kp = Knapsack()

dir_name = "set_pop/"

methods = ["bitflip", "scaling", "profitflip"]
ext = ".csv"

base_sol = pd.read_csv(dir_name + "baseline/pops_gen" + str(500) + ext, header = None).to_numpy()

plt.close("all")
plt.rcParams["font.size"] = 20

for m in methods:

    p = Path(dir_name + m)
    l = list(p.glob('**/'))

    for f in l[1:]:

        fig, ax = plt.subplots(1, 1)

        cmp_sol = pd.read_csv(str(f) + "/pops_gen" + str(500) + ext, header = None).to_numpy()

        if m == "scaling" and(f.parts[2] == "0.6" or f.parts[2] == "0.8"):

            cp_sol = base_sol.copy()
            kp.shift_size(float(f.parts[2]))
            obj_base = kp.evaluate(cmp_sol)
            obj_prj = kp.evaluate(cp_sol)

            kp.shift_size(1.0)

        else:
            obj_base = kp.evaluate(base_sol)
            obj_prj = kp.evaluate(cmp_sol)

        ax.scatter(obj_base[:, 0], obj_base[:, 1], s = 150,  marker= '+', label = "Task1")
        ax.scatter(obj_prj[:, 0], obj_prj[:, 1], s = 100,  marker= 'x', label = "Task2")
        ax.legend(fontsize = 15, bbox_to_anchor=(1.35, 1))

        n = dir_name + m + "/projection_" + f.parts[2]
        fig.savefig(n + ".svg", bbox_inches='tight')
        subprocess.call("inkscape " + n + ".svg -M " + n + ".emf")
        os.remove(n + ".svg")
