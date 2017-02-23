"""
This class is designed to load and partition the data.

Part of this class should be the data cleaning assumptions
"""
import pandas as pd
import os
import glob


class MetaReader(object):
    """
    This class will read in the Metadata files and return a pandas dataframe
    """
    def __init__(self, path):
        """
        The MetaReader will read in the files that are expected in the following structure

        <year>/<district>/<meta data files>

        The metadata files are expected to be as they are off of the pems website

        example: d11_text_meta_2015_01_01.txt

        :param path: the location the folder that contains the year/district/meta_files structure
        """
        self.path = path

    def read_files(self):
        """
        discover the files from the path and then load the latest filename

        From our exploration we have decided that the latest file is the most applicable to our
        analysis and that any of the variation within the year doesn't need to be included within our analysis
        since not subtle station location changes over time

        :return: pandas dataframe
        :rtype: pandas
        """
        meta_files = glob.glob(self.path)
        print "files found: %s" % meta_files

        # Note: do the filename convention the last file will always be at the end of the list
        print "using the last file: %s" % meta_files[-1]

        meta_file = meta_files[-1]
        date = str('_'.join(meta_file.split('_')[4:7])).split('.')[0]
        df = pd.read_table(meta_file, index_col=None, header=0)
        date_col = pd.Series([date] * len(df))
        df['file_date'] = date_col
        return df