import matplotlib.pyplot as plt
import scipy.fftpack
import pandas as pd
import numpy as np
from scipy import signal
import time
import datetime as dt
import matplotlib
import matplotlib.dates as mdates
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import wavelet_lib as wl

data_dir = "../data/External/"
data_5min_path = data_dir + "station_5min/2015/d11/"
meta_path = data_dir + "meta/2015/d11/"

df = pd.read_csv( data_dir + '2015_station_days_with_meta.csv.zip', usecols=range(1,20))
df = df.ix[df['Partition'] == 'Weekdays']
flow_df = df.pivot(index='Station', columns='Time', values='Flow')

def plot_morlet(omega, scaling, station=1108148):
    a = flow_df[flow_df.index==1108148]
    a = np.array(a.transpose())
    a = np.concatenate(a)
    a = np.repeat(a, 5)

    plt.figure(figsize=(15,3))
    my_wave = signal.morlet(len(a),w=omega,s=scaling)
    #print len([i for i in my_wave if abs(i)>.01])

    plt.plot(my_wave)
    mid = len(my_wave)/2
    plt.vlines([mid, mid+60, mid - 60], -.8, .8, alpha=0.25, colors='red')
    plt.vlines([mid-15, mid-45, mid+15, mid+45], -.8, .8, linestyles='dashed', alpha=0.1)
    plt.vlines([mid+30, mid-30], -.8, .8, alpha=0.15)
    plt.xticks([mid, mid+60, mid-60], ['0hr', '1hr', '-1hr'])
    plt.show()

    plt.figure(figsize=(15,8))
    wt = wl.my_wavelet_transform(a,my_wave)
    plt.plot(wt, color='b', label = 'transform (omega {})'.format(str(omega)))
    plt.plot(a, color='r', label = 'original signal')
    plt.plot(wl.smooth_amplitude(wt)*100, color='g', label = 'tranform smoothed')
    plt.vlines([(len(a)/24)*j for j in range(25)],-1000,1000, alpha=0.25, colors='red')
    plt.vlines([(len(a)/24)*j+30 for j in range(25)],-1000,1000, alpha=0.1, linestyles='dashed')
    plt.ylabel('Flow')
    xticks = range(0, 1441, 60)
    plt.xticks( xticks, ['{:02}:00'.format(i) for i in range(len(xticks))], rotation=45 )

    plt.legend()
    plt.show()

meta_file = meta_path + 'd11_text_meta_2015_12_17.txt'
meta_df = pd.read_csv( meta_file, delimiter='\t' ) \
    .rename( columns={'ID':'Station'}) \
    .set_index('Station')

a = flow_df[flow_df.index==1108148]
a = np.array(a.transpose())
a = np.concatenate(a)
a = np.repeat(a, 5)
my_wave = signal.morlet( len(a), w=3, s=8 )

def wiggle_heatmap(freeway=5, direction='S', lanetype='ML'):
    idx1 = meta_df['Fwy'] == freeway
    idx2 = meta_df['Dir'] == direction
    idx3 = meta_df['Type'] == lanetype
    fwy_df = meta_df.ix[idx1&idx2&idx3,:].sort_values('Abs_PM', ascending=False)

    my_list = []
    for station in fwy_df.index:
        a = flow_df[flow_df.index==station]
        a = np.array(a.transpose())
        a = np.concatenate(a)
        a = np.repeat(a, 5)
        wt = wl.my_wavelet_transform(a,my_wave)
        my_list.append(wl.smooth_amplitude(wt))
    my_array = np.vstack(my_list)

    x_lims = [dt.datetime(2017,1,1,0,0,0),dt.datetime(2017,1,1,23,59,59)]
    x_lims = mdates.date2num(x_lims)
    y_lims = [0, len(my_list)]

    fig, ax = plt.subplots()
    fig.set_size_inches(18.5, 10.5)
    title = 'Wiggle Propagation on {} {}'.format(fwy_df.Fwy.unique()[0], fwy_df.Dir.unique()[0])
    ax.set_title(title, fontsize=20)
    ax.set_xlabel('Time of Day')
    ax.set_ylabel('Station Order')
    #plt.xlabel('Time of Day')
    #plt.ylabel('Station Order')

    ax.imshow(np.real(my_array), cmap='hot', extent = [x_lims[0], x_lims[1],  y_lims[0], y_lims[1]],
          aspect='auto')

    vlines = [dt.datetime(2017,1,1,i,0,0) for i in range(24)]
    ax.vlines( vlines, 0, 101, colors='cyan', linestyles='dashed', linewidth=2)

    mask = (meta_df.Fwy==freeway) & (meta_df.Dir==direction) & (meta_df.Type.isin(['FF','ML']))
    m = meta_df[mask].sort_values('Abs_PM')
    i, ff, ffn = 0, [], []
    for n in m.iterrows():
        if n[1].Type == 'ML':
            i += 1
        else:
            ff.append(i)
            ffn.append(n[1].Name)
    ax.hlines( ff, x_lims[0], x_lims[1], colors='magenta', linestyles='dashed', linewidth=2 )

    ax.xaxis_date()

    date_format = mdates.DateFormatter('%H:%M')

    ax.xaxis.set_major_formatter(date_format)

    fig.autofmt_xdate()

    plt.show()

    return my_array

idx1 = meta_df['Fwy'] == 5
idx2 = meta_df['Dir'] == 'S'
idx3 = meta_df['Type'] == 'ML'
fwy_df = meta_df.ix[idx1&idx2&idx3,:].sort_values('Abs_PM', ascending=False)

def wiggle_heatmap_segment( small, start_time, end_time ):
    fig, ax = plt.subplots()
    fig.set_size_inches(6, 10)

    title = 'Wiggle Propagation on {} {} between {} and {}'.format(
        fwy_df.Fwy.unique()[0], fwy_df.Dir.unique()[0], start_time, end_time )
    ax.set_title(title)
    ax.set_xlabel('Time of Day')
    ax.set_ylabel('Station Order')

    vlines = [i*60 for i in range((end_time-start_time)+1)]
    plt.xticks(vlines, ['{:02}:00'.format(i/60 + start_time) for i in vlines])
    ax.vlines( vlines, 0, 101, colors='cyan', linestyles='dashed', linewidth=2)
    ax.imshow(small, cmap='hot', aspect='auto' )

    plt.show()
