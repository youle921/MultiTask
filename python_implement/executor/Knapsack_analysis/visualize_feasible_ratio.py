# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 20:42:36 2021

@author: youle
"""

"""
probability reference
1. Pythonで学ぶ統計学　2. 確率分布[scipy.stats徹底理解] - Qiita
(https://qiita.com/y_itoh/items/c388ff82360906240daf)
"""
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt


n_obj = 2 # 目的(制約)数
n_item = 500

p = 0.5 # 初期解における1の確率
beta = 0.5 # 容量の制限(総重量×betaがナップサック容量)

binom = stats.binom.pmf(np.arange(1, n_item+1), n_item, p)
norm = stats.norm.cdf(x = (55*n_item*beta)/np.arange(1, n_item + 1), loc = 55, scale = (8100/(12*np.arange(1, n_item+1)))**0.5)
# 全実行可能解中における，アイテム数がiの実行可能解の割合
results = binom * norm**n_obj

plt.figure()
plt.plot(results)
plt.title("アイテム数に関する実行可能解の分布")
plt.show()

plt.figure()
plt.plot(np.cumsum(results))
plt.title("アイテム数に関する累積実行可能割合")
plt.show()

print(F'実行可能解の割合は{results.sum()}です')
