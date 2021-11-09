import sys
import os
sys.path.append(os.pardir)

import implementation
from implementation.problems.real_world_problem.objective_visualizer import visualizer

ins = visualizer()
names = [f'../{alg}/1019' for alg in ["MO-MFEA", "MO-MFEA-II"]]
names.extend([f'../{alg}/1017' for alg in ["EMEA", "Island_Model"]])
for n in names:
    print(n)
    ins.visualization(os.path.join(__file__, n))
    ins.visualization_fix_range(os.path.join(__file__, n))
ins.single_visualization(os.path.join(__file__, "../NSGA-II/1017"))
ins.single_visualization_fix_range(os.path.join(__file__, "../NSGA-II/1017"))