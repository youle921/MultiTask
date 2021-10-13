# Note: this is a revised version of the file downloaded from Dr. Miqing Li's web site (http://www.cs.bham.ac.uk/~limx/)
#
# This is the nine objective version of the car cab design problem
#
# Reference:
# K. Deb and H. Jain, "An evolutionary many-objective optimization algorithm using reference-point-based nondominated sorting approach, part I: solving problems with box constraints," IEEE TEVC, vol. 18, no. 4, pp. 577-601, 2014

import numpy as np
from .RE_base import RE_base


class RE91(RE_base):

    def __init__(self):

        super().__init__()

        self.problem_name = 'Car cab design'

        self.n_objectives = 9
        self.ndim = 7
        self.n_constraints = 0
        self.n_original_constraints = 0

        self.set_IGD_ref("RE91")
        self.set_HV_ref("RE91")

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

        x1, x2, x3, x4, x5, x6, x7 = x.T

        # stochastic variables
        x8 = 0.006 * (np.random.randn(x.shape[0])) + 0.345
        x9 = 0.006 * (np.random.randn(x.shape[0])) + 0.192
        x10 = 10 * (np.random.randn(x.shape[0]))
        x11 = 10 * (np.random.randn(x.shape[0]))

        # First function
        f[0] = 1.98 + 4.9 * x1 + 6.67 * x2 + 6.98 * x3 \
            + 4.01 * x4 + 1.75 * x5 + 0.00001 * x6 + 2.73 * x7
        # Second function
        f[1] = np.clip(1.16 - 0.3717 * x2 * x4 - 0.00931 * x2 *
                       x10 - 0.484 * x3 * x9 + 0.01343 * x6 * x10, 0, None)
        # Third function
        f[2] = np.clip((0.261 - 0.0159 * x1 * x2 - 0.188 * x1 * x8 - 0.019 * x2 * x7 + 0.0144 * x3 * x5 +
                        0.87570001 * x5 * x10 + 0.08045 * x6 * x9 + 0.00139 * x8 * x11 + 0.00001575 * x10 * x11)/0.32, 0, None)
        # Fourth function
        f[3] = np.clip((0.214 + 0.00817 * x5 - 0.131 * x1 * x8 - 0.0704 * x1 * x9 + 0.03099 * x2 * x6 - 0.018 * x2 * x7 + 0.0208 * x3 * x8 + 0.121 * x3 *
                        x9 - 0.00364 * x5 * x6 + 0.0007715 * x5 * x10 - 0.0005354 * x6 * x10 + 0.00121 * x8 * x11 + 0.00184 * x9 * x10 - 0.018 * x2**2)/0.32, 0, None)
        # Fifth function
        f[4] = np.clip((0.74 - 0.61 * x2 - 0.163 * x3 * x8 + 0.001232 *
                        x3 * x10 - 0.166 * x7 * x9 + 0.227 * x2**2)/0.32, 0, None)
        # Sixth function
        tmp = ((28.98 + 3.818 * x3 - 4.2 * x1 * x2 + 0.0207 * x5 * x10 + 6.63 * x6 * x9 - 7.77 * x7 * x8 + 0.32 * x9 * x10) + (33.86 + 2.95 * x3 + 0.1792 *
                                                                                                                               x10 - 5.057 * x1 * x2 - 11 * x2 * x8 - 0.0215 * x5 * x10 - 9.98 * x7 * x8 + 22 * x8 * x9) + (46.36 - 9.9 * x2 - 12.9 * x1 * x8 + 0.1107 * x3 * x10))/3
        f[5] = np.clip(tmp/32, 0, None)
        # Seventh function
        f[6] = np.clip((4.72 - 0.5 * x4 - 0.19 * x2 * x3 - 0.0122 * x4 *
                        x10 + 0.009325 * x6 * x10 + 0.000191 * x11**2)/4.0, 0, None)
        # Eighth function
        f[7] = np.clip((10.58 - 0.674 * x1 * x2 - 1.95 * x2 * x8 + 0.02054 *
                        x3 * x10 - 0.0198 * x4 * x10 + 0.028 * x6 * x10)/9.9, 0, None)
        # Ninth function
        f[8] = np.clip((16.45 - 0.489 * x3 * x7 - 0.843 * x5 * x6 + 0.0432 *
                        x9 * x10 - 0.0556 * x9 * x11 - 0.000786 * x11**2)/15.7, 0, None)

        return f.T
