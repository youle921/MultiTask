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
        save_path = Path(__file__).parent / "tmp/result_obj.csv"

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
            print(np.median(hv))
        else:
            print(np.median(hv))

if __name__ == "__main__":

    dir_path = Path(__file__).parent
    hv_path = dir_path.relative_to(dir_path.cwd()) / "hv/hv.bat"
    # hv_path = str((P/ Path("..hv/hv.bat").resolve())
    args = sys.argv

    target_dir = "final_pops"

    # 引数を与えない場合，直下にある"target_dir"ディレクトリ内のdatファイルに対して計算
    if len(args) < 2:

        p = Path()
        dir_list = list(p.glob("**/" + target_dir))

        calc_hv(dir_list)

    # 引数を与える場合，引数のディレクトリ下のすべてのディレクトリを対象に，ディレクトリ内のdatファイルに対して計算
    else:
        print(args[1])
        dir_list = list(Path(args[1]).glob("*/**"))
        calc_hv(dir_list, save = 0)

