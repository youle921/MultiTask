# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 23:48:42 2020

@author: t.urita
"""

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from pathlib import Path

from class_kp import Knapsack

from inversion import kp_inversion
from scaling import kp_scaling
from coverage import *

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

methods = ["scaling", "inversion"]
paths = []
paths.append(Path("set_seed/" + methods[0]))
paths.append(Path("set_seed/" + methods[1]))

l1 = list(paths[0].glob("**/obj.csv"))
l2 = list(paths[1].glob("**/obj.csv"))

kp = Knapsack()
base_pop = pd.read_csv("set_seed/base_result/pops.csv", header = None).to_numpy()
base_obj = kp.evaluate(base_pop)

for s, i in zip(l1, l2):

    # plt.close("all")
    rate = float(s.parts[2])

    kp_in = kp_inversion(rate)
    kp_sk = kp_scaling(1 + rate)

    obj = {}
    obj["scaling"] = pd.read_csv(s, header = None).to_numpy()
    obj["inversion"] = pd.read_csv(i, header = None).to_numpy()

    tmp = pd.read_csv(s / ".." / "pops.csv", header = None).to_numpy()
    obj["scaling_to1"] = kp.evaluate(tmp)

    tmp = pd.read_csv(i / ".." / "pops.csv", header = None).to_numpy()
    obj["inversion_to1"] = kp.evaluate(tmp)

    base_mig = {}
    base_mig["to_scaling"] =  kp_sk.evaluate(base_pop.copy())
    base_mig["to_inversion"] = kp_in.evaluate(base_pop.copy())

    cs_to2 = coverage(obj["scaling"], base_mig["to_scaling"])
    cs_to1 = coverage(base_obj, obj["scaling_to1"])
    ci_to2 = coverage(obj["inversion"], base_mig["to_inversion"])
    ci_to1 = coverage(base_obj, obj["inversion_to1"])

    print(cs_to2, cs_to1, ci_to2, ci_to1)
    # f1, ax1 = plt.subplots(1, 1)
    # ax1.scatter(base_obj[:, 0], base_obj[:, 1])
    # ax1.scatter(obj["scaling_to1"][:, 0], obj["scaling_to1"][:, 1])
    # ax1.set_title("scaling_Task1")
    # ax1.axis("equal")
    # f1.show()

    # f1, ax1 = plt.subplots(1, 1)
    # ax1.scatter(obj["scaling"][:, 0], obj["scaling"][:, 1])
    # ax1.scatter(base_mig["to_scaling"][:, 0], base_mig["to_scaling"][:, 1])
    # ax1.set_title("scaling_task2")
    # ax1.axis("equal")
    # f1.show()

    # f1, ax1 = plt.subplots(1, 1)
    # ax1.scatter(base_obj[:, 0], base_obj[:, 1])
    # ax1.scatter(obj["inversion_to1"][:, 0], obj["inversion_to1"][:, 1])
    # ax1.set_title("inversion_Task1")
    # ax1.axis("equal")
    # f1.show()

    # f1, ax1 = plt.subplots(1, 1)
    # ax1.scatter(obj["inversion"][:, 0], obj["inversion"][:, 1])
    # ax1.scatter(base_mig["to_inversion"][:, 0], base_mig["to_inversion"][:, 1])
    # ax1.set_title("inversion_task2")
    # ax1.axis("equal")
    # f1.show()

parents = np.random.randint(0, 200, size = (100000, 2))

offs = bit_flip_mutation(uniform_crossover(base_pop[parents[:, 0], :], base_pop[parents[:, 1], :]))

evaluation = kp.evaluate(offs)
cov = coverage(base_obj, evaluation)


u_eval = np.unique(evaluation, axis = 0).T
plt.scatter(u_eval[0], u_eval[1], marker = '+', c = "gray")
plt.scatter(base_obj[:, 0], base_obj[:, 1], c = "red")