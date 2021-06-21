# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 22:40:35 2021

@author: youle
"""
import numpy as np

# for debugging(check heatmap of g)
def tchebycheff_multi(sol, vec, z):

    g = ((np.abs(sol - z)[:, None, :]) * vec[None, :, :]).max(axis = 2)

    return g

def PBI_multi(sol, vec, z, theta = 5):

    d1 = (((sol - z)[:, None, :]*vec[None, :, :])**2).sum(axis = 2)**0.5 / np.linalg.norm(vec, axis = 1)

    d2 = ((((sol - z)[:, None, :]) - d1[:, :, None] * vec[None, :, :])**2).sum(axis = 2)**0.5
    # d2 = (((sol - z - d1[:, None])[:, None, :] * vec[None, :, :])**2).sum(axis = 2)**0.5

    return d1 + d2 *theta

if __name__ == "__main__":

    import seaborn as sns
    import matplotlib.pyplot as plt

    nsol = 50
    ndiv= 5

    vec = np.array([[i, 1 - i] for i in np.linspace(0, 1, ndiv)])

# Test using heatmap

    mesh = np.linspace(0, 1, int(nsol**0.5))
    sol = np.array([[x, y] for x in mesh for y in mesh])

    z = sol.min(axis = 0)

    tch_g = tchebycheff_multi(sol, vec, z)
    PBI_g = PBI_multi(sol, vec, z)

    for c in tch_g.T:
        plt.figure()
        sns.heatmap(c.reshape([-1 ,int(nsol**0.5)]).T[::-1])
        plt.show()

    for c in PBI_g.T:
        plt.figure()
        sns.heatmap(c.reshape([-1 ,int(nsol**0.5)]).T[::-1])
        plt.show()

    # sol = np.array([[np.sin(x * 0.5 * np.pi), np.cos(x * 0.5 * np.pi)] for x in np.linspace(0, 1, nsol)])
    # z = sol.min(axis = 0)

    # tch_g = tchebycheff_multi(sol, vec, z)
    # PBI_g = PBI_multi(sol, vec, z)

    # fig, axs = plt.subplots(nrows = 2, ncols = 3)
    # cm = plt.cm.get_cmap('jet')

    # for v, c, ax in zip(vec, tch_g.T, axs.flatten()):
    #     ax.scatter(*sol.T, c = c, vmin = c.min(), vmax = c.max(), cmap = cm)
    #     ax.quiver(0, 0, *v, scale = 1)
    #     ax.set_title("weight_vector: " + str(v))
    #     ax.set_aspect("equal")

    # axs[-1, -1].axis('off')
    # fig.suptitle("Tchebycheff")
    # fig.tight_layout()
    # fig.show()

    # fig2, axs2 = plt.subplots(nrows = 2, ncols = 3)
    # cm = plt.cm.get_cmap('jet')

    # for v, c, ax in zip(vec, PBI_g.T, axs2.flatten()):
    #     ax.scatter(*sol.T, c = c, vmin = c.min(), vmax = c.max(), cmap = cm)
    #     ax.quiver(0, 0, *v, scale = 1)
    #     ax.set_title("weight_vector: " + str(v))
    #     ax.set_aspect("equal")

    # axs2[-1, -1].axis('off')
    # fig2.suptitle("PBI")
    # fig2.tight_layout()
    # fig2.show()
