import numpy as np
import matplotlib.pyplot as plt
from poincare import period_temporal
from modelo_thyristor_coop import rk4_numba
import sys

#-------------
It0 = 0.1
Vt0 = 0.1
Vs0 = 0.1
N_steps = 1250000//3
dt = 0.003
#  Rs0 = 3.2
#  Iin0 = 1.2
Cm = 10.0

dimRs = dimIin = 210
#-------------
with open("results_lean_agus/Cm10.0/periodsgrid_total.npy", "rb") as f:
    periodsgrid_total = np.load(f)

#  It_OT, Vt_OT, Vs_OT = rk4_numba(It0, Vt0, Vs0, N_steps, dt, Rs0, Iin0, Cm)

#  period_n, period_t = period_temporal(Vs_OT[int(800/dt):], dt)
#  times = np.arange(0, int(dt*N_steps), dt)

with open("periods_burst_grid.npy", "rb") as f:
    periodstgrid_total = np.load(f)

import seaborn as sns
fig, ax = plt.subplots(figsize=(16,9))

#  Rsrange = np.linspace(0.01, 5, dimRs)
#  Iinrange = np.linspace(0.01, 2.5, dimIin)
#  kk, tt = np.meshgrid(Rsrange, Iinrange)
#  cm1 = ax.pcolormesh(kk, tt, periodstgrid_total)



center = 30
#  sns.heatmap(periodstgrid_total, cmap="coolwarm", center=center, vmax=center+1, vmin=center-1)
sns.heatmap(periodstgrid_total, cmap="coolwarm")
ax.invert_yaxis()
plt.show()



raise

periods_t_grid = np.empty(shape=(dimIin,dimRs))*np.nan
Rsrange = np.linspace(0.01, 5, dimRs)
Iinrange = np.linspace(0.01, 2.5, dimIin)

def ptg(index):
    for i in range(index*dimIin//15, (index+1)*dimIin//15):
        for j in range(dimRs):
            if periodsgrid_total[i][j]==1:
                _, _, Vs_OT = rk4_numba(It0, Vt0, Vs0, N_steps, dt,
                                        Rsrange[j], Iinrange[i], Cm)
                _, period_t = period_temporal(Vs_OT[int(800/dt):], dt)
                periods_t_grid[i][j] = period_t
    return periods_t_grid

index = int(sys.argv[1])
periods_t_grid_n = ptg(index)
with open(f"periods_t_grid_{index}.npy", "wb") as f:
    np.save(f, periods_t_grid_n)
