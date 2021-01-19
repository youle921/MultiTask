# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 02:11:02 2021

@author: t.urita
"""
import numpy as np
from sklearn import preprocessing

def modify_objective_function(obj, vio, ratio):

    scaled_obj = preprocessing.minmax_scale(obj)
    max_vio = vio.max(axis = 0)
    scaled_vio_mean = (vio / np.where(max_vio == 0, 1, max_vio)).mean(axis = 1)[:, None]

    flag = ratio != 0
    is_infeasible = vio.sum(axis = 1) != 0

    d_factor = (flag * scaled_obj**2 + scaled_vio_mean**2)**0.5

    x = (1 - ratio) * flag * scaled_vio_mean
    y = ratio * is_infeasible[:, None] * scaled_obj
    p_factor = x + y

    return d_factor + p_factor
