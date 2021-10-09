# This is a three-objective version of the two bar truss design problem
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


class RE31(RE_base):

    def __init__(self):

        super().__init__()

        self.problem_name = 'Two bar truss design'
        self.set_IGD_ref("RE31")
        self.n_objectives = 3
        self.ndim = 3
        self.n_constraints = 0
        self.n_original_constraints = 3

        self.lower = np.empty(self.ndim)
        self.lower[[0, 1]] = 0.00001
        self.lower[2] = 1.0

        self.upper = np.empty(self.ndim)
        self.upper[[0, 1]] = 100.0
        self.upper[2] = 3.0

    def evaluate(self, pop, eps=1e-7):

        x = self.reverse_projection(pop)

        f = np.zeros([self.n_objectives, x.shape[0]])
        g = np.zeros([self.n_original_constraints, x.shape[0]])

        x1, x2, x3 = x.T

        # First original objective function
        f[0] = x1 * np.sqrt(16.0 + x3**2) + x2 * np.sqrt(1.0 + x3**2)
        # Second original objective function
        f[1] = (20.0 * np.sqrt(16.0 + x3**2)) / (x1 * x3 + eps)

        # Constraint functions
        g[0] = 0.1 - f[0]
        g[1] = 100000.0 - f[1]
        g[2] = 100000 - ((80.0 * np.sqrt(1.0 + x3**2)) / (x3 * x2 + eps))
        g = np.where(g < 0, -g, 0)
        f[2] = g.sum(axis=0)

        return f.T
