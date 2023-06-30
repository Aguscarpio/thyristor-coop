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
direction = str(sys.argv[8])

dir_path = f"results_barridos/{str(direction)}"

if not os.path.isdir(f"{dir_path}"):
    os.system(f"mkdir {dir_path}")


minRs = 1.7
maxRs = 3.8
minIin = 0.13
maxIin = 1.6
#  minRs = 2.39
#  maxRs = 2.44
#  minIin = 1.24
#  maxIin = 1.28


def select_direction(enum_arr, direction):
    if direction == "up":
        return enum_arr
    if direction == "down":
        return reversed(list(enum_arr))

# main function
def run_arnold(arn_number, ncpus, dimRs, dimIin, N_steps, dt, Cm):
    It0 = Vt0 = Vs0 = 0.1
    # empty grid to fill with period calculations
    periods_grid = np.empty(shape=(dimIin,dimRs))*np.nan

    # Integer needed
    splitted_size = dimIin//ncpus

    # loop through parameters grid (splitted in ncpus parts)
    Rs_index = arn_number*splitted_size
    for Rs in np.split(np.linspace(minRs, maxRs, dimRs),ncpus)[arn_number]:
        for Iin_index, Iin in select_direction(enumerate(np.linspace(minIin, maxIin, dimIin)), direction):
            It_OT, Vt_OT, Vs_OT = rk4_numba(It0, Vt0, Vs0, N_steps, dt, Rs, Iin, Cm)
            It0, Vt0, Vs0 = It_OT[-1], Vt_OT[-1], Vs_OT[-1]
            periods_grid[Iin_index][Rs_index] = period(Vs_OT[-550000:], dt)
        Rs_index += 1

        # Save values (a file per partition)
        with open(f"{dir_path}/periodsgrid_{arn_number}.npy", "wb") as f:
            np.save(f, periods_grid)
    with open(f"{dir_path}/periodsgrid_{arn_number}.npy", "wb") as f:
        np.save(f, periods_grid)

run_arnold(arn_number, ncpus, dimRs, dimIin, N_steps, dt, Cm)
