# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def reflect_kp(items, lower = 10, upper = 100):

    return upper + lower - items

def shift_kp(items, shift, lower = 10, upper = 100):

    shift_items = items + shift
    idx = shift_items > upper
    shift_items[idx] = shift_items[idx] - upper + lower

    return shift_items

def draw_heatmap(data, ax, title):

    sns.heatmap(data, cmap = 'bwr', ax = ax, square = True, xticklabels = 30, yticklabels = 30)

    ax.set_title(title)

    ax.set_xlabel("weight")
    ax.set_xticklabels([10, 40, 70, 100])

    ax.set_ylabel("profit")
    ax.set_yticklabels([100, 70, 40, 10])

weight = np.repeat(np.array([i for i in range(10, 101)])[:, np.newaxis], 91, axis = 1).T
profit = np.repeat(np.array([i for i in range(100, 9, -1)])[:, np.newaxis], 91, axis = 1)

items = np.stack((profit, weight))

gain = items[0, :, :] / items[1, :, :]
gain_list = [gain]

ref_items = reflect_kp(items)

gain_list.append(ref_items[0, :, :] / items[1, :, :])
gain_list.append(items[0, :, :] / ref_items[1, :, :])
gain_list.append(ref_items[0, :, :] / ref_items[1, :, :])

titles = ["original", "ref_profit", "ref_weight", "ref_items"]

fig, axes = plt.subplots(2, 2)
ax = axes.reshape([-1, 1])

for i in range(len(gain_list)):
    draw_heatmap(gain_list[i], ax[i, 0], titles[i])

plt.tight_layout()

