import pandas as pd
import numpy as np
import datetime as dt
from scipy.interpolate import interp1d, Akima1DInterpolator
import datetime
from datetime import datetime as dt
from pylab import *
from sklearn import preprocessing
import glob


def loadHighwayData(csvfile="../../I15S_data2.csv"):
    _df = pd.read_csv(csvfile)
    _df['WeekdayWeekend'] = _df['Timestamp'].apply(lambda x: strTimestampToWeekDayEnd(x))
    _df['WeekdayNumber'] = _df['Timestamp'].apply(lambda x: strTimestampToWeekdayNum(x))
    return _df


def prettytime(x):
    # minutes = x*5
    hours = x * 5 // 60
    minutes = (x * 5) - hours * 60
    if hours < 10:
        fhours = '0' + str(hours)
    else:
        fhours = str(hours)

    if minutes < 10:
        fminutes = '0' + str(minutes)
    else:
        fminutes = str(minutes)

    return fhours + ":" + fminutes


def interpolate(meanVector, type, factor):
    y = meanVector
    y_len = len(y)
    x = np.arange(0, y_len)

    if type == 'akima':
        interpolate = Akima1DInterpolator(x, y)
    elif type == 'cubic':
        interpolate = interp1d(x, y, kind='cubic')
    elif type == 'linear':
        interpolate = interp1d(x, y, kind='linear')
    else:
        interpolate = Akima1DInterpolator(x, y)

    myArray = ''
    mid_factor = factor / 2

    for i in range(factor):
        my_x = np.arange(i, y_len, factor)
        try:
            myArray += interpolate(my_x)
        except:
            myArray = interpolate(my_x)
        np.append(myArray, interpolate(my_x), axis=0)

    my_x = np.arange(mid_factor, y_len, factor)

    if type == 'akima':
        extrapolate = Akima1DInterpolator(my_x, myArray / factor)
    elif type == 'cubic':
        extrapolate = interp1d(my_x, myArray / factor, kind='cubic')
    elif type == 'linear':
        extrapolate = interp1d(my_x, myArray / factor, kind='linear')
    else:
        extrapolate = Akima1DInterpolator(my_x, myArray / factor)

    new_x = np.arange(mid_factor, y_len - mid_factor)
    interpolated = extrapolate(np.arange(mid_factor, y_len - mid_factor))

    # pad front and back with mean vector

    xprime = np.append(np.arange(0, mid_factor), new_x)
    xprime = np.append(xprime, np.arange(max(xprime) + 1, y_len))
    yprime = np.append(y[:mid_factor], interpolated)
    yprime = np.append(yprime, y[-mid_factor:])

    return xprime, yprime


def smooth_vector(vector, type='akima', factor=6):
    meanVector = vector
    smoothedVector = interpolate(meanVector, type, factor)[1]
    diff = meanVector - smoothedVector  # Wiggle magnitude
    diffVector = diff / np.sqrt(sum([i ** 2 for i in diff]))  # Normalize Diff vector
    timelabels = interpolate(meanVector, type, factor)[0]

    prettyTime = []
    for i in timelabels:
        prettyTime.append(prettytime(i))

    meanVector_scaled = preprocessing.scale(meanVector)
    smoothedVector_scaled = preprocessing.scale(smoothedVector)

    vectors = {'meanVector': meanVector, 'meanVector_scaled': meanVector_scaled, 'smoothedVector': smoothedVector,
               'smoothedVector_scaled': smoothedVector_scaled, 'diffVector': diffVector, 'timelabels': timelabels,
               'prettyTime': prettyTime}

    return vectors


def strTimestampToWeekdayWeekend(ts):
    mydate = datetime.date(int(ts[0:4]), int(ts[5:7]), int(ts[8:10]))
    if mydate.weekday() < 5:
        mydatetype = 'Weekday'
    else:
        mydatetype = 'Weekend'
    return mydate.weekday(), mydatetype


def strTimestampToWeekdayNum(ts):
    mydate = datetime.date(int(ts[0:4]), int(ts[5:7]), int(ts[8:10]))
    return mydate.weekday()


def strTimestampToWeekDayEnd(ts):
    mydate = datetime.date(int(ts[0:4]), int(ts[5:7]), int(ts[8:10]))
    if mydate.weekday() < 5:
        mydatetype = 'Weekday'
    else:
        mydatetype = 'Weekend'
    return mydatetype


def chartMetrics(_df, title, type='akima', factor=8, days='All', metrics='All', byStation=False, stationGrid=False,
                 output_file=False):
    if days == 'Weekdays':
        _df = _df[_df['WeekdayWeekend'] == 'Weekday']
    elif days == 'Weekends':
        _df = _df[_df['WeekdayWeekend'] == 'Weekend']

    if metrics == 'All':
        metrics = ['AvgDensity', 'AvgOccupancy', 'TotalFlow', 'AvgSpeed']
        tick_count = 36
        subplot_height = 10
    else:
        metrics = [metrics]
        tick_count = 24
        subplot_height = 20

    if byStation:
        subplotByStation(_df, metrics, type, factor, title, tick_count, subplot_height)
    else:
        if stationGrid:
            subplot_height = 80
            tick_count = 48
            showstationGrid(_df, metrics, type, factor, title, tick_count, subplot_height, stationGrid)
        else:
            subplotMeanWiggle(_df, metrics, type, factor, title, tick_count, subplot_height)

    if output_file:
        _df.to_csv(output_file)


def subplotMeanWiggle(dftemp, metrics, type, factor, title, tick_count, subplot_height):
    # Start subplotMeanWiggle
    fig = plt.figure(figsize=(20, subplot_height))

    for i, m in enumerate(metrics):
        mv = np.array(dftemp[['Time', m]].groupby(['Time']).mean()[m])

        vectors = smooth_vector(mv, type, factor)

        ax = fig.add_subplot(2, len(metrics), i + 1)
        plt.plot(vectors['meanVector_scaled'], linewidth=.4, color="black")
        plt.plot(vectors['timelabels'], vectors['smoothedVector_scaled'], linewidth=.6)
        for j in range(0, 288, 12):
            plt.axvline(x=i, linewidth=.3, color='gray')
        ax.set_xticks(range(0, 288, tick_count))
        ax.set_xticklabels(vectors['prettyTime'][::tick_count])
        plt.title(m + ":" + str(title))

        ax = fig.add_subplot(2, len(metrics), i + len(metrics) + 1)
        plt.plot(vectors['timelabels'], vectors['diffVector'], color="blue", linewidth=.5)
        plt.title(m + ": Normalized Wiggle Magnitude")
        plt.ylim(-.5, .5)
        for i in range(0, 288, 12):
            plt.axvline(x=i, linewidth=.3, color='gray')
        # plt.yaxis(vectors['prettyTime'])
        ax.set_xticks(range(0, 288, tick_count))
        ax.set_xticklabels(vectors['prettyTime'][::tick_count])
    plt.show()


def subplotByStation(dftemp, metrics, type, factor, title, tick_count, subplot_height):
    # Start subplotByStation
    # just perform analysis on first metric
    metrics = metrics[0]

    fig = plt.figure(figsize=(20, subplot_height))

    # df = {}
    for s in list(dftemp['Station'].unique()):
        data = dftemp[dftemp['Station'] == s]

        # my_max = data[metrics].max()
        # my_min = data[metrics].min()
        mv = np.array(
            data[['Time', metrics]].groupby(['Time']).mean()[metrics])
        vectors = smooth_vector(mv, type, factor)

        df_temp = pd.DataFrame.from_records(vectors)
        df_temp['station'] = s

        ax = fig.add_subplot(2, 1, 1)
        plt.plot(df_temp['timelabels'], df_temp['smoothedVector'], label=s)
        for i in range(0, 288, 12):
            plt.axvline(x=i, linewidth=.3, color='gray')
        ax.set_xticks(range(0, 288, tick_count))
        ax.set_xticklabels(vectors['prettyTime'][::tick_count])
        plt.title(str(title))

        ax = fig.add_subplot(2, 1, 2)
        plt.plot(df_temp['timelabels'], df_temp['diffVector'], label=s, linewidth=.5)
        plt.title("Normalized Wiggles Magnitude (diff from mean)")
        plt.ylim(-.5, .5)
        for i in range(0, 288, 12):
            plt.axvline(x=i, linewidth=.1, color='gray')
        ax.set_xticks(range(0, 288, tick_count))
        ax.set_xticklabels(df_temp['prettyTime'][::tick_count])
    plt.show()


def showstationGrid(dftemp, metrics, type, factor, title, tick_count, subplot_height, stationGrid):
    metrics = metrics[0]

    fig = plt.figure(figsize=(30, subplot_height))

    df = {}

    stations = list(dftemp.sort_values(['Latitude'], ascending=False)['Station'].unique())
    l = len(stations)

    my_max = dftemp[dftemp['Station'].isin(stations)][metrics].mean() * 5

    k = 1
    for s in stations:
        data = dftemp[dftemp['Station'] == s]
        lat = data['Latitude'].min()
        lon = data['Longitude'].min()

        mv = np.array(
            data[['Time', metrics]].groupby(['Time']).mean()[metrics])
        vectors = smooth_vector(mv, type, factor)

        df_temp = pd.DataFrame.from_records(vectors)
        df_temp['station'] = s

        ax = fig.add_subplot(l, l // 3, k)
        plt.plot(df_temp['timelabels'], df_temp['smoothedVector'], label=s)
        for i in range(0, 288, 12):
            plt.axvline(x=i, linewidth=.3, color='gray')
        ax.set_ylim(0, my_max)
        ax.set_xticks(range(0, 288, tick_count))
        ax.set_xticklabels(vectors['prettyTime'][::tick_count])
        plt.title("Latitude:" + str(lat))

        ax = fig.add_subplot(l, l // 3, k + l)
        plt.plot(df_temp['timelabels'], df_temp['diffVector'], label=s)
        for i in range(0, 288, 12):
            plt.axvline(x=i, linewidth=.3, color='gray')
        ax.set_ylim(-0.5, 0.5)
        ax.set_xticks(range(0, 288, tick_count))
        ax.set_xticklabels(vectors['prettyTime'][::tick_count])
        plt.title("Latitude:" + str(lat))

        k += 1

    plt.show()


def getRankOneStations(_df):
    # Rank1 Stations:
    rank1 = [1108313, 1108315, 1108317, 1108328, 1108331, 1108339, 1108341, 1108343, 1108351, 1108353, 1108360,
             1108372, 1108389, 1108401, 1108413, 1108419, 1108421, 1108423, 1108427, 1108429, 1108465, 1108473,
             1108486, 1108512, 1108523, 1108531, 1108543, 1108547, 1108560, 1108562, 1108564, 1108572, 1108582,
             1108592, 1108597, 1108623, 1108625, 1108627, 1108649, 1108661, 1108687, 1108693, 1108700, 1108717,
             1108728, 1108739, 1108741, 1108743, 1108745, 1108760, 1111514, 1111526, 1111531, 1111535, 1111557,
             1111569, 1111570, 1111575, 1112989, 1113126, 1113138, 1113147, 1113292, 1113318, 1113364, 1113720,
             1113740, 1115240, 1115450, 1115486, 1115537, 1115612, 1115616, 1115624, 1115649, 1115656, 1115663,
             1115721, 1115739, 1115771, 1115779, 1115787, 1115811, 1115820, 1115838, 1115897, 1115921, 1115929,
             1115937, 1115946, 1116092, 1116098, 1116119, 1116133, 1116139, 1116145, 1116158, 1116318, 1117836,
             1117850, 1117899, 1118013, 1118170, 1118260, 1118521, 1118529, 1118707, 1118796, 1118957, 1119528,
             1119645, 1119653, 1119679, 1119683, 1119689, 1119694, 1119699, 1119749, 1119762, 1119842, 1119850,
             1119865, 1119871, 1119890, 1119897, 1119934, 1119947, 1119954, 1119960, 1119966, 1119972, 1119978,
             1119984, 1119990, 1119997, 1120356, 1120362, 1121037, 1121038, 1121105, 1121112, 1121118, 1122394,
             1122469, 1122479, 1122507, 1122552, 1122560, 1122575, 1122594, 1122645, 1122646, 1123030, 1123031,
             1123078, 1123081, 1125314, 1125348, 1125353, 1125689, 1125836, 1125865, 1125872, 1125879]
    return _df[_df['Station'].isin(rank1)]


def plotAllYears(_list, _title, j, akima, chartType, fig):
    ax = fig.add_subplot(2, 2, j)
    plt.title(_title)
    legend_items = []
    for a in _list:
        _df = pd.read_csv(a, sep=',', header=None)
        vectors = smooth_vector(_df.values[0], type='akima', factor=akima)
        plt.plot(vectors['timelabels'], vectors[chartType])
        legend_items.append(a[a.find('grouping') - 5:a.find('grouping') - 1])
        # for i in range(0,288,12):
        #    plt.axvline(x=i, linewidth=.3, color='gray')
        ax.set_xticks(range(0, 288, 24))
        ax.set_xticklabels(vectors['prettyTime'][::24])
        plt.legend([b for b in legend_items])
        j += 1


def getWigglesForAllYears():
    all_means_weekday = glob.glob("../cohort1/final/data/weekday/total_flow_weekday_mean_vector.pivot_*")
    all_means_weekend = glob.glob("../cohort1/final/data/weekend/total_flow_weekend_mean_vector.pivot_*")

    fig = plt.figure(figsize=(20, 10))

    plotAllYears(all_means_weekday, "Weekday Mean Flow", 1, 12, 'smoothedVector', fig)
    plotAllYears(all_means_weekday, "Weekend Wiggle Magnitude", 2, 12, 'diffVector', fig)
    plotAllYears(all_means_weekend, "Weekend Mean Flow", 3, 12, 'smoothedVector', fig)
    plotAllYears(all_means_weekend, "Weekend Wiggle Magnitude", 4, 12, 'diffVector', fig)
