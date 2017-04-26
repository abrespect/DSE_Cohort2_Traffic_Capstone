import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import pandas as pd
import numpy as np
import time
from os import listdir
from os.path import isfile, join
from datetime import time

import datetime as dt

import glob


import sys
sys.path.append('../')
import trafficpassion.AnalyzeWiggles as aw

data_5min_path = "../../../data/5min/2015/d11/"
meta_path = "../../../data/meta/2015/d11/"

#get all files to process
onlyfiles = [f for f in listdir(data_5min_path) if isfile(join(data_5min_path, f))]

#print onlyfiles[0:3]

colnames = [
    'Timestamp','Station','District','Freeway','Direction_of_Travel',
    'LaneType','StationLength','Samples',
    'Perc_Observed','TotalFlow','AvgOccupancy','AvgSpeed',
    'Lane1_Samples','Lane1_Flow','Lane1_AvgOcc','Lane1_AvgSpeed','Lane1_Observed',
    'Lane2_Samples','Lane2_Flow','Lane2_AvgOcc','Lane2_AvgSpeed','Lane2_Observed',
    'Lane3_Samples','Lane3_Flow','Lane3_AvgOcc','Lane3_AvgSpeed','Lane3_Observed',
    'Lane4_Samples','Lane4_Flow','Lane4_AvgOcc','Lane4_AvgSpeed','Lane4_Observed',
    'Lane5_Samples','Lane5_Flow','Lane5_AvgOcc','Lane5_AvgSpeed','Lane5_Observed',
    'Lane6_Samples','Lane6_Flow','Lane6_AvgOcc','Lane6_AvgSpeed','Lane6_Observed',
    'Lane7_Samples','Lane7_Flow','Lane7_AvgOcc','Lane7_AvgSpeed','Lane7_Observed',
    'Lane8_Samples','Lane8_Flow','Lane8_AvgOcc','Lane8_AvgSpeed','Lane8_Observed'
]
colnames = [c.lower() for c in colnames]

from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql.functions import hour, mean,minute, stddev, count,max as psmax,min as psmin


struct_list = [
    StructField("timestamp",TimestampType(),True),
    StructField("station",IntegerType(),True),
    StructField("district",IntegerType(),True),
    StructField("freeway",IntegerType(),True),
    StructField("direction_of_travel",StringType(),True),
    StructField("lanetype",StringType(),True),
    StructField("stationlength",DoubleType(),True),
    StructField("samples",IntegerType(),True),
    StructField("perc_observed",IntegerType(),True),
    StructField("totalflow",IntegerType(),True),
    StructField("avgoccupancy",DoubleType(),True),
    StructField("avgspeed",DoubleType(),True),
    StructField("lane1_samples",IntegerType(),True),
    StructField("lane1_flow",IntegerType(),True),
    StructField("lane1_avgocc",DoubleType(),True),
    StructField("lane1_avgspeed",DoubleType(),True),
    StructField("lane1_observed",IntegerType(),True),
    StructField("lane2_samples",IntegerType(),True),
    StructField("lane2_flow",IntegerType(),True),
    StructField("lane2_avgocc",DoubleType(),True),
    StructField("lane2_avgspeed",DoubleType(),True),
    StructField("lane2_observed",IntegerType(),True),
    StructField("lane3_samples",IntegerType(),True),
    StructField("lane3_flow",IntegerType(),True),
    StructField("lane3_avgocc",DoubleType(),True),
    StructField("lane3_avgspeed",DoubleType(),True),
    StructField("lane3_observed",IntegerType(),True),
    StructField("lane4_samples",IntegerType(),True),
    StructField("lane4_flow",IntegerType(),True),
    StructField("lane4_avgocc",DoubleType(),True),
    StructField("lane4_avgspeed",DoubleType(),True),
    StructField("lane4_observed",IntegerType(),True),
    StructField("lane5_samples",IntegerType(),True),
    StructField("lane5_flow",IntegerType(),True),
    StructField("lane5_avgocc",DoubleType(),True),
    StructField("lane5_avgspeed",DoubleType(),True),
    StructField("lane5_observed",IntegerType(),True),
    StructField("lane6_samples",IntegerType(),True),
    StructField("lane6_flow",IntegerType(),True),
    StructField("lane6_avgocc",DoubleType(),True),
    StructField("lane6_avgspeed",DoubleType(),True),
    StructField("lane6_observed",IntegerType(),True),
    StructField("lane7_samples",IntegerType(),True),
    StructField("lane7_flow",IntegerType(),True),
    StructField("lane7_avgocc",DoubleType(),True),
    StructField("lane7_avgspeed",DoubleType(),True),
    StructField("lane7_observed",IntegerType(),True),
    StructField("lane8_samples",IntegerType(),True),
    StructField("lane8_flow",IntegerType(),True),
    StructField("lane8_avgocc",DoubleType(),True),
    StructField("lane8_avgspeed",DoubleType(),True),
    StructField("lane8_observed",IntegerType(),True)
]

schema_struct = StructType(struct_list)

files = [data_5min_path + filename for filename in onlyfiles]

def load_data( spark ):
    rdd = spark.read.csv(
        files,
        header='false',
        timestampFormat='MM/dd/yyyy HH:mm:ss',
        schema=schema_struct,
        inferSchema='false'
    )

    #print rdd.take(1)

    station_time = (
        rdd.groupBy([
            'station',
            hour("timestamp").alias("hour"),
            minute("timestamp").alias("minute")
        ]).agg(
            mean("totalflow").alias("flow_mean"),
            stddev("totalflow").alias("flow_std"),
            count("totalflow").alias("flow_count"),
            psmax("totalflow").alias("flow_max"),
            psmin("totalflow").alias("flow_min")
        )
    )

    df = station_time.toPandas()

    #print df.station.unique().shape

    df['flow_std_plus_mean'] = df.flow_mean + df.flow_std
    df['flow_std_minus_mean'] = df.flow_mean - df.flow_std

    df['time'] = df.apply(lambda x:time(int(x.hour),int(x.minute)),axis = 1)

    df.sort_values('time',inplace=True)

    return df

from scipy.interpolate import interp1d, Akima1DInterpolator
from sklearn import preprocessing
def interpolate(meanVector, kind, factor):
    y = meanVector
    y_len = len(y)
    x = np.arange(0,y_len)

    interpolator = {
        'akima': Akima1DInterpolator(x, y),
        'cubic': interp1d(x, y, kind='cubic'),
        'linear': interp1d(x, y, kind='linear')
    }

    interpolate = interpolator[kind]

    mid_factor = factor/2

    interp = [interpolate(np.arange(i,y_len, factor)) for i in range(factor)]
    myArray = reduce(lambda x,y:x+y,interp)

    my_x = np.arange(mid_factor,y_len, factor)

    extrapolator = {
        'akima': Akima1DInterpolator(my_x, myArray/factor),
        'cubic': interp1d(my_x, myArray/factor, kind='cubic'),
        'linear': interp1d(my_x, myArray/factor, kind='linear')
    }

    extrapolate = extrapolator[kind]

    new_x = np.arange(mid_factor,y_len-mid_factor)
    interpolated = extrapolate( np.arange(mid_factor,y_len-mid_factor))

    #wut??
    #pad front and back with mean vector
    xprime = np.append(np.arange(0,mid_factor), new_x)
    xprime = np.append(xprime, np.arange(max(xprime)+1,y_len))
    yprime = np.append(y[:mid_factor], interpolated)
    yprime = np.append(yprime, y[-mid_factor:])

    return yprime


def smooth_vector(meanVector, kind='akima', factor=6):
    smoothedVector = interpolate(meanVector, kind, factor )
    diff = meanVector - smoothedVector
    diffVector = diff/np.linalg.norm(diff)

    return {
        'smoothedVector': smoothedVector,
        'diffVector': diffVector
    }

def loadMeta():
    meta_dir= meta_path + 'd11_text_meta_2015_*.txt'
    meta_files = glob.glob(meta_dir)

    meta_file_list = []
    for meta_file in meta_files:
        date = str('_'.join(meta_file.split('_')[4:7])).split('.')[0]
        df = pd.read_table(meta_file, index_col=None, header=0)
        date_col = pd.Series([date] * len(df))
        df['file_date'] = date_col
        # drop rows that are missing latitude / longitude values
        #df.dropna(inplace=True, subset=['Latitude', 'Longitude'], how='any')
        meta_file_list.append(df)

    meta_frame = pd.concat(meta_file_list).drop_duplicates(subset='ID', keep='last')

    usefwy = [ 56, 125, 805,  52, 163,   8,  15,   5, 905,  78,  94,  54]

    meta_frame = meta_frame[meta_frame.Fwy.apply(lambda x: x in usefwy)]

    #Add freeway name FwyDir
    meta_frame['freeway'] = meta_frame.Fwy.apply(str) + meta_frame.Dir

    r_c = {}
    for c in meta_frame.columns:
        r_c[c]=c.lower()

    meta_frame=meta_frame.rename(columns = r_c )
    return meta_frame

meta_df = loadMeta()
meta_df = meta_df[ meta_df.type.isin(['ML', 'OR', 'FR']) ]

i5s_mask = (meta_df.fwy==5) & (meta_df.dir=='S')
meta_group = meta_df[ i5s_mask ] \
    .sort_values('abs_pm', ascending=False) \
    .groupby('abs_pm')

postmiles = meta_df[i5s_mask].sort_values('abs_pm', ascending=False).abs_pm.unique()

station_set = []
stations = []

# Build clusters of OR/FR and surrounding mainline
prev_ml, next_ml = 0, 0
for i, pm in enumerate(postmiles):
    pm_df = meta_group.get_group(pm)
    types = pm_df.type.unique()

    # Find next_ml
    for j in range(i+1, len(postmiles)):
        next_df = meta_group.get_group(postmiles[j])
        if 'ML' in next_df.type.unique():
            next_ml = next_df[next_df.type=='ML'].iloc[0].id
            break
        next_ml = 0

    if ('OR' in types) | ('FR' in types):
        if prev_ml != 0:
            stations.append( prev_ml )
        stations = pm_df.id.unique().tolist()
        if next_ml != 0:
            stations.append( next_ml )
        station_set.append( stations )

    if 'ML' in types:
        prev_ml = pm_df[pm_df.type=='ML'].iloc[0].id

type_map = {'ML':'Main-Line', 'OR': 'ON-Ramp', 'FR':'OFF-Ramp'}

def make_maps_url( stations, fancy=False, only_ramps=False ):
    if fancy:
        url = 'http://maps.google.com/maps/api/staticmap?&size=1024x1024&zoom=14&maptype=roadmap&'
        marker = 'markers=color:{}|label:{}|{},{}&'
        for i, s in enumerate(stations):
            s_df = meta_df[meta_df.id==s].iloc[0]
            if only_ramps and (s_df.type=='ML'):
                continue
            color = 'blue' if s_df.type == 'ML' else 'red'
            label = '{}_[{}]_{}'.format(s_df.type, s_df.abs_pm, s_df.id )
            lat, lon = s_df.latitude, s_df.longitude
            url += marker.format(color, label, lat, lon)
        return url
    else:
        urls = []
        base_url = 'https://www.google.com/maps/place'
        for i, s in enumerate(stations):
            s_df = meta_df[meta_df.id==s].iloc[0]
            if only_ramps and (s_df.type=='ML'):
                continue
            label = '{} [{}] {} - {}'.format(type_map[s_df.type], s_df.abs_pm, s_df.id, s_df['name'] )
            lat, lon = s_df.latitude, s_df.longitude
            url = '{}/{},{}'.format(base_url, lat, lon)
            urls.append( [url, label] )
        return urls

def plot_ramp_wiggles( station_df, t_min=6, t_max=9, rampid=1108673, links=True, figsize=(15,5) ):

    found = False
    for stations in station_set:
        if rampid in stations:
            found = True
            break
    if not found:
        print 'could not find ramp station id {}'.format(rampid)
        return

    plt.figure(figsize = figsize)

    colors = ['#e41a1c','#377eb8','#4daf4a','#984ea3',
              '#ff7f00','#ffff33','#a65628','#f781bf','#999999']
    hddl=[]

    # sort stations by abs_pm
    abs_pm = [meta_df[meta_df.id==s].iloc[0].abs_pm for s in stations]
    stations = [x for (y,x) in sorted(zip(abs_pm,stations))]

    if links:
        for url in make_maps_url(stations, only_ramps=True ):
            print url[1], url[0]

    for idx, r in enumerate(stations):

        r_df = station_df.get_group(r).copy()
        vectors = smooth_vector(r_df['flow_mean'].values, 'akima', 24)
        r_df.loc[:,'smoothedVector'] = vectors['smoothedVector']
        r_df.loc[:,'diffVector'] = vectors['diffVector']

        s_df = meta_df[meta_df.id==r].iloc[0]
        width = 2.0 if s_df.type != 'ML' else 0.5
        linestyle = '--' if s_df.type != 'ML' else '-'
        label = '{} [ID: {}] {}'.format(type_map[s_df.type], s_df.id, s_df['name'] )

        r_df= r_df.set_index('time').sort_index().loc[dt.time(t_min, 0):dt.time(t_max, 0),:].reset_index()

        hddl += plt.plot(r_df['time'], r_df['diffVector'], color=colors[idx],
                         linewidth=width, label=label, linestyle=linestyle)

    plt.legend(handles=hddl, bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=2, mode="expand", borderaxespad=0., fontsize=10)

    #name = fwy_df[ fwy_df.id==p[1] ].name.tolist()[0]
    #plt.title('diffVector plot for %s %s %i (%s)'%(fwy,d,p[1],name))

    for i in range(0, len(r_df), 12):
        plt.axvline(x=r_df['time'].iloc[i], linewidth=0.5, color='gray')
        if i < (len(r_df)-6):
            plt.axvline(x=r_df['time'].iloc[i+6], linewidth=0.1, color='gray')

    ticks = [dt.time(i,0) for i in range(t_min, t_max+1)]
    ticktext = ['{}{}'.format((i if i < 13 else i%12), ('am' if i < 12 else 'pm')) for i in range(t_min, t_max+1)]
    plt.xticks(ticks, ticktext)

    plt.xlabel('Time of Day')
    plt.ylabel('Wiggle Magnitude (normalized)')
    plt.show()
