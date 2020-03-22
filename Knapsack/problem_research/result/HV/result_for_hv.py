# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 01:40:09 2019

@author: t.urita
"""

from pathlib import Path
import pandas as pd
import numpy as np

import subprocess as sub

p = Path()
dir_list = list(p.glob("**/final_pops"))

#hv_path = "d:/research/Multitask/hv/hv.bat"
# hv_path = "C:/Users/y5ule/research/MultiTask/hv/hv.bat"

hv_path = str(Path("../../../../hv/hv.bat").resolve())

for l in dir_list:

    save_path = Path(str(l) + "/result_2obj.csv")

    if save_path.exists():
        save_path.unlink()

    with save_path.open(mode = 'a') as f:

        for i in l.glob("*.dat"):
            data = pd.read_csv(i, sep = " ", header = None).dropna(axis = 1)

            np.savetxt(f, -data, delimiter = '\t', fmt = '%d')
            f.write("\n")

    a = sub.check_output([hv_path, str(save_path), "-a", "-r", "0"])
    hv = np.fromstring(a.decode(), sep = "\r\n")
    np.savetxt(str(l) + "/hv.csv", hv, delimiter = ',')

