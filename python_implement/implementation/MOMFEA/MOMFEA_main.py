# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:54:46 2020

@author: t.urita
"""
import numpy as np
import matplotlib.pyplot as plt

from MOMFEA.populations import populations
from ..operator import *

def mfea_crossover(parents, sf):

    rmp = 0.9
    offspring1 = parents[0].copy()
    offspring2 = parents[1].copy()

    inter_cross = (sf[0] != sf[1]) * (np.random.rand(sf[0].shape[0]) < rmp)
    inter_mu = (sf[0] != sf[1]) != inter_cross

    mask = (np.random.rand(offspring1.shape[0], 1) < 0.9) * (np.random.rand(*offspring1.shape,) < 0.5)
    mask[inter_mu] = False

    offspring1[mask] = parents[1][mask]
    offspring2[mask] = parents[0][mask]

    sf0 = sf[0].copy()
    mask = inter_cross * (np.random.rand(inter_cross.shape[0]) < 0.5)
    sf0[mask] = sf[1][mask]

    sf1 = sf[1].copy()
    mask = inter_cross * (np.random.rand(inter_cross.shape[0]) < 0.5)
    sf1[mask] = sf[0][mask]

    return np.vstack((offspring1, offspring2)), np.hstack((sf0, sf1))

def bitflip_mutation(offs):

    off = offs
    mutation_ratio = 1 / off.shape[1]
    mutation_mask = np.random.rand(*off.shape,) < mutation_ratio
    off[mutation_mask] = 1 - off[mutation_mask]

    return off

class MOMFEA:

    def __init__(self, ndim, nobj, npop, noff, problem_list, code, rmp = 0.9):

        self.pops = populations(len(problem_list), npop, ndim, nobj).pop

        self.problems = problem_list

        self.npop = npop
        self.noff = noff
        self.nprob = len(problem_list)

        self.code = code
        self.rmp = rmp

        if code == "real":
            self.crossover = SBX
            self.mutation = polynomial_mutation
        elif code == "bin":
            self.crossover = mfea_crossover
            self.mutation = bitflip_mutation

    def init_pop(self):

        self.neval = 0

        if self.code == "real":
            self.pops["variables"] = np.random.rand(*self.pops["variables"].shape,)
        elif self.code == "bin":
            self.pops["variables"] = np.random.randint(2, size = self.pops["variables"].shape)

        for i, p in enumerate(self.problems):
            self.pops["objectives"][i] = p.evaluate(self.pops["variables"][i])
            self.init_eval(self.pops, i)

            self.neval += self.pops["variables"][i].shape[0]

    def init_eval(self, pop, sf):

        r = self.NDsorting(pop["objectives"][sf], self.npop)
        pop["pareto_rank"][sf] = r

        for i in range(max(r) + 1):
            pop["crowding_distance"][sf][r == i] = self.calc_cd(pop["objectives"][sf][r == i])

    def execute(self, max_eval):

        offs = {}

        # offs["variables"] = np.zeros([self.nprob * self.noff, self.pops["variables"].shape[2]])
        # offs["skill_factor"] = np.zeros(self.nprob * self.noff)
        n, mod= divmod(max_eval - self.neval, self.noff * self.nprob)

        rep = np.empty([self.nprob, n])

        for gen in range(n):

            old_pop = self.pops["variables"].copy()

            parents = []
            skill_factor = []

            for t_size in range(2):
                p, sf = self.mfea_selection()
                parents.append(self.pops["variables"][sf, p])
                skill_factor.append(sf)

            tmp, offs["skill_factor"]= self.crossover(parents, skill_factor)
            offs["variables"] = self.mutation(tmp)

            for task_no, p in enumerate(self.problems):
                off = {}
                mask = offs["skill_factor"] == task_no
                off["variables"] = offs["variables"][mask]
                off["objectives"] = p.evaluate(off["variables"])
                self.update(off, task_no)

            # visualize objective space
            # plt.cla()
            # plt.scatter(*self.pops["objectives"][0].T,)
            # plt.pause(0.01)

            for l in range(self.nprob):

                rep[l, gen] = self.npop - np.sum((self.pops["variables"][l][:, None, :] == old_pop[l][None, :, :]).sum(axis = 2) == self.pops["variables"].shape[2])

        if mod != 0:

            parents = []
            parents.append(self.pops["variables"][self.selection()])
            parents.append(self.pops["variables"][self.selection()])

            offs["variables"] = self.mutation(self.crossover(parents))
            offs["objectives"][:mod] = self.problem.evaluate(offs["variables"][:mod])
            offs["objectives"][mod:] = 0
            self.update(offs)

        self.neval = max_eval

        return rep

    def mfea_selection(self):

        rand_idx = np.random.randint(self.npop, size = [int(self.noff*self.nprob*0.5), 2])
        sf = np.random.randint(self.nprob, size = [int(self.noff*self.nprob*0.5), 2])

        idx = np.argmin([self.pops["pareto_rank"][sf[:, 0], rand_idx[:, 0]], self.pops["pareto_rank"][sf[:, 1], rand_idx[:, 1]]], axis = 0)
        same_pr = self.pops["pareto_rank"][sf[:, 0], rand_idx[:, 0]] == self.pops["pareto_rank"][sf[:, 1], rand_idx[:, 1]]
        idx[same_pr] = np.argmax([self.pops["crowding_distance"][sf[same_pr, 0], rand_idx[same_pr, 0]],\
                                  self.pops["crowding_distance"][sf[same_pr, 1], rand_idx[same_pr, 1]]], axis = 0)

        return rand_idx[range(sf.shape[0]), idx], sf[range(sf.shape[0]), idx]

    def mfea_crossover(self, parents, sf):

        inner_cross = sf[0] == sf[1]
        inter_cross = ~inner_cross * (np.random.rand(self.noff) < self.rmp)
        inter_mu = ~inner_cross != inter_cross

        inner_offs = self.crossover(parents[0][inner_cross], parents[1][inner_cross])
        inter_offs = self.crossover(parents[0][inter_cross], parents[1][inter_cross])
        no_cross = [parents[0][inter_mu], parents[1][inter_mu]]

        offs = np.vstack([inner_offs[0], inter_offs[0], no_cross[0], \
                          inner_offs[1], inter_offs[1], no_cross[1]])

        offs_sf = np.empty(self.noff)
        mask = inter_offs * (np.random.rand(self.noff) < 0.5)
        offs_sf[:int(self.noff/2)] = (1-mask)*sf[0] + mask*sf[1]
        offs_sf[int(self.noff/2):] = (1-mask)*sf[1] + mask*sf[0]

        return self.mutation(offs), offs_sf

    def update(self, offs, sf):

        union = {}
        union["variables"] = np.vstack((self.pops["variables"][sf] ,offs["variables"]))
        union["objectives"] = np.vstack((self.pops["objectives"][sf], offs["objectives"]))
        # union["variables"], idx = np.unique(np.vstack((self.pops["variables"][sf] ,offs["variables"])),\
        #                                       axis = 0, return_index = True)
        # union["objectives"] = np.vstack((self.pops["objectives"][sf], offs["objectives"]))[idx]

        r = self.NDsorting(union["objectives"], self.npop)

        offset = 0
        for i in range(max(r)):

            n = sum(r == i)

            self.pops["objectives"][sf][offset:offset + n] = union["objectives"][r == i]
            self.pops["variables"][sf][offset:offset + n] = union["variables"][r == i]
            self.pops["pareto_rank"][sf][offset:offset + n] = i
            self.pops["crowding_distance"][sf][offset:offset + n] = self.calc_cd(union["objectives"][r == i])

            offset +=n

        cd = self.calc_cd(union["objectives"][r == max(r)])
        remain = np.argsort(-cd)[:self.npop - offset]
        self.pops["objectives"][sf][offset:] = union["objectives"][r == max(r)][remain]
        self.pops["variables"][sf][offset:] = union["variables"][r == max(r)][remain]
        self.pops["pareto_rank"][sf][offset:] = max(r)
        self.pops["crowding_distance"][sf][offset:] = cd[remain]
