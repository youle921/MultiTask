import sys
import os
sys.path.append(os.path.join(os.pardir, '..'))

import implementation
from implementation.problems.reproblems_master import *
from implementation.NSGAII import NSGAII
from runner.runner import EMOA_runner

runner = EMOA_runner(NSGAII, all_probs, os.path.dirname(__file__), ["IGD"])
runner.run()

