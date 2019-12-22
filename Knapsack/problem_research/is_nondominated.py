# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 01:20:43 2019

@author: t.urita
"""

import numpy as np

def divide_solution(f):

    pf, idx = nondominated_solution(f)
    dominated = np.delete(f, idx, 0)

    return pf, dominated, idx

def nondominated_solution(f):

    true_idx = np.arange(f.shape[0])
    obj = f.copy()

    i = 0

    while(obj.shape[0] > i):

        key = true_idx[i]
        idx = np.logical_not(is_dominated(obj, obj[i, :]))
        obj = obj[idx]
        true_idx = true_idx[idx]

        i = np.where(true_idx == key)[0][0] + 1

    return obj, true_idx

def is_dominated(obj, key):

    n_obj = len(key)

    return np.logical_and(np.sum(obj <= key, axis = 1) == n_obj, np.sum(obj == key, axis = 1) != n_obj)

if __name__ == "__main__":

    import matplotlib.pyplot as plt

    sol = np.random.rand(1000, 2)
    sol2, idx = nondominated_solution(sol)

    d_sol = np.delete(sol, idx, 0)

    plt.scatter(d_sol[:, 0], d_sol[:, 1])
    plt.scatter(sol2[:, 0], sol2[:, 1])

    plt.show()




