# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 23:48:42 2020

@author: t.urita
"""

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.ticker as ptick
from pathlib import Path

from class_kp import Knapsack

from inversion import kp_inversion
from scaling import kp_scaling
# from coverage import *

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

def plot_sol_off(l, base_sol, v_sol, off, base, variant):

    l.append(plt.subplots(1, 1))
    t1_eval = np.unique(base.evaluate(off.copy()), axis = 0)

    l[-1][1].scatter(t1_eval[:, 0], t1_eval[:, 1], marker = '+', c = "gray")
    l[-1][1].scatter(base_sol[:, 0], base_sol[:, 1])

    l[-1][1].xaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
    l[-1][1].yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
    l[-1][1].ticklabel_format(style='sci',scilimits=(0,0))

    l[-1][0].show()

    l.append(plt.subplots(1, 1))
    t2_eval = np.unique(variant.evaluate(off), axis = 0)

    l[-1][1].scatter(t2_eval[:, 0], t2_eval[:, 1], marker = '+', c = "gray")
    l[-1][1].scatter(v_sol[:, 0], v_sol[:, 1])

    l[-1][1].xaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
    l[-1][1].yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
    l[-1][1].ticklabel_format(style='sci',scilimits=(0,0))

    l[-1][0].show()


methods = ["scaling", "inversion"]
paths = []
paths.append(Path("set_seed/" + methods[0]))
paths.append(Path("set_seed/" + methods[1]))

l1 = list(paths[0].glob("**/obj.csv"))
l2 = list(paths[1].glob("**/obj.csv"))

kp = Knapsack()
base_pop = pd.read_csv("set_seed/base_result/pops.csv", header = None).to_numpy()
base_obj = kp.evaluate(base_pop)

parents = np.random.randint(0, 200, size = (10000, 2))
f1 = []
f2 = []

plt.close("all")
plt.rcParams["font.size"] = 20

for s, i in zip(l1, l2):


    rate = float(s.parts[2])

    kp_in = kp_inversion(rate)
    kp_sk = kp_scaling(1 + rate)

    obj = {}

    sk_pop = pd.read_csv(s / ".." / "pops.csv", header = None).to_numpy()
    obj["scaling"] = kp_sk.evaluate(sk_pop)
    sk_offs = bit_flip_mutation(uniform_crossover(base_pop[parents[:, 0], :], sk_pop[parents[:, 1], :]))

    in_pop = pd.read_csv(i / ".." / "pops.csv", header = None).to_numpy()
    obj["inversion"] = kp_in.evaluate(in_pop)
    in_offs = bit_flip_mutation(uniform_crossover(base_pop[parents[:, 0], :], in_pop[parents[:, 1], :]))

    plot_sol_off(f1, base_obj, obj["scaling"], sk_offs, kp, kp_sk)
    plot_sol_off(f2, base_obj, obj["inversion"], in_offs, kp, kp_in)

# evaluation = kp.evaluate(offs)

# u_eval = np.unique(evaluation, axis = 0).T
# plt.scatter(u_eval[0], u_eval[1], marker = '+', c = "gray")
# plt.scatter(base_obj[:, 0], base_obj[:, 1], c = "red")

import subprocess

rate = ["0.05", "0.05", "0.1", "0.1", "0.15", "0.15", "0.2", "0.2", "0.25", "0.25"]
for i, f in enumerate(f1):
    if i % 2 == 0:
        f[0].savefig("set_seed/scaling/crx_t1_" + rate[i] + ".svg", bbox_inches='tight')
        subprocess.call("inkscape set_seed/scaling/crx_t1_" + rate[i] +".svg -M set_seed/scaling/crx_t1_" + rate[i] +".emf")
    else:
        f[0].savefig("set_seed/scaling/crx_t2_" + rate[i] + ".svg", bbox_inches='tight')
        subprocess.call("inkscape set_seed/scaling/crx_t2_" + rate[i] +".svg -M set_seed/scaling/crx_t2_" + rate[i] +".emf")

for i, f in enumerate(f2):
    if i % 2 == 0:
        f[0].savefig("set_seed/inversion/crx_t1_" + rate[i] + ".svg", bbox_inches='tight')
        subprocess.call("inkscape set_seed/inversion/crx_t1_" + rate[i] +".svg -M set_seed/inversion/crx_t1_" + rate[i] +".emf")
    else:
        f[0].savefig("set_seed/inversion/crx_t2_" + rate[i] + ".svg", bbox_inches='tight')
        subprocess.call("inkscape set_seed/inversion/crx_t2_" + rate[i] +".svg -M set_seed/inversion/crx_t2_" + rate[i] +".emf")
