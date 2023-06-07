#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2022

@author: aguscarpio99
"""
import argparse
import os

target_program = "arnold_n.py"

parser = argparse.ArgumentParser(description='Computes n-period for solutions'+
            ' generated by a model for a (dimRs x dimIin) parameter space grid')

parser.add_argument('-ncpus', type=int, nargs=1, default=[1],
                help='Number of child processes'+
                     '\nIt is recommended to use at most the number of '+
                     'available CPU cores')

parser.add_argument('-dimRs', type=int, nargs=1, default=[16],
                help='Rs parameter dimension, corresponding to Rs-Iin plane')

parser.add_argument('-dimIin', type=int, nargs=1, default=[16],
                help='Iin parameter dimension, corresponding to Rs-Iin plane')

parser.add_argument('-N_steps', type=int, nargs=1, default=[900000],
                help='Number of steps performed on each simulation'+
                     '\nConsider the program runs a whole simulation for each'
                     ' cell of the grid')

parser.add_argument('-dt', type=float, nargs=1, help='dt', default=[0.00004])


# TODO:
parser.add_argument('--progressbar', action='store_true',
                help='display progressbar')

args = parser.parse_args()
ncpus = args.ncpus[0]
N_steps = args.N_steps[0]
dt = args.dt[0]
dimRs = args.dimRs[0]
dimIin = args.dimIin[0]

if not os.path.isdir(f"results_lean_agus"):
    os.system(f"mkdir results_lean_agus")

for arn_number in range(ncpus):
    os.system(f"python3 {target_program} {arn_number} {ncpus}" +
            f" {dimRs} {dimIin} {N_steps} {dt} &")
