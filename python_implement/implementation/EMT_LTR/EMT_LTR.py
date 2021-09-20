import numpy as np

from scipy.spatial import distance
from scipy.linalg import eig

from ..MOMFEA import MOMFEA

class EMTLTR(MOMFEA):

    def execute(self, max_eval):

        n, mod= divmod(max_eval - self.neval, self.noff * self.ntask)

        offs = {}
        assigned_offs = {}

        parents = np.empty([2, int(self.noff * self.ntask * 0.5), self.pops["variables"].shape[2]])
        skill_factor = np.empty(parents.shape[:2], dtype = int)
        p_idx = np.empty_like(skill_factor)

        for gen in range(n):

            self._learn_rmp()

            for t_idx in range(2):

                p_idx[t_idx], skill_factor[t_idx]= self._mfea_selection()
                parents[t_idx] = self.pops["variables"][skill_factor[t_idx], p_idx[t_idx]]

            offs["variables"], offs["skill_factor"] = self._mfea_crossover(p_idx, parents, skill_factor)

            for task_no, p in enumerate(self.problems):

                assigned_offs["variables"] = offs["variables"][offs["skill_factor"] == task_no]
                assigned_offs["objectives"] = p.evaluate(assigned_offs["variables"])

                self._update(assigned_offs, task_no)

            self._set_factorial_rank()

        # if mod != 0:

        #     parents = []
        #     parents.append(self.pops["variables"][self.selection()])
        #     parents.append(self.pops["variables"][self.selection()])

        #     offs["variables"] = self.mutation(self.crossover(parents))
        #     offs["objectives"][:mod] = self.problem.evaluate(offs["variables"][:mod])
        #     offs["objectives"][mod:] = 0
        #     self.update(offs)

        self.neval = max_eval

        return

    def _search_boundary(self, M, boundaries):

        prj_lb = []
        prj_ub = []
        d = M[0].shape[1]

        for m, b in zip(M, self.boundaries):

            mask = m < 0
            lb_, ub_ = np.repeat(b, d, axis = 1).reshape([2, -1, d])
            lb = lb_ * (~mask) + ub_ * mask
            ub = ub_ * (~mask) + lb_ * mask
            prj_lb.append((lb * m).sum(axis = 0))
            prj_ub.append((ub * m).sum(axis = 0))

        return np.min(prj_lb, axis = 0), np.min(prj_ub, axis = 0)

    def LTR(self):

        npop = 100
        ntask = 2
        ndim = [10, 15]

        sol1 = np.random.rand(npop, ndim[0])
        sol2 = np.random.rand(npop, ndim[1])
        sol1_class, sol2_class = np.random.randint(4, size = [2, npop])

        Z = np.zeros([npop * ntask, sum(ndim)])
        for i, sol in enumerate(self.pops["variables"]):
            Z[i * npop:(i + 1) * npop, sum(ndim[:i]):sum(ndim[:i + 1])] = sol

        Z = Z.T

        dist_s1 = distance.cdist(sol1, sol1, metric='euclidean')
        w1 = np.exp(-dist_s1)
        d1 = np.eye(npop) * dist_s1.sum(axis = 1)

        dist_s2 = distance.cdist(sol2, sol2, metric='euclidean')
        w2 = np.exp(-dist_s2)
        d2 = np.eye(npop) * dist_s2.sum(axis = 1)

        L = np.zeros([npop * ntask] * 2)
        for i, (d, w) in enumerate(zip([d1, d2], [w1, w2])):
            L[i * npop: (i + 1) * npop, i * npop: (i + 1) * npop] = d - w

        all_sol_class = np.array([*sol1_class, *sol2_class,])
        Ws = all_sol_class[:, None] == all_sol_class[None, :]
        Ds = np.eye(npop * ntask) * Ws.sum(axis = 1)
        Ls = Ds - Ws

        Wd = ~Ws
        Dd = np.eye(npop * ntask) * Wd.sum(axis = 1)
        Ld = Dd - Wd

        eig_val, eig_vec = eig((Z.dot((L + Ls))).dot(Z.T), (Z.dot(Ld)).dot(Z.T))

        eig_idx = eig_val.argsort()
        M = eig_vec[:, eig_idx[np.in1d(eig_idx, eig_val.nonzero())]]

        M = eig_vec[eig_idx]
        to_latent_space = np.split(M, np.cumsum(ndim)[:-1])
        to_decision_space = [np.linalg.pinv(m) for m in to_latent_space]

        boundary0 = np.array([[0] + [-100] * 9, [1] + [100]*9])
        boundary1 = np.array([[0] + [-50] * 14, [1] + [50]*14])

        out = search_boundary(to_latent_space, [boundary0, boundary1])