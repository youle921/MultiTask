# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 23:40:10 2021

@author: youle
"""
# %%

import matplotlib.pyplot as plt
import seaborn as sns

from load_data import load_HV_log, load_IGD_log, load_normalized_IGD_log

dirs = ["NSGA-II/1017", "MO-MFEA/1019", "MO-MFEA-II/1019", "EMEA/1017", "Island_Model/1017"]
alg_name = ["NSGA-II", "MO-MFEA", "MO-MFEA-II", "EMEA", "Island Model"]

normalized_IGD_results = [load_normalized_IGD_log(d)[1] for d in dirs]

key = normalized_IGD_results[1].keys()

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 24

# %% normalized igd plots

figs = []
axs = []
for k in key:

    igd_fig = plt.figure()
    igd_ax = igd_fig.add_subplot(111, xmargin = 0.03, ymargin = 0.15)
    # igd_fig.suptitle(k)

    for igd_data, name in zip(normalized_IGD_results, alg_name):
        igd_ax.plot(range(1,51), igd_data[k][:50, 0], label = name)

    igd_ax.yaxis.set_major_formatter("{x:,.2f}")
    igd_ax.xaxis.set_major_formatter("{x:,.0f}")
    igd_ax.set_xticks(range(0, 51, 10))

    igd_ax.grid()
    igd_ax.set(xlabel = "Number of Generations", ylabel = "IGD")

    figs.append(igd_fig)
    axs.append(igd_ax)

    # igd_fig.savefig(f'{k}_normalized_IGD_50gen.svg', bbox_inches = "tight", transparent = True)

# %%
for i, (k, f) in enumerate(zip(key, figs)):

    f.savefig(f'{int(i / 2) + 1}_{i % 2 + 1}_{k}_normalized_IGD_50gen.svg', bbox_inches = "tight")