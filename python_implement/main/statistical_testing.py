# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 18:30:03 2021

@author: youle
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from autorank import autorank, plot_stats
from autorank._util import cd_diagram

from load_data import load_HV_log, load_IGD_log, load_normalized_IGD_log

dirs = ["NSGA-II/1017", "MO-MFEA/1019", "MO-MFEA-II/1019", "EMEA/1017", "Island_Model/1017"]
alg_name = ["NSGA-II", "MO-MFEA", "MO-MFEA-II", "EMEA", "Island Model"]

order = ["Four bar truss design", "Reinforced concrete beam design", "Pressure vessel design","Hatch cover design","Coil compression spring design","Two bar truss design", "Welded beam design","Disc brake design","Vehicle crashworthiness design","Speed reducer design","Gear train design","Rocket injector design","Car side impact design","Conceptual marine design"]


def get_testing_data(pos = 50):

    normalized_all_IGD_results = [load_normalized_IGD_log(d)[0] for d in dirs]

    testing_data = {}
    for k in order:
        tmp = pd.DataFrame()
        for i, data in enumerate(normalized_all_IGD_results):
            tmp[alg_name[i]] = data[k][:, pos - 1]
        testing_data[k] = tmp

    return testing_data

data = get_testing_data(25)

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 16

axs = []
# %%
for n, d in data.items():
    result = autorank(d, alpha = 0.05, verbose = False, order = "ascending")

    if result[1] < 0.05:

        print(n)
        plot_stats(result)
        # cd_diagram(result, True, None, 6)
        # plt.savefig(f'{n}_diagram.svg', bbox_inches = "tight")
