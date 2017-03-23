# import pandas as pd
import numpy as np
# import gzip
# import datetime as dt
# from os import listdir
# from os.path import isfile, join
# import time
# import itertools

# from operator import itemgetter

# import matplotlib.pyplot as plt

# from sklearn import cluster
# from sklearn.neighbors import kneighbors_graph
# from sklearn.cross_validation import train_test_split
# from sklearn.metrics import confusion_matrix

import sys

sys.path.append('../')


# import c2utils.timer as timer


def count_bad_sensors(df):
    count_nan_df = df
    count_nan_df.loc[:, 'Station'] = count_nan_df['Station'].astype(str)
    count_nan_df = count_nan_df[['Station', 'Timestamp', 'TotalFlow', 'AvgOccupancy', 'AvgSpeed']]
    num = count_nan_df._get_numeric_data()
    num[num > 0] = 0
    count_nan_df = count_nan_df.replace(np.nan, 1)
    count_nan_df = count_nan_df.groupby('Station').sum().reset_index()
    count_nan_df.loc[:, 'Total'] = count_nan_df['TotalFlow'] + count_nan_df['AvgOccupancy'] + count_nan_df['AvgSpeed']
    count_nan_df = count_nan_df.sort_values('Total')
    return count_nan_df


def calc_avg_obs(df):
    count_nan_df = df
    count_nan_df['Station'] = count_nan_df['Station'].astype(str)
    count_nan_df = count_nan_df[['Station', '% Observed']]
    count_nan_df = count_nan_df.groupby('Station').mean().reset_index()
    return count_nan_df
