import sys
import os
sys.path.append(os.path.join(os.pardir, '..'))

import implementation
from implementation.problems.MTO_benchmark import task_list
from implementation.Island_Model import Island_Model
from runner.MT_runner import MT_runner

runner = MT_runner(Island_Model, task_list, os.path.dirname(__file__), ["IGD"])
runner.run()