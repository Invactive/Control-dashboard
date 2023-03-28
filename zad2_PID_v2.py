import numpy as np
import matplotlib.pyplot as plt
import math as mt
import json


DATA = {}

# Constants
beta = 0.75
m = 1200  # [kg]

# Simulation params
Tp = 0.1  # [s]
T_sim = 40  # [s]
N = int(T_sim / Tp) + 1

# Limits
Fc_max = 1500
Fc_min = -1500
U_max = 10
U_min = -10

# Set voltage value
u = [-10]
v_zad = 20

# Actuator
Fc = [0]

# Initial values
t = [0.0]
v = [0.0]
x = [0.0, 0.0, 0.0]
e_n = [0.0]
I = 0

# Regulator
kp = 1
Ti = 0.01
Td = 0

# Main loop - generating data
for n in range(1, N):
    t.append(n * Tp)
    if len(v) > 2:
        x.append(v[-2] * Tp + x[-1])

    e_n.append(v_zad - v[-1])

    P = kp * e_n[-1]
    I = I + Ti * e_n[-1] * (t[-1] - t[-2])
    # D = Td * (e_n[-1] - e_n[-2]) / (t[-1] - t[-2])

    u.append(max(min(P+I, U_max), U_min))

    if u[-1] < 0:
        v.append(
            round(Tp * (Fc[-1] + beta * round(v[-1] * v[-1], 2)) / m + v[-1], 5))
    else:
        v.append(
            round(Tp * (Fc[-1] - beta * round(v[-1] * v[-1], 2)) / m + v[-1], 5))

    Fc.append((Fc_max - Fc_min) / (U_max - U_min) * (u[- 1] - U_min) + Fc_min)

DATA["t"] = t
DATA["x"] = x
DATA["u"] = u
DATA["v"] = v
DATA["e"] = e_n

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
