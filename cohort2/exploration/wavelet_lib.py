import matplotlib.pyplot as plt
import scipy.fftpack
import pandas as pd
import numpy as np
from scipy.ndimage.interpolation import shift
from scipy import signal

def my_shifter(b):
    length = len(b)
    end = length
    start = -1 * (end -1)
    #c = np.array[]
    d = []
    for i in range(start,end):
        shifted = shift(b, i, cval=0)
        d.append(shifted)
    return np.vstack(d)  


def my_wavelet_transform(a,my_wave):
    wt = np.dot(my_shifter(a),my_wave)
    length = len(a)
    if length%2 == 1: #if odd
        start = length/2
        end = length/2 * -1
        wt = wt[start:end]
    else:
        start = length/2
        end = length/2 * -1 + 1
        wt = wt[start:end]

    return np.flip(wt,0)

def smooth_amplitude(wt):
    wtr = np.real(wt)
    pos_neg = []
    last_flag = ''
    flipper = 0
    for i,num in enumerate(wtr):
        if num < 0:
            flag = 'neg'
        else:
            flag = 'pos'
        if last_flag == '':
            last_flag = flag
        if last_flag == flag:
            pos_neg.append(flipper)
            last_flag = flag
        else:
            flipper += 1
            pos_neg.append(flipper)
            last_flag = flag
    my_dict = {}
    for i in set(pos_neg):
        idx = [j for j,num in enumerate(pos_neg) if num == i]
        start = min(idx)
        end = max(idx)+1
        my_max = max( abs(wtr[start:end]))
        my_dict[i]=my_max
    mag_reduction = [my_dict[i] for i in pos_neg]
    return wtr/mag_reduction