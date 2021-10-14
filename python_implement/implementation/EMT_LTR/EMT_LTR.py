import numpy as np

from scipy.spatial import distance
from scipy.linalg import eig, eigh

from ..MOMFEA import MOMFEA

class EMTLTR(MOMFEA):

    def __init__(self, params, problem_list):

        super().__init__(params, problem_list)

        for p in problem_list:
            p.project_uss = False

        self.lb = [p.lower for p in problem_list]
        self.ub = [p.upper for p in problem_list]
        self.ndim =  [p.ndim for p in self.problems]

        self.pops["variables"] = []
        for i in range(self.ntask):
            self.pops["variables"].append(np.empty([self.npop, self.ndim[i]]))

        self.interval = 10
        if "interval" in params:
            self.interval = params["interval"]

    def init_pop(self):

        for i, p in enumerate(self.problems):

            if self.code == "real":
                self.pops["variables"][i] = np.random.rand(*self.pops["variables"][i].shape,)\
                                            * (self.ub[i] - self.lb[i]) + self.lb[i]
            elif self.code == "bin":
                self.pops["variables"][i] = np.random.randint(2, size = self.pops["variables"][i].shape)

            self.pops["objectives"][i] = p.evaluate(self.pops["variables"][i])
            self._init_eval(i)

        self._set_factorial_rank()
        self.neval = self.npop* self.ntask

        self._LTR()

    def execute(self, max_eval):

        n, mod= divmod(max_eval - self.neval, self.noff * self.ntask)

        offs = {}
        assigned_offs = {}

        parents = np.empty([2, int(self.noff * self.ntask * 0.5), self.to_latent_space[0].shape[1]])
        skill_factor = np.empty(parents.shape[:2], dtype = int)
        p_idx = np.empty_like(skill_factor)

        for gen in range(n):

            if (gen + 2) % self.interval == 0:
                self._LTR()
                parents = np.empty([2, int(self.noff * self.ntask * 0.5), self.to_latent_space[0].shape[1]])

            for t_idx in range(2):

                p_idx[t_idx], skill_factor[t_idx]= self._mfea_selection()
                tmp = [self.pops["variables"][sf][idx] for sf, idx in zip(skill_factor[t_idx], p_idx[t_idx])]
                parents[t_idx] = np.array([*map(lambda p, sf: np.dot(p, self.to_latent_space[sf]), tmp, skill_factor[t_idx])])

            offs["variables"], offs["skill_factor"] = self._mfea_crossover(parents, skill_factor)

            for task_no, p in enumerate(self.problems):

                # assigned_offs["variables"] = np.clip(np.dot(offs["variables"][offs["skill_factor"] == task_no],\
                #                                             self.to_decision_space[task_no]),\
                #                                       self.lb[task_no] ,self.ub[task_no])
                assigned_offs["variables"] = \
                    self.mutation(np.dot(offs["variables"][offs["skill_factor"] == task_no],
                                          self.to_decision_space[task_no]),
                                  lower = self.lb[task_no], upper = self.ub[task_no])

                # assigned_offs["variables"] = \
                #     np.clip(np.dot(self.mutation(offs["variables"][offs["skill_factor"] == task_no],
                #                          lower = self.prj_lb[task_no], upper = self.prj_ub[task_no]),
                #                    self.to_decision_space[task_no]),
                #             self.lb[task_no], self.ub[task_no])
                assigned_offs["objectives"] = p.evaluate(assigned_offs["variables"])

                self._update(assigned_offs, task_no)

            self._set_factorial_rank()

        self.neval = max_eval

        return

    def _mfea_crossover(self, parents, sf):

        offs = parents.copy()

        do_cross = (np.random.rand(*sf[0].shape,) < self.rmp) | (sf[0] == sf[1])
        offs[:, do_cross] = np.split(self.crossover([parents[0][do_cross],
                                                     parents[1][do_cross]]), 2)
        offs = offs.reshape([np.prod(offs.shape[:2]), -1])

        offs_sf = np.vstack([sf[0], sf[1]])

        mask = (np.random.rand(*offs_sf.shape,) < 0.5)[:, do_cross]

        offs_sf[0][do_cross][mask[0]] = sf[1][do_cross][mask[0]]
        offs_sf[1][do_cross][mask[1]] = sf[0][do_cross][mask[1]]

        return offs, offs_sf.reshape(-1)
        return self.mutation(offs, lower = self.uss_boundaries[0], upper = self.uss_boundaries[1]), offs_sf.reshape([-1])

    def _search_boundary(self, M, boundaries):

        self.prj_lb = []
        self.prj_ub = []
        d = M[0].shape[1]

        for m, b in zip(M, boundaries):

            mask = m < 0
            lb_, ub_ = np.repeat(b, d, axis = 1).reshape([2, -1, d])
            lb = lb_ * (~mask) + ub_ * mask
            ub = ub_ * (~mask) + lb_ * mask
            self.prj_lb.append((lb * m).sum(axis = 0))
            self.prj_ub.append((ub * m).sum(axis = 0))

        # return np.min(prj_lb, axis = 0), np.max(prj_ub, axis = 0)

    def _LTR(self):

        sol_class = np.empty([self.ntask, self.npop])
        for i in range(self.ntask):

            is_front = self.pops["pareto_rank"][i] == 0
            sum_obj_front = self.pops["objectives"][i][is_front].sum(axis = 1)
            sol_class[i][is_front] = sum_obj_front > np.median(sum_obj_front)

            sum_obj_no_front = self.pops["objectives"][i][~is_front].sum(axis = 1)
            sol_class[i][~is_front] = 2 + (sum_obj_no_front > np.median(sum_obj_no_front))

        sol_class = sol_class.reshape(-1)
        Z = np.zeros([self.npop * self.ntask, sum(self.ndim)])
        L = np.zeros([self.npop * self.ntask] * 2)

        for i, sol in enumerate(self.pops["variables"]):

            dist = distance.cdist(sol, sol, metric = 'euclidean')
            L[i * self.npop: (i + 1) * self.npop, i * self.npop: (i + 1) * self.npop] = \
                -(w := np.exp(-dist)) + np.eye(self.npop) *w.sum(axis = 1)

            Z[i * self.npop:(i + 1) * self.npop, sum(self.ndim[:i]):sum(self.ndim[:i + 1])] = sol

        Z = Z.T

        Ws = sol_class[:, None] == sol_class[None, :]
        Ds = np.eye(self.npop * self.ntask) * Ws.sum(axis = 1)
        Ls = Ds - Ws

        Wd = ~Ws
        Dd = np.eye(self.npop * self.ntask) * Wd.sum(axis = 1)
        Ld = Dd - Wd

        l_factor = Z @ (L + Ls) @ (Z.T)
        r_factor = Z @ Ld @ Z.T

        sym_l = (tri := np.tril(l_factor)) + tri.T -np.diag(l_factor.diagonal())
        sym_r = (tri := np.tril(r_factor)) + tri.T -np.diag(r_factor.diagonal())

        # if not(np.allclose(l_factor, l_factor.T)) or not(np.allclose(r_factor, r_factor.T)):
        #     print("cannot use eigh")
        #     eig_val, eig_vec = eig(Z @ (L + Ls) @ (Z.T), Z @ Ld @Z.T)

        try:
            # eig_val, eig_vec = eigh((Z.dot(L + Ls)).dot(Z.T), (Z.dot(Ld)).dot(Z.T))
            # eig_val, eig_vec = eigh(sym_l/sym_r.max(), sym_r/sym_r.max())
            eig_val, eig_vec = eigh(sym_l, sym_r)
            eig_vec /= np.linalg.norm(eig_vec, axis = 0)
        except:
            eig_val, eig_vec = eig(sym_l, sym_r)

        eig_idx = eig_val.argsort()
        M = eig_vec[:, eig_idx[np.in1d(eig_idx, eig_val.nonzero())]]
        if type(eig_val[0]) is np.float64:
            M = eig_vec[:, eig_idx[np.in1d(eig_idx, eig_val.nonzero())]]
        else:
            M = np.real(eig_vec[:, eig_idx[np.in1d(eig_idx, np.where(np.logical_and(np.imag(eig_val) == 0, np.real(eig_val) != 0))[0])]])

        self.to_latent_space = np.split(M, np.cumsum(self.ndim)[:-1])
        self.to_decision_space = [np.linalg.pinv(m) for m in self.to_latent_space]

        boundary = [*map(lambda lb, ub: np.vstack([lb, ub]), self.lb, self.ub)]

        self.uss_boundaries = self._search_boundary(self.to_latent_space, boundary)

        return