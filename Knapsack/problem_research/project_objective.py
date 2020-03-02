# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 20:04:00 2020

@author: t.urita
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ptick

import numpy as np

from pathlib import Path

import subprocess
import os

from class_kp import Knapsack
from inversion import kp_inversion
from scaling import kp_scaling

def uniform_crossover(parent1, parent2):

    offspring = parent1
    mask = np.random.rand(*parent1.shape) > 0.5
    offspring[mask] = parent2[mask]

    return offspring

def bit_flip_mutation(offspring):

    mutation_ratio = 1 / offspring.shape[1]
    mutation_mask = np.random.rand(*offspring.shape) < mutation_ratio
    offspring[mutation_mask] = 1 - offspring[mutation_mask]

    return offspring

def create_offs(pop1, pop2):
    rand = np.random.randint(0, 200, size = [100000, 2])
    p1 = pop1[rand[:, 0],:]
    p2 = pop2[rand[:, 1],:]

    return(bit_flip_mutation(uniform_crossover(p1, p2)))

kp = Knapsack()

dir_name = "set_seed/"

methods = ["scaling", "inversion"]
ext = ".csv"

obj_base = pd.read_csv(dir_name + "base_result/obj" + ext, header = None).to_numpy()
sol_base = pd.read_csv(dir_name + "base_result/pops" + ext, header = None).to_numpy()

kp_variants = []

kp_variants.append(kp_scaling(1.25))
kp_variants.append(kp_inversion(0.25))

plt.close("all")
plt.rcParams["font.size"] = 20

f1 = []
f2 = []

for i, m in enumerate(methods):

    f1.append(plt.subplots(1, 1))
    f1[-1][1].scatter(obj_base[:, 0], obj_base[:, 1], s = 150, marker = '+', label = "Task1")
    # f1.append(plt.subplots(1, 1))
    # f1[-1][1].scatter(obj_base[:, 0], obj_base[:, 1], zorder = 10, label = "population")

    f2.append(plt.subplots(1, 1))
    base_prj = kp_variants[i].evaluate(sol_base.copy()).T
    f2[-1][1].scatter(base_prj[0], base_prj[1], s = 150, marker = '+', label = "Task1")

    p = Path(dir_name + m)

    for l in p.glob("0.25/**/obj.csv"):
        # cmp_obj = pd.read_csv(l, header = None).to_numpy()

        cmp_sol = pd.read_csv(l / '..' / 'pops.csv', header = None).to_numpy()
        cmp_obj = kp_variants[i].evaluate(cmp_sol)
        # f2.append(plt.subplots(1, 1))
        f2[-1][1].scatter(cmp_obj[:, 0], cmp_obj[:, 1], s = 150, marker = '+')
        # f2[-1][1].scatter(cmp_obj[:, 0], cmp_obj[:, 1], zorder = 10, label = "population")


        cmp_prj = kp.evaluate(cmp_sol.copy()).T
        f1[-1][1].scatter(cmp_prj[0], cmp_prj[1], s = 150, marker = "+", label = "Task2")

    # f1[-1][1].legend(fontsize = 15, bbox_to_anchor=(1.35, 1))

    f1[-1][1].xaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
    f1[-1][1].yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
    f1[-1][1].ticklabel_format(style='sci',scilimits=(0,0))
    f1[-1][0].show()

    # f2[-1][1].legend(fontsize = 15, bbox_to_anchor=(1.35, 1))

    f2[-1][1].xaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
    f2[-1][1].yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
    f2[-1][1].ticklabel_format(style='sci',scilimits=(0,0))
    f2[-1][0].show()

        # n = dir_name + m + "/projection_" + f.parts[2]
        # fig.savefig(n + ".svg", bbox_inches='tight')
        # subprocess.call("inkscape " + n + ".svg -M " + n + ".emf")
        # os.remove(n + ".svg")

# f1[0][0].savefig("set_seed/scaling/prj_t1_0.25.svg", bbox_inches='tight')
# subprocess.call("inkscape set_seed/scaling/prj_t1_0.25.svg -M set_seed/scaling/prj_t1_0.25.emf")
# f2[0][0].savefig("set_seed/scaling/prj_t2_0.25.svg", bbox_inches='tight')
# subprocess.call("inkscape set_seed/scaling/prj_t2_0.25.svg -M set_seed/scaling/prj_t2_0.25.emf")

# f1[1][0].savefig("set_seed/inversion/prj_t1_0.25.svg", bbox_inches='tight')
# subprocess.call("inkscape set_seed/inversion/prj_t1_0.25.svg -M set_seed/inversion/prj_t1_0.25.emf")
# f2[1][0].savefig("set_seed/inversion/prj_t2_0.25.svg", bbox_inches='tight')
# subprocess.call("inkscape set_seed/inversion/prj_t2_0.25.svg -M set_seed/inversion/prj_t2_0.25.emf")