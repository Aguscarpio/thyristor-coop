import numpy as np
import matplotlib.pyplot as plt
from poincare import period_temporal
from modelo_thyristor_coop import rk4_numba
from matplotlib.colors import LinearSegmentedColormap
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

dimRs = dimIin = 1400
#-------------
cmap = LinearSegmentedColormap.from_list('my_gradient', (
    # Edit this gradient at https://eltos.github.io/gradient/#E4D522-FFFFFF-65A151
    (0.000, (0.906, 0.753, 0.086)),
    (0.500, (0.922, 0.933, 0.847)),
    (1.000, (0.396, 0.631, 0.318))))
#-------------
with open("results_lean_agus/Cm10.0/periodsgrid_total.npy", "rb") as f:
    periodsgrid_total = np.load(f)

#  It_OT, Vt_OT, Vs_OT = rk4_numba(It0, Vt0, Vs0, N_steps, dt, Rs0, Iin0, Cm)

#  period_n, period_t = period_temporal(Vs_OT[int(800/dt):], dt)
#  times = np.arange(0, int(dt*N_steps), dt)

#  with open("periods_t_grid.npy", "rb") as f:
#  with open("periods_burst_grid_210.npy", "rb") as f:
    #  periodsbgrid_total = np.load(f)

#  with open("periods_t_grid.npy", "rb") as f:
    #  periodstgrid_total = np.load(f)

#  import seaborn as sns
#  fig, ax = plt.subplots(figsize=(16,9))

#  #  Rsrange = np.linspace(0.01, 5, dimRs)
#  #  Iinrange = np.linspace(0.01, 2.5, dimIin)
#  #  kk, tt = np.meshgrid(Rsrange, Iinrange)
#  #  cm1 = ax.pcolormesh(kk, tt, periodstgrid_total)

#  periodsbgrid_total[22][131] = np.nan

#  center = 0.5
#  sat = 0.5
#  spikes = sns.heatmap(periodstgrid_total, cmap="seismic", center=30, vmax=100, vmin=0)#, vmax=center+1, vmin=center-1)
#  bursts = sns.heatmap(periodsbgrid_total, cmap=cmap)
#  spikes.set_facecolor("#bbbbbb")
#  ax.invert_yaxis()
#  ax.get_xaxis().set_ticks([])
#  ax.get_yaxis().set_ticks([])
#  plt.show()



#  raise

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
