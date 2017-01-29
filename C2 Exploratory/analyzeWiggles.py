
import pandas as pd
import numpy as np
import datetime as dt
from scipy.interpolate import interp1d, Akima1DInterpolator


def interpolate(meanVector, type, factor):
    y = meanVector
    y_len = len(y)
    x = np.arange(0,y_len)

    if type=='akima':
        interpolate = Akima1DInterpolator(x, y)
    elif type=='cubic':
        interpolate = interp1d(x, y, kind='cubic')
    elif type=='linear':
        interpolate = interp1d(x, y, kind='linear')
    else:
        interpolate = Akima1DInterpolator(x, y)



    myArray = ''
    mid_factor = factor/2

    for i in range(factor):
        my_x = np.arange(i,y_len, factor)
        try:
            myArray += interpolate(my_x)
        except:
            myArray = interpolate(my_x)
        np.append(myArray, interpolate(my_x), axis=0)

    my_x = np.arange(mid_factor,y_len, factor)

    if type=='akima':
        extrapolate = Akima1DInterpolator(my_x, myArray/factor)
    elif type=='cubic':
        extrapolate = interp1d(my_x, myArray/factor, kind='cubic')
    elif type=='linear':
        extrapolate = interp1d(my_x, myArray/factor, kind='linear')
    else:
        extrapolate = Akima1DInterpolator(my_x, myArray/factor)


    new_x = np.arange(mid_factor,y_len-mid_factor)
    interpolated = extrapolate( np.arange(mid_factor,y_len-mid_factor))

    #pad front and back with mean vector

    xprime = np.append(np.arange(0,mid_factor), new_x)
    xprime = np.append(xprime, np.arange(max(xprime)+1,y_len))
    yprime = np.append(y[:mid_factor], interpolated)
    yprime = np.append(yprime, y[-mid_factor:])

    return xprime, yprime



def smooth(mvpath, type='akima', factor=6):
    meanVector = pd.read_csv(mvpath, header=None).values[0]
    smoothedVector = interpolate(meanVector, type, factor )[1]
    diff = meanVector - smoothedVector #Wiggle magnitude
    diffVector = diff/np.sqrt(sum([i**2 for i in diff])) # Normalize vector
    timelabels = interpolate(meanVector, type, factor )[0]

    vectors = {'meanVector': meanVector, 'smoothedVector': smoothedVector, 'diffVector': diffVector, 'timelabels':timelabels}

    return vectors





