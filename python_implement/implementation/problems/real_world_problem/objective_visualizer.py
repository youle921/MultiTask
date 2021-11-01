# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from. import all_probs, get_prob_pairs

class visualizer:

    def __init__(self):

        self.problemset = get_prob_pairs()
        self.problems = all_probs

    def visualization(self, parent_path):

        for prob, prob_no in zip(self.problemset[3:], range(len(self.problemset))):

            # preprocessing
            task = prob.tasks

            paths = [f'{parent_path}/{prob.problem_name}_{t.problem_name}' for t in task]

            for i in range(1):

                objs = [np.load(f'{path}/trial{i + 1}_objectives.npz')["arr_0"] for path in paths]
                metrics = [np.loadtxt(f'{path}/IGD_log_trial{i + 1}.csv', delimiter = ",") for path in paths]

                for n, (obj, met) in enumerate(zip(objs, metrics)):
                    pf = task[n].IGD_ref[task[n].IGD_ref[:, 0].argsort()]

                    for g, (obj_, met_) in enumerate(zip(obj[:50], met)):

                        fig = plt.figure()
                        plt.ion()
                        fig.suptitle(f'IGD: {met_:.4e}')

                        if obj_.shape[1] > 3:
                            return
                        elif obj_.shape[1] == 2:
                            ax = fig.add_subplot(111, xmargin = 0.1, ymargin = 0.1)
                            ax.scatter(*obj_.T, label = "Population")
                            ax.plot(pf[:, 0], pf[:, 1], c = "k", label = "Pareto Front")
                        elif obj_.shape[1] == 3:
                            ax = Axes3D(fig)
                            ax.scatter(*obj.T, alpha = 1, label = "Population")
                            ax.scatter(*pf.T, color = "k", alpha = 1, label = "Pareto Front")

                        ax.legend()
                        plt.ioff()
                        plt.savefig(f'{paths[n]}/gen{g + 1}_pop.png', dpi = 720)
                        plt.close()

    def single_calculation(self, parent_path):

        for task, prob_no in zip(self.problems, range(len(self.problems))):

            path = f'{parent_path}/{task.problem_name}'
            metric = np.empty([2, 31, 1000])

            for i in range(31):

                obj = np.load(f'{path}/trial{i + 1}_objectives.npz')["arr_0"]

                for idx, (calculator, metric_name) in enumerate(zip(self.single_calculator, self.metric_names)):

                    if metric_name == "HyperVolume":
                        if "normalize_objective" in dir(task):
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
