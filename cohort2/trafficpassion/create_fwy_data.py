import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import time

def reduce_data_by_dict(df, keyval_dict):
    for key, val in keyval_dict.iteritems():
        df = df[df[key] == val]
    return df


def create_freeway_stats_df(_df, _meta_redux):
    # Get the Station's Absolute marker by merging meta
    freeway = _df.merge(_meta_redux, 
                              left_on=['Station', 'District','Freeway #', 'Direction'], 
                              right_on=['ID', 'District', 'Fwy', 'Dir'])
    
    #print "freeway and meta merged"
    
    #print freeway[:5]
    #print freeway[:-5]
    
    #freeway = freeway[freeway['% Observed'] > 95 ]
    
    index_fields = ['timeOfDay', 'Abs_PM']
    stats = ['mean','std']
    
    #Reduce columns of dataset only to columns of interest
    freeway_metrics = freeway[['Total Flow', 'Avg Occupancy', 'Avg Speed', 'timeOfDay', 'Abs_PM'] ]

    fwy_grouping = freeway_metrics[['Total Flow', 
                                    'Avg Occupancy', 'Avg Speed', 
                                    'timeOfDay', 'Abs_PM'] ].groupby(index_fields)
    
    metrics = fwy_grouping.agg([np.mean, np.std])
    
    metric_names = set([a[0] for a in metrics.columns if a[0] not in index_fields])
    metric_stats = ['mean+std', 'mean', 'mean-std']
    
    new_cols = []
    for a in metric_names:
        for b in metric_stats:
            name = "_".join([a.replace(" ", ""),b])
            #print name
            new_cols.append(name)
            if b == 'mean+std':
                metrics[name] = metrics[a]['mean']+ metrics[a]['std']
            elif b == 'mean-std':
                metrics[name] = metrics[a]['mean']- metrics[a]['std']
            else:
                metrics[name] = metrics[a]['mean']
                
    fields = new_cols+index_fields
    
    #print fields
    
    metrics = metrics.reset_index()
    #print metrics.columns
    metrics = metrics[fields]

    return metrics




def import_fwy_data(_fwy,_dir,_daynum):
    raw_5_min_filepath = '../../../five_min_frame.csv'
    raw_meta_filepath = '../../../d11_traffic_data/meta/d11/d11_text_meta_2015_01_01.txt'
    
    weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    myname = "".join([ "i",
                      str(_fwy),
                      str(_dir), 
                      "_", 
                      weekday[_daynum]])
    filepath = "".join(["../data/metric_statistics/",myname,".csv"])

    meta = pd.read_csv(raw_meta_filepath, sep='\t')
    meta = meta[['ID', 'Fwy','District', 'Dir','Abs_PM']]

    raw_5_min_data = pd.read_csv(raw_5_min_filepath, nrows=10000000)

    #print 'traffic data import complete'

    raw_5_min_data['time'] = pd.to_datetime(raw_5_min_data['Timestamp'], format="%m/%d/%Y %H:%M:%S")
    raw_5_min_data['timeOfDay'] = raw_5_min_data['time'].apply(lambda x: x.strftime("%H:%M")) 
    raw_5_min_data['Weekday'] = raw_5_min_data['time'].dt.weekday

    #print "traffic data processed"  

    keyval_dict = {"District": 11, 
                   "Freeway #": _fwy, 
                   "Lane Type": 'ML', 
                   "Direction": _dir}
    thresholds_alldays = {"Total Flow": [reduce_data_by_dict(raw_5_min_data, keyval_dict)['Total Flow'].mean(), 
     reduce_data_by_dict(raw_5_min_data, keyval_dict)['Total Flow'].std()],
"Avg Speed": [reduce_data_by_dict(raw_5_min_data, keyval_dict)['Avg Speed'].mean(),
      reduce_data_by_dict(raw_5_min_data, keyval_dict)['Avg Speed'].std()],
"Avg Occupancy": [reduce_data_by_dict(raw_5_min_data, keyval_dict)['Avg Occupancy'].mean(),
        reduce_data_by_dict(raw_5_min_data, keyval_dict)['Avg Occupancy'].std()]}
    
    #print thresholds_alldays

    keyval_dict = {"District": 11, 
                   "Freeway #": _fwy, 
                   "Lane Type": 'ML', 
                   "Direction": _dir,
                   "Weekday": _daynum} 

    freeway_redux = reduce_data_by_dict(raw_5_min_data, keyval_dict)
    #print "freeway data reduced"

    meta_dict= {"District": 11, "Fwy": _fwy,  "Dir": _dir}
    meta_redux = reduce_data_by_dict(meta, meta_dict)
    #print "meta data reduced"

    df = create_freeway_stats_df(freeway_redux, meta_redux)
    #print "stats created"

    df.to_csv(filepath)

    return df, thresholds_alldays


