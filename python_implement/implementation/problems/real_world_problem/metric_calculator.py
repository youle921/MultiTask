# -*- coding: utf-8 -*-
import numpy as np

from. import all_probs, get_prob_pairs
from ...indicator import HV, IGD

def get_NDsolution(sol):

    # for minmization problem(compalator: >)
    is_dominated = (sol[:, None, :] >= sol[None, :, :]).prod(axis = 2) & \
        (sol[:, None, :] > sol[None, :, :]).max(axis = 2)

    NDsolution = is_dominated.max(axis = 1) == 0

    return sol[NDsolution]

def get_NDsolution_3dim(sol):

    is_dominated = (sol[:, :, None, :] >= sol[:, None, :, :]).prod(axis = -1) &\
        (sol[:, :, None, :] > sol[:, None, :, :]).max(axis = -1)

    NDsolution = is_dominated.max(axis = -1) == 0

    return [s[nd] for s, nd in zip(sol, NDsolution)]

class calculator:

    def __init__(self, metric):

        self.problemset = get_prob_pairs()
        self.problems = all_probs
        self.metric_calculator = {}

        if "IGD" in metric:
            self.metric_calculator["IGD"] = [[IGD.IGD(p.IGD_ref) for p in problem.tasks]
                                             for problem in self.problemset]

        if "HV" in metric:
            self.metric_calculator["HV"] = [[HV.HyperVolume(p.HV_ref) for p in problem.tasks]
                                            for problem in self.problemset]

        if "normalized_IGD" in metric:
            self.metric_calculator["normalized_IGD"] = [[IGD.normalized_IGD(p.IGD_ref) for p in problem.tasks]
                                                        for problem in self.problemset]
        self.single_calculator = []
        for calc in self.metric_calculator:
            self.single_calculator.append([c for calc_pair in calc for c in calc_pair])

    def calculation(self, parent_path):

        for prob, prob_no in zip(self.problemset, range(len(self.problemset))):

            # preprocessing
            task = prob.tasks
            metric = np.empty([len(self.metric_calculator), len(task), 31, 1000])

            paths = [f'{parent_path}/{prob.problem_name}_{t.problem_name}' for t in task]

            for i in range(31):

                obj = [np.load(f'{path}/trial{i + 1}_objectives.npz')["arr_0"] for path in paths]

                # calculate and show metrics
                for idx, (calculator, metric_name) in enumerate(zip(self.metric_calculator.values(), self.metric_calculator.keys())):

                    for task_no in range(2):
                        if metric_name == "HyperVolume" and "normalize_objective" in dir(task[task_no]):
                            metric[idx, task_no, i] = [
                                *map(lambda p:calculator[prob_no][task_no]
                                             .compute(task[task_no].normalize_objective(p)),
                                     get_NDsolution_3dim(obj[task_no]))]
                        else:
                            metric[idx, task_no, i] = [
                                *map(calculator[prob_no][task_no].compute, obj[task_no])]

                        np.savetxt(f'{paths[task_no]}/{metric_name}_log_trial{i + 1}.csv', metric[idx, task_no, i], delimiter = ",")

            print(f'{"*":*^50}')

            for t in range(len(task)):
                print(f'{task[t].problem_name:^50}')

                for met, data in zip(self.metric_names, metric[:, t]):

                    print(f'{met:-^50}')

                    print(f'5,000 eval: {np.median(data[:, 49]):.4e}')
                    print(f'20,000 eval: {np.median(data[:, 199]):.4e}')

                    np.savetxt(f'{paths[t]}/all_{met}_log.csv', np.vstack([np.median(data, axis = 0), data.std(axis = 0)]).T, delimiter = ",")


    def single_calculation(self, parent_path):

        for prob_no, task in enumerate(self.problems):

            path = f'{parent_path}/{task.problem_name}'
            metric = np.empty([2, 31, 1000])

            for i in range(31):

                obj = np.load(f'{path}/trial{i + 1}_objectives.npz')["arr_0"]

                for idx, (calculator, metric_name) in enumerate(zip(self.single_calculator, self.metric_calculator.keys())):

                    if metric_name == "HyperVolume":
                        metric[idx, i] = [*map(lambda p:calculator[prob_no].compute
                                            (task.normalize_objective(p)), get_NDsolution_3dim(obj))]
                    else:
                        metric[idx, i] = [*map(calculator[prob_no].compute, obj)]

                    np.savetxt(f'{path}/{metric_name}_log_trial{i + 1}.csv', metric[idx, i], delimiter = ",")

            print(f'{"*":*^50}')

            print(f'{task.problem_name:^50}')
            for met, data in zip(self.metric_names, metric):

                print(f'{met:-^50}')

                print(f'5,000 eval: {np.median(data[:, 49]):.4e}')
                print(f'20,000 eval: {np.median(data[:, 199]):.4e}')

                np.savetxt(f'{path}/all_{met}_log.csv', np.vstack([np.median(data, axis = 0), data.std(axis = 0)]).T, delimiter = ",")
