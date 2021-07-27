# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 02:04:13 2021

@author: youle
"""

import numpy as np
from sklearn import preprocessing

# size = [1,2,3,5,7,10,15,20,30]
size = [1,5,10,20,30,40,50,60]

dir_names = [f'0716/m_size={i}_a=10_b=2' for i in size]

names = ["CIHS", "CIMS", "CILS", "PIHS", "PIMS", "PILS", "NIHS", "NIMS", "NILS"]
names_ = [f'{n}_{t}' for n in names for t in ["T1", "T2"]]

results = np.empty([len(size), 18])

for i, d in enumerate(dir_names):
    mean = np.loadtxt(d + "/all_results.csv", delimiter = ",")[:, 0]
    results[i] = mean

rank = np.argsort(results, axis = 0).argsort(axis = 0) + 1
norm_score = preprocessing.minmax_scale(results, axis = 0)

import matplotlib.pyplot as plt
plt.figure(figsize = (8, 4))
for r, s in zip(rank, size):
    plt.plot(names_, r, label = f'size: {s}')

plt.xlabel("Problems")
plt.ylabel("Rank")

plt.setp(plt.gca().get_xticklabels(), rotation=45)
plt.legend(bbox_to_anchor = (1.05, 1))
plt.gca().axis("auto")
plt.tight_layout()
plt.show()

plt.figure(figsize = (8, 4))
for score, s in zip(norm_score, size):
    plt.plot(names_, score, label = f'size: {s}')

plt.xlabel("Problems")
plt.ylabel("Score")

plt.setp(plt.gca().get_xticklabels(), rotation=45)
plt.legend(bbox_to_anchor = (1.05, 1))
plt.gca().axis("auto")
plt.tight_layout()
plt.show()