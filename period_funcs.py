#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2022

@author: aguscarpio99
"""
import numpy as np
import matplotlib.pyplot as plt


def true_neighbours(X, Y, i, j, order, T, Rtol):
    R = 0
    for o in range(order):
        R += abs(X[i+o*T]-X[j+o*T]+(Y[i+o*T]-Y[j+o*T])*1j)
    #  print(R)
    if R<Rtol:
        return True
    return False

def period(X, Y):
    dXdt = np.gradient(X)
    dYdt = np.gradient(Y)
    TH = np.arctan2(dYdt, dXdt)

    dTH = np.diff(TH)
    dTH[dTH < -6] += 2*np.pi
    dTH[dTH > 6] -= 2*np.pi
    cumulative_dTH = np.abs(np.cumsum(dTH))[:250000]
    # 2000 arbitrario
    idx = np.argmax(np.gradient(cumulative_dTH[:25000]))

    vueltas = (cumulative_dTH-cumulative_dTH[idx])/(2*np.pi)
    land = np.logical_and
    candidate_idxs = []
    for i in range(1,9):
                candidate_idxs += list(np.where(land(vueltas[:-1]<i, vueltas[1:]>i))[0])
    for i_cand in candidate_idxs:
        #  if true_neighbours(X, Y, idx, i_cand, 30, 300, 0.1):
        if true_neighbours(X, Y, idx, i_cand, 12, 1500, 0.25):
            return round(vueltas[i_cand])
    return np.nan
