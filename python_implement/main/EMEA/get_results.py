import sys
import os
sys.path.append(os.path.join(os.pardir, '..'))

import implementation
from implementation.problems.real_world_problem.metric_calculator import calculator

ins = calculator(["IGD", "HV"])
ins.calculation(os.path.join(__file__, '../1017'))