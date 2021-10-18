# -*- coding: utf-8 -*-
import numpy as np

from. import all_probs, get_prob_pairs
from ...indicator import HV, IGD

def get_NDsolution(self, sol):

    # for minmization problem(compalator: >)
    is_dominated = (sol[:, None, :] >= sol[None, :, :]).prod(axis = 2) & \
        (sol[:, None, :] > sol[None, :, :]).max(axis = 2)

    NDsolution = is_dominated.max(axis = 1) == 0

    return sol[NDsolution]

class calculator:

    def __init__(self, metric):

        self.problemset = get_prob_pairs()
        self.metric_calculator = []
        self.metric_names = []

        if "IGD" in metric:
            self.metric_calculator.append(
                [[IGD.IGD(p.IGD_ref) for p in problem.tasks] for problem in self.problemset])
            self.metric_names.append("IGD")
        if "HV" in metric:
            self.metric_calculator.append(
                [[HV.HyperVolume(p.HV_ref) for p in problem.tasks] for problem in self.problemset])
            self.metric_names.append("HyperVolume")

    def calculation(self, path):

        for prob, prob_no in zip(self.problemset, range(len(self.problemset))):

            # preprocessing
            metric = np.empty([2, 2, 31, 1000])

            for i in range(1, 3):

                task = prob.tasks

                paths = [f'{path}/{prob.problem_name}_{t.problem_name}'
                        for t in task]
                obj = [np.load(f'{path}/trial{i}_objectives.npz')["arr_0"] for path in paths]

                # calculate and show metrics
                for idx, (calculator, metric_name) in enumerate(zip(self.metric_calculator, self.metric_names)):

                    for task_no in range(2):
                        if metric_name == "HyperVolume" and "normalize_objective" in dir(task[task_no]):
                            metric[idx, task_no, i] = [
                                *map(lambda p:calculator[prob_no][task_no]
                                             .compute(task[task_no].normalize_objective(p)),
                                     obj[task_no])]
                        else:
                            metric[idx, task_no, i] = [
                                *map(calculator[prob_no][task_no].compute, obj[task_no])]

                        np.savetxt(f'{paths[task_no]}/{metric_name}_log_trial{i}.csv', metric[idx, task_no, i], delimiter = ",")

            for t in range(len(self.problemset)):
                print(self.problemset[t].problem_name)
                for metric, data in zip(self.metric_names, metric[:, t]):
                    print(metric)
                    print(f'5,000 eval: {np.median(data[:, 49]):.4e}')
                    print(f'20,000 eval: {np.median(data[:, 199]):.4e}')
                    np.savetxt(f'{paths[t]}/all_{metric}_log.csv', np.vstack([np.median(data, axis = 0), data.std(axis = 0)]).T)

