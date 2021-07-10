# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 01:25:57 2021

@author: youle
"""

from scipy import stats
import numpy as np

def calc_feasible_ratio(n_items, n_rules):

    n_pairs = n_items * (n_items - 1) * 0.5
    ratio = [[(n_pairs - (i * (i - 1) * 0.5) - j)/(n_pairs - j) for i in range(n_items + 1)] for j in range(n_rules)]
    prob = stats.binom.pmf(np.arange(n_items + 1), n_items, 0.5)

    return prob * np.clip(ratio, 0, None).prod(axis = 0)

def rule_generator(n_items, n_rules):

    n = n_items*(n_items-1)*0.5

    candidate = np.random.choice(int(n), n_rules)

    second = np.ceil(((8 * candidate)**0.5 - 1) / 2)
    first = ((second + 1) * second)/2 - candidate

    return np.array([first, second], dtype = int).T

def check_feasible(pop, rules):

    n_rules = rules.shape[0]
    violated = pop[:, rules].sum(axis = 2) == rules.shape[1]

    if n_rules > 1:
        is_feasible = ~np.logical_or(*violated.T,)
        return is_feasible
    else:
        return ~violated

n_items = 10
n_rules = 3

rules = rule_generator(n_items, n_rules)

n_pop = 5
pop = np.random.randint(0, 2, size = [n_pop, n_items])

mask = check_feasible(pop, rules)
r = calc_feasible_ratio(10, 2).sum()