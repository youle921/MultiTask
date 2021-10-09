# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 00:58:09 2021

@author: youle
"""
import numpy as np
from ...base_class.base_problem import problem

class RE_base(problem):

    def set_IGD_ref(self, name):

        self.IGD_ref = np.loadtxt(
            f'{self.current_dir}/approximated_Pareto_fronts/{name}.csv', delimiter=',')
