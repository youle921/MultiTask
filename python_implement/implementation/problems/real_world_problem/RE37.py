# This is the rocket injector design problem.
#
# Reference:
# R. Vaidyanathan, K. Tucker, N. Papila, W. Shyy, CFD-Based Design Optimization For Single Element Rocket Injector, in: AIAA Aerospace Sciences Meeting, 2003, pp. 1-21
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


class RE37(RE_base):

    def __init__(self):

        super().__init__()

        self.problem_name = 'Rocket injector design'
        self.set_IGD_ref("RE37")
        self.n_objectives = 3
        self.ndim = 4
        self.n_constraints = 0
        self.n_original_constraints = 0

        self.lower = np.full(self.ndim, 0)
        self.upper = np.full(self.ndim, 1)

    def evaluate(self, pop):

        x = self.reverse_projection(pop)

        f = np.zeros([self.n_objectives, x.shape[0]])

        xAlpha, xHA, xOA, xOPTT = x.T

        # f1 (TF_max)
        f[0] = 0.692 + (0.477 * xAlpha) - (0.687 * xHA) - (0.080 * xOA) - (0.0650 * xOPTT) - (0.167 * xAlpha**2) - (0.0129 * xHA * xAlpha) + (0.0796 * xHA**2) - (0.0634 *
                                                                                                                                                                  xOA * xAlpha) - (0.0257 * xOA * xHA) + (0.0877 * xOA**2) - (0.0521 * xOPTT * xAlpha) + (0.00156 * xOPTT * xHA) + (0.00198 * xOPTT * xOA) + (0.0184 * xOPTT**2)
        # f2 (X_cc)
        f[1] = 0.153 - (0.322 * xAlpha) + (0.396 * xHA) + (0.424 * xOA) + (0.0226 * xOPTT) + (0.175 * xAlpha**2) + (0.0185 * xHA * xAlpha) - (0.0701 * xHA**2) - (
            0.251 * xOA * xAlpha) + (0.179 * xOA * xHA) + (0.0150 * xOA**2) + (0.0134 * xOPTT * xAlpha) + (0.0296 * xOPTT * xHA) + (0.0752 * xOPTT * xOA) + (0.0192 * xOPTT**2)
        # f3 (TT_max)
        f[2] = 0.370 - (0.205 * xAlpha) + (0.0307 * xHA) + (0.108 * xOA) + (1.019 * xOPTT) - (0.135 * xAlpha**2) + (0.0141 * xHA * xAlpha) + (0.0998 * xHA**2) + (0.208 * xOA * xAlpha) - (0.0301 * xOA * xHA) - (0.226 * xOA**2) + (0.353 * xOPTT * xAlpha) - \
            (0.0497 * xOPTT * xOA) - (0.423 * xOPTT**2) + (0.202 * xHA * xAlpha**2) - (0.281 * xOA * xAlpha**2) - (0.342 * xHA**2 *
                                                                                                                   xAlpha) - (0.245 * xHA**2 * xOA) + (0.281 * xOA**2 * xHA) - (0.184 * xOPTT**2 * xAlpha) - (0.281 * xHA * xAlpha * xOA)

        return f.T
