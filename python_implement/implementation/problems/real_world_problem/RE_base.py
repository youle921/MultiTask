# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 00:58:09 2021

@author: youle
"""
import numpy as np
import os

from ...base_class.base_problem import problem

class RE_base(problem):

    def __init__(self):

        super().__init__()

        self.current_dir = os.path.dirname(__file__)

    def set_IGD_ref(self, name):

        self.IGD_ref = np.loadtxt(
            f'{self.current_dir}/approximated_Pareto_fronts/{name}.csv', delimiter=',')

    def set_HV_ref(self, name):

        self.HV_ref = np.full(self.n_objectives, 1.1)
        self.nadir = np.loadtxt(f'{self.current_dir}/ideal_nadir_points/nadir_point_{name}.dat')
        self.ideal = np.loadtxt(f'{self.current_dir}/ideal_nadir_points/ideal_point_{name}.dat')

    def normalize_objective(self, pop):

        return (pop - self.ideal) / (self.nadir - self.ideal)
