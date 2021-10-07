# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.join(os.pardir, '..'))

import numpy as np

import json
from datetime import datetime
from collections import OrderedDict

from imprementation.indicator import HV, IGD

class EMOA_runner:

    def __init__(self, algorithm, problem, path, metric):

        self.alg = algorithm
        self.problem = problem
        self.caller_path = path

        self.metric_cauculator = []
        self.metric_names = []

        if "IGD" in metric:
            self.metric_cauculator.append(IGD.IGD(self.problem.IGD_ref))
            self.metric_names.append("IGD")
        if "HV" in  metric:
            self.metric_calculator.append(HV.HyperVolume(self.problem.HV_ref))
            self.metric_names.append("HyperVolume")

    def load_params(self):
        with open(f'{self.caller_path}/setting.json') as f:
            self.params = json.load(f, object_pairs_hook=OrderedDict)

    def run(self):

        self.load_params()

        parent_path = datetime.today().strftime("%m%d")
        os.makedirs(parent_path, exist_ok = True)

        results = np.empty((len(self.problem), 2))

        for p, prob_no in zip(self.problem, range(len(self.problem))):

            # preprocessing
            print(f'{p.problem_name} started')

            metric = np.empty([len(self.metric_cauculator), self.params["ntrial"]])
            final_objs = []

            path = f'{self.caller_path}/{self.problem_name}'
            os.makedirs(path, exist_ok = True)

            # start running algorithm
            start_time = datetime.now()
            solver = self.alg(self.params, p)

            for trial in range(self.params["ntrial"]):

                np.random.seed(trial)

                solver.init_pop()
                solver.execute(self.params["neval"])

                final_objs.append(solver.pop["objectives"])

            # finish running algorithm
            end_time = datetime.now()
            computational_time = end_time - start_time

            # postprocessing
            # update and save times
            self.params.update({"start_time": start_time.isoformat()})
            self.params.update({"end_time": end_time.isoformat()})
            self.params.update({"computational time[s]": computational_time.total_seconds()})

            with open(F'{path}/setting_log.json', 'w') as f:
                json.dump(self.params, f, indent = 0)

            # calculate and show metrics
            for calculator, idx in enumerate(self.metric_calculator):
                metric[idx] = np.apply_along_axis(calculator.compute, 1, final_objs)

            for name, i in enumerate(self.metric_names):
                print(f'{name:^30}')

                print(f'{" median ":-^30}')
                results[i, 0] = np.median(metric[i])
                print(results[i, 0])

                print(f'{" standard deviation ":-^30}')
                results[i, 1] = metric[i].std()
                print(results[i, 1])

                np.savetxt(f'{path}/all_{name}s.csv', metric[i], delimiter = ",")

            print(f'\n {p.problem_name} Finished\n')

        for name, result in zip(self.metric_names, results):
            np.savetxt(f'{parent_path}/all_{name}_results.csv', result, delimiter = ',')