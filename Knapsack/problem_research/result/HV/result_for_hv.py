# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 01:40:09 2019

@author: t.urita
"""

from pathlib import Path
import numpy as np
import pandas as pd

import subprocess as sub
import sys

def calc_hv(dirs, save = 1):

    for l in dirs:

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

        if save:
            np.savetxt(str(l) + "/hv.csv", hv, delimiter = ',')
        else:
            print(np.median(hv))

hv_path = str(Path("../../../../hv/hv.bat").resolve())
args = sys.argv

if len(args) < 2:

    p = Path()
    dir_list = list(p.glob("**/final_pops"))

    calc_hv(dir_list)

else:
    dir_list = list(Path(args[1]).glob("**/final_pops"))
    calc_hv(dir_list, save = 0)

