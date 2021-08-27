# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 01:52:22 2021

@author: youle
"""

import numpy as np

npop = 10

pop = {}
pop["variables"] = np.random.rand(npop, 8)

learned_size = np.zeros([2])
class_probability = np.zeros([2])

mu = np.empty([2, 8])
sigma = np.empty([2, 8])

n = 10
in_front = np.array([True, True, True, False, False, False, False, True, False, False])

pos_n = in_front.sum()
neg_n = n - pos_n

neg_denom = learned_size[0] + neg_n
pos_denom = learned_size[1] + pos_n

class_probability[0] = (learned_size.sum() * class_probability[0] + neg_n)\
    / (learned_size.sum() + n)
class_probability[1] = (learned_size.sum() * class_probability[1] + in_front.sum())\
    / (learned_size.sum() + n)

tmp_s0 = ((sigma[0] + mu[0]**2) * learned_size[0] + (pop["variables"][~in_front].var(axis = 0) + pop["variables"][~in_front].mean(axis = 0)**2) *neg_n) / neg_denom
tmp_s1 = ((sigma[1] + mu[1]**2) * learned_size[1] + (pop["variables"][in_front].var(axis = 0) + pop["variables"][in_front].mean(axis = 0)**2) *pos_n) / pos_denom

mu[0] = (learned_size[0] * mu[0] + pop["variables"][~in_front].sum(axis = 0))\
    / neg_denom
mu[1] = (learned_size[1] * mu[1] + pop["variables"][in_front].sum(axis = 0))\
    /pos_denom

sigma[0] = tmp_s0 - mu[0]**2
sigma[1] = tmp_s1 - mu[1]**2

learned_size[0] += neg_n
learned_size[1] += pos_n

mu_copy = mu.copy()
sigma_copy = sigma.copy()

pop2 = {}

pop2["variables"] = np.random.rand(npop, 8)
n = 10
in_front = np.array([True, True, True, False, False, False, False, True, False, False])

pos_n = in_front.sum()
neg_n = n - pos_n

neg_denom = learned_size[0] + neg_n
pos_denom = learned_size[1] + pos_n

class_probability[0] = (learned_size.sum() * class_probability[0] + neg_n)\
    / (learned_size.sum() + n)
class_probability[1] = (learned_size.sum() * class_probability[1] + in_front.sum())\
    / (learned_size.sum() + n)

tmp_s0 = ((sigma[0] + mu[0]**2) * learned_size[0] + (pop2["variables"][~in_front].var(axis = 0) + pop2["variables"][~in_front].mean(axis = 0)**2) *neg_n) / neg_denom
tmp_s1 = ((sigma[1] + mu[1]**2) * learned_size[1] + (pop2["variables"][in_front].var(axis = 0) + pop2["variables"][in_front].mean(axis = 0)**2) *pos_n) / pos_denom

mu[0] = (learned_size[0] * mu[0] + pop2["variables"][~in_front].sum(axis = 0))\
    / neg_denom
mu[1] = (learned_size[1] * mu[1] + pop2["variables"][in_front].sum(axis = 0))\
    /pos_denom

sigma[0] = tmp_s0 - mu[0]**2
sigma[1] = tmp_s1 - mu[1]**2

learned_size[0] += neg_n
learned_size[1] += pos_n

not_front_pop = np.vstack([pop["variables"][~in_front] , pop2["variables"][~in_front]])
in_front_pop = np.vstack([pop["variables"][in_front] , pop2["variables"][in_front]])

correct_mu = np.vstack([not_front_pop.mean(axis = 0), in_front_pop.mean(axis = 0)])
correct_sigma = np.vstack([not_front_pop.var(axis = 0), in_front_pop.var(axis = 0)])

check_mu = np.isclose(mu, correct_mu)
check_sigma = np.isclose(sigma, correct_sigma)
