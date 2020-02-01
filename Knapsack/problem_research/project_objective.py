# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 20:04:00 2020

@author: t.urita
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from class_kp import Knapsack

kp = Knapsack()

dir_name = "set_pop/"

methods = ["bitflip", "scaling"]
ext = ".csv"

base_sol = np.loadtxt(dir_name + "baseline/pops_gen" + str(500) + ext, delimiter = ',')

for m in methods:

    p = Path(dir_name + m)
    l = list(p.glob('**/'))

    for f in l[1:]:

        fig, ax = plt.subplots(1, 1)

        cmp_sol = np.loadtxt(str(f) + "/pops_gen" + str(500) + ext, delimiter = ',')

        if m == "scaling" and(f.parts[2] == "0.6" or f.parts[2] == "0.8"):

            cp_sol = base_sol.copy()
            kp.shift_size(float(f.parts[2]))
            obj_base = kp.evaluate(cmp_sol)
            obj_prj = kp.evaluate(cp_sol)

            kp.shift_size(1.0)

        else:
            obj_base = kp.evaluate(base_sol)
            obj_prj = kp.evaluate(cmp_sol)

        ax.scatter(obj_base[:, 0], obj_base[:, 1], s = 150,  marker= '+')
        ax.scatter(obj_prj[:, 0], obj_prj[:, 1], s = 100,  marker= 'x')

        fig.show()
