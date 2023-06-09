import numpy as np
import matplotlib.pyplot as plt
from poincare import period_temporal
from modelo_thyristor_coop import rk4_numba
from matplotlib.colors import LinearSegmentedColormap
import matplotlib
import xarray as xr

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
cmap = LinearSegmentedColormap.from_list('my_gradient', (
    # Edit this gradient at https://eltos.github.io/gradient/#E4D522-FFFFFF-65A151
    (0.000, (0.396, 0.631, 0.318)),
    (0.500, (0.922, 0.933, 0.847)),
    (1.000, (0.906, 0.753, 0.086))))
#-------------
with open("results_lean_agus/Cm10.0/periodsgrid_total.npy", "rb") as f:
    periodsgrid_total = np.load(f)

with open("periods_burst_grid.npy", "rb") as f:
    periodsbgrid_total = np.load(f)

with open("periods_t_grid.npy", "rb") as f:
    periodstgrid_total = np.load(f)

import seaborn as sns
fig, [ax, ax1] = plt.subplots(2, 1, figsize=(16,9), sharex=True, sharey=True)

#  Rsrange = np.linspace(0.01, 5, dimRs)
#  Iinrange = np.linspace(0.01, 2.5, dimIin)
#  kk, tt = np.meshgrid(Rsrange, Iinrange)
#  cm1 = ax.pcolormesh(kk, tt, periodstgrid_total)

periodsbgrid_total[22][131] = np.nan

#  p1_idx = np.where(periodsgrid_total == 1)
#  nan_idx = np.where(np.isnan(periodstgrid_total))
#  p1_set = set((i,j) for i,j in zip(p1_idx[0], p1_idx[1]))
#  nan_set = set((i,j) for i,j in zip(nan_idx[0], nan_idx[1]))
#  p1nan_set = p1_set.intersection(nan_set)
p1nan = np.where(np.logical_and(periodsgrid_total == 1, np.isnan(periodstgrid_total)))

periodstgrid_total[p1nan] = 60

#--------------
#  cbar_ax1 = fig.add_axes([.67, .55, .01, .3])
#  cbar_ax2 = fig.add_axes([.78, .55, .01, .3])
#--------------

#  periodstgrid_total = xr.DataArray(periodstgrid_total.repeat(3, axis=0).repeat(3, axis=1), dims=("Iin", r"$\tau_s$"), coords={r"$\tau_s$": 0.1*np.linspace(0.01, 5, 3*210), "Iin": np.linspace(0.01, 2.5, 3*210)})
periodstgrid_total = xr.DataArray(periodstgrid_total, dims=("Iin", r"$\tau_s$"), coords={r"$\tau_s$": 0.1*np.linspace(0.01, 5, 1400), "Iin": np.linspace(0.01, 2.5, 1400)})
periodsbgrid_total = xr.DataArray(periodsbgrid_total, dims=("Iin", r"$\tau_s$"), coords={r"$\tau_s$": 0.1*np.linspace(0.01, 5, 3*210), "Iin": np.linspace(0.01, 2.5, 3*210)})

rb = periodstgrid_total.plot(ax=ax, cmap="seismic", center=30, vmin=0)
rbb_pos = rb.colorbar.ax.get_position()
rb.colorbar.ax.set_position([rbb_pos.x0-0.08, rbb_pos.y0, rbb_pos.width, rbb_pos.height])
periodsbgrid_total.plot(ax=ax, cmap=cmap, robust=True)
ax.set_xlabel("")
#  spikes = sns.heatmap(periodstgrid_total, cmap="seismic", center=30, vmax=100, vmin=0, ax=ax)#, vmax=center+1, vmin=center-1)
#  bursts = sns.heatmap(periodsbgrid_total, cmap=cmap, ax=ax, robust=True)
ax.set_facecolor("#bbbbbb")
ax.set_xlim(0.03)
#  ax.invert_yaxis()

#  ax.get_yaxis().set_ticks([k*3*210/5 for k in range(6)], [0, 0.5, 1.0, 1.5, 2.0, 2.5])
#  print(ax.get_position())
#  print(ax1.get_position())


minRs = 0.01
maxRs = 5
minIin = 0.01
maxIin = 2.5
dimIin = 1400
dimRs = 1400
Iinrange = np.linspace(minIin, maxIin, dimIin)
Rsrange = np.linspace(minRs, maxRs, dimRs)
tausrange = 0.1*Rsrange

kk, tt = np.meshgrid(tausrange, Iinrange)

colors = plt.cm.get_cmap('tab20',16)(np.arange(8))
cmap = matplotlib.colors.ListedColormap(colors, "")

cm1 = ax1.pcolormesh(kk, tt, periodsgrid_total, cmap=cmap, vmin=0.5, vmax=8.5)
cbar = plt.colorbar(cm1)
pos = ax1.get_position()
pos.x1 = ax.get_position().x1
ax1.set_position(pos)
cbarpos = cbar.ax.get_position()
cbar.ax.set_position([cbarpos.x0-0.102, cbarpos.y0, cbarpos.width, cbarpos.height])

ax1.set_xlabel(r"$\tau_s$ (a.u)", size=18)
ax1.set_ylabel(r"$I_{in} $ (a.u)", size=18)
ax.tick_params(axis='both', which='major', labelsize=18)
ax1.tick_params(axis='both', which='major', labelsize=18)
ax.set_ylabel(r"$I_{in} $ (a.u)", size=18)

ax1.set_facecolor("#eeeeee")

axp1 = fig.add_axes([0.76, 0.72, 0.1, 0.15])
axp2 = fig.add_axes([0.89, 0.72, 0.1, 0.15])
axp3 = fig.add_axes([0.76, 0.52, 0.1, 0.15])
axp4 = fig.add_axes([0.89, 0.52, 0.1, 0.15])


with open("p1_red.npy", "rb") as f:
    Vs_OT = np.load(f)
axp1.plot(np.arange(0,len(Vs_OT))*0.001, Vs_OT, "#a20000")

with open("p1_blue.npy", "rb") as f:
    Vs_OT = np.load(f)
axp2.plot(np.arange(0,len(Vs_OT))*0.001, Vs_OT, "#00007c")

with open("p4_yellow.npy", "rb") as f:
    Vs_OT = np.load(f)
axp3.plot(np.arange(0,len(Vs_OT))*0.001, Vs_OT, "#e9da85")

with open("p4_green.npy", "rb") as f:
    Vs_OT = np.load(f)
axp4.plot(np.arange(0,len(Vs_OT))*0.001, Vs_OT, "#b8d1a5")

axp1.set_ylim(0, 6.7)
axp2.set_ylim(0, 6.7)
axp3.set_ylim(0, 6.7)
axp4.set_ylim(0, 6.7)


plt.show()

periodsbgrid_total.plot.surface()
plt.show()
