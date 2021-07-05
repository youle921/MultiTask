# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 00:48:07 2020

@author: t.urita
"""
import numpy as np

import os
import sys
sys.path.append(os.path.dirname(__file__))

from base_class import MTO_base_class
from distance_function import griewank, ackley

class NILS:

    def __init__(self):

        self.t1 = NILS_t1()
        self.t2 = NILS_t2()

    def evaluate_value(self, population):

        return [self.t1.evaluate, self.t2.evaluate]

    def get_tasks(self):

        return [self.t1, self.t2]

class NILS_t1(MTO_base_class):

    def __init__(self, n = 25):

        super().__init__()

        self.dim = n

        self.dist_f = griewank
        self.lower = np.array([0] + [0] + [-50] * (n - 2))
        self.upper = np.array([1] + [1] + [50] * (n - 2))

        self.shift_vector = np.loadtxt(self.current_path + "/shift_data/S_NILS_1.txt")
        self.set_reference_point("sphere")

    def f1(self, population):

        return self.dist_f(population[:, 1:]) * np.cos(np.pi * population[:, 0] * 0.5) * np.cos(np.pi * population[:, 1] * 0.5)

    def f2(self, population):

        return self.dist_f(population[:, 1:]) * np.cos(np.pi * population[:, 0] * 0.5) * np.sin(np.pi * population[:, 1] * 0.5)

    def f3(self, population):

        return self.dist_f(population[:, 1:]) * np.sin(np.pi * population[:, 0] * 0.5)

    def evaluate(self, population):

        tf_pop = self.transforn_population(population[:, :self.dim])

        f1_value = self.f1(tf_pop)
        f2_value = self.f2(tf_pop)
        f3_value = self.f3(tf_pop)

        return np.vstack([f1_value, f2_value, f3_value]).T

    def shift_population(self, pop):

        pop[:, 2:] -= self.shift_vector

        return pop

class NILS_t2(MTO_base_class):

    def __init__(self, n = 50):

        super().__init__()

        self.dim = n

        self.dist_f = ackley
        self.lower = np.array([0] + [0] + [-100] * (n - 2))
        self.upper = np.array([1] + [1] + [100] * (n - 2))

        self.set_reference_point("concave")

    def f1(self, population):

        return (population[:, 0] + population[:, 1])/2

    def f2(self, population):

        return self.dist_f(population[:, 1:]) * (1 - (0.5*(population[:, 0] + population[:, 1])/self.dist_f(population[:, 1:]))**2)

if __name__ == "__main__":

    task_name = "NILS"

    tasks = NILS()
    prob1 = tasks.t1
    prob2 = tasks.t2

    # test code T1
    pop1 = np.loadtxt("check_obj/" + task_name +"/t1/FinalVAR1.dat")
    correct_obj1 = np.loadtxt("check_obj/" + task_name + "/t1/FinalFUN1.dat")
    correct_igd1 = np.loadtxt("check_obj/" + task_name + "/t1/IGDHisWithAllSol1.dat")[999, 1]

    calc_obj1 = prob1.evaluate(pop1)

    print("-----Task1-----")
    print("accumulated error = " + str(np.sum(correct_obj1 - calc_obj1)))

    print("      correct IGD = " + str(correct_igd1))
    print("   calculated IGD = " + str(prob1.calc_IGD(calc_obj1)) + "\n")

    # test code T2
    pop2 = np.loadtxt("check_obj/" + task_name +"/t2/FinalVAR1.dat")
    correct_obj2 = np.loadtxt("check_obj/" + task_name + "/t2/FinalFUN1.dat")
    correct_igd2 = np.loadtxt("check_obj/" + task_name + "/t2/IGDHisWithAllSol1.dat")[999, 1]

    calc_obj2 = prob2.evaluate(pop2)
    print("-----Task2-----")
    print("accumulated error = " + str(np.sum(correct_obj2 - calc_obj2)))

    print("      correct IGD = " + str(correct_igd2))
    print("   calculated IGD = " + str(prob2.calc_IGD(calc_obj2)))

    # prob1.IGD_ref = (prob1.IGD_ref - np.min(prob1.IGD_ref, axis = 0))/ (np.max(prob1.IGD_ref, axis = 0) - np.min(prob1.IGD_ref, axis = 0))

    # igd = prob1.calc_IGD(calc_obj1)