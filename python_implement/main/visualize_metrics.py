# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 23:40:10 2021

@author: youle
"""
import matplotlib.pyplot as plt
import seaborn as sns

from load_data import load_HV_log, load_IGD_log, load_normalized_IGD_log

dirs = ["NSGA-II/1017", "MO-MFEA/1019", "MO-MFEA-II/1019", "EMEA/1017", "Island_Model/1017"]
alg_name = ["NSGA-II", "MO-MFEA", "MO-MFEA-II", "EMEA", "Island Model"]

HV_results = [load_HV_log(d)[1] for d in dirs]
IGD_results = [load_IGD_log(d)[1] for d in dirs]

key = HV_results[1].keys()

# %%

import matplotlib.pyplot as plt
import seaborn as sns

from load_data import load_HV_log, load_IGD_log, load_normalized_IGD_log

dirs = ["NSGA-II/1017", "MO-MFEA/1019", "MO-MFEA-II/1019", "EMEA/1017", "Island_Model/1017"]
alg_name = ["NSGA-II", "MO-MFEA", "MO-MFEA-II", "EMEA", "Island Model"]

normalized_IGD_results = [load_normalized_IGD_log(d)[1] for d in dirs]

key = normalized_IGD_results[1].keys()

plt.rcParams["font.size"] = 16
# %% 50 gen plot
for k in key:

    hv_fig = plt.figure()
    hv_ax = hv_fig.add_subplot(111, xmargin = 0.03, ymargin = 0.17)
    hv_fig.suptitle(k)

    igd_fig = plt.figure()
    igd_ax = igd_fig.add_subplot(111, xmargin = 0.03, ymargin = 0.15)
    igd_fig.suptitle(k)

    for hv_data, igd_data, name in zip(HV_results, IGD_results, alg_name):
        hv_ax.plot(range(1, 51), hv_data[k][:50, 0], label = name)
        igd_ax.plot(range(1,51), igd_data[k][:50, 0], label = name)

    hv_ax.yaxis.set_major_formatter("{x:,.1e}")
    hv_ax.xaxis.set_major_formatter("{x:,.0f}")
    hv_ax.grid()
    hv_ax.set(xlabel = "Number of Generations", ylabel = "HyperVolume")
    hv_ax.legend()

    hv_fig.savefig(f'{k}_HyperVolume_50gen.svg', bbox_inches = "tight", transparent = True)

    igd_ax.yaxis.set_major_formatter("{x:,.1e}")
    igd_ax.xaxis.set_major_formatter("{x:,.0f}")
    igd_ax.grid()
    igd_ax.set(xlabel = "Number of Generations", ylabel = "IGD")
    igd_ax.legend()

    igd_fig.savefig(f'{k}_IGD_50gen.svg', bbox_inches = "tight", transparent = True)

# %% all gen plot
# plt.close("all")

for k in key:

    hv_fig = plt.figure()
    hv_ax = hv_fig.add_subplot(111, xmargin = 0.03, ymargin = 0.17)
    hv_fig.suptitle(k)

    igd_fig = plt.figure()
    igd_ax = igd_fig.add_subplot(111, xmargin = 0.03, ymargin = 0.15)
    igd_fig.suptitle(k)

    for hv_data, igd_data, name in zip(HV_results, IGD_results, alg_name):
        hv_ax.plot(range(1, 1001), hv_data[k][:, 0], label = name)
        igd_ax.plot(range(1, 1001), igd_data[k][:, 0], label = name)

    hv_ax.yaxis.set_major_formatter("{x:,.1e}")
    hv_ax.xaxis.set_major_formatter("{x:,.0f}")
    hv_ax.grid()
    hv_ax.set(xlabel = "Number of Generations", ylabel = "HyperVolume")
    hv_ax.legend()

    # hv_fig.savefig(f'{k}_HyperVolume.svg', bbox_inches = "tight", transparent = True)

    igd_ax.yaxis.set_major_formatter("{x:,.1e}")
    igd_ax.xaxis.set_major_formatter("{x:,.0f}")
    igd_ax.grid()
    igd_ax.set(xlabel = "Number of Generations", ylabel = "IGD")

    igd_ax.legend()

    # igd_fig.savefig(f'{k}_IGD.svg', bbox_inches = "tight", transparent = True)
    
# %% normalized igd plots
for k in key:

    igd_fig = plt.figure()
    igd_ax = igd_fig.add_subplot(111, xmargin = 0.03, ymargin = 0.15)
    igd_fig.suptitle(k)

    for igd_data, name in zip(normalized_IGD_results, alg_name):
        igd_ax.plot(range(1,51), igd_data[k][:50, 0], label = name)

    igd_ax.yaxis.set_major_formatter("{x:,.1e}")
    igd_ax.xaxis.set_major_formatter("{x:,.0f}")
    igd_ax.grid()
    igd_ax.set(xlabel = "Number of Generations", ylabel = "IGD")
    igd_ax.legend()

    igd_fig.savefig(f'{k}_normalized_IGD_50gen.svg', bbox_inches = "tight", transparent = True)