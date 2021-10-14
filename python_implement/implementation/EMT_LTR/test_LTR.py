# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 03:07:41 2021

@author: youle
"""
import numpy as np
from scipy.spatial import distance
from scipy.linalg import eig

def search_boundary(M, boundaries):

    prj_lb = []
    prj_ub = []
    d = M[0].shape[1]

    for m, b in zip(M, boundaries):
        mask = m < 0
        lb_, ub_ = np.repeat(b, d, axis = 1).reshape([2, -1, d])
        lb = lb_ * (~mask) + ub_*mask
        ub = ub_ * (~mask) + lb_ * mask
        prj_lb.append((lb * m).sum(axis = 0))
        prj_ub.append((ub * m).sum(axis = 0))

    return np.min(prj_lb, axis = 0), np.max(prj_ub, axis = 0)

npop = 100
ntask = 2
ndim = [10, 15]

sol1 = np.random.rand(npop, ndim[0])
sol2 = np.random.rand(npop, ndim[1])
sol1_class, sol2_class = np.random.randint(4, size = [2, npop])

Z = np.zeros([npop * ntask, sum(ndim)])
for i, sol in enumerate([sol1, sol2]):
    Z[i * npop:(i + 1) * npop, sum(ndim[:i]):sum(ndim[:i + 1])] = sol

Z = Z.T

dist_s1 = distance.cdist(sol1, sol1, metric='euclidean')
w1 = np.exp(-dist_s1)
d1 = np.eye(npop) * dist_s1.sum(axis = 1)

dist_s2 = distance.cdist(sol2, sol2, metric='euclidean')
w2 = np.exp(-dist_s2)
d2 = np.eye(npop) * dist_s2.sum(axis = 1)

L = np.zeros([npop * ntask] * 2)
for i, (d, w) in enumerate(zip([d1, d2], [w1, w2])):
    L[i * npop: (i + 1) * npop, i * npop: (i + 1) * npop] = d - w

all_sol_class = np.array([*sol1_class, *sol2_class,])
Ws = all_sol_class[:, None] == all_sol_class[None, :]
Ds = np.eye(npop * ntask) * Ws.sum(axis = 1)
Ls = Ds - Ws

Wd = ~Ws
Dd = np.eye(npop * ntask) * Wd.sum(axis = 1)
Ld = Dd - Wd

eig_val, eig_vec = eig((Z.dot((L + Ls))).dot(Z.T), (Z.dot(Ld)).dot(Z.T))

eig_idx = eig_val.argsort()
M = eig_vec[:, eig_idx[np.in1d(eig_idx, eig_val.nonzero())]]

to_latent_space = np.split(M, np.cumsum(ndim)[:-1])
to_decision_space = [np.linalg.pinv(m) for m in to_latent_space]

boundary0 = np.array([[0] + [-100] * 9, [1] + [100]*9])
boundary1 = np.array([[0] + [-50] * 14, [1] + [50]*14])

out = search_boundary(to_latent_space, [boundary0, boundary1])