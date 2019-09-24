'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from freegenes.logger import bot
from io import StringIO
import csv


def str2csv(string, newline="\n", delim=","):
    '''given a string with csv content, read in as csv and return rows,
       with the header in the first row.
    '''
    rows = []
    reader = csv.reader(string.split(newline), delimiter=delim)
    for row in reader:
        if row:
            rows.append(row)
    return rows

