'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

import os
import re
import semver
from freegenes.logger import bot, decodeUtf8String
import subprocess
import sys
import shlex

################################################################################
# Local commands and requests
################################################################################

def _process_sudo_cmd(cmd, sudo, sudo_options):
    if sudo and sudo_options is not None:
        if isinstance(sudo_options, str):
            sudo_options = shlex.split(sudo_options)
        cmd = ['sudo'] + sudo_options + cmd
    elif sudo:
        cmd = ['sudo'] + cmd
    return cmd


def check_install(software, quiet=True):
    '''check_install will attempt to run the singularity command, and
       return True if installed. The command line utils will not run 
       without this check.
    '''

    cmd = [software, '--version']
    found = False

    try:
        version = run_command(cmd, quiet=True)
    except: # FileNotFoundError
        return found

    if version is not None:
        if version['return_code'] == 0:
            found = True

        if not quiet:
            version = version['message']
            bot.info("Found %s version %s" % (software.upper(), version))

    return found


def which(software):
    '''which returns the full path to where software is installed.
    '''
    cmd = ['which', software]
    result = run_command(cmd, quiet=True)['message'][0]
    return result.strip('\n')
    


def get_installdir():
    '''get_installdir returns the installation directory of the application
    '''
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def stream_command(cmd, no_newline_regexp="Progess", sudo=False, sudo_options=None):
    '''stream a command (yield) back to the user, as each line is available.

       # Example usage:
       results = []
       for line in stream_command(cmd):
           print(line, end="")
           results.append(line)

       Parameters
       ==========
       cmd: the command to send, should be a list for subprocess
       no_newline_regexp: the regular expression to determine skipping a
                          newline. Defaults to finding Progress
       sudo_options: string or list of strings that will be passed as options to sudo

    '''
    cmd = _process_sudo_cmd(cmd, sudo, sudo_options)

    process = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               universal_newlines=True)
    for line in iter(process.stdout.readline, ""):
        if not re.search(no_newline_regexp, line):
            yield line
    process.stdout.close()
    return_code = process.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def run_command(cmd, 
                sudo=False,
                capture=True,
                no_newline_regexp="Progess",
                quiet=False,
                sudo_options=None):

    '''run_command uses subprocess to send a command to the terminal. If
       capture is True, we use the parent stdout, so the progress bar (and
       other commands of interest) are piped to the user. This means we 
       don't return the output to parse.

       Parameters
       ==========
       cmd: the command to send, should be a list for subprocess
       sudo: if needed, add to start of command
       no_newline_regexp: the regular expression to determine skipping a
                          newline. Defaults to finding Progress
       capture: if True, don't set stdout and have it go to console. This
                option can print a progress bar, but won't return the lines
                as output.
       sudo_options: string or list of strings that will be passed as options to sudo
    '''
    cmd = _process_sudo_cmd(cmd, sudo, sudo_options)

    stdout = None
    if capture:
        stdout = subprocess.PIPE

    # Use the parent stdout and stderr
    process = subprocess.Popen(cmd,
                               stderr=subprocess.PIPE,
                               stdout=stdout)
    lines = []
    found_match = False

    for line in process.communicate():
        if line:
            line = decodeUtf8String(line)
            lines.append(line)
            if re.search(no_newline_regexp, line) and found_match:
                if not quiet:
                    sys.stdout.write(line)
                found_match = True
            else:
                if not quiet:
                    sys.stdout.write(line)
                    print(line.rstrip())
                found_match = False

    output = {'message': lines,
              'return_code': process.returncode}

    return output
