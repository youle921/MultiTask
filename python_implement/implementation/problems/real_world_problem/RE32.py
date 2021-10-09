# This is a three-objective version of the disc brake design prolem
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


class RE32(RE_base):

    def __init__(self):

        super().__init__()

        self.problem_name = 'Welded beam design'
        self.set_reference_point("RE32")
        self.n_objectives = 3
        self.ndim = 4
        self.n_constraints = 0
        self.n_original_constraints = 4

        self.lower = np.empty(self.ndim)
        self.lower[[0, 3]] = 0.125
        self.lower[[1, 2]] = 0.1

        self.upper = np.empty(self.ndim)
        self.upper[[0, 3]] = 5.0
        self.upper[[1, 2]] = 10.0

    def evaluate(self, pop, eps=1e-7):

        x = self.reverse_projection(pop)

        f = np.zeros([self.n_objectives, x.shape[0]])
        g = np.zeros([self.n_original_constraints, x.shape[0]])

        x1, x2, x3, x4 = x.T

        P = 6000
        L = 14
        E = 30 * 1e6

        # // deltaMax = 0.25
        G = 12 * 1e6
        tauMax = 13600
        sigmaMax = 30000

        # First original objective function
        f[0] = (1.10471 * x1**2 * x2) + (0.04811 * x3 * x4) * (14.0 + x2)
        # Second original objective function
        f[1] = (4 * P * L**3) / (E * x4 * x3**3 + eps)

        # Constraint functions
        M = P * (L + (x2 / 2))
        tmpVar = (x2**2 / 4.0) + ((x1 + x3) / 2.0)**2
        R = np.sqrt(tmpVar)
        tmpVar = (x2**2 / 12.0) + ((x1 + x3) / 2.0)**2
        J = 2 * np.sqrt(2) * x1 * x2 * tmpVar

        tauDashDash = (M * R) / (J + eps)
        tauDash = P / (np.sqrt(2) * x1 * x2 + eps)
        tmpVar = tauDash**2 + \
            ((2 * tauDash * tauDashDash * x2) / (2 * R + eps)) + tauDashDash**2
        tau = np.sqrt(tmpVar)
        sigma = (6 * P * L) / (x4 * x3**2 + eps)
        tmpVar = 4.013 * E * np.sqrt((x3**2 * x4**6) / 36.0) / L**2
        tmpVar2 = (x3 / (2 * L)) * np.sqrt(E / (4 * G))
        PC = tmpVar * (1 - tmpVar2)

        g[0] = tauMax - tau
        g[1] = sigmaMax - sigma
        g[2] = x4 - x1
        g[3] = PC - P
        g = np.where(g < 0, -g, 0)
        f[2] = g.sum(axis=0)

        return f.T
