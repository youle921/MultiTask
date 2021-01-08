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

        # HV計算用の.csvファイルを作成
        save_path = Path(str(l) + "/result_obj.csv")

        if save_path.exists():
            save_path.unlink()

        with save_path.open(mode = 'a') as f:

            for i in l.glob("*.dat"):
                # dataは最小化問題を仮定
                data = pd.read_table(i, sep = " ", header = None).dropna(axis = 1)

                np.savetxt(f, -data, delimiter = '\t', fmt = '%d')
                f.write("\n")

        a = sub.check_output([hv_path, str(save_path), "-a", "-r", "0"])
        hv = np.fromstring(a.decode(), sep = "\r\n")

        if save:
            np.savetxt(str(l) + "/hv.csv", hv, delimiter = ',')
        else:
            print(np.median(hv))

hv_path = str(Path(__file__).parent / Path("hv/hv.bat").resolve())
args = sys.argv

# 引数を与えない場合，直下にあるfinal_popsディレクトリ内のdatファイルに対して計算
if len(args) < 2:

    p = Path()
    dir_list = list(p.glob("**/final_pops"))

    calc_hv(dir_list)

# 引数を与える場合，引数のディレクトリ下にあるfinal_popsディレクトリ内のdatファイルに対して計算
else:
    dir_list = list(Path(args[1]).glob("**/final_pops"))
    calc_hv(dir_list, save = 0)

