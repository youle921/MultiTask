# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 00:52:15 2021

@author: youle
"""

from abc import ABCMeta, abstractmethod

class problem(metaclass = ABCMeta):

    def __init__(self):

        self.problem_name = "problem"

        self.ndim = -1

        self.upper = None
        self.lower = None

        self.IGD_ref = None
        self.HV_ref = None

        self.code = 'real'
        self.project_uss = True

    @abstractmethod
    def evaluate(self, pop):
        pass

    def set_IGD_ref(self):
        pass

    def reverse_projection(self, pop):
        
        if self.project_uss:
            return pop[:, :self.ndim] * (self.upper - self.lower)[None, :] + self.lower[None, :]
        else:
            return pop[:, :self.ndim]