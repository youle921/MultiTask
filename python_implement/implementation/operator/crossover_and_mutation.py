# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 16:29:35 2020

@author: t.urita
"""
import numpy as np

# crossover operator

# binary
def uniform_crossover(parents):

    offspring1 = parents[0].copy()
    offspring2 = parents[1].copy()
    mask = (np.random.rand(offspring1.shape[0], 1) < 0.9) * (np.random.rand(*offspring1.shape,) < 0.5)
    offspring1[mask] = parents[1][mask]
    offspring2[mask] = parents[0][mask]

    return np.vstack((offspring1, offspring2))
# binary end

# real
def SBX(parents, pc = 0.9, DI = 20):

    beta = np.zeros_like(parents[0])
    mu = np.random.rand(*beta.shape,)

    mask = mu <= 0.5
    beta[mask] = (2 * mu[mask]) ** (1/(1+DI))
    beta[~mask] = (2 - 2 * mu[~mask]) **(-1/(1+DI))

    beta = beta * (-1)**np.random.randint(0, high = 2, size = (*beta.shape,))
    beta[np.random.rand(*beta.shape,) < 0.5] = 1
    beta[np.random.rand(*beta.shape,) > pc] = 1

    off1 = (parents[0] + parents[1])/2 + beta * (parents[0] - parents[1])/2
    off2 = (parents[0] + parents[1])/2 - beta * (parents[0] - parents[1])/2

    return np.clip(np.vstack([off1, off2]), 0, 1)

def SBX_java(parents, pc = 0.9, DI = 20):

    low = 0
    high = 1
    eps = 1e-14
    cmp_mask = parents[0] > parents[1]

    big_p = parents[0]*cmp_mask + parents[1]*(~cmp_mask)
    small_p = parents[0]*(~cmp_mask) + parents[1]*cmp_mask

    # create c1
    same_var = (big_p - small_p) < eps
    beta = np.ones_like(big_p)
    beta[~same_var] = 1 + (2* (small_p[~same_var] - low) / (big_p[~same_var] - small_p[~same_var]))
    alpha = 2 - beta**(-(DI+1))

    rand = np.random.rand(*big_p.shape,)
    rand_mask = rand <= (1/alpha)

    betaq = np.zeros_like(big_p)
    betaq[rand_mask] = (rand[rand_mask] * alpha[rand_mask])**(1/(DI+1))
    betaq[~rand_mask] = (1/(2 - rand[~rand_mask] * alpha[~rand_mask]))**(1/(DI+1))

    c1 = 0.5 * (big_p + small_p - betaq * (big_p -small_p))
    c1[same_var] = small_p[same_var]

    # create c2
    beta[~same_var] = 1 + (2* (high - big_p[~same_var]) / (big_p[~same_var] - small_p[~same_var]))
    alpha = 2 - beta**(-(DI+1))

    rand_mask = rand <= (1/alpha)

    betaq[rand_mask] = (rand[rand_mask] * alpha[rand_mask])**(1/(DI+1))
    betaq[~rand_mask] = (1/(2 - rand[~rand_mask] * alpha[~rand_mask]))**(1/(DI+1))

    c2 = 0.5 * (big_p + small_p + betaq * (big_p -small_p))
    c2[same_var] = big_p[same_var]

    # java default----
    off1 = c1
    off2 = c2

    no_crossover = np.random.rand(off1.shape[0]) > pc
    off1[no_crossover] = parents[0][no_crossover]
    off2[no_crossover] = parents[1][no_crossover]

    swap_only = (~no_crossover[:, None]) * (np.random.rand(*off1.shape,) > 0.5)

    off1[swap_only] = parents[1][swap_only]
    off2[swap_only] = parents[0][swap_only]
    # java default end----

    # no swapping
    # off2 = c1 * cmp_mask + c2 * (~cmp_mask)
    # off1 = c2 * cmp_mask + c1 * (~cmp_mask)

    # no_crossover = np.random.rand(off1.shape[0]) > pc
    # off1[no_crossover] = parents[0][no_crossover]
    # off2[no_crossover] = parents[1][no_crossover]

    # do swaping
    # rand_pos = np.random.rand(*big_p.shape,) < 0.5

    # off1 = c1 * rand_pos + c2 * (~rand_pos)
    # off2 = c2 * rand_pos + c1 * (~rand_pos)

    # no_crossover = (np.random.rand(off1.shape[0]) > pc)[:, None] + (np.random.rand(*off1.shape,) > 0.5)

    # off1[no_crossover] = parents[0][no_crossover]
    # off2[no_crossover] = parents[1][no_crossover]

    return np.clip(np.vstack([off1, off2]), 0, 1)
# real end

# crossover end

# mutation operator

# binary
def bitflip_mutation(offs):

    off = offs
    mutation_ratio = 1 / off.shape[1]
    mutation_mask = np.random.rand(*off.shape,) < mutation_ratio
    off[mutation_mask] = 1 - off[mutation_mask]

    return off
# binary end

# real
def PM(offs, pm = 1, DI = 20, low = 0, high = 1):

    lower = np.ones_like(offs) * low
    upper = np.ones_like(offs) * high

    mask = np.random.rand(*offs.shape,) < pm/offs.shape[1]
    rand = np.random.rand(*offs.shape,)

    tmp = mask * (rand<=0.5)
    offs[tmp] = offs[tmp] + (upper[tmp]-lower[tmp]) * ((2*rand[tmp] + (1-2*rand[tmp])*\
                      (1 - (offs[tmp]-lower[tmp]) / (upper[tmp]-lower[tmp]))**(DI+1))**(1/(DI+1)) -1)

    tmp = mask * (rand > 0.5)
    offs[tmp] = offs[tmp] + (upper[tmp]-lower[tmp]) * (1 - (2*(1-rand[tmp]) + 2*(rand[tmp]-0.5)*\
                      (1-(upper[tmp]-offs[tmp]) / (upper[tmp]-lower[tmp]))**(DI+1)) **(1/(DI+1)))

    return np.clip(offs, low, high)
# real end

# mutation end

if __name__ == "__main__":

    import matplotlib.pyplot as plt
    import seaborn as sns

    # sol1 = np.random.rand(5, 2)*0.25
    # sol2 = np.random.rand(5, 2)*0.25 + 0.75


    repeat_num = 100000
    sol1 = np.array([[0.25, 0.25]]*repeat_num)
    sol2 = np.array([[0.75, 0.75]]*repeat_num)

    # sol1 = np.random.rand(repeat_num, 2)
    # sol2 = np.random.rand(repeat_num, 2)

    np.random.seed(0)
    offs = SBX([sol1, sol2])

    np.random.seed(0)
    offs2 = SBX_java([sol1, sol2])

    # plt.figure()
    # plt.scatter(*sol1.T)
    # plt.scatter(*sol2.T)
    # plt.hist(offs[:, 0], bins = 1000, histtype="stepfilled")
    # plt.show()
#
    # plt.figure()
    # plt.scatter(*offs2[:5].T)
    # plt.scatter(*offs2[5:].T)
    # plt.hist(offs2[:, 0], bins = 1000, histtype="stepfilled")
    # plt.ylim = (0, 500)
    # plt.show()

    sns.jointplot(*offs.T,)
    sns.jointplot(*offs2.T,)

# heat = np.empty([4,4])
# for i in range(4):
#     for j in range(4):
#         heat[i, j] = np.sum((offs2[:, 0] > i * 0.25) * (offs2[:, 0] <= (i+1) * 0.25) * (offs2[:, 1] > j * 0.25) * (offs2[:, 1] <= (j+1) * 0.25))