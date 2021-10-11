# This is a two-objective version of the hatch cover design problem.
#
# Reference:
# H. M. Amir and T. Hasegawa, "Nonlinear Mixed-Discrete Structural Optimization," J. Struct. Eng., vol. 115, no. 3, pp. 626-646, 1989.
#
#  Copyright (c) 2018 Ryoji Tanabe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from .RE_base import RE_base


class RE24(RE_base):

    def __init__(self):

        super().__init__()

        self.problem_name = 'Hatch cover design'
        self.set_IGD_ref("RE24")
        self.set_HV_ref("RE24")
        self.n_objectives = 2
        self.ndim = 2
        self.n_constraints = 0
        self.n_original_constraints = 4

        self.lower = np.full(self.ndim, 0.5)

        self.upper = np.empty(self.ndim)
        self.upper[0] = 4
        self.upper[1] = 50

    def evaluate(self, pop, eps=1e-7):

        x = self.reverse_projection(pop)

        f = np.zeros([self.n_objectives, x.shape[0]])
        g = np.zeros([self.n_original_constraints, x.shape[0]])

        x1, x2 = x.T

        # First original objective function
        f[0] = x1 + (120 * x2)

        E = 700000
        sigma_b_max = 700
        tau_max = 450
        delta_max = 1.5
        sigma_k = (E * x1**2) / 100
        sigma_b = 4500 / (x1 * x2 + eps)
        tau = 1800 / (x2 + eps)
        delta = (56.2 * 10000) / (E * x1 * x2**2 + eps)

        g[0] = 1 - (sigma_b / sigma_b_max)
        g[1] = 1 - (tau / tau_max)
        g[2] = 1 - (delta / delta_max)
        g[3] = 1 - (sigma_b / sigma_k + eps)
        g = np.where(g < 0, -g, 0)
        f[1] = g.sum(axis=0)

        return f.T
