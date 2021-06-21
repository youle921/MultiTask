import itertools
import numpy as np

def generate_weight_vector(nobj, d, n):

    candidate = itertools.permutations(range(d+1), nobj)
    vec = np.array([*filter(lambda l: sum(l) == d, candidate)]) / d

    dist_mat = ((vec[:, None, :] - vec[None, :, :])**2).sum(axis = 2)
    neighbor = np.argsort(dist_mat)[:, :n]

    return vec, neighbor