# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 01:52:22 2021

@author: youle
"""

def padding_pop(target, dim):

    padded_pop = np.zeros([target.shape[0], dim])
    padded_pop[:, :target.shape[1]] = target

    return padded_pop

import numpy as np

npop = 10

pops = [{}, {}]

pops[0]["objectives"] = np.random.rand(npop, 3)
pops[0]["variables"] = np.random.rand(npop, 8)

pops[1]["objectives"] = np.random.rand(npop, 2)
pops[1]["variables"] = np.random.rand(npop, 5)

matrix = [[], []]

for alg_idx in range(2):

    for source_obj in range(pops[alg_idx]["objectives"].shape[1]):

        W_list = []

        for target_obj in range(pops[1 - alg_idx]["objectives"].shape[1]):

            sorted_idx = pops[alg_idx]["objectives"][:, source_obj].argsort()
            source_pop = pops[alg_idx]["variables"][sorted_idx]

            sorted_idx = pops[1 - alg_idx]["objectives"][:, target_obj].argsort()
            target_pop = pops[1 - alg_idx]["variables"][sorted_idx]

            d1 = source_pop.shape[1]
            d2 = target_pop.shape[1]

            if d1 != d2:
                if d1 > d2:
                    target_pop = padding_pop(target_pop, d1)
                else:
                    source_pop = padding_pop(source_pop, d2)

            xx = target_pop.T
            noise = source_pop.T

            d, n = xx.shape
            xxb = np.ones([d + 1, n])
            xxb[:d] = xx
            noise_xb = np.ones_like(xxb)
            noise_xb[:d] = noise

            Q = np.dot(noise_xb, noise_xb.T)
            P = np.dot(xxb, noise_xb.T)

            reg = 1e-5 * np.eye(d + 1)
            reg[-1, -1] = 0
            W = np.dot(P, np.linalg.inv(Q + reg))

            W_list.append(W[:d, :d])
        matrix[alg_idx].append(W_list)