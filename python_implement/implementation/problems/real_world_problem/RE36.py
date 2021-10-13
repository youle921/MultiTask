# This is a three objective version of the gear train design problem.
#
# Reference:
# Kalyanmoy Deb and Aravind Srinivasan, "Innovization: Innovative Design Principles Through Optimization," KanGAL Report Number 2005007, Indian Institute of Technology Kanpur (2005).
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


class RE36(RE_base):

    def __init__(self):

        super().__init__()

        self.problem_name = 'Gear train design'

        self.n_objectives = 3
        self.ndim = 4
        self.n_constraints = 0
        self.n_original_constraints = 1

        self.set_IGD_ref("RE36")
        self.set_HV_ref("RE36")

        self.lower = np.full(self.ndim, 12)
        self.upper = np.full(self.ndim, 60)

    def evaluate(self, pop):

        x = self.reverse_projection(pop)

        f = np.zeros([self.n_objectives, x.shape[0]])
        g = np.zeros([self.n_original_constraints, x.shape[0]])

        # all the four variables must be inverger values
        x1, x2, x3, x4 = np.round(x.T)

        # First original objective function
        f[0] = np.abs(6.931 - ((x3 / x1) * (x4 / x2)))
        # Second original objective function (the maximum value among the four variables)
        f[1] = np.max([x1, x2, x3, x4], axis=0)

        g[0] = 0.5 - (f[0] / 6.931)
        g = np.where(g < 0, -g, 0)
        f[2] = g[0]

        return f.T
