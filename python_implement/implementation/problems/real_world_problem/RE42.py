# This is the four objective version of the conceptual marine design
#
# Reference:
#  M. G. Parsons and R. L. Scott, "Formulation of Multicriterion Design Optimization Problems for Solution With Scalar Numerical Optimization Methods," J. Ship Research, vol. 48, no. 1, pp. 61-76, 2004.
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

class RE42(RE_base):

    def __init__(self):

        super().__init__()

        self.problem_name = 'Conceptual marine design'

        self.n_objectives = 4
        self.ndim = 6
        self.n_constraints = 0
        self.n_original_constraints = 9

        self.set_IGD_ref("RE42")
        self.set_HV_ref("RE42")

        self.lower = np.empty(self.ndim)
        self.lower[0] = 150.0
        self.lower[1] = 20.0
        self.lower[2] = 13.0
        self.lower[3] = 10.0
        self.lower[4] = 14.0
        self.lower[5] = 0.63

        self.upper = np.empty(self.ndim)
        self.upper[0] = 274.32
        self.upper[1] = 32.31
        self.upper[2] = 25.0
        self.upper[3] = 11.71
        self.upper[4] = 18.0
        self.upper[5] = 0.75

    def evaluate(self, pop):

        x = self.reverse_projection(pop)

        f = np.zeros([self.n_objectives, x.shape[0]])
        # NOT g
        constraintFuncs = np.zeros([self.n_original_constraints, x.shape[0]])

        x_L, x_B,x_D,x_T, x_Vk, x_CB = x.T

        displacement = 1.025 * x_L * x_B * x_T * x_CB
        V = 0.5144 * x_Vk
        g = 9.8065
        Fn = V / (g * x_L)**0.5
        a = (4977.06 * x_CB**2) - (8105.61 * x_CB) + 4456.51
        b = (-10847.2 * x_CB**2) + (12817.0 * x_CB) - 6960.32

        power = (displacement**(2.0/3.0) * x_Vk**3) / (a + (b * Fn))
        outfit_weight = 1.0 * x_L**0.8 * x_B**0.6 * x_D**0.3 * x_CB**0.1
        steel_weight = 0.034 * x_L**1.7 * x_B**0.7 * x_D**0.4 * x_CB**0.5
        machinery_weight = 0.17 * power**0.9
        light_ship_weight = steel_weight + outfit_weight + machinery_weight

        ship_cost = 1.3 * ((2000.0 * steel_weight**0.85) +
                           (3500.0 * outfit_weight) + (2400.0 * power**0.8))
        capital_costs = 0.2 * ship_cost

        DWT = displacement - light_ship_weight

        running_costs = 40000.0 * DWT**0.3

        round_trip_miles = 5000.0
        sea_days = (round_trip_miles / 24.0) * x_Vk
        handling_rate = 8000.0

        daily_consumption = ((0.19 * power * 24.0) / 1000.0) + 0.2
        fuel_price = 100.0
        fuel_cost = 1.05 * daily_consumption * sea_days * fuel_price
        port_cost = 6.3 * DWT**0.8

        fuel_carried = daily_consumption * (sea_days + 5.0)
        miscellaneous_DWT = 2.0 * DWT**0.5

        cargo_DWT = DWT - fuel_carried - miscellaneous_DWT
        port_days = 2.0 * ((cargo_DWT / handling_rate) + 0.5)
        RTPA = 350.0 / (sea_days + port_days)

        voyage_costs = (fuel_cost + port_cost) * RTPA
        annual_costs = capital_costs + running_costs + voyage_costs
        annual_cargo = cargo_DWT * RTPA

        f[0] = annual_costs / annual_cargo
        f[1] = light_ship_weight
        # f_2 is dealt as a minimization problem
        f[2] = -annual_cargo

        # Reformulated objective functions
        constraintFuncs[0] = x_L / x_B - 6.0
        constraintFuncs[1] = -(x_L / x_D) + 15.0
        constraintFuncs[2] = -(x_L / x_T) + 19.0
        constraintFuncs[3] = 0.45 * DWT**0.31 - x_T
        constraintFuncs[4] = 0.7 * x_D + 0.7 - x_T
        constraintFuncs[5] = 500000.0 - DWT
        constraintFuncs[6] = DWT - 3000.0
        constraintFuncs[7] = 0.32 - Fn

        KB = 0.53 * x_T
        BMT = ((0.085 * x_CB - 0.002) * x_B**2) / (x_T * x_CB)
        KG = 1.0 + 0.52 * x_D
        constraintFuncs[8] = (KB + BMT - KG) - (0.07 * x_B)

        constraintFuncs = np.where(constraintFuncs < 0, -constraintFuncs, 0)
        f[3] = constraintFuncs.sum(axis=0)

        return f.T