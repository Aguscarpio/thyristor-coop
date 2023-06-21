#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2023, 12 Jun

@author: aguscarpio99
"""
import numpy as np
import matplotlib.pyplot as plt

def period(X, dt):
    dXdt = np.gradient(X)
    peaks_idx = np.where(np.diff(np.sign(dXdt))<0)
    X_peaks = X[peaks_idx]
    if np.max(X)-np.min(X) < 0.01:
        return 0
    max_period = 8
    for i in range(1, min(max_period, len(X_peaks)-1)+1):
        if max(X_peaks[i:] - X_peaks[:-i]) < 0.02:
            return i
    return np.nan

    #  sorted_X_peaks = np.sort(X[peaks_idx])
    #  for i in range(1, 8+1):
        #  if len(X_peaks[:-i] - X_peaks[i:])==0:
            #  return 0
        #  if max(X_peaks[:-i] - X_peaks[i:]) <= max(np.abs(dXdt))*dt:
            #  return i
    #  return 0
    #  n_groups = len(np.where(np.diff(sorted_X_peaks)>(max(np.abs(dXdt))*dt))[0])
    #  if n_groups > 0:
        #  return n_groups+1
    #  if
def period_temporal(X, dt):
    dXdt = np.gradient(X)
    peaks_idx = np.where(np.diff(np.sign(dXdt))<0)
    X_peaks = X[peaks_idx]
    if np.max(X)-np.min(X) < 0.01:
        return 0, 0
    max_period = 8
    for i in range(1, min(max_period, len(X_peaks)-1)+1):
        if max(X_peaks[i:] - X_peaks[:-i]) < 0.02:
            return i, dt*(peaks_idx[0][-1]-peaks_idx[0][-1-i])
    return np.nan, np.nan
