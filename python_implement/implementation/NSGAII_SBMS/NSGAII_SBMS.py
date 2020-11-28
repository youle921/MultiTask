# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 16:17:36 2020

@author: t.urita
"""
import numpy as np
import matplotlib.pyplot as plt

from ..NSGAII.nsgaii_main import NSGAII
from ..operator import *
from ..NSGAII.NSGA_util import NDsorting, calc_cd, mating

class NSGAII_SBMS(NSGAII):

    def __init__(self, ndim, nobj, npop, noff, problem, code, t_num_alpha, t_num_beta):

        super().__init__(ndim, nobj, npop, noff, problem, code)

        # 目的関数空間上で選択する解の個数
        self.alpha = t_num_alpha
        # 決定変数空間上で選択する解の個数
        self.beta = t_num_beta

    def selection(self):

        parents = []

        idx1 = mating(self.pop["pareto_rank"], self.pop["crowding_distance"], \
                     int(self.noff/2) * self.alpha).reshape([-1, self.alpha])

        candidate = self.pop["objectives"][idx1]
        center = candidate.mean(axis = 1)
        dist = ((candidate - center[:, None, :])**2).sum(axis = 2)

        parents1 = idx1[range(idx1.shape[0]), dist.argmax(axis = 1)]
        parents.append(self.pop["variables"][parents1])

        idx2 = mating(self.pop["pareto_rank"], self.pop["crowding_distance"], \
                     int(self.noff/2) * self.beta).reshape([-1, self.beta])

        dist = ((self.pop["variables"][idx2] - parents[0][:, None, :])**2).sum(axis = 2)

        parents2 = idx2[range(idx2.shape[0]), dist.argmin(axis = 1)]
        parents.append(self.pop["variables"][parents2])

        return parents