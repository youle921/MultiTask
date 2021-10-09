# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 00:48:07 2020

@author: t.urita
"""
import numpy as np

from MTO_base import MTO_base
from distance_function import rosenbrock, sphere

class NIMS:

    def __init__(self):

        super().__init__([NIMS_t1(), NIMS_t2()])

        self.problem_name = "NIMS"

class NIMS_t1(MTO_base):

    def __init__(self):

        super().__init__()

        self.problem_name = 'task1'

        self.ndim = 20

        self.dist_f = rosenbrock
        self.lower = np.array([0] + [0] + [-20] * (self.ndim - 2))
        self.upper = np.array([1] + [1] + [20] * (self.ndim - 2))

        self.set_IGD_ref("sphere")

    def f1(self, population):

        return self.dist_f(population[:, 1:]) * np.cos(np.pi * population[:, 0] * 0.5) * np.cos(np.pi * population[:, 1] * 0.5)

    def f2(self, population):

        return self.dist_f(population[:, 1:]) * np.cos(np.pi * population[:, 0] * 0.5) * np.sin(np.pi * population[:, 1] * 0.5)

    def f3(self, population):

        return self.dist_f(population[:, 1:]) * np.sin(np.pi * population[:, 0] * 0.5)

    def evaluate(self, population):

        tf_pop = self.transforn_population(population[:, :self.ndim])

        f1_value = self.f1(tf_pop)
        f2_value = self.f2(tf_pop)
        f3_value = self.f3(tf_pop)

        return np.vstack([f1_value, f2_value, f3_value]).T

class NIMS_t2(MTO_base):

    def __init__(self):

        super().__init__()

        self.problem_name = 'task2'

        self.ndim = 20

        self.dist_f = sphere
        self.lower = np.array([0] + [0] + [-20] * (self.ndim - 2))
        self.upper = np.array([1] + [1] + [20] * (self.ndim - 2))

        self.rotation_matrix = np.loadtxt(self.current_path + "/matrix_data/M_NIMS_2.txt")
        self.set_IGD_ref("concave")

    def f1(self, population):

        return (population[:, 0] + population[:, 1])/2

    def f2(self, population):

        return self.dist_f(population[:, 1:]) * (1 - (0.5*(population[:, 0] + population[:, 1])/self.dist_f(population[:, 1:]))**2)

    def rotate_population(self, pop):

        pop[:, 2:] = np.dot(pop[:, 2:], self.rotation_matrix.T)

        return pop

if __name__ == "__main__":

    task_name = "NIMS"

    tasks = NIMS()
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