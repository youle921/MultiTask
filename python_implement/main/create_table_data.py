# -*- coding: utf-8 -*-
import numpy as np
from load_data import load_HV_log, load_IGD_log, load_normalized_IGD_log

dirs = ["NSGA-II/1017", "MO-MFEA/1019", "MO-MFEA-II/1019", "EMEA/1017", "Island_Model/1017"]
alg_name = ["NSGA-II", "MO-MFEA", "MO-MFEA-II", "EMEA", "Island Model"]

# key = normalized_IGD_results[1].keys()

order = ["Four bar truss design", "Reinforced concrete beam design", "Pressure vessel design","Hatch cover design","Coil compression spring design","Two bar truss design", "Welded beam design","Disc brake design","Vehicle crashworthiness design","Speed reducer design","Gear train design","Rocket injector design","Car side impact design","Conceptual marine design"]

def get_table_data(pos = 50):

    normalized_IGD_results = [load_normalized_IGD_log(d)[1] for d in dirs]

    table_data = []
    for k in order:
        tmp = []
        for i, data in enumerate(normalized_IGD_results):
            tmp.append(data[k][pos - 1, 0])
        table_data.append(tmp)

    table_data = np.array(table_data)

    return table_data

data = get_table_data(15)