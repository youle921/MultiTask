# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 00:48:07 2020

@author: t.urita
"""
import numpy as np

from ...base_class.base_problem_set import problem_set

from .MTO_base import MTO_base
from .distance_function import griewank, ackley

class PILS(problem_set):

    def __init__(self):

        super().__init__([PILS_t1(), PILS_t2()])

        self.problem_name = "PILS"

class PILS_t1(MTO_base):

    def __init__(self):

        super().__init__()

        self.problem_name = 'task1'

        self.ndim = 50

        self.dist_f = griewank
        self.lower = np.array([0] + [-50] * (self.ndim - 1))
        self.upper = np.array([1] + [50] * (self.ndim - 1))

        self.set_IGD_ref("circle")

    def f1(self, population):

        return self.dist_f(population[:, :]) * np.cos(np.pi * population[:, 0] * 0.5)

    def f2(self, population):

        return self.dist_f(population[:, :]) * np.sin(np.pi * population[:, 0] * 0.5)

class PILS_t2(MTO_base):

    def __init__(self):

        super().__init__()

        self.problem_name = 'task2'

        self.ndim = 50

        self.dist_f = ackley
        self.lower = np.array([0] + [-100] * (self.ndim - 1))
        self.upper = np.array([1] + [100] * (self.ndim - 1))

        self.shift_vector = np.loadtxt(self.current_dir + "/shift_data/S_PILS_2.txt")
        self.set_IGD_ref("circle")

    def f1(self, population):

        return self.dist_f(population[:, :]) * np.cos(np.pi * population[:, 0] * 0.5)

    def f2(self, population):

        return self.dist_f(population[:, :]) * np.sin(np.pi * population[:, 0] * 0.5)

if __name__ == "__main__":

    task_name = "PILS"

    tasks = PILS()
    prob1 = tasks.t1
    prob2 = tasks.t2

    # test code T1
    pop1 = np.loadtxt("check_obj/" + task_name +"/t1/FinalVAR1.dat")
    correct_obj1 = np.loadtxt("check_obj/" + task_name + "/t1/FinalFUN1.dat")
    correct_igd1 = np.loadtxt("check_obj/" + task_name + "/t1/IGDHisWithAllSol1.dat")[999, 1]

    calc_obj1 = prob1.evaluate(pop1)
    print("-----Task1-----")
    print("accumulated error = " + str(np.sum(np.abs(correct_obj1 - calc_obj1))))

    print("      correct IGD = " + str(correct_igd1))
    print("   calculated IGD = " + str(prob1.calc_IGD(calc_obj1)) + "\n")

    # test code T2
    pop2 = np.loadtxt("check_obj/" + task_name +"/t2/FinalVAR1.dat")
    correct_obj2 = np.loadtxt("check_obj/" + task_name + "/t2/FinalFUN1.dat")
    correct_igd2 = np.loadtxt("check_obj/" + task_name + "/t2/IGDHisWithAllSol1.dat")[999, 1]

    calc_obj2 = prob2.evaluate(pop2)
    print("-----Task2-----")
    print("accumulated error = " + str(np.sum(np.abs(correct_obj2 - calc_obj2))))

    print("      correct IGD = " + str(correct_igd2))
    print("   calculated IGD = " + str(prob2.calc_IGD(calc_obj2)))