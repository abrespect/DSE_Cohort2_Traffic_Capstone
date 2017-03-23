# -*- coding: utf-8 -*-

import time
import sys

"""
##
## Example Usage
##
from time import sleep
import trafficepassion.timer as tm

items = list(range(0, 700))
n_items = len(items)

pb = tm.ProgressBar( n_items, prefix='Progress:', suffix='Complete', timer=True )
pb.update(i)
for i, item in enumerate(items):
    sleep(0.1)
    pb.update( i )
"""


def timestr(t, prefix='', suffix=''):
    """
    Convert given time in seconds into a string (with sec/min/hrs)
    @params:
        t          - Required  : time in seconds (float)
        prefix     - Optional  : prefix string to append (Str)
        suffix     - Optional  : suffix string to append (Str)
    """
    if t > 60:
        if t > 3600:
            return '{0}{1:.2f} hrs{2}'.format(prefix, t / 3600, suffix)
        return '{0}{1:.2f} min{2}'.format(prefix, t / 60, suffix)
    return '{0}{1:.2f} sec{2}'.format(prefix, t, suffix)


class ProgressBar(object):
    def __init__(self, total, prefix='', suffix='', decimals=1, bar_length=50, timer=False):
        """
        @params:
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            bar_length  - Optional  : character length of bar (Int)
        """
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.bar_length = bar_length
        self.timer = timer
        self.start = time.time()

    def update(self, iteration, prefix=None, suffix=None, timer=None):
        """
        Call in a loop to create terminal progress bar
        For optional parameters, None means use current values
        @params:
            iteration   - Required  : current iteration (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            timer       - Optional  : include time (bool)
        """
        if prefix is not None:
            self.prefix = prefix
        if suffix is not None:
            self.suffix = suffix
        if timer is not None:
            self.timer = timer
            self.start = time.time()

        str_format = "{0:." + str(self.decimals) + "f}"
        percents = str_format.format(100 * (iteration / float(self.total)))
        filled_length = int(round(self.bar_length * iteration / float(self.total)))
        bar = '█' * filled_length + '-' * (self.bar_length - filled_length)

        elapsed = '' if timer == False else timestr(time.time() - self.start, prefix='[', suffix=']')
        sys.stdout.write('\r%s |%s| %s%s %s %s' % (self.prefix, bar, percents, '%', self.suffix, elapsed)),

        if iteration == self.total:
            sys.stdout.write('\n')
            sys.stdout.flush()
