'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from freegenes.main.twist import Client
from .shell import (
    ipython,
    python,
    run_bpython
)

def main(args, options, parser):

    # Choose executor based on what is available 
    lookup = {'ipython': ipython,
              'python': python,
              'bpython': run_bpython}

    shells = ['ipython', 'python', 'bpython']

    # Prepare client
    client = Client()

    # Otherwise present order of liklihood to have on system
    for shell in shells:
        try:
            return lookup[shell](client)
        except ImportError:
            pass
