import sys
import os
sys.path.append(os.path.join(os.pardir, '..'))

import implementation
from implementation.problems.real_world_problem import get_prob_pairs, get_random_prob_pairs
from implementation.EMEA import EMEA
from runner.MT_runner import MT_runner

task_list = get_prob_pairs()
runner = MT_runner(EMEA, task_list, os.path.join(__file__, '..'), ["IGD", "HV"])
runner.run()
