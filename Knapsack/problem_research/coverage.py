# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 23:20:44 2020

@author: t.urita
"""

import numpy as np

# coverage_ is defined as the percentage
# of the solutions in b that are dominated
# by all solution in a
def coverage_(a, b):
    dom = a[None, :,  :] >= b[:, None, :]

    return np.mean(np.min(np.sum(dom, axis = 2), axis = 1) == a.shape[1])

def coverage(a, b):
    dom = a[None, :,  :] >= b[:, None, :]

    return np.mean(np.max(np.sum(dom, axis = 2), axis = 1) == a.shape[1])

def dominate(a, b):

    dom = a[None, :,  :] < b[:, None, :]

    return (np.max(np.sum(dom, axis = 2), axis = 1) == a.shape[1])


if __name__== "__main__":

    a = np.array([[2,2],[3,2],[3,3],[1,1]])
    b = np.array([[2,2],[3,2],[4,3]])

    c1 = coverage(a, b)
    c2 = coverage(b, a)


