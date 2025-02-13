# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.join(os.pardir, '..'))

import numpy as np

import json
from datetime import datetime
from collections import OrderedDict

from implementation.indicator import HV, IGD

class EMOA_runner:

    def __init__(self, algorithm, problem, path, metric):

        self.alg = algorithm
        self.problem = problem
        self.caller_path = path

        self.metric_calculator = {}

        if "IGD" in metric:
            self.metric_calculator["IGD"] = [IGD.IGD(p.IGD_ref) for p in self.problem]

        if "HV" in  metric:
            self.metric_calculator["HV"] = [HV.HyperVolume(p.HV_ref) for p in self.problem]

        if "normalized_IGD" in metric:
            self.metric_calculator["normalized_IGD"] = [IGD.normalized_IGD(p.IGD_ref) for p in self.problem]

    def load_params(self):
        with open(f'{self.caller_path}/setting.json') as f:
            self.params = json.load(f, object_pairs_hook=OrderedDict)

        if "n_eval" in self.params:
            self.criteria = self.params["n_eval"]
        elif "n_gen" in self.params:
            self.criteria = self.params["n_gen"]

    def run(self):

        self.load_params()

        parent_path = f'{self.caller_path}/{datetime.today().strftime("%m%d")}'
        os.makedirs(parent_path, exist_ok = True)

        results = np.empty([len(self.metric_calculator), len(self.problem), 2])

        for p, prob_no in zip(self.problem, range(len(self.problem))):

            # preprocessing
            print(f'  {p.problem_name} Started  '.center(50, '*'))

            metric = np.empty([len(self.metric_calculator), self.params["n_trial"]])
            final_objs = []
            final_nd_objs = []

            path = f'{parent_path}/{p.problem_name}'
            os.makedirs(path, exist_ok = True)

            # start running algorithm
            start_time = datetime.now()
            solver = self.alg(self.params, p)

            for trial in range(self.params["n_trial"]):

                np.random.seed(trial)

                solver.init_pop()
                solver.execute(self.criteria)

                solver.output_log(path, trial + 1)

                final_objs.append(solver.pop["objectives"])
                final_nd_objs.append(solver.get_NDsolution)

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

            print(f'{"metric calculating...":^50}')
            # calculate and show metrics
            for idx, (metric_name, calculator) in enumerate(self.metric_calculator.items()):

                if metric_name == "HyperVolume":
                    if "normalize_objective" in dir(p):
                        metric[idx] = [*map(lambda obj:calculator[prob_no].compute
                                            (p.normalize_objective(obj)), final_objs)]
                    else:
                        metric[idx] = [*map(calculator[prob_no].compute, final_nd_objs)]

                else:
                    metric[idx] = [*map(calculator[prob_no].compute, final_objs)]

            for i, name in enumerate(self.metric_calculator.keys()):
                print(f'{name:^50}')

                print(f'{" median ":-^50}')
                results[i, prob_no, 0] = np.median(metric[i])
                print(results[i, prob_no, 0])

                print(f'{" standard deviation ":-^50}')
                results[i, prob_no, 1] = metric[i].std()
                print(results[i, prob_no, 1])

                np.savetxt(f'{path}/all_{name}s.csv', metric[i], delimiter = ",")

            print(f'  {p.problem_name} Finished  '.center(50, '*'), '\n\n')

        for name, result in zip(self.metric_names, results):
            np.savetxt(f'{parent_path}/all_{name}_results.csv', result, delimiter = ',')


    def run_tracing(self):

        self.load_params()

        parent_path = f'{self.caller_path}/{datetime.today().strftime("%m%d")}'
        os.makedirs(parent_path, exist_ok = True)

        results = np.empty([len(self.metric_calculator), len(self.problem), 2])

        for p, prob_no in zip(self.problem, range(len(self.problem))):

            # preprocessing
            print(f'  {p.problem_name} Started  '.center(50, '*'))

            metric = np.empty([len(self.metric_calculator), self.params["n_trial"]])
            final_objs = []
            final_nd_objs = []

            path = f'{parent_path}/{p.problem_name}'
            os.makedirs(path, exist_ok = True)

            # start running algorithm
            start_time = datetime.now()
            solver = self.alg(self.params, p)

            for trial in range(self.params["n_trial"]):

                np.random.seed(trial)

                solver.init_pop()
                trace_log = solver.execute(self.criteria)

                np.savetxt(f'{path}/trial{trial + 1}_trace_log.csv', trace_log, delimiter = ",")

                final_objs.append(solver.pop["objectives"])
                final_nd_objs.append(solver.get_NDsolution)

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

            print(f'{"metric calculating...":^50}')
            # calculate and show metrics
            for idx, (metric_name, calculator) in enumerate(self.metric_calculator.items()):

                if metric_name == "HyperVolume":
                    if "normalize_objective" in dir(p):
                        metric[idx] = [*map(lambda obj:calculator[prob_no].compute
                                            (p.normalize_objective(obj)), final_objs)]
                    else:
                        metric[idx] = [*map(calculator[prob_no].compute, final_nd_objs)]

                else:
                    metric[idx] = [*map(calculator[prob_no].compute, final_objs)]

            for i, name in enumerate(self.metric_calculator.keys()):
                print(f'{name:^50}')

                print(f'{" median ":-^50}')
                results[i, prob_no, 0] = np.median(metric[i])
                print(results[i, prob_no, 0])

                print(f'{" standard deviation ":-^50}')
                results[i, prob_no, 1] = metric[i].std()
                print(results[i, prob_no, 1])

                np.savetxt(f'{path}/all_{name}s.csv', metric[i], delimiter = ",")

            print(f'  {p.problem_name} Finished  '.center(50, '*'), '\n\n')

        for name, result in zip(self.metric_calculator.keys(), results):
            np.savetxt(f'{parent_path}/all_{name}_results.csv', result, delimiter = ',')
