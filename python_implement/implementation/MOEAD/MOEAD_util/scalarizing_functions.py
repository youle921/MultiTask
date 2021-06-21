# -*- coding: utf-8 -*-
import numpy as np

# vec must be 1dim, or 2dim with same number of sol
def tchebycheff(sol, vec, z):

    g = (np.abs(sol - z) * vec).max(axis = 1)

    return g

def PBI(sol, vec, z, theta = 5):

    if vec.ndim == 1:
        d1 = np.linalg.norm((sol - z)*vec, axis = 1) / np.linalg.norm(vec)
        d2 = np.linalg.norm(sol - z - d1[:, None] * vec[None, :], axis = 1)
    else:
        d1 = np.linalg.norm((sol - z)*vec, axis = 1) / np.linalg.norm(vec, axis = 1)
        d2 = np.linalg.norm(sol - z - d1[:, None] * vec, axis = 1)

    return d1 + d2 *theta

