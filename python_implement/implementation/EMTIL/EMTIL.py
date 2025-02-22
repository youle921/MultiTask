# -*- coding: utf-8 -*-

import numpy as np


from .nsgaii_for_EMTIL import NSGAII_EMTIL

def norm_dist(x, mu, sigma, eps = 1e-8):

    return (1 / (np.sqrt(2 * np.pi * sigma + eps))) * np.exp(-1 * ((x - mu)**2 / (2 * sigma + eps)))

class EMTIL:

    def __init__(self, params, problem_list):

        self.mig_size = params["migration_size"]

        self.p = 0.3
        self.l = 0.3

        if "p" in params:
            self.p = params["p"]
        if "lambda" in params:
            self.l = params["lambda"]

        ndim = max([p.ndim for p in problem_list])

        self.algs = []
        for task in problem_list:
            self.algs.append(NSGAII_EMTIL(params, task, ndim))

        self.class_probability = np.zeros([2, 2])
        self.mu = np.zeros([2, 2, ndim])
        self.sigma = np.ones_like(self.mu)
        self.learned_size = np.zeros_like(self.class_probability)
        
        self.external_size = np.zeros(2)

    def init_pop(self):

        for alg in self.algs:
            alg.init_pop()
            
        self.class_probability = np.zeros([2, 2])
        self.mu = np.zeros_like(self.mu)
        self.sigma = np.ones_like(self.mu)
        self.learned_size = np.zeros_like(self.class_probability)
        
        self.external_size = np.zeros(2)

    def execute(self, max_gen):

        pop_size = self.algs[0].pop["variables"].shape[0]
        inject_pop = [alg.pop["variables"][np.random.permutation(pop_size)[:self.mig_size]] for alg in self.algs]
        
        for alg, inj_pop in zip(self.algs, inject_pop[::-1]):
            alg.migration_gen(inj_pop)
            
        self.learning(inject_pop)

        for g in range(2, max_gen):

            inject_pop = self.get_inject_pop()
            
            for alg, inj_pop in zip(self.algs, inject_pop[::-1]):
                alg.migration_gen(inj_pop)
                
            self.learning(inject_pop)

        return

    def learning(self, injected_pop):

        for i in range(len(self.algs)):
            
            n = injected_pop[0].shape[0]

            NDpop = self.algs[1 - i].pop["variables"][self.algs[1 - i].pop["pareto_rank"] == 0]
            in_front = (NDpop[:, None, :] == injected_pop[i][None, :, :]).min(axis = 2).max(axis = 0)

            pos_n = in_front.sum()
            neg_n = n - pos_n
            
            self.class_probability[i][0] = (self.learned_size[i].sum() * self.class_probability[i][0] + neg_n)\
                                            / (self.learned_size[i].sum() + n)
            
            self.class_probability[i][1] = 1 - self.class_probability[i][0]
            # self.class_probability[i][1] = (self.learned_size[i].sum() * self.class_probability[i][1] + pos_n)\
            #                                 / (self.learned_size[i].sum() + n)

            neg_denom = self.learned_size[i][0] + neg_n
            
            if neg_denom > 0:

                tmp_s0 = ((self.sigma[i][0] + self.mu[i][0]**2) * self.learned_size[i][0] + (injected_pop[i][~in_front].var(axis = 0) + injected_pop[i][~in_front].mean(axis = 0)**2) * neg_n) / neg_denom

                self.mu[i][0] = (self.learned_size[i][0] * self.mu[i][0] + injected_pop[i][~in_front].sum(axis = 0))\
                    / neg_denom
                self.sigma[i][0] = tmp_s0 - self.mu[i][0]**2

            if pos_n > 0:

                target_individual = injected_pop[i][in_front]

            else:

                target_individual = NDpop
                pos_n = target_individual.shape[0]
                                            
            pos_denom = self.learned_size[i][1] + self.external_size[i] + pos_n

            tmp_s1 = ((self.sigma[i][1] + self.mu[i][1]**2) * (self.learned_size[i][1] + self.external_size[i]) + (target_individual.var(axis = 0) + target_individual.mean(axis = 0)**2) * pos_n) / pos_denom

            self.mu[i][1] = ((self.learned_size[i][1] + self.external_size[i]) * self.mu[i][1] + target_individual.sum(axis = 0))\
                / pos_denom
            self.sigma[i][1] = tmp_s1 - self.mu[i][1]**2

            self.learned_size[i][0] += neg_n
            # self.learned_size[i][1] += pos_n
            
            if neg_n == self.mig_size:
                self.external_size[i] += pos_n
                
            else:
                self.learned_size[i][1] += pos_n

        return

    def get_inject_pop(self):

        inject_pop = []
        n,dim = self.algs[0].pop["variables"].shape

        for i in range(len(self.algs)):
            
            conditional_prob = norm_dist(self.algs[i].pop["variables"][:, None, :], self.mu[i][None, :, :], self.sigma[i][None, :, :]).prod(axis = 2)
            label = (conditional_prob * self.class_probability[i]).argmax(axis = 1)

            remain = self.mig_size - (label == 1).sum()
            tmp = np.empty([self.mig_size, dim])

            if remain > 0:

                rand_mig = np.random.permutation(np.arange(n)[label == 0])[:remain]
                tmp[remain:] = self.algs[i].pop["variables"][label == 1]
                tmp[:remain] = self.algs[i].pop["variables"][rand_mig]

            else:

                mig = np.random.permutation(np.arange(n)[label == 1])[:self.mig_size]
                tmp[...] = self.algs[i].pop["variables"][mig]

            rand_mask = np.random.rand(self.mig_size) < self.p
            rand = np.random.rand(*tmp.shape,)[rand_mask] * (self.l * 2) - self.l

            tmp[rand_mask] += rand
            inject_pop.append(tmp)

        return np.clip(inject_pop, 0, 1)