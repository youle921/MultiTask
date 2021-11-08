# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 22:04:37 2020

@author: youle
"""
import numpy as np

from ..base_class.EMOA_base import Algorithm
from ..operator import *
from .NSGA_util import NDsorting, calc_cd, mating
from. import NSGAII

class NSGAII_tracing(NSGAII):


    def init_pop(self):

        if self.code == "real":
            self.pop["variables"][...] = \
                np.random.rand(*self.pop["variables"].shape,)

        elif self.code == "bin":
            self.pop["variables"][...] = \
                np.random.randint(2, size=self.pop["variables"].shape)

        self.pop["objectives"] = self.eval_method(self.pop["variables"])
        self._init_eval()

        self.neval = self.npop

        self.trace_log = []

    def _update(self, offs, inter_cross):

        union = self.concat_pops(self.pop, offs)
        tmp = np.hstack([[0] * self.npop, inter_cross])
        trace = np.empty(self.npop, dtype = int)
        r = NDsorting(union["objectives"], self.npop)

        offset = 0
        for i in range(max(r)):

            n = sum(r == i)

            self.pop["objectives"][offset: offset + n] = union["objectives"][r == i]
            self.pop["variables"][offset: offset + n] = union["variables"][r == i]
            self.pop["pareto_rank"][offset: offset + n] = i
            self.pop["crowding_distance"][offset: offset + n] = calc_cd(union["objectives"][r == i])
            trace[offset:offset + n] = tmp[r == i]

            offset += n
        cd = calc_cd(union["objectives"][r == max(r)])
        remain = np.argsort(-cd)[: self.npop - offset]

        self.pop["objectives"][offset:] = union["objectives"][r ==max(r)][remain]
        self.pop["variables"][offset:] = union["variables"][r ==max(r)][remain]
        self.pop["pareto_rank"][offset:] = max(r)
        self.pop["crowding_distance"][offset:] = calc_cd(self.pop["objectives"][offset:])
        trace[offset:] = tmp[r == max(r)][remain]

        return trace