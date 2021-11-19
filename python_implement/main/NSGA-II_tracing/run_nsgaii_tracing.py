import sys
import os
sys.path.append(os.path.join(os.pardir, '..'))

import implementation
from implementation.problems.real_world_problem import all_probs
from implementation.NSGAII import NSGAII_tracing
from runner.runner import EMOA_runner

runner = EMOA_runner(NSGAII_tracing, all_probs, os.path.join(__file__, '..'), ["normalized_IGD"])
runner.run_tracing()
