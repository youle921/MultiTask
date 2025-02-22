# This is the four objective version of the car side impact design problem
#
# Reference:
# Himanshu Jain, Kalyanmoy Deb: An Evolutionary Many-Objective Optimization Algorithm Using Reference-Point Based Nondominated Sorting Approach, Part II: Handling Constraints and Extending to an Adaptive Approach. IEEE Trans. Evolutionary Computation 18(4): 602-622 (2014)
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


class RE41(RE_base):

    def __init__(self):

        super().__init__()

        self.problem_name = 'Car side impact design'

        self.n_objectives = 4
        self.ndim = 7
        self.n_constraints = 0
        self.n_original_constraints = 10

        self.set_IGD_ref("RE41")
        self.set_HV_ref("RE41")

        self.lower = np.empty(self.ndim)
        self.lower[[0, 2, 3]] = 0.5
        self.lower[1] = 0.45
        self.lower[4] = 0.875
        self.lower[[5, 6]] = 0.4

        self.upper = np.empty(self.ndim)
        self.upper[[0, 2, 3]] = 1.5
        self.upper[1] = 1.35
        self.upper[4] = 2.625
        self.upper[[5, 6]] = 1.2

    def evaluate(self, pop):

        x = self.reverse_projection(pop)

        f = np.zeros([self.n_objectives, x.shape[0]])
        g = np.zeros([self.n_original_constraints, x.shape[0]])

        x1, x2, x3, x4, x5, x6, x7 = x.T

        # First original objective function
        f[0] = 1.98 + 4.9 * x1 + 6.67 * x2 + 6.98 * x3 + \
            4.01 * x4 + 1.78 * x5 + 0.00001 * x6 + 2.73 * x7
        # Second original objective function
        f[1] = 4.72 - 0.5 * x4 - 0.19 * x2 * x3
        # Third original objective function
        Vmbp = 10.58 - 0.674 * x1 * x2 - 0.67275 * x2
        Vfd = 16.45 - 0.489 * x3 * x7 - 0.843 * x5 * x6
        f[2] = 0.5 * (Vmbp + Vfd)

        # Constraint functions
        g[0] = 1 - (1.16 - 0.3717 * x2 * x4 - 0.0092928 * x3)
        g[1] = 0.32 - (0.261 - 0.0159 * x1 * x2 - 0.06486 * x1 -
                       0.019 * x2 * x7 + 0.0144 * x3 * x5 + 0.0154464 * x6)
        g[2] = 0.32 - (0.214 + 0.00817 * x5 - 0.045195 * x1 - 0.0135168 * x1 + 0.03099 * x2 *
                       x6 - 0.018 * x2 * x7 + 0.007176 * x3 + 0.023232 * x3 - 0.00364 * x5 * x6 - 0.018 * x2**2)
        g[3] = 0.32 - (0.74 - 0.61 * x2 - 0.031296 *
                       x3 - 0.031872 * x7 + 0.227 * x2**2)
        g[4] = 32 - (28.98 + 3.818 * x3 - 4.2 * x1 *
                     x2 + 1.27296 * x6 - 2.68065 * x7)
        g[5] = 32 - (33.86 + 2.95 * x3 - 5.057 * x1 * x2 -
                     3.795 * x2 - 3.4431 * x7 + 1.45728)
        g[6] = 32 - (46.36 - 9.9 * x2 - 4.4505 * x1)
        g[7] = 4 - f[1]
        g[8] = 9.9 - Vmbp
        g[9] = 15.7 - Vfd

        g = np.where(g < 0, -g, 0)
        f[3] = g.sum(axis=0)

        return f.T
