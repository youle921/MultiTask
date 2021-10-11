# This is a two-objective version of the reinforced concrete beam design problem.
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


class RE21(RE_base):

    def __init__(self):

        super().__init__()

        self.problem_name = 'Four bar truss design'
        self.set_IGD_ref("RE21")
        self.set_HV_ref("RE21")

        self.n_objectives = 2
        self.ndim = 4

        F = 10.0
        sigma = 10.0
        tmp_val = F / sigma

        self.upper = np.full(self.ndim, 3 * tmp_val)

        self.lower = np.empty(self.ndim)
        self.lower[[0, 3]] = tmp_val
        self.lower[[1, 2]] = np.sqrt(2.0) * tmp_val

    def evaluate(self, pop, eps=1e-7):

        x = self.reverse_projection(pop)

        f = np.zeros([self.n_objectives, x.shape[0]])

        x1, x2, x3, x4 = x.T

        F = 10.0
        E = 2.0 * 1e5
        L = 200.0

        f[0] = L * ((2 * x1) + np.sqrt(2.0) * x2 + np.sqrt(x3) + x4)
        f[1] = ((F * L) / E) * ((2.0 / (x1 + eps)) + (2.0 * np.sqrt(2.0) /
                                                      (x2 + eps)) - (2.0 * np.sqrt(2.0) / (x3 + eps)) + (2.0 / (x4 + eps)))

        return f.T
