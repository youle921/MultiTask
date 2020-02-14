# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 02:18:29 2020

@author: t.urita
"""

import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

def min_hamming(data, ref):
    dist = np.logical_xor(data[:, None, :], ref[None, :, :])

    return np.min(np.sum(dist, axis = 2), axis = 1)

def differ_hamning(data, ref):

#    differ[:, 0]: number of to0 bit
#    differ[:, 1]: number of to1 bit
    differ = np.empty([data.shape[0], 2])

    dist = np.logical_xor(data[:, None, :], ref[None, :, :])
    idx = np.sum(dist, axis = 2).argmin(axis = 1)
    min_dist = dist[range(0, data.shape[0]), idx, :]
    differ[:, 0] = np.logical_and(ref[idx, :], min_dist).sum(axis = 1)
    differ[:, 1] = np.sum(min_dist, axis = 1) - differ[:, 0]

    return differ

dir_name = "set_seed/"
ext = ".csv"

names = ["scaling/", "inversion/"]

# dist_list = np.zeros([51, 3])
# dist_list[0, 0] = 0
# dist_list[1:, 0] = [i * 10 for i in range(1, 51)]

base_data = pd.read_csv(dir_name + "base_result/pops" + ext, header = None).to_numpy()
# for i in range(50):
#     base_data[i + 1] = np.loadtxt(dir_name + "baseline" + names[1] + str((i + 1) * 10) + ext, delimiter = ',')

# for m in range(len(methods)):

#     for j in range(len(pfr)):

#         d1 = np.loadtxt(dir_name + methods[m] + '/' + names[0] + params[0] + pfr[j] + names[1] + str(1) + ext, delimiter = ',')
#         dist_list[0, 1] = np.average(min_hamming(d1, base_data[0]))
#         dist_list[0, 2] = np.average(min_hamming(base_data[0], d1))

#         for i in range(50):

#             d1 = np.loadtxt(dir_name + methods[m] + '/' + names[0] + params[0] + pfr[j] + names[1] + str((i + 1) * 10) + ext, delimiter = ',')

#             dist_list[i + 1, 1] = np.average(min_hamming(d1, base_data[i + 1]))
#             dist_list[i + 1, 2] = np.average(min_hamming(base_data[i + 1], d1))

#         dif = differ_hamning(d1, base_data[i + 1])

#         if m == 0:
#             np.savetxt(dir_name + methods[m] + "/hamming_distance_" + pfr[j] + ext, dist_list, delimiter = ',')
#             np.savetxt(dir_name + methods[m] + "/differ_hamming_" + pfr[j] + ext, dif, delimiter = ',')
#         else:
#             np.savetxt(dir_name + methods[m] + "/hamming_distance_" + sr[j] + ext, dist_list, delimiter = ',')
#             np.savetxt(dir_name + methods[m] + "/differ_hamming_" + sr[j] + ext, dif, delimiter = ',')


for n in names:
    path = Path(dir_name + n)

    for l in path.glob("**/pops.csv"):

        d1 = pd.read_csv(l, header = None).to_numpy()
        dif = differ_hamning(d1, base_data)

        np.savetxt(dir_name + n + "differ_hamming_"+ l.parts[2] + ext, dif, delimiter = ',')

# dif = differ_hamning(d1, base_data[i + 1])

# np.savetxt(dir_name + methods[0] + "/hamming_distance_0.1" + ext, dist_list, delimiter = ',')
# np.savetxt(dir_name + methods[0] + "/differ_hamming_0.1" + ext, dif, delimiter = ',')


#ref_data = np.loadtxt(dir_name + names[0] + "1.0" + names[1] + "500" + ext, delimiter = ',')
#
#for comp in ["0.6", "0.8", "1.2", "1.4"]:
#
#    plt.clf()
#    comp_data = np.loadtxt(dir_name + names[0] + comp + names[1] + "500" + ext, delimiter = ',')
#    dif = differ_hamning(comp_data, ref_data)
#
#    plt.scatter(dif[:, 0], dif[:, 1])
#
#plt.show()
