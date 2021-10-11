# This is a two-objective version of the pressure vessel design problem.
#
# Reference:
# B. K. Kannan and S. N. Kramer, "An Augmented Lagrange Multiplier Based Method for Mixed Integer Discrete Continuous Optimization and Its Applications to Mechanical Design, Journal of Mechanical Design, vol. 116, no. 2, pp. 405-411, 1994.
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


class RE23(RE_base):

    def __init__(self):

        super().__init__()

        self.problem_name = 'Pressure vessel design'
        self.set_IGD_ref("RE23")
        self.set_HV_ref("RE23")
        self.n_objectives = 2
        self.ndim = 4
        self.n_constraints = 0
        self.n_original_constraints = 3

        self.lower = np.empty(self.ndim)
        self.lower[[0, 1]] = 1
        self.lower[[2, 3]] = 10

        self.upper = np.full(self.ndim, 100)

    def evaluate(self, pop):

        x = self.reverse_projection(pop)

        f = np.zeros([self.n_objectives, x.shape[0]])
        g = np.zeros([self.n_original_constraints, x.shape[0]])

        x1 = 0.0625 * np.round(x[:, 0])
        x2 = 0.0625 * np.round(x[:, 1])
        x3, x4 = x.T[2:]

        # First original objective function
        f[0] = (0.6224 * x1 * x3 * x4) + (1.7781 * x2 * x3**2)\
            + (3.1661 * x1**2 * x4) + (19.84 * x1**2 * x3)

        # Original constraint functions
        g[0] = x1 - (0.0193 * x3)
        g[1] = x2 - (0.00954 * x3)
        g[2] = (np.pi * x3**2 * x4) + ((4.0/3.0) * (np.pi * x3**3)) - 1296000
        g = np.where(g < 0, -g, 0)
        f[1] = g.sum(axis=0)

        return f.T
