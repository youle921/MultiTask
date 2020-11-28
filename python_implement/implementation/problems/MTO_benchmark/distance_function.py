# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 16:47:47 2020

@author: t.urita
"""
import numpy as np

def sphere(x):

    x_ = x[:, 1:]
    return 1 + np.sum(x_**2, axis = 1)

def mean(x):

    x_ = x[:, 1:]
    return 1 + 9/(x.shape[1] - 1) * np.sum(abs(x_), axis = 1)

def rosenbrock(x):

    dim = x.shape[1]

    return 1 + (100 * ((x[:, 1:dim-1])**2 - x[:, 2:dim])**2 + (1 - x[:, 1:dim - 1])**2).sum(axis = 1)

def rastrigin(x):

    x_ = x[:, 1:]
    return 1 + (x_**2 - 10 * np.cos(2*np.pi * x_) + 10).sum(axis = 1)

def ackley(x):

    x_ = x[:, 1:]
    sc = 1/(x.shape[1]-1)

    return 21 + np.e - 20 * np.exp(-0.2* (sc * (x_**2).sum(axis = 1))**0.5)\
        - np.exp(sc * (np.cos(2*np.pi * x_)).sum(axis = 1))

def griewank(x):

    x_ = x[:, 1:]
    div = np.arange(1, x.shape[1])**0.5

    return 2 + (1/4000) * (x_**2).sum(axis = 1) -np.cos(x_/div).prod(axis = 1)