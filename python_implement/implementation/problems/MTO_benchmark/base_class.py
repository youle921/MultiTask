# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 01:45:26 2020

@author: youle
"""
import numpy as np
import os

class MTO_base_class:

    def __init__(self):

        self.upper = None
        self.lower = None

        self.shift_vector = None
        self.rotation_matrix = None

        self.IGD_ref = None
        self.current_path = os.path.dirname(__file__)

        self.code = 'real'

    def set_reference_point(self, pf_type):

        self.IGD_ref = np.loadtxt(self.current_path + "/pf/" + pf_type + ".pf")

    def evaluate(self, population):

        # self.repair_population(population)

        tf_pop = self.transforn_population(population[:, :self.ndim])

        f1_value = self.f1(tf_pop)
        f2_value = self.f2(tf_pop)

        return np.vstack([f1_value, f2_value]).T

    def repair_population(self, pop):

        pop[pop > 1] = 1
        pop[pop < 0] = 0

# apply transformation(normalize + shift + rotate)
    def transforn_population(self, pop):

        pop_ = self.reverse_normalize(pop)

        if not(self.shift_vector is None):
            pop_ = self.shift_population(pop_)
        if not(self.rotation_matrix is None):
            pop_ = self.rotate_population(pop_)

        return pop_

    def reverse_normalize(self, pop):

        tf_pop = pop * (self.upper - self.lower)[None, :] + self.lower[None, :]

        return tf_pop

    def shift_population(self, pop):

        pop[:, 1:] -= self.shift_vector

        return pop

    def rotate_population(self, pop):

        pop[:, 1:] = np.dot(pop[:, 1:], self.rotation_matrix.T)

        return pop

    def calc_IGD(self, objective):

        dist = np.sqrt(np.sum((self.IGD_ref[:, None, :] - objective[None, :, :])**2, axis = 2))
        min_dist = np.min(dist, axis = 1)
        sqrt_sum =  np.sqrt((min_dist**2).sum())

        return sqrt_sum/self.IGD_ref.shape[0]