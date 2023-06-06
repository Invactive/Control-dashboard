import numpy as np
import matplotlib.pyplot as plt
import math as mt
import json


DATA = {}

# Constants
#parametry procesu
m = 5.3 * float(10**(-2)) #kg
FemP1 = 3.5969 * float(10**(-2)) #H
FemP2 = 5.2356 * float(10**(-3)) #m
f1 = 1.4142 * float(10**(-4)) #ms
f2 = 4.5626 * float(10**(-3)) #m
k = 2.6 * float(10**(0)) #A
c = -4.44 * float(10**(-2)) #A
g = 9.81

# Simulation params
#parametry eksperymentu symulacyjnego
Tp = 0.0001
Tsim = 2
N = int(Tsim/Tp) + 1

# Limits
umax = 5
umin = 0
e_nmin = 0
x3max = 2.38
x3min = 0.03884
x1max = 0.0105
x1min = 0
zadana = 0.005


# # Set voltage value
# u = [-10]
# v_zad = 20

# # Actuator
# Fc = [0]

# Initial values
#wartości początkowe
x1 = [0]
x2 = [0]
x3 = [0]
y =  [0]
u = [0]
e_n = [0]
t = [0]
P = 0
I = 0
D = 0

# Regulator
#nastawy regulatora
kp = 80
Td = 10
Ti = 120

# Main loop - generating data
for n in range(1, N):
    t.append(n * Tp)

    e_n.append(zadana - y[-1])
    u.append(max(min(P+D+I, umax), umin))

    x1.append(max(min(( x1[-1] + Tp*x2[-1] ), x1max), x1min))
    x2.append( x2[-1] + Tp*(g - (x3[-1]**2) * 1/(2*m) * FemP1/FemP2 * np.exp((-x1[-1]/FemP2))) )
    x3.append(max(min(( x3[-1] + Tp * f2/f1 * np.exp((x1[-1]/f2)) * (k*u[-1] + c - x3[-1]) ), x3max), x3min))

    P = kp * -e_n[-1]
    I = I + Ti * -e_n[-1] * (t[-1] - t[-2])
    D = Td * -(e_n[-1] - e_n[-2]) / (t[-1] - t[-2])
    y.append(x1[-1])


DATA["Time t [s]"] = t
DATA["Position x [m]"] = x1
DATA["Control signal u [V]"] = u
DATA["Speed v [m/s]"] = x2
DATA["Error e [m]"] = e_n

with open("DATA.json", "w") as outfile:
    json.dump(DATA, outfile)

# # Plotting output
# fig, ax = plt.subplots(3, 1, figsize=(8, 10))
# ax[0].plot(t, v)
# ax[0].set_title('Speed change in time')
# ax[0].set_xlabel('Time [s]')
# ax[0].set_ylabel('Speed [m/s]')
# ax[0].grid(True)

# ax[1].plot(t, x)
# ax[1].set_title('Position change in time')
# ax[1].set_xlabel('Time [s]')
# ax[1].set_ylabel('Position [m]')
# ax[1].grid(True)

# ax[2].plot(t, e_n)
# ax[2].set_title('Speed error')
# ax[2].set_xlabel('Time [s]')
# ax[2].set_ylabel('speed [m/s]')
# ax[2].grid(True)

# plt.tight_layout()
# plt.show()
