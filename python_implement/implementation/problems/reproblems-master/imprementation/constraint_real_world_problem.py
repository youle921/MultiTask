#!/usr/bin/env python
"""
  A real-world multi-objective problem suite (the RE benchmark set)
  Reference:
  Ryoji Tanabe, Hisao Ishibuchi, "An Easy-to-use Real-world Multi-objective Problem Suite" Applied Soft Computing. 89: 106078 (2020)
   Copyright (c) 2020 Ryoji Tanabe

  I re-implemented the RE problem set by referring to its C source code (reproblem.c). While variables directly copied from the C source code are written in CamelCase, the other variables are written in snake_case. It is somewhat awkward.

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import numpy as np

class CRE21():

    def __init__(self):

        self.problem_name = 'CRE21'
        self.n_objectives = 2
        self.ndim = 3
        self.n_constraints = 3

        self.upper = np.zeros(self.ndim)
        self.lower = np.zeros(self.ndim)
        self.lower[0] = 0.00001
        self.lower[1] = 0.00001
        self.lower[2] = 1.0
        self.upper[0] = 100.0
        self.upper[1] = 100.0
        self.upper[2] = 3.0

    def evaluate(self, x):
        f = np.zeros(x.shape[0], self.n_objectives)
        g = np.zeros(self.n_constraints)

        x1 = x[0]
        x2 = x[1]
        x3 = x[2]

        # First original objective function
        f[0] = x1 * np.sqrt(16.0 + (x3 * x3)) + x2 * np.sqrt(1.0 + x3 * x3)
        # Second original objective function
        f[1] = (20.0 * np.sqrt(16.0 + (x3 * x3))) / (x1 * x3)

        # Constraint functions
        g[0] = 0.1 - f[0]
        g[1] = 100000.0 - f[1]
        g[2] = 100000 - ((80.0 * np.sqrt(1.0 + x3 * x3)) / (x3 * x2))
        g = np.where(g < 0, -g, 0)

        return f, g

class CRE22():
    def __init__(self):
        self.problem_name = 'CRE22'
        self.n_objectives = 2
        self.ndim = 4
        self.n_constraints = 4

        self.upper = np.zeros(self.ndim)
        self.lower = np.zeros(self.ndim)
        self.lower[0] = 0.125
        self.lower[1] = 0.1
        self.lower[2] = 0.1
        self.lower[3] = 0.125
        self.upper[0] = 5.0
        self.upper[1] = 10.0
        self.upper[2] = 10.0
        self.upper[3] = 5.0

    def evaluate(self, x):
        f = np.zeros(x.shape[0], self.n_objectives)
        g = np.zeros(self.n_constraints)

        x1 = x[0]
        x2 = x[1]
        x3 = x[2]
        x4 = x[3]

        P = 6000
        L = 14
        E = 30 * 1e6

        # // deltaMax = 0.25
        G = 12 * 1e6
        tauMax = 13600
        sigmaMax = 30000

        # First original objective function
        f[0] = (1.10471 * x1 * x1 * x2) + (0.04811 * x3 * x4) * (14.0 + x2)
        # Second original objective function
        f[1] = (4 * P * L * L * L) / (E * x4 * x3 * x3 * x3)

        # Constraint functions
        M = P * (L + (x2 / 2))
        tmpVar = ((x2 * x2) / 4.0) + np.power((x1 + x3) / 2.0, 2)
        R = np.sqrt(tmpVar)
        tmpVar = ((x2 * x2) / 12.0) + np.power((x1 + x3) / 2.0, 2)
        J = 2 * np.sqrt(2) * x1 * x2 * tmpVar

        tauDashDash = (M * R) / J
        tauDash = P / (np.sqrt(2) * x1 * x2)
        tmpVar = tauDash * tauDash + ((2 * tauDash * tauDashDash * x2) / (2 * R)) + (tauDashDash * tauDashDash)
        tau = np.sqrt(tmpVar)
        sigma = (6 * P * L) / (x4 * x3 * x3)
        tmpVar = 4.013 * E * np.sqrt((x3 * x3 * x4 * x4 * x4 * x4 * x4 * x4) / 36.0) / (L * L)
        tmpVar2 = (x3 / (2 * L)) * np.sqrt(E / (4 * G))
        PC = tmpVar * (1 - tmpVar2)

        g[0] = tauMax - tau
        g[1] = sigmaMax - sigma
        g[2] = x4 - x1
        g[3] = PC - P
        g = np.where(g < 0, -g, 0)

        return f, g

class CRE23():
    def __init__(self):
        self.problem_name = 'CRE23'
        self.n_objectives = 2
        self.ndim = 4
        self.n_constraints = 4

        self.upper = np.zeros(self.ndim)
        self.lower = np.zeros(self.ndim)
        self.lower[0] = 55
        self.lower[1] = 75
        self.lower[2] = 1000
        self.lower[3] = 11
        self.upper[0] = 80
        self.upper[1] = 110
        self.upper[2] = 3000
        self.upper[3] = 20

    def evaluate(self, x):
        f = np.zeros(x.shape[0], self.n_objectives)
        g = np.zeros(self.n_constraints)

        x1 = x[0]
        x2 = x[1]
        x3 = x[2]
        x4 = x[3]

        # First original objective function
        f[0] = 4.9 * 1e-5 * (x2 * x2 - x1 * x1) * (x4 - 1.0)
        # Second original objective function
        f[1] = ((9.82 * 1e6) * (x2 * x2 - x1 * x1)) / (x3 * x4 * (x2 * x2 * x2 - x1 * x1 * x1))

        # Reformulated objective functions
        g[0] = (x2 - x1) - 20.0
        g[1] = 0.4 - (x3 / (3.14 * (x2 * x2 - x1 * x1)))
        g[2] = 1.0 - (2.22 * 1e-3 * x3 * (x2 * x2 * x2 - x1 * x1 * x1)) / np.power((x2 * x2 - x1 * x1), 2)
        g[3] = (2.66 * 1e-2 * x3 * x4 * (x2 * x2 * x2 - x1 * x1 * x1)) / (x2 * x2 - x1 * x1) - 900.0
        g = np.where(g < 0, -g, 0)

        return f, g

class CRE24():
    def __init__(self):
        self.problem_name = 'CRE24'
        self.n_objectives = 2
        self.ndim = 7
        self.n_constraints = 11

        self.lower = np.zeros(self.ndim)
        self.upper = np.zeros(self.ndim)

        self.lower[0] = 2.6
        self.lower[1] = 0.7
        self.lower[2] = 17
        self.lower[3] = 7.3
        self.lower[4] = 7.3
        self.lower[5] = 2.9
        self.lower[6] = 5.0
        self.upper[0] = 3.6
        self.upper[1] = 0.8
        self.upper[2] = 28
        self.upper[3] = 8.3
        self.upper[4] = 8.3
        self.upper[5] = 3.9
        self.upper[6] = 5.5

    def evaluate(self, x):
        f = np.zeros(x.shape[0], self.n_objectives)
        g = np.zeros(self.n_constraints)

        x1 = x[0]
        x2 = x[1]
        x3 = np.round(x[2])
        x4 = x[3]
        x5 = x[4]
        x6 = x[5]
        x7 = x[6]

        # First original objective function (weight)
        f[0] = 0.7854 * x1 * (x2 * x2) * (((10.0 * x3 * x3) / 3.0) + (14.933 * x3) - 43.0934) - 1.508 * x1 * (x6 * x6 + x7 * x7) + 7.477 * (x6 * x6 * x6 + x7 * x7 * x7) + 0.7854 * (x4 * x6 * x6 + x5 * x7 * x7)

        # Second original objective function (stress)
        tmpVar = np.power((745.0 * x4) / (x2 * x3), 2.0)  + 1.69 * 1e7
        f[1] =  np.sqrt(tmpVar) / (0.1 * x6 * x6 * x6)

        # Constraint functions
        g[0] = -(1.0 / (x1 * x2 * x2 * x3)) + 1.0 / 27.0
        g[1] = -(1.0 / (x1 * x2 * x2 * x3 * x3)) + 1.0 / 397.5
        g[2] = -(x4 * x4 * x4) / (x2 * x3 * x6 * x6 * x6 * x6) + 1.0 / 1.93
        g[3] = -(x5 * x5 * x5) / (x2 * x3 * x7 * x7 * x7 * x7) + 1.0 / 1.93
        g[4] = -(x2 * x3) + 40.0
        g[5] = -(x1 / x2) + 12.0
        g[6] = -5.0 + (x1 / x2)
        g[7] = -1.9 + x4 - 1.5 * x6
        g[8] = -1.9 + x5 - 1.1 * x7
        g[9] =  -f[1] + 1300.0
        tmpVar = np.power((745.0 * x5) / (x2 * x3), 2.0) + 1.575 * 1e8
        g[10] = -np.sqrt(tmpVar) / (0.1 * x7 * x7 * x7) + 1100.0
        g = np.where(g < 0, -g, 0)

        return f, g

class CRE25():
    def __init__(self):
        self.problem_name = 'CRE25'
        self.n_objectives = 2
        self.ndim = 4
        self.n_constraints = 1

        self.lower = np.full(self.ndim, 12)
        self.upper = np.full(self.ndim, 60)

    def evaluate(self, x):
        f = np.zeros(x.shape[0], self.n_objectives)
        g = np.zeros(self.n_constraints)

        # all the four variables must be inverger values
        x1 = np.round(x[0])
        x2 = np.round(x[1])
        x3 = np.round(x[2])
        x4 = np.round(x[3])

        # First original objective function
        f[0] = np.abs(6.931 - ((x3 / x1) * (x4 / x2)))
        # Second original objective function (the maximum value among the four variables)
        l = [x1, x2, x3, x4]
        f[1] = max(l)

        g[0] = 0.5 - (f[0] / 6.931)
        g = np.where(g < 0, -g, 0)

        return f, g

class CRE31():
    def __init__(self):
        self.problem_name = 'CRE31'
        self.n_objectives = 3
        self.ndim = 7
        self.n_constraints = 10

        self.lower = np.zeros(self.ndim)
        self.upper = np.zeros(self.ndim)
        self.lower[0] = 0.5
        self.lower[1] = 0.45
        self.lower[2] = 0.5
        self.lower[3] = 0.5
        self.lower[4] = 0.875
        self.lower[5] = 0.4
        self.lower[6] = 0.4
        self.upper[0] = 1.5
        self.upper[1] = 1.35
        self.upper[2] = 1.5
        self.upper[3] = 1.5
        self.upper[4] = 2.625
        self.upper[5] = 1.2
        self.upper[6] = 1.2

    def evaluate(self, x):
        f = np.zeros(x.shape[0], self.n_objectives)
        g = np.zeros(self.n_constraints)

        x1 = x[0]
        x2 = x[1]
        x3 = x[2]
        x4 = x[3]
        x5 = x[4]
        x6 = x[5]
        x7 = x[6]

        # First original objective function
        f[0] = 1.98 + 4.9 * x1 + 6.67 * x2 + 6.98 * x3 + 4.01 * x4 + 1.78 * x5 + 0.00001 * x6 + 2.73 * x7
        # Second original objective function
        f[1] = 4.72 - 0.5 * x4 - 0.19 * x2 * x3
        # Third original objective function
        Vmbp = 10.58 - 0.674 * x1 * x2 - 0.67275 * x2
        Vfd = 16.45 - 0.489 * x3 * x7 - 0.843 * x5 * x6
        f[2] = 0.5 * (Vmbp + Vfd)

        # Constraint functions
        g[0] = 1 -(1.16 - 0.3717 * x2 * x4 - 0.0092928 * x3)
        g[1] = 0.32 -(0.261 - 0.0159 * x1 * x2 - 0.06486 * x1 -  0.019 * x2 * x7 + 0.0144 * x3 * x5 + 0.0154464 * x6)
        g[2] = 0.32 -(0.214 + 0.00817 * x5 - 0.045195 * x1 - 0.0135168 * x1 + 0.03099 * x2 * x6 - 0.018 * x2 * x7  + 0.007176 * x3 + 0.023232 * x3 - 0.00364 * x5 * x6 - 0.018 * x2 * x2)
        g[3] = 0.32 -(0.74 - 0.61 * x2 - 0.031296 * x3 - 0.031872 * x7 + 0.227 * x2 * x2)
        g[4] = 32 -(28.98 + 3.818 * x3 - 4.2 * x1 * x2 + 1.27296 * x6 - 2.68065 * x7)
        g[5] = 32 -(33.86 + 2.95 * x3 - 5.057 * x1 * x2 - 3.795 * x2 - 3.4431 * x7 + 1.45728)
        g[6] =  32 -(46.36 - 9.9 * x2 - 4.4505 * x1)
        g[7] =  4 - f[1]
        g[8] =  9.9 - Vmbp
        g[9] =  15.7 - Vfd
        g = np.where(g < 0, -g, 0)

        return f, g

class CRE32():
    def __init__(self):
        self.problem_name = 'CRE32'
        self.n_objectives = 3
        self.ndim = 6
        self.n_constraints = 9

        self.lower = np.zeros(self.ndim)
        self.upper = np.zeros(self.ndim)
        self.lower[0] = 150.0
        self.lower[1] = 20.0
        self.lower[2] = 13.0
        self.lower[3] = 10.0
        self.lower[4] = 14.0
        self.lower[5] = 0.63
        self.upper[0] = 274.32
        self.upper[1] = 32.31
        self.upper[2] = 25.0
        self.upper[3] = 11.71
        self.upper[4] = 18.0
        self.upper[5] = 0.75

    def evaluate(self, x):
        f = np.zeros(x.shape[0], self.n_objectives)
        # NOT g
        constraintFuncs = np.zeros(self.n_constraints)

        x_L = x[0]
        x_B = x[1]
        x_D = x[2]
        x_T = x[3]
        x_Vk = x[4]
        x_CB = x[5]

        displacement = 1.025 * x_L * x_B * x_T * x_CB
        V = 0.5144 * x_Vk
        g = 9.8065
        Fn = V / np.power(g * x_L, 0.5)
        a = (4977.06 * x_CB * x_CB) - (8105.61 * x_CB) + 4456.51
        b = (-10847.2 * x_CB * x_CB) + (12817.0 * x_CB) - 6960.32

        power = (np.power(displacement, 2.0/3.0) * np.power(x_Vk, 3.0)) / (a + (b * Fn))
        outfit_weight = 1.0 * np.power(x_L , 0.8) * np.power(x_B , 0.6) * np.power(x_D, 0.3) * np.power(x_CB, 0.1)
        steel_weight = 0.034 * np.power(x_L ,1.7) * np.power(x_B ,0.7) * np.power(x_D ,0.4) * np.power(x_CB ,0.5)
        machinery_weight = 0.17 * np.power(power, 0.9)
        light_ship_weight = steel_weight + outfit_weight + machinery_weight

        ship_cost = 1.3 * ((2000.0 * np.power(steel_weight, 0.85))  + (3500.0 * outfit_weight) + (2400.0 * np.power(power, 0.8)))
        capital_costs = 0.2 * ship_cost

        DWT = displacement - light_ship_weight

        running_costs = 40000.0 * np.power(DWT, 0.3)

        round_trip_miles = 5000.0
        sea_days = (round_trip_miles / 24.0) * x_Vk
        handling_rate = 8000.0

        daily_consumption = ((0.19 * power * 24.0) / 1000.0) + 0.2
        fuel_price = 100.0
        fuel_cost = 1.05 * daily_consumption * sea_days * fuel_price
        port_cost = 6.3 * np.power(DWT, 0.8)

        fuel_carried = daily_consumption * (sea_days + 5.0)
        miscellaneous_DWT = 2.0 * np.power(DWT, 0.5)

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
        constraintFuncs[0] = (x_L / x_B) - 6.0
        constraintFuncs[1] = -(x_L / x_D) + 15.0
        constraintFuncs[2] = -(x_L / x_T) + 19.0
        constraintFuncs[3] = 0.45 * np.power(DWT, 0.31) - x_T
        constraintFuncs[4] = 0.7 * x_D + 0.7 - x_T
        constraintFuncs[5] = 500000.0 - DWT
        constraintFuncs[6] = DWT - 3000.0
        constraintFuncs[7] = 0.32 - Fn

        KB = 0.53 * x_T
        BMT = ((0.085 * x_CB - 0.002) * x_B * x_B) / (x_T * x_CB)
        KG = 1.0 + 0.52 * x_D
        constraintFuncs[8] = (KB + BMT - KG) - (0.07 * x_B)
        constraintFuncs = np.where(constraintFuncs < 0, -constraintFuncs, 0)

        return f, constraintFuncs

class CRE51():
    def __init__(self):
        self.problem_name = 'CRE51'
        self.n_objectives = 5
        self.ndim = 3
        self.n_constraints = 7

        self.lower = np.zeros(self.ndim)
        self.upper = np.zeros(self.ndim)
        self.lower[0] = 0.01
        self.lower[1] = 0.01
        self.lower[2] = 0.01
        self.upper[0] = 0.45
        self.upper[1] = 0.10
        self.upper[2] = 0.10

    def evaluate(self, x):
        f = np.zeros(x.shape[0], self.n_objectives)
        g = np.zeros(self.n_constraints)

        # First original objective function
        f[0] = 106780.37 * (x[1] + x[2]) + 61704.67
        #Second original objective function
        f[1] = 3000 * x[0]
        # Third original objective function
        f[2] = 305700 * 2289 * x[1] / np.power(0.06*2289, 0.65)
        # Fourth original objective function
        f[3] = 250 * 2289 * np.exp(-39.75*x[1]+9.9*x[2]+2.74)
        # Fifth original objective function
        f[4] = 25 * (1.39 /(x[0]*x[1]) + 4940*x[2] -80)

        # Constraint functions
        g[0] = 1 - (0.00139/(x[0]*x[1])+4.94*x[2]-0.08)
        g[1] = 1 - (0.000306/(x[0]*x[1])+1.082*x[2]-0.0986)
        g[2] = 50000 - (12.307/(x[0]*x[1]) + 49408.24*x[2]+4051.02)
        g[3] = 16000 - (2.098/(x[0]*x[1])+8046.33*x[2]-696.71)
        g[4] = 10000 - (2.138/(x[0]*x[1])+7883.39*x[2]-705.04)
        g[5] = 2000 - (0.417*x[0]*x[1] + 1721.26*x[2]-136.54)
        g[6] = 550 - (0.164/(x[0]*x[1])+631.13*x[2]-54.48)
        g = np.where(g < 0, -g, 0)

        return f, g

if __name__ == '__main__':
    np.random.seed(seed=1)
    fun = RE21()

    x = fun.lbound + (fun.ubound - fun.lbound) * np.random.rand(fun.n_variables)
    print("Problem = {}".format(fun.problem_name))
    print("Number of objectives = {}".format(fun.n_objectives))
    print("Number of variables = {}".format(fun.n_variables))
    print("Number of constraints = {}".format(fun.n_constraints))
    print("Lower bounds = ", fun.lbound)
    print("Upper bounds = ", fun.ubound)
    print("x = ", x)

    if 'CRE' in fun.problem_name:
        f, g = fun.evaluate(x)
        print("f(x) = {}".format(f))
        print("g(x) = {}".format(g))
    else:
        f = fun.evaluate(x)
        print("f(x) = {}".format(f))
