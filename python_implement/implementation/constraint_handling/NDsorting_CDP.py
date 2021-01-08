# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 22:41:43 2021

@author: t.urita
"""
import numpy as np

def NDsorting_CDP(union, violation, num):

    r = 0
    rank = -np.ones(union.shape[0], dtype = int)

    # for minmization problem(compalator: >)

    feasible_mask = violation.sum(axis = 1) == 0
    feasible_num = feasible_mask.sum()
    union_feasible = union[feasible_mask]

    union_sorted = union_feasible[np.argsort(union_feasible[:, 0])]
    is_dominated = (union_feasible[:, None, :] >= union_feasible[None, :, :]).prod(axis = 2) * \
        (union_feasible[:, None, :] > union_feasible[None, :, :]).max(axis = 2)

    feasible_rank = -np.ones(feasible_num)
    if feasible_num > num:

        while(np.sum(feasible_rank != -1) < num):

            NDsolution = is_dominated.max(axis = 1) == 0
            feasible_rank[NDsolution] = r
            r += 1

            is_dominated[:, NDsolution] = 0
            is_dominated[NDsolution] = 1

    else:
        while(np.sum(feasible_rank != -1) < feasible_num):

            NDsolution = is_dominated.max(axis = 1) == 0
            feasible_rank[NDsolution] = r
            r += 1

            is_dominated[:, NDsolution] = 0
            is_dominated[NDsolution] = 1

        order = np.argsort(violation.sum(axis = 1))[feasible_num : num]
        rank[order] = 1000 + np.arange(num - feasible_num)

    rank[feasible_mask] = feasible_rank
    return rank