'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from freegenes.main import Client

def main(args, options, parser):

    # Choose executor based on what is available 
    lookup = {'ipython': ipython,
              'python': python,
              'bpython': run_bpython}

    shells = ['ipython', 'python', 'bpython']

    # Otherwise present order of liklihood to have on system
    for shell in shells:
        try:
            return lookup[shell]()
        except ImportError:
            pass

def ipython():
    '''give the user an ipython shell
    '''
    client = Client()
    try:
        from IPython import embed
    except ImportError:
        return python()

    embed(using=False)

def run_bpython():
    '''give the user a bpython shell
    '''
    client = Client()
    try:
        import bpython
    except ImportError:
        return python()

    bpython.embed(locals_={'client': client})

def python():
    '''give the user a python shell
    '''
    import code
    client = Client()
    code.interact(local={"client":client})
