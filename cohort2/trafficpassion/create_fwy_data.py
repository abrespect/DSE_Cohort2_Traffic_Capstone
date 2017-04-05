import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import time

# Set global variables
metric_colnames =  ['Total Flow', 'Avg Occupancy', 'Avg Speed']
index_colnames = ['timeOfDay', 'Abs_PM']
helper_colnames = ['Weekday']

# Define Functions

##### reduce_data_by_dict
# This function is a universal function that takes a dict and selects dataframes based on the identified key value pair
def reduce_data_by_dict(df, keyval_dict):
    for key, val in keyval_dict.iteritems():
        df = df[df[key] == val]
    return df


##### get_fwy_data
# This function loads the raw, minute data (takes a LONG time to load).  From this it selects only 1 freeway and direction.
# It may make sense to run this only once, but the data for each freeway could get rather large.
# There's an opportunity to use spark RDD's to increase performance
def get_fwy_data(_fwy,_dir, overwrite=False, output_csv=False, nimportrows=-1):
    # Ensure proper naming convention for file
    myname = "".join([ "i",
                  str(_fwy),
                  str(_dir)])
    filepath = "".join(["../data/metric_statistics/",myname,".csv"])

    # Check to see if the file should be overwritten or if it is not available.
    try:
        if overwrite == False:
            freeway = pd.read_csv(filepath, sep='\t')
    except:
        overwrite = True

    if overwrite:
        # import raw data
        raw_5_min_filepath = '../../../five_min_frame.csv'

        if nimportrows == -1:
            raw_5_min_data = pd.read_csv(raw_5_min_filepath, nrows=nimportrows)
        else:
            raw_5_min_data = pd.read_csv(raw_5_min_filepath)

        raw_meta_filepath = '../../../d11_traffic_data/meta/d11/d11_text_meta_2015_01_01.txt'
        meta = pd.read_csv(raw_meta_filepath, sep='\t')

        # Filter raw and meta datasets by freeway and direction
        # Reduce raw_5_min data
        keyval_dict = {"District": 11, 
                   "Freeway #": _fwy, 
                   "Lane Type": 'ML', 
                   "Direction": _dir}
        redux_5_min = reduce_data_by_dict(raw_5_min_data, keyval_dict)
        
        #Reduce meta
        keyval_dict = {"District": 11, 
                   "Fwy": _fwy, 
                   "Dir": _dir}
        redux_meta = reduce_data_by_dict(meta, keyval_dict)
        
        # Create helper columns
        raw_5_min_data['time'] = pd.to_datetime(raw_5_min_data['Timestamp'], format="%m/%d/%Y %H:%M:%S")
        raw_5_min_data['timeOfDay'] = raw_5_min_data['time'].apply(lambda x: x.strftime("%H:%M")) 
        raw_5_min_data['Weekday'] = raw_5_min_data['time'].dt.weekday
        
        # Keep only columns used
        redux_5_min = raw_5_min_data[metric_colnames + helper_colnames +  ['Station', 'timeOfDay', 'District','Freeway #', 'Direction']]
        redux_meta = redux_meta[['ID', 'Fwy','District', 'Dir','Abs_PM']]
        
        # Get the Station's Absolute marker by merging meta
        freeway = redux_5_min.merge(redux_meta, 
                              left_on=['Station', 'District','Freeway #', 'Direction'],
                              right_on=['ID', 'District', 'Fwy', 'Dir'])

        # Export for later use
        if output_csv:
            freeway.to_csv(filepath)
    
    return freeway

##### get_fwy_dataByDay
# Using the existing freeway, this function restricts the dataset to a specific day of the week and writes the results to a csv
def get_fwy_dataByDay(df, _daynum, overwrite=False, output_csv=False): 
    weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    myname = "".join([ "i",
                str(_fwy),
                str(_dir), 
                "_", 
                weekday[_daynum]])
    
    # Check to see if the file should be overwritten or if it is not available.
    try:
        if overwrite == False:
            freewayByDay = pd.read_csv(filepath, sep='\t')
    except:
        overwrite = True
    
    if overwrite:
        keyval_dict = {"Weekday": _daynum} 
        freewayByDay = reduce_data_by_dict(df, keyval_dict)
    
    if output_csv:
        freewayByDay.to_csv(filepath)

    return freewayByDay



# Still working on this
def create_freeway_stats(df):
    index_fields = index_colnames()
    stats = ['mean','std']
    
    #Reduce columns of dataset only to columns of interest
    fwy_grouping = df[['Total Flow', 'Avg Occupancy', 'Avg Speed', 'timeOfDay', 'Abs_PM'] ].groupby(index_fields)

    metrics = fwy_grouping.agg([np.mean, np.std])
    metric_stats = ['mean+std', 'mean', 'mean-std']
    
    new_cols = []
    for a in metric_colnames():
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
    
    metrics = metrics.reset_index()
    metrics = metrics[fields]

    return metrics