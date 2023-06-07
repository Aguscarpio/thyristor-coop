import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import pandas as pd
import matplotlib as mpl
mpl.rcParams['text.usetex'] = True

minRs = 0.01
maxRs = 8
minIin = 0.01
maxIin = 3
dimIin = 140
dimRs = 140

#  size=24

with open(f"periodsgrid_total.npy", "rb") as f:
    periods_grid_super = np.load(f)

def clean(arr):
    for i in range(dimRs):
        for j in range(dimRs):
            nb=arr[np.ix_(*((z-1, z, z+1-S) for z,S in zip((i,j), arr.shape)))].ravel()
            if np.count_nonzero(np.isnan(nb))>3:
                arr[i][j] = np.nan

Iinrange = np.linspace(minIin, maxIin, dimIin)
Rsrange = np.linspace(minRs, maxRs, dimRs)

kk, tt = np.meshgrid(Rsrange, Iinrange)

colors = plt.cm.get_cmap('tab20',16)(np.arange(16))
cmap = matplotlib.colors.ListedColormap(colors, "")

fig, ax1 = plt.subplots(1, 1, figsize=(16,9))
cm1 = ax1.pcolormesh(kk, tt, periods_grid_super, cmap=cmap, vmin=0.5, vmax=16.5)
ax1.set_xlabel(r"$R_s$ (a.u)", size=24)
ax1.set_ylabel(r"$I_{in} $ (ms)", size=24)
ax1.tick_params(axis='both', which='major', labelsize=24)
plt.show()

raise
def area(vs):
    a = 0
    x0,y0 = vs[0]
    for [x1,y1] in vs[1:]:
        dx = x1-x0
        dy = y1-y0
        a += 0.5*(y0*dx - x0*dy)
        x0 = x1
        y0 = y1
    return a

eps = 0.1
n = 17
fig, ax = plt.subplots(figsize=(16,9))
#  from skimage import measure
for n in range(1,n):
    pgsectors = np.zeros_like(periods_grid_super)
    for periods_grid in periods_grids_list:
        pgcopy = np.copy(periods_grid)
        pgcopy[pgcopy!=n] = 0
        pgsectors += pgcopy
    pgsectors[pgsectors!=0] = n
    clusterized = measure.label(pgsectors>0)
    for region in measure.regionprops(clusterized):
        if region['area'] < 10:
            pgsectors[clusterized==region['label']] = 0
    ax.contourf(kk, tt, pgsectors, levels=[n-eps, n+eps], colors=[colors[n-1], "#000"], alpha=0.2)
    size = 30
    #  ax.set_xlabel("Rs", size=size)
    #  ax.set_ylabel(r"$\Iin$)", size=size)
    ax.tick_params(axis='both', which='major', labelsize=size)
    ax.tick_params(axis='both', which='minor', labelsize=size)
    aaa = ax.contour(kk, tt, pgsectors, levels=[n-eps, n+eps], colors=[colors[n-1], "#000"], linewidths=[3,0], alpha=0.8)

#  for n in [17]:
    #  pgsectors = np.zeros_like(periods_grid_super)
    #  for periods_grid in periods_grids_list:
        #  pgcopy = np.copy(periods_grid)
        #  pgcopy[np.isnan(pgcopy)] = n
        #  pgcopy[pgcopy!=n] = 0
        #  pgsectors += pgcopy
    #  pgsectors[pgsectors!=0] = n
    #  ax.contourf(kk, tt, pgsectors, levels=[n-eps, n+eps], colors=["#999", "#000"], alpha=0.2)
    #  aaa = ax.contour(kk, tt, pgsectors, levels=[n-eps, n+eps], colors=["#999", "#000"], linewidths=[3,0], alpha=0.8)


#  for i in range(1):
    #  contour = aaa.collections[i]
    #  for path in contour.get_paths():
        #  if area(path.vertices)<1:
            #  path.remove()
            #  break

#  plt.savefig("arnolds.pdf")
#  ax.set_xlabel("Rs")
#  ax.set_ylabel("Iin (ms)")
plt.show()





raise
ax.invert_yaxis()
colorbar = ax.collections[0].colorbar
n=16
r = colorbar.vmax - colorbar.vmin
colorbar.set_ticks([colorbar.vmin + 0.5 * r / (n) + r * i / (n) for i in range(n)])
colorbar.set_ticklabels([i for i in range(1,17)])
plt.show()
