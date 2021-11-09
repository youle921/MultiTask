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

        for prob, prob_no in zip(self.problemset, range(len(self.problemset))):

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
                            
                            ax = fig.add_subplot(111, projection = '3d')
                            ax.scatter(*obj_.T, alpha = 1, label = "Population")
                            ax.scatter(*pf.T, color = "k", alpha = 1, label = "Pareto Front")

                        ax.legend()
                        plt.ioff()
                        plt.savefig(f'{paths[n]}/gen{g + 1}_pop.png', dpi = 720)
                        plt.close()

    def single_visualization(self, parent_path):

        for task, prob_no in zip(self.problems, range(len(self.problems))):

            path = f'{parent_path}/{task.problem_name}'

            for i in range(1):

                obj = np.load(f'{path}/trial{i + 1}_objectives.npz')["arr_0"]
                metrics = np.loadtxt(f'{path}/IGD_log_trial{i + 1}.csv', delimiter = ",")
                
                pf = task.IGD_ref[task.IGD_ref[:, 0].argsort()]

                for g, (obj_, met_) in enumerate(zip(obj[:50], metrics)):

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
                        
                        ax = fig.add_subplot(111, projection = '3d')
                        ax.scatter(*obj_.T, alpha = 1, label = "Population")
                        ax.scatter(*pf.T, color = "k", alpha = 1, label = "Pareto Front")

                    ax.legend()
                    plt.ioff()
                    plt.savefig(f'{path}/gen{g + 1}_pop.png', dpi = 720)
                    plt.close()

    def visualization_fix_range(self, parent_path):

        for prob, prob_no in zip(self.problemset, range(len(self.problemset))):

            # preprocessing
            task = prob.tasks

            paths = [f'{parent_path}/{prob.problem_name}_{t.problem_name}' for t in task]

            for i in range(1):

                objs = [np.load(f'{path}/trial{i + 1}_objectives.npz')["arr_0"] for path in paths]
                metrics = [np.loadtxt(f'{path}/IGD_log_trial{i + 1}.csv', delimiter = ",") for path in paths]

                for n, (obj, met) in enumerate(zip(objs, metrics)):
                    
                    pf = task[n].IGD_ref[task[n].IGD_ref[:, 0].argsort()]
                    
                    width = pf.max(axis = 0) * 0.1
                    if pf.shape[1] == 2:
                        xmin, ymin = pf.min(axis = 0) - width
                        xmax, ymax = pf.max(axis = 0) + width
                    elif pf.shape[1] == 3:
                        xmin, ymin, zmin = pf.min(axis = 0) - width
                        xmax, ymax, zmax = pf.max(axis = 0) + width

                    for g, (obj_, met_) in enumerate(zip(obj[:50], met)):

                        fig = plt.figure()
                        plt.ion()
                        fig.suptitle(f'IGD: {met_:.4e}')

                        if obj_.shape[1] > 3:
                            return
                        
                        elif obj_.shape[1] == 2:
                            
                            ax = fig.add_subplot()
                            ax.scatter(*obj_.T, label = "Population")
                            ax.plot(pf[:, 0], pf[:, 1], c = "k", label = "Pareto Front")
                            ax.set(xlim = (xmin, xmax), ylim = (ymin, ymax))

                        elif obj_.shape[1] == 3:
                            
                            ax = fig.add_subplot(111, projection = '3d')
                            ax.scatter(*obj_.T, alpha = 1, label = "Population")
                            ax.scatter(*pf.T, color = "k", alpha = 1, label = "Pareto Front")
                            
                            ax.set_xlim3d(xmin, xmax)
                            ax.set_ylim3d(ymin, ymax)
                            ax.set_zlim3d(zmin, zmax)

                        ax.legend()
                        plt.ioff()
                        plt.savefig(f'{paths[n]}/gen{g + 1}_pop_fixed.png', dpi = 720)
                        plt.close()

    def single_visualization_fix_range(self, parent_path):

        for task, prob_no in zip(self.problems, range(len(self.problems))):

            path = f'{parent_path}/{task.problem_name}'

            for i in range(1):

                obj = np.load(f'{path}/trial{i + 1}_objectives.npz')["arr_0"]
                metrics = np.loadtxt(f'{path}/IGD_log_trial{i + 1}.csv', delimiter = ",")
                
                pf = task.IGD_ref[task.IGD_ref[:, 0].argsort()]
                
                width = pf.max(axis = 0) * 0.1
                if pf.shape[1] == 2:
                    xmin, ymin = pf.min(axis = 0) - width
                    xmax, ymax = pf.max(axis = 0) + width
                elif pf.shape[1] == 3:
                    xmin, ymin, zmin = pf.min(axis = 0) - width
                    xmax, ymax, zmax = pf.max(axis = 0) + width


                for g, (obj_, met_) in enumerate(zip(obj[:50], metrics)):

                    fig = plt.figure()
                    plt.ion()
                    fig.suptitle(f'IGD: {met_:.4e}')

                    if obj_.shape[1] > 3:
                        return
                    
                    elif obj_.shape[1] == 2:
                        
                        ax = fig.add_subplot(111)
                        ax.scatter(*obj_.T, label = "Population")
                        ax.plot(pf[:, 0], pf[:, 1], c = "k", label = "Pareto Front")
                        ax.set(xlim = (xmin, xmax), ylim = (ymin, ymax))
                        
                    elif obj_.shape[1] == 3:
                        
                        ax = fig.add_subplot(111, projection = '3d')
                        ax.scatter(*obj_.T, alpha = 1, label = "Population")
                        ax.scatter(*pf.T, color = "k", alpha = 1, label = "Pareto Front")
                        
                        ax.set_xlim3d(xmin, xmax)
                        ax.set_ylim3d(ymin, ymax)
                        ax.set_zlim3d(zmin, zmax)

                    ax.legend()
                    plt.ioff()
                    plt.savefig(f'{path}/gen{g + 1}_pop_fixed.png', dpi = 720)
                    plt.close()