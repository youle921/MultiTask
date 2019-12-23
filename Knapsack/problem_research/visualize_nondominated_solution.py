# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 03:00:44 2019

@author: t.urita
"""
import numpy as np
import matplotlib.pyplot as plt
import itertools

from class_kp import Knapsack
from is_nondominated import divide_solution

def solution_plot(f):

    pf, dom, _ = divide_solution(f)
    pf = np.unique(pf, axis = 0)
    dom = np.unique(dom, axis = 0)

    fig, ax = plt.subplots(1, 1)

    ax.scatter(dom[:, 0], dom[:, 1], c = "gray")
    ax.scatter(pf[:, 0], pf[:, 1], c = "red")

    ax.set_xlim(None, np.max(pf[:, 0]) * 1.2)
    ax.set_ylim(None, np.max(pf[:, 1]) * 1.2)

    ax.set_aspect('equal')

    fig.show()

def pf_plot(f):

    pf, _, _ = divide_solution(f)
    pf = np.unique(pf, axis = 0)

    fig, ax = plt.subplots(1, 1)

    ax.scatter(pf[:, 0], pf[:, 1], c = "red")

    ax.set_xlim(None, np.max(pf[:, 0]) * 1.2)
    ax.set_ylim(None, np.max(pf[:, 1]) * 1.2)

    ax.set_aspect('equal')

    fig.show()

np.random.seed(1)
item_num = 15

kp = Knapsack(items = item_num)
sol = np.array(list(itertools.product((0, 1), repeat = item_num)))

f = kp.evaluate(sol)
pf, _, _ = divide_solution(f)
u_pf = np.unique(pf, axis = 0)

sol = np.array(list(itertools.product((0, 1), repeat = item_num)))
kp.shift_size(0.6)
f2 = kp.evaluate(sol)
pf2,_ ,idx2  = divide_solution(f2)
_, u_id = np.unique(pf2, axis = 0, return_index = True)
idx2 = idx2[u_id]

sol = np.array(list(itertools.product((0, 1), repeat = item_num)))
kp.shift_size(0.8)
f3 = kp.evaluate(sol)
pf3, _, idx3 = divide_solution(f3)
_, u_id = np.unique(pf3, axis = 0, return_index = True)
idx3 = idx3[u_id]

sol = np.array(list(itertools.product((0, 1), repeat = item_num)))
kp.shift_size(1.2)
f4 = kp.evaluate(sol)
pf4,_ ,idx4  = divide_solution(f4)
_, u_id = np.unique(pf4, axis = 0, return_index = True)
idx4 = idx4[u_id]

sol = np.array(list(itertools.product((0, 1), repeat = item_num)))
kp.shift_size(1.4)
f5 = kp.evaluate(sol)
pf5, _, idx5 = divide_solution(f5)
_, u_id = np.unique(pf5, axis = 0, return_index = True)
idx5 = idx5[u_id]

# for i in range(pf.shape[0]):
#     print(np.sum(np.sum(f == pf[i, :], axis = 1) == f.shape[1]))

# _, _, idx = divide_solution(f)
# pf2, _, _ = divide_solution(f2)

# plt.scatter(f2[:, 0], f2[:, 1], c = 'gray')
# plt.scatter(f2[idx, 0], f2[idx, 1], s = 200, c='red', marker = '+', linewidths = '1')
# plt.scatter(pf2[:, 0], pf2[:, 1], s = 200, marker = 'x', linewidths = '1')

# X = f[idx]

# U = f2[idx] - X

# plt.quiver(X[:, 0], X[:, 1], U[:, 0], U[:, 1], angles = 'xy', scale_units = 'xy', scale = 1)

plt.scatter(u_pf[:, 0], u_pf[:, 1])
plt.scatter(f[idx2, 0], f[idx2, 1])
plt.scatter(f[idx3, 0], f[idx3, 1])
plt.scatter(f[idx4, 0], f[idx4, 1], s = 200, marker = '+')
plt.scatter(f[idx5, 0], f[idx5, 1], s = 200, marker = 'x')


plt.legend(['  = 1.0', '  = 0.6', '  = 0.8', '  = 1.2', '  = 1.4'], fontsize = 15, bbox_to_anchor=(1.4, 1))
plt.rcParams["font.size"] = 20
plt.savefig('repair.svg', bbox_inches='tight')
