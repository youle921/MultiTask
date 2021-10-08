# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.join(os.pardir, '..'))

import numpy as np

import json
from datetime import datetime
from collections import OrderedDict

from implementation.indicator import HV, IGD
from .runner import EMOA_runner

class MT_runner(EMOA_runner):

    def __init__(self, algorithm, problemset, path, metric):

        self.alg = algorithm
        self.problemset = problemset
        self.caller_path = path

        self.metric_calculator = []
        self.metric_names = []

        if "IGD" in metric:
            self.metric_calculator.append([[IGD.IGD(p.IGD_ref) for p in problem.get_tasks()] for problem in self.problemset])
            self.metric_names.append("IGD")
        if "HV" in  metric:
            self.metric_calculator.append([[HV.HyperVolume(p.HV_ref) for p in problem] for problem in self.problemset])
            self.metric_names.append("HyperVolume")

    def run(self):

        self.load_params()

        parent_path = f'{self.caller_path}/{datetime.today().strftime("%m%d")}'
        os.makedirs(parent_path, exist_ok = True)

        results = np.empty([len(self.metric_calculator), len(self.problemset), 2, 2])

        for prob, prob_no in zip(self.problemset, range(len(self.problemset))):

            # preprocessing
            print(f'{prob.problem_name} Started')

            metric = np.empty([len(self.metric_calculator), 2, self.params["n_trial"]])
            final_objs = [[], []]

            task = prob.get_tasks()

            path = [f'{parent_path}/{prob.problem_name}_{t.problem_name}' for t in task]
            [os.makedirs(task_path, exist_ok = True) for task_path in path]

            # start running algorithm
            start_time = datetime.now()
            solver = self.alg(self.params, task)

            for trial in range(self.params["n_trial"]):

                np.random.seed(trial)

                solver.init_pop()
                solver.execute(self.criteria)

                for i, obj in enumerate(solver.pops["objectives"]):
                    final_objs[i].append(obj)

            # finish running algorithm
            end_time = datetime.now()
            computational_time = end_time - start_time

            # postprocessing
            # update and save times
            self.params.update({"start_time": start_time.isoformat()})
            self.params.update({"end_time": end_time.isoformat()})
            self.params.update({"computational time[s]": computational_time.total_seconds()})

            for task_path in path:
                with open(F'{task_path}/setting_log.json', 'w') as f:
                    json.dump(self.params, f, indent = 0)

            # calculate and show metrics
            for idx, calculator in enumerate(self.metric_calculator):
                for task_no in range(2):
                    metric[idx, task_no] = [*map(calculator[prob_no][task_no].compute, final_objs[task_no])]

            for i, name in enumerate(self.metric_names):
                print(f'{name:^30}')

                print(f'{" median ":-^30}')
                results[i, prob_no, :, 0] = np.median(metric[i], axis = 1)
                print(results[i, prob_no, :, 0])

                print(f'{" standard deviation ":-^30}')
                results[i, prob_no, :, 1] = metric[i].std(axis = 1)
                print(results[i, prob_no, :, 1])

            for task_no in range(2):
                np.savetxt(f'{path[task_no]}/all_{name}s.csv', metric[i, task_no], delimiter = ",")

            print(f'{prob.problem_name} Finished\n')

        for name, result in zip(self.metric_names, results):
            np.savetxt(f'{parent_path}/all_{name}_results.csv', result.reshape(-1, 2), delimiter = ',')