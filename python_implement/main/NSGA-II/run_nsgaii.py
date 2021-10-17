import sys
import os
sys.path.append(os.path.join(os.pardir, '..'))

import implementation
from implementation.problems.real_world_problem import all_probs
from implementation.NSGAII import NSGAII
from runner.runner import EMOA_runner

runner = EMOA_runner(NSGAII, all_probs, os.path.join(__file__, '..'), ["IGD", "HV"])
runner.run()

