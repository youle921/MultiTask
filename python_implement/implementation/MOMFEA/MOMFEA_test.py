# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 23:22:50 2020

@author: t.urita
"""

from class_kp import Knapsack
from inversion import kp_inversion
from scaling import kp_scaling
from MOMFEA.MOMFEA_main import MOMFEA

import numpy as np
import matplotlib.pyplot as plt

p = [Knapsack(), kp_scaling(1.1)]

solver = MOMFEA(500, 2, 100, 100, p, 'bin')


for i in range(10):
    solver.init_pop()
    solver.execute(200000)

    sol = solver.pops["objectives"][0][solver.pops["pareto_rank"][0] == 0]
    np.savetxt("result/HV/inversion/base/final_pops/pops" + str(i) + ".dat", sol)
    sol = solver.pops["objectives"][1][solver.pops["pareto_rank"][1] == 0]
    np.savetxt("result/HV/inversion/inversion/final_pops/pops" + str(i) + ".dat", sol)
    print(i)

# sol = solver.pops["objectives"][0][solver.pops["pareto_rank"][0] == 0]
# np.savetxt("result/HV/inversion/base/final_pops/pops" + str(5) + ".dat", sol)
# sol = solver.pops["objectives"][1][solver.pops["pareto_rank"][1] == 0]
# np.savetxt("result/HV/inversion/inversion/final_pops/pops" + str(5) + ".dat", sol)