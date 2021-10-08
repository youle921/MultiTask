import sys
import os
sys.path.append(os.path.join(os.pardir, '..'))

import implementation
from implementation.problems.MTO_benchmark import *
from implementation.MOMFEA import MOMFEA
from runner.MT_runner import MT_runner

runner = MT_runner(MOMFEA, task_list, os.path.dirname(__file__), ["IGD"])
runner.run()

