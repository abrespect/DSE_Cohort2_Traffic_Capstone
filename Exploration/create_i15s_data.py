
data_5min_path = "./station_5min/2015/d11/"
import pandas as pd
import numpy as np
import gzip
import time
from bokeh.io import curdoc, vform, output_notebook, push_notebook, output_file, show
from bokeh.models import ColumnDataSource, HBox, VBox
from bokeh.models.widgets import Slider, Button, DataTable, DateFormatter, TableColumn
from bokeh.plotting import Figure,show
from bokeh.models.layouts import WidgetBox
from bokeh.layouts import row, column
from os import listdir
from os.path import isfile, join
from ipywidgets import interact
import datetime as dt

onlyfiles = [f for f in listdir(data_5min_path) if isfile(join(data_5min_path, f))]

colnames = ['Timestamp', 'Station', 'District', 'Freeway #', 'Direction', 'Lane Type', 'Station Length', 'Samples',
            '% Observed', 'TotalFlow', 'AvgOccupancy', 'AvgSpeed', 'Lane 1 Samples', 'Lane 1 Flow', 'Lane 1 Avg Occ',
            'Lane 1 Avg Speed', 'Lane 1 Observed', 'Lane 2 Samples', 'Lane 2 Flow', 'Lane 2 Avg Occ',
            'Lane 2 Avg Speed', 'Lane 2 Observed', 'Lane 3 Samples', 'Lane 3 Flow', 'Lane 3 Avg Occ',
            'Lane 3 Avg Speed', 'Lane 3 Observed', 'Lane 4 Samples', 'Lane 4 Flow', 'Lane 4 Avg Occ',
            'Lane 4 Avg Speed', 'Lane 4 Observed', 'Lane 5 Samples', 'Lane 5 Flow', 'Lane 5 Avg Occ',
            'Lane 5 Avg Speed', 'Lane 5 Observed', 'Lane 6 Samples', 'Lane 6 Flow', 'Lane 6 Avg Occ',
            'Lane 6 Avg Speed', 'Lane 6 Observed', 'Lane 7 Samples', 'Lane 7 Flow', 'Lane 7 Avg Occ',
            'Lane 7 Avg Speed', 'Lane 7 Observed', 'Lane 8 Samples', 'Lane 8 Flow', 'Lane 8 Avg Occ',
            'Lane 8 Avg Speed', 'Lane 8 Observed']

meta_path = "./station_5min/2015/meta_data/d11/"
meta_files = [f for f in listdir(meta_path) if isfile(join(meta_path, f))]
meta_data = pd.read_table(meta_path+meta_files[0])  # metafiles[0]

df_list = []
print "there are {} files".format(len(onlyfiles))
for i, filename in enumerate(onlyfiles):
    t1 = time.time()
    with gzip.open(data_5min_path+filename, 'rb') as f:
        file_content = pd.read_csv(f,header=None,names=colnames)
        file_content = file_content.ix[(file_content['Freeway #'] == 15) & (file_content['Direction'] == 'S') &
                                                                  (file_content['Lane Type'] == 'ML'),:]
        df_list.append(file_content)
    t2 = time.time()
    print i, t2-t1
    # if i == 1:
    #     break

big_df = pd.concat(df_list)
df_list = None #clear memory space

small_df = big_df#.ix[(big_df['Freeway #'] == 15) & (big_df['Direction'] == 'S') & (big_df['Lane Type'] == 'ML'),:]
small_df = small_df[['Timestamp', 'Station', 'District', 'Freeway #', 'Direction', 'Lane Type', 'Station Length',
                     'Samples', '% Observed', 'TotalFlow', 'AvgOccupancy', 'AvgSpeed']]
meta_data = meta_data[['ID','Latitude','Longitude']]
meta_data.columns = ['Station','Latitude','Longitude']
small_df = small_df.merge(meta_data)

# Creates an index for each station from N to S.  Index 0 is the northernmost station.  Index N is the southernmost.
station_index = small_df[['Station','Latitude']].drop_duplicates().sort_values('Latitude',ascending=False)\
    .reset_index(drop=True).reset_index()

small_df = small_df.merge(station_index)
small_df['Timestamp'] = pd.to_datetime(small_df['Timestamp'])
small_df['Time'] = small_df['Timestamp'].apply(lambda x:x.time())
small_df['Date'] = small_df['Timestamp'].apply(lambda x:x.date())


small_df.to_csv("I15S_data2.csv")

