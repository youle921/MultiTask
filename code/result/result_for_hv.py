# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 01:40:09 2019

@author: t.urita
"""

from pathlib import Path
import numpy as np

header = ["#nObjectives: [2]", "#nTrials: [100]"]

solution_header = ["#nSols: [100]"]

p = Path.cwd()
l = list(p.glob("*.dat"))

save_path = Path("result_2obj.csv")

with save_path.open(mode = 'a') as f:

#    for h in header:
#        f.write(h + "\n")

    for path in l:
        data = np.loadtxt(path)

#        f.write(solution_header[0] + "\n")
        np.savetxt(f, -data, delimiter = '\t', fmt = '%d')
        f.write("\n")

