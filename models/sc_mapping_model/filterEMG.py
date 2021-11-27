# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 13:55:15 2020

@author: AlexVosk
"""

import numpy as np
from scipy.signal import butter, lfilter

def butter_bandpass(lowcut, highcut, fs, order=3):
    nyq = 0.5 * fs
    # nyq = 1024
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_lowpass(cutoff, fs, order=3):
    nyq = 0.5 * fs
    # nyq = 1024
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_bandstop_filter(data, lowcut, highcut, fs, order):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    i, u = butter(order, [low, high], btype='bandstop')
    y = lfilter(i, u, data)
    return y


# main filter
def filterEMG(chunk, fmin, fmax, fs):
    if fmin > 0:
        bband, aband = butter_bandpass(lowcut=fmin, highcut=fmax, fs = fs, order=3)
    else:
        bband, aband = butter_lowpass(cutoff = fmax, fs = fs, order=3)
    
    chunk = lfilter(bband, aband, chunk, axis=0)
    chunk = np.abs(chunk)

    blow, alow = butter_lowpass(cutoff = 2, fs = fs, order=5)
    chunk = lfilter(blow, alow, chunk, axis=0)

    return chunk

