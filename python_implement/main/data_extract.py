# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 01:26:22 2021

@author: youle
"""
import numpy as np
import pathlib

# names = [f'{alg}/1019' for alg in ["MO-MFEA", "MO-MFEA-II"]]
# names.extend([f'{alg}/1017' for alg in ["EMEA", "Island_Model", "NSGA-II"]])

names = ["NSGA-II/1219"]
for parent_path in names:
    p = pathlib.Path(parent_path)
    dirs = p.glob("*design/")

    for d in dirs:

        igd_files = d.glob("normalized_IGD_log*.csv")

        last_gen_IGD = [np.loadtxt(ip)[49] for ip in igd_files]

        idx = np.where(last_gen_IGD == np.median(last_gen_IGD))[0][0] + 1
        idx = 1

        pops = np.load(f'{str(d)}/trial{idx}_objectives.npz')["arr_0"][:50]
        metrics = np.loadtxt(f'{str(d)}/normalized_IGD_log_trial{idx}.csv', delimiter = ",")[:50]

        np.savez_compressed(f'../../../../streamlit_env/population_visualization/{str(d)}/objectives', pops)
        np.savetxt(f'../../../../streamlit_env/population_visualization/{str(d)}/normalized_IGD.csv', metrics, delimiter = ",")


path = ["MO-MFEA-II/1019/problem set2_Hatch cover design"]