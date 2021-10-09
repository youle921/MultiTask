# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 01:45:26 2020

@author: youle
"""
import numpy as np
import os

from ...base_class.base_problem import problem

class MTO_base(problem):

    def __init__(self):

        super().__init__()

        self.shift_vector = None
        self.rotation_matrix = None
        
        self.current_dir = os.path.dirname(__file__)

    def set_IGD_ref(self, pf_type):

        self.IGD_ref = np.loadtxt(f'{self.current_dir}/PF/{pf_type}.csv', delimiter = ',')

    def evaluate(self, population):

        # self.repair_population(population)
        tf_pop = self.transforn_population(population[:, :self.ndim])
        f1_value = self.f1(tf_pop)
        f2_value = self.f2(tf_pop)

        return np.vstack([f1_value, f2_value]).T

# apply transformation(normalize + shift + rotate)
    def transforn_population(self, pop):

        if self.project_uss:
            pop_ = self.reverse_projection(pop)
        else:
            pop_ = pop.copy()

        if not(self.shift_vector is None):
            pop_ = self.shift_population(pop_)
        if not(self.rotation_matrix is None):
            pop_ = self.rotate_population(pop_)

        return pop_

    def shift_population(self, pop):

        pop[:, 1:] -= self.shift_vector

        return pop

    def rotate_population(self, pop):

        pop[:, 1:] = np.dot(pop[:, 1:], self.rotation_matrix.T)

        return pop