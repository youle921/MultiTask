# This is a three-objective version of the speed reducer design problem.
#
# Reference:
#  C. A. C. Coello and G. T. Pulido, "Multiobjective structural optimization using a microgenetic algorithm," Stru. and Multi. Opt., vol. 30, no. 5, pp. 388-403, 2005.
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


class RE35(RE_base):

    def __init__(self):

        super().__init__()

        self.problem_name = 'Speed reducer design'

        self.n_objectives = 3
        self.ndim = 7
        self.n_constraints = 0
        self.n_original_constraints = 11

        self.set_IGD_ref("RE35")
        self.set_HV_ref("RE35")

        self.lower = np.empty(self.ndim)
        self.lower[0] = 2.6
        self.lower[1] = 0.7
        self.lower[2] = 17
        self.lower[[3, 4]] = 7.3
        self.lower[5] = 2.9
        self.lower[6] = 5.0

        self.upper = np.empty(self.ndim)
        self.upper[0] = 3.6
        self.upper[1] = 0.8
        self.upper[2] = 28
        self.upper[[3, 4]] = 8.3
        self.upper[5] = 3.9
        self.upper[6] = 5.5

    def evaluate(self, pop):

        x = self.reverse_projection(pop)

        f = np.zeros([self.n_objectives, x.shape[0]])
        g = np.zeros([self.n_original_constraints, x.shape[0]])

        x1, x2, x3, x4, x5, x6, x7 = x.T
        x3 = np.round(x3)

        # First original objective function (weight)
        f[0] = 0.7854 * x1 * x2**2 * (((10.0 * x3**2) / 3.0) + (14.933 * x3) - 43.0934) - 1.508 * x1 * (
            x6**2 + x7**2) + 7.477 * (x6**3 + x7**3) + 0.7854 * (x4 * x6**2 + x5 * x7**2)

        # Second original objective function (stress)
        tmpVar = ((745.0 * x4) / (x2 * x3))**2.0 + 1.69 * 1e7
        f[1] = np.sqrt(tmpVar) / (0.1 * x6**3)

        # Constraint functions
        g[0] = -(1.0 / (x1 * x2**2 * x3)) + 1.0 / 27.0
        g[1] = -(1.0 / (x1 * x2**2 * x3**2)) + 1.0 / 397.5
        g[2] = -x4**3 / (x2 * x3 * x6**4) + 1.0 / 1.93
        g[3] = -(x5**3) / (x2 * x3 * x7**4) + 1.0 / 1.93
        g[4] = -(x2 * x3) + 40.0
        g[5] = -(x1 / (x2 )) + 12.0
        g[6] = -5.0 + x1 / x2
        g[7] = -1.9 + x4 - 1.5 * x6
        g[8] = -1.9 + x5 - 1.1 * x7
        g[9] = -f[1] + 1300.0
        tmpVar = ((745.0 * x5) / (x2 * x3))**2.0 + 1.575 * 1e8
        g[10] = -np.sqrt(tmpVar) / (0.1 * x7**3) + 1100.0
        g = np.where(g < 0, -g, 0)
        f[2] = g.sum(axis=0)

        return f.T
