#!/usr/bin/env python
"""
This class is designed to load and partition the data.

Part of this class should be the data cleaning assumptions
"""
import pandas as pd
import argparse
import glob
import numpy as np


def merge_path(directory, year, district, data_type):
    return "%s/%s/%s/%s/*.txt" % (directory, data_type, year, district)


class MetaHandler(object):
    """
    This class will read in the Metadata files and return a pandas dataframe
    """
    def __init__(self, directory, year, district):
        """
        The MetaReader will read in the files that are expected in the following structure

        <year>/<district>/<meta data files>

        The metadata files are expected to be as they are off of the pems website

        example: d11_text_meta_2015_01_01.txt

        :param str directory: the location the folder that contains the year/district/meta_files structure
        :param str year: the year folder to read
        :param str district: the district folder to read
        """
        self.directory = directory
        self.year = year
        self.district = district
        self.path = merge_path(self.directory, self.year, self.district, 'meta')

    def read_files(self, hdf_store):
        """
        discover the files from the path and then load the latest filename

        From our exploration we have decided that the latest file is the most applicable to our
        analysis and that any of the variation within the year doesn't need to be included within our analysis
        since not subtle station location changes over time

        :return: pandas dataframe
        :rtype: pd.DataFrame
        """
        print "self.path: %s" % self.path
        meta_files = glob.glob(self.path)
        print "files found: %s" % meta_files

        # Note: Our assumption is that the latest metadata entry is always correct, however some of the metadata
        # entries do have missing data, like lat/lon.  So we will read in all of the rows, drop rows that
        # don't comply and then use the latest record

        meta_file_list = []
        for meta_file in meta_files:
            date = str('_'.join(meta_file.split('_')[4:7])).split('.')[0]
            df = pd.read_table(meta_file, index_col=None, header=0)
            date_col = pd.Series([date] * len(df))
            df['file_date'] = date_col
            # drop rows that are missing latitude / longitude values TODO: determine if this is ok.
            df.dropna(inplace=True, subset=['Latitude', 'Longitude'], how='any')
            meta_file_list.append(df)
        df = pd.concat(meta_file_list).drop_duplicates(subset='ID', keep='last')

        # drop unnecessary columns
        columns_to_keep = [u'ID', u'Fwy', u'Dir', u'District', u'County', u'City', u'State_PM',
                           u'Abs_PM', u'Latitude', u'Longitude', u'Length', u'Type', u'Lanes',
                           u'Name', u'file_date']
        df = df[columns_to_keep]

        sets = df.groupby(['Fwy', 'Dir']).size().reset_index().rename(columns={0: 'count'})

        for index, item in sets.iterrows():
            print index
            if item.Dir == "N":
                sort_order = ('Abs_PM', True)
            elif item.Dir == "S":
                sort_order = ('Abs_PM', False)
            elif item.Dir == "E":
                sort_order = ('Abs_PM', True)
            elif item.Dir == "W":
                sort_order = ('Abs_PM', False)
            else:
                raise RuntimeError("unknown direction found")

            store_key = 'meta'
            data_to_store = df[(df.Fwy == item.Fwy) & (df.Dir == item.Dir)] \
                .sort_values(by=sort_order[0], ascending=sort_order[1])
            data_to_store.index = np.arange(0, data_to_store.shape[0])
            hdf_store.append(store_key, data_to_store, data_columns=True)

        return df


class FiveMinuteHandler(object):
    """
    This class is designed to read/write the FiveMinute dataframe into our aggregated format
    """
    def __init__(self, directory, year, district, columns_to_keep='default'):
        """
        The MetaReader will read in the files that are expected in the following structure

        <year>/<district>/<5min data files>

        The metadata files are expected to be as they are off of the pems website

        example: d11_text_station_5min_2015_01_01.txt

        :param str directory: the location the folder that contains the year/district/meta_files structure
        :param str year: the year folder to read
        :param str district: the district folder to read
        :param list columns_to_keep: a list of the columns that should be kept when the 5min data is read in
        """
        # need to come up with dynamic way of doing this
        self.five_min_base_header = ['Timestamp', 'Station', 'District', 'Fwy', 'Dir', 'Type',
                                     'Length', 'Samples', 'Observed', 'Total_Flow', 'Avg_Occupancy',
                                     'Avg_Speed']
        self.five_min_extra_header = ['Lane_%s_Samples', 'Lane_%s_Flow', 'Lane_%s_Avg_Occ', 'Lane_%s_Avg_Speed',
                                      'Lane_%s_Observed']
        self.directory = directory
        self.year = year
        self.district = district
        self.path = merge_path(self.directory, self.year, self.district, 'station_5min')
        self.header = None
        if columns_to_keep == 'default':
            self.columns_to_keep = ['Timestamp', 'Station', 'District', 'Fwy', 'Dir', 'Type',
                                    'Length', 'Samples', 'Observed', 'Total_Flow', 'Avg_Occupancy',
                                    'Avg_Speed']
        else:
            self.columns_to_keep = columns_to_keep

    def create_header(self, file_path):
        """
        This function will read the first row of a file and then determine the header based upon the
        length of the first row from the 5 minute frame

        :param file_path:
        :return:
        """
        with open(file_path) as infile:
            first_row = infile.next()
            row_length = len(first_row.split(','))
            lanes = (row_length - len(self.five_min_base_header)) / float(len(self.five_min_extra_header))
            if not lanes.is_integer():
                msg = "the number of lanes didn't come out as a whole number.  Needs to be reviewed"
                raise RuntimeError(msg)
            else:
                lanes = int(lanes)
        header = self.five_min_base_header
        for i in range(1, lanes + 1):
            new_header = [item % i for item in self.five_min_extra_header]
            header += new_header
        return header

    def import_data(self, meta_frame, hdf_store):
        """
        Import the data from csv and put it into the store in our expected format / style

        :param pd.DataFrame meta_frame: the meta data frame
        :param hdf_store: the hdf_store to write to
        :return: single dataframe of the year
        :rtype: pd.DataFrame
        """
        five_min_files = glob.glob(self.path)
        total = len(five_min_files)

        header = self.create_header(five_min_files[0])

        store_key = 'data'
        for index in range(0, total):
            five_min_file = five_min_files[index]

            if index % (total/10) == 0:
                print "{0:.2f}".format(index/float(total))
            df = pd.read_csv(five_min_file, index_col=None, header=None, names=header)
            # drop columns to reduce size
            if self.columns_to_keep:
                df = df[self.columns_to_keep]

            hdf_store.append(store_key, df, data_columns=['Fwy', 'Dir', 'Type', 'Station', 'Timestamp'])

    def sort_store(self, data_frame):
        """
        This function will lay out the hdf file in the format that we want

        structure: year/district/freeway/direction/station type

        :param pd.DataFrame data_frame:
        :return:
        """
        sets = data_frame.groupby(['Fwy', 'Dir']).size().reset_index().rename(columns={0: 'count'})

        basic_key = 'y%s/d%s' % (self.year, self.district)
        for index, item in sets.iterrows():
            print "storing item: %s" % item
            if item.Dir == "N":
                sort_order = ('Abs_PM', True)
            elif item.Dir == "S":
                sort_order = ('Abs_PM', False)
            elif item.Dir == "E":
                sort_order = ('Abs_PM', True)
            elif item.Dir == "W":
                sort_order = ('Abs_PM', False)
            else:
                raise RuntimeError("unknown direction found")

            for station_type in data_frame['Lane Type'].unique():
                store_key = '%s/%s/five_min/%s/%s' % (basic_key, item.Fwy, item.Dir, station_type)
                data_to_store = meta_frame[(data_frame.Fwy == item.Fwy) & (data_frame.Dir == item.Dir)] \
                    .sort_values(by=sort_order[0], ascending=sort_order[1])
                data_to_store.index = np.arange(0, data_to_store.shape[0])
                store.append(store_key, data_to_store)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This script is designed to generate hdf files based upon the 5min'
                                                 'traffic files and meta data files.  Structure assumed is'
                                                 '<year>/<district>/<type> where type is "meta" or "station_5min"')
    parser.add_argument('directory', help='The directory where the files are located')
    parser.add_argument('store_location', help='full path to the hdf store')
    parser.add_argument('--year', default='2015', help='The year to generate')
    parser.add_argument('--district', default='d11', help='The district to generate')

    args = parser.parse_args()
    # set the hdf format to table
    pd.set_option('io.hdf.default_format', 'table')
    store = pd.HDFStore(args.store_location, mode='a')

    meta = MetaHandler(args.directory, args.year, args.district)
    meta_frame = meta.read_files()
    # meta.write_data(meta_frame)

    five_min = FiveMinuteHandler(args.directory, args.year, args.district)
    five_min_frame = five_min.import_data()
    print "creating store"
    five_min.create_store(five_min_frame)






