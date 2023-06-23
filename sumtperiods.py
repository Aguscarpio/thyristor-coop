import numpy as np

n_cpus = 15
for n in range(n_cpus):
    with open(f"periods_burst_grid_{n}.npy", "rb") as f:
        pg = np.load(f)
    if n==0:
        pg_total = np.zeros_like(pg)
    pgc = np.copy(pg)
    pgc[np.isnan(pgc)] = 0
    pg_total += pgc

pg_total[pg_total==0] = np.nan

with open("periods_burst_grid.npy", "wb") as g:
    np.save(g, pg_total)
