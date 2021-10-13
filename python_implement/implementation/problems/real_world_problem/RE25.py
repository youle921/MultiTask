# This is a two-objective version of the coil compression spring design problem.
#
# Reference:
# J. Lampinen and I. Zelinka, "Mixed integer-discrete-continuous optimization by differential evolution, part 2: a practical example," in International Conference on Soft Computing, 1999, pp. 77-81.
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


class RE25(RE_base):

    def __init__(self):

        super().__init__()

        self.problem_name = 'Coil compression spring design'

        self.n_objectives = 2
        self.ndim = 3
        self.n_constraints = 0
        self.n_original_constraints = 6

        self.set_IGD_ref("RE25")
        self.set_HV_ref("RE25")

        self.lower = np.empty(self.ndim)
        self.lower[0] = 1
        self.lower[1] = 0.6
        self.lower[2] = 0.09

        self.upper = np.empty(self.ndim)
        self.upper[0] = 70
        self.upper[1] = 3
        self.upper[2] = 0.5

        self.feasible_vals = np.array([0.009, 0.0095, 0.0104, 0.0118, 0.0128, 0.0132, 0.014, 0.015, 0.0162, 0.0173, 0.018, 0.02, 0.023, 0.025, 0.028, 0.032, 0.035, 0.041, 0.047,
                                       0.054, 0.063, 0.072, 0.08, 0.092, 0.105, 0.12, 0.135, 0.148, 0.162, 0.177, 0.192, 0.207, 0.225, 0.244, 0.263, 0.283, 0.307, 0.331, 0.362, 0.394, 0.4375, 0.5])

    def evaluate(self, pop):

        x = self.reverse_projection(pop)

        f = np.zeros([self.n_objectives, x.shape[0]])
        g = np.zeros([self.n_original_constraints, x.shape[0]])

        x1 = np.round(x[:, 0])
        x2 = x[:, 1]
        idx = np.abs(self.feasible_vals[:, None] - x[:, 2]).argmin(axis=0)
        x3 = self.feasible_vals[idx]

        # first original objective function
        f[0] = (np.pi**2 * x2 * x3**2 * (x1 + 2)) / 4.0

        # constraint functions
        Cf = ((4.0 * (x2 / x3) - 1) /
              (4.0 * (x2 / x3) - 4)) + (0.615 * x3 / x2)
        Fmax = 1000.0
        S = 189000.0
        G = 11.5 * 1e+6
        K = (G * x3**4) / (8 * x1 * x2**3)
        lmax = 14.0
        lf = (Fmax / K) + 1.05 * (x1 + 2) * x3
        # dmin = 0.2
        # Dmax = 3
        Fp = 300.0
        sigmaP = Fp / K
        sigmaPM = 6
        sigmaW = 1.25

        g[0] = -((8 * Cf * Fmax * x2) / (np.pi * x3**3)) + S
        g[1] = -lf + lmax
        g[2] = -3 + (x2 / x3)
        g[3] = -sigmaP + sigmaPM
        g[4] = -sigmaP - ((Fmax - Fp) / K) - 1.05 * (x1 + 2) * x3 + lf
        g[5] = sigmaW - ((Fmax - Fp) / K)

        g = np.where(g < 0, -g, 0)
        f[1] = g.sum(axis=0)

        return f.T
