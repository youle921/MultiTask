# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 02:08:17 2021

@author: youle
"""

import numpy as np
import scipy.optimize as opt

def norm_dist(x, mu, var, eps = 1e-8):

    return (1 / (np.sqrt(2 * np.pi * var + eps))) * np.exp(-1 * ((x - mu)**2 / (2 * var + eps)))

def loglik(rmp, probmatrix):

    ntasks = probmatrix.shape[2]

    factor = np.full([ntasks, ntasks], 0.5 * (ntasks - 1) * rmp / ntasks)
    factor[np.diag_indices(ntasks)] = 1 - factor[np.diag_indices(ntasks)]

    f = (-np.log((probmatrix * factor[:, None, :]).sum(axis = 2)).sum())

    return f

ntasks = 2
ndim = 10

npop = 100

pop1 = np.random.rand(npop, ndim)*0.25
pop2 = np.random.rand(npop, ndim)*np.array([0.25]*7 + [0.26]*3)

noise = np.random.rand(2, int(pop1.shape[0] * 0.1), ndim)

# noise_pop1 = np.loadtxt("pop1.csv", delimiter = ",")
# noise_pop2 = np.loadtxt("pop2.csv", delimiter = ",")

mean = np.empty([ntasks, pop1.shape[1]])
var = np.empty_like(mean)

noise_pop1 = np.array([*pop1, *noise[0]])
noise_pop2 = np.array([*pop2, *noise[1]])

mean[0] = noise_pop1.mean(axis = 0)
var[0] = noise_pop1.var(axis = 0, ddof = 1)

mean[1] = noise_pop2.mean(axis = 0)
var[1] = noise_pop2.var(axis = 0, ddof = 1)

probmatrix = np.empty([2, npop, 2])

probmatrix[0] = (norm_dist(pop1[None, :, :], mean[:, None, :], var[:, None, :])).prod(axis = 2).T
probmatrix[1] = (norm_dist(pop2[None, :, :], mean[:, None, :], var[:, None, :])).prod(axis = 2).T

rmp = opt.fminbound(loglik, 0, 1, args = ([probmatrix]))

rmp = np.clip(rmp + np.random.randn() * 0.01, 0, 1)
