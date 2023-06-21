#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2022

@author: aguscarpio99
"""

import matplotlib.pyplot as plt
import numpy as np
import sys
import os
from numba import njit
from modelo_thyristor_coop import rk4_numba
from save import save_return, save_data
#  from period_funcs import period
from poincare import period

# TODO: Let users pick the model (+ options than just delayed_wilsoncowan_rk4)

# Parameters passed with run.py
arn_number, ncpus, dimRs, dimIin, N_steps = [int(n) for n in sys.argv[1:6]]
dt = float(sys.argv[6])
Cm = float(sys.argv[7])

dir_path = f"results_lean_agus/Cm{str(Cm)}"

if not os.path.isdir(f"{dir_path}"):
    os.system(f"mkdir {dir_path}")

It0 = Vt0 = Vs0 = 0.1

#  minRs = 1.5
#  maxRs = 4.5
#  minIin = 0.1
#  maxIin = 2
minRs = 0.01
maxRs = 5
minIin = 0.01
maxIin = 2.5
#  Rs 0.01-8
#  Iin 0.01-3
#  Cm = 10

# main function
def run_arnold(arn_number, ncpus, dimRs, dimIin, N_steps, dt, Cm):

    # empty grid to fill with period calculations
    periods_grid = np.empty(shape=(dimIin,dimRs))*np.nan

    # Integer needed
    splitted_size = dimRs//ncpus

    # loop through parameters grid (splitted in ncpus parts)
    Iin_index = arn_number*splitted_size
    for Iin in np.split(np.linspace(minIin, maxIin, dimIin),ncpus)[arn_number]:
        Rs_index = 0
        for Rs in np.linspace(minRs, maxRs, dimRs):
            # Numerical integration of the model
            It_OT, Vt_OT, Vs_OT = rk4_numba(It0, Vt0, Vs0, N_steps, dt, Rs, Iin, Cm)
            # Period calculation with imported function
            #  periods_grid[Iin_index][Rs_index] = period(It_OT[-550000:], Vt_OT[-550000:])
            periods_grid[Iin_index][Rs_index] = period(Vs_OT[-550000:], dt)
            Rs_index += 1
        Iin_index += 1

        # Save values (a file per partition)
        with open(f"{dir_path}/periodsgrid_{arn_number}.npy", "wb") as f:
            np.save(f, periods_grid)
    with open(f"{dir_path}/periodsgrid_{arn_number}.npy", "wb") as f:
        np.save(f, periods_grid)

run_arnold(arn_number, ncpus, dimRs, dimIin, N_steps, dt, Cm)

#  run_arnold(0, 1, 4, 4, 1800000, 0.001)
