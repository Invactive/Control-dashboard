import numpy as np
from fuzzy_logic.terms import Term
from fuzzy_logic.variables import FuzzyVariable, SugenoVariable, LinearSugenoFunction
from fuzzy_logic.sugeno_fs import SugenoFuzzySystem
from fuzzy_logic.mf import TriangularMF
import json


# Constants
# Model parameters
m = 5.3 * float(10**(-2))  # kg
FemP1 = 3.5969 * float(10**(-2))  # H
FemP2 = 5.2356 * float(10**(-3))  # m
f1 = 1.4142 * float(10**(-4))  # ms
f2 = 4.5626 * float(10**(-3))  # m
k = 2.6 * float(10**(0))  # A
c = -4.44 * float(10**(-2))  # A
g = 9.81

# Limits
umax = 5
umin = 0
e_nmin = 0
x3max = 2.38
x3min = 0.03884
x1max = 0.0105
x1min = 0
setpoint = 0.006

# Simulation params
Tp = 0.0001
Tsim = 2

NB_l = -x1max  # -0.0105
NB_h = -x1max/8  # -0.0013125

NS_l = -x1max  # -0.0105
NS_h = 0

ZE_l = -x1max/10  # -0.0105
ZE_h = x1max/10  # 0.00105

PS_l = 0
PS_h = x1max  # 0.0105

PB_l = x1max/8  # 0.0013125
PB_h = x1max  # 0.0105


def generateData(mass: float,
                 Tsim: float,
                 Tp: float,
                 Td: float,
                 setpoint: float,
                 output: str):
    N = int(Tsim/Tp) + 1
    x1 = [0]
    x2 = [0]
    x3 = [0]
    y = [0]
    u1 = [0]
    e_n = [0]
    t = [0]
    DATA = {}

    # Fuzzy controller
    t1: Term = Term('NB', TriangularMF(NB_l, -x1max, NB_h))
    t2: Term = Term('NS', TriangularMF(NS_l, -x1max/8, NS_h))
    t3: Term = Term('ZE', TriangularMF(ZE_l, 0, ZE_h))
    t4: Term = Term('PS', TriangularMF(PS_l, x1max/8, PS_h))
    t5: Term = Term('PB', TriangularMF(PB_l, x1max, PB_h))
    e: FuzzyVariable = FuzzyVariable('e', -x1max, x1max, t1, t2, t3, t4, t5)

    u: SugenoVariable = SugenoVariable('u',
                                       LinearSugenoFunction(
                                           'NB', {e: -0.9}, 0),
                                       LinearSugenoFunction(
                                           'NS', {e: -0.4}, 0.1),
                                       LinearSugenoFunction(
                                           'ZE', {e: 0.25}, 0.25),
                                       LinearSugenoFunction(
                                           'PS', {e: 0.4}, 0.4),
                                       LinearSugenoFunction(
                                           'PB', {e: 0.9}, 0.9)
                                       )

    FS: SugenoFuzzySystem = SugenoFuzzySystem([e], [u])
    FS.rules.append(FS.parse_rule('if (e is NB) then (u is PB)'))
    FS.rules.append(FS.parse_rule('if (e is NS) then (u is PS)'))
    FS.rules.append(FS.parse_rule('if (e is ZE) then (u is ZE)'))
    FS.rules.append(FS.parse_rule('if (e is PS) then (u is NS)'))
    FS.rules.append(FS.parse_rule('if (e is PB) then (u is NB)'))

    e_n = [x1max - y[-1]]
    result = FS.calculate({e: e_n[-1]})
    u_n = [result[u]]
    D = 0
    Td = 2
    # Main loop - generating data
    for n in range(1, N):
        t.append(n * Tp)

        e_n.append(setpoint - y[-1])
        u1.append(max(min(result[u]+D, umax), umin))
        result = FS.calculate({e: e_n[-1]})
        y.append(x1[-1])

        x1.append(max(min((x1[-1] + Tp*x2[-1]), x1max), x1min))
        x2.append(x2[-1] + Tp*(g - (x3[-1]**2) * 1/(2*mass)
                               * FemP1/FemP2 * np.exp((-x1[-1]/FemP2))))
        x3.append(max(min((x3[-1] + Tp * f2/f1 * np.exp((x1[-1]/f2))
                           * (k*u1[-1] + c - x3[-1])), x3max), x3min))

        D = Td * -(e_n[-1] - e_n[-2]) / (t[-1] - t[-2])

        DATA["setpoint"] = setpoint
        DATA["t"] = t   # time s
        DATA["x"] = x1  # position m
        DATA["u"] = u1   # control signal
        DATA["v"] = x2  # speed m/s
        DATA["e"] = e_n  # error m

    with open(output, "w") as outfile:
        json.dump(DATA, outfile)
