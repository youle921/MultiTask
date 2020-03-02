# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 13:56:05 2020

@author: y5ule
"""
# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

import os
import subprocess

dir_name = "set_seed/"

methods = ["scaling", "inversion"]
names = ["differ_hamming_"]
ext = ".csv"

plt.close("all")

for m in methods:

    plt.rcParams["font.size"] = 20
    # fig1, ax1 = plt.subplots(1, 1)
    fig2, ax2 = plt.subplots(1, 1)

    path = Path(dir_name + m)
    for l, mk, i in zip(path.glob(names[0] + "*"), [",", "o", "x", "+", "v"], range(5, 0, -1)):
        # plot_data = pd.read_csv(dir_name + m + names[0] + s + ext, header = None).values
        # ax1.plot(plot_data[:, 0], (plot_data[:, 1] + plot_data[:, 2])/2, linewidth = 3, marker = 'o')
        scatter_data = pd.read_csv(l, header = None).to_numpy()
        sz = 36
        if mk == "+":
            sz = 200
        if mk == "x":
            sz = 100
        ax2.scatter(scatter_data[:, 0], scatter_data[:, 1], s = sz, marker = mk, zorder = i)

    # ax1.set_xlim(0, 505)
    # ax1.set_xticks((0, 100, 200, 300, 400, 500))
    # ax1.set_xticklabels([0, 100, 200, 300, 400, 500])
    # ax1.set_ylim(-5, 250)

    ax2.set_ylim(-2, 65)
    # ax2.set_yticks((0, 25, 50, 75, 100, 125, 150))
    ax2.set_xlim(-2, 65)
    # ax2.set_xticks((0, 25, 50, 75, 100, 125, 150))

    # if i == 2:
    #     ax2.set_ylim(10, 70)
    #     ax2.set_yticks((10, 30, 50, 70))
    #     ax2.set_xlim(10, 70)
    #     ax2.set_xticks((10, 30, 50, 70))

        # ax1.legend(['dist(0.1, 0.0)', 'dist(0.2, 0.0)', 'dist(0.3, 0.0)', 'dist(0.4, 0.0)', 'dist(0.5, 0.0)'], fontsize = 15, bbox_to_anchor=(1.5, 1))
    ax2.legend(['  =          ', '  =          ', '  =          ', '  =          ', '  =          '], fontsize = 15, bbox_to_anchor= (1.55, 1))

    ax2.set_aspect('equal')


#    ax.legend(['dist(0.6, 1.0)', 'dist(0.8, 1.0)', 'dist(1.2, 1.0)', 'dist(1.4, 1.0)'], fontsize = 15, loc = 'upper right')
#    plt.show()

    graph_names = [dir_name + m + '/dist', dir_name + m + '/dif']
    # fig1.savefig(graph_names[0] + '.svg', bbox_inches='tight')
    fig2.savefig(graph_names[1] + '.svg', bbox_inches='tight')

    # subprocess.call("inkscape " + graph_names[0] + ".svg -M " +  graph_names[0] + ".emf", shell = False)
    # os.remove(graph_names[0] + '.svg')
    subprocess.call("inkscape " + graph_names[1] + ".svg -M " +  graph_names[1] + ".emf", shell = False)
    os.remove(graph_names[1] + '.svg')


