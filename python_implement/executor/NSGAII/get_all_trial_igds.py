# -*- coding: utf-8 -*-

"""
Created on Mon Oct 12 02:38:33 2020

@author: t.urita
"""
import pathlib
import numpy as np

path = "D:/research/MultiTask/code/result/実験結果/result/NSGA2/PIMS/Task1/IGDHisWithAllSol"

files = pathlib.Path(path)
igds = files.glob("IGDHis*.dat")

igd_list = np.empty(31)

for i, p in enumerate(igds):
    data = np.loadtxt(p)
    igd_list[i] = data[-1, 1]