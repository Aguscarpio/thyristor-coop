import numpy as np
import matplotlib.pyplot as plt
from poincare import period_temporal
from modelo_thyristor_coop import rk4_numba
import sys

#-------------
It0 = 0.1
Vt0 = 0.1
Vs0 = 0.1
N_steps = 1250000
dt = 0.003
#  Rs0 = 3.2
#  Iin0 = 1.2
Cm = 10.0

dimRs = dimIin = 210
#-------------
with open("results_lean_agus/Cm10.0/periodsgrid_total.npy", "rb") as f:
    periodsgrid_total = np.load(f)

periods_burst_grid = np.empty(shape=(dimIin,dimRs))*np.nan
Rsrange = np.linspace(0.01, 5, dimRs)
Iinrange = np.linspace(0.01, 2.5, dimIin)

def pbg(index):
    for i in range(15+index*8, 15+(index+1)*8):
    #  for i in range(index*dimIin//15, (index+1)*dimIin//15):
        for j in range(82, 140):
            if periodsgrid_total[i][j] not in [0, 1]:
                _, _, Vs_OT = rk4_numba(It0, Vt0, Vs0, N_steps, dt,
                                        Rsrange[j], Iinrange[i], Cm)
                Vs_OT_notrans = Vs_OT[int(800/dt):]
                mid_val = (min(Vs_OT_notrans) + max(Vs_OT_notrans))/2
                periods_burst_grid[i][j] = np.mean(Vs_OT_notrans>mid_val)
                if max(Vs_OT_notrans)-min(Vs_OT_notrans)<0.05:
                    periods_burst_grid[i][j] = np.nan
    return periods_burst_grid

index = int(sys.argv[1])
periods_burst_grid_n = pbg(index)
with open(f"periods_burst_grid_{index}.npy", "wb") as f:
    np.save(f, periods_burst_grid_n)
