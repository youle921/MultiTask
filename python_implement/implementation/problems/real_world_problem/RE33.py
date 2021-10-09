# This is a three-objective version of the disc brake design problem
#
# Reference:
#  T. Ray and K. M. Liew, "A swarm metaphor for multiobjective design optimization," Eng. opt., vol. 34, no. 2, pp. 141–153, 2002.
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


class RE33(RE_base):

    def __init__(self):

        super().__init__()

        self.problem_name = 'Disc breke design'
        self.set_IGD_ref("RE33")
        self.n_objectives = 3
        self.ndim = 4
        self.n_constraints = 0
        self.n_original_constraints = 4

        self.lower = np.empty(self.ndim)
        self.lower[0] = 55
        self.lower[1] = 75
        self.lower[2] = 1000
        self.lower[3] = 11

        self.upper = np.empty(self.ndim)
        self.upper[0] = 80
        self.upper[1] = 110
        self.upper[2] = 3000
        self.upper[3] = 20

    def evaluate(self, pop, eps=1e-7):

        x = self.reverse_projection(pop)

        f = np.zeros([self.n_objectives, x.shape[0]])
        g = np.zeros([self.n_original_constraints, x.shape[0]])

        x1, x2, x3, x4 = x.T

        # First original objective function
        f[0] = 4.9 * 1e-5 * (x2**2 - x1**2) * (x4 - 1.0)
        # Second original objective function
        f[1] = ((9.82 * 1e6) * (x2**2 - x1**2)) / \
            (x3 * x4 * (x2**3 - x1**3) + eps)

        # Reformulated objective functions
        g[0] = (x2 - x1) - 20.0
        g[1] = 0.4 - (x3 / (3.14 * (x2**2 - x1**2) + eps))
        g[2] = 1.0 - (2.22 * 1e-3 * x3 * (x2**3 - x1**3))\
            / ((x2**2 - x1**2)**2 + eps)
        g[3] = (2.66 * 1e-2 * x3 * x4 * (x2**3 - x1**3))\
            / (x2**2 - x1**2 + eps) - 900.0
        g = np.where(g < 0, -g, 0)
        f[2] = g.sum(axis=0)

        return f.T
