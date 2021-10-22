import sys
import os
sys.path.append(os.pardir)

import implementation
from implementation.problems.real_world_problem.metric_calculator import calculator

ins = calculator(["IGD", "HV"])
names = [f'../{alg}/1019' for alg in ["MO-MFEA", "MO-MFEA-II"]]
names.extend([f'../{alg}/1017' for alg in ["EMEA", "Island_Model"]])
for n in names:
    print(n)
    ins.calculation(os.path.join(__file__, n))
# ins.single_calculation(os.path.join(__file__, "../NSGA-II/1017"))