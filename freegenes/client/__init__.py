'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

import argparse
import sys
import os


def get_parser():

    parser = argparse.ArgumentParser(description="FreeGenes Python",
                                formatter_class=argparse.RawTextHelpFormatter,
                                add_help=False)

    # Global Options
    parser.add_argument('--debug', '-d', dest="debug", 
                        help="use verbose logging to debug.", 
                        default=False, action='store_true')

    parser.add_argument('--quiet', '-q', dest="quiet", 
                        help="suppress all normal output", 
                        default=False, action='store_true')

    parser.add_argument('--version', dest="version", 
                        help="show version and exit", 
                        default=False, action='store_true')

    subparsers = parser.add_subparsers(help='description',
                                       title='actions',
                                       dest="command", metavar='general usage')

    subparsers.add_parser("shell", help="Interact with freegenes python")
    subparsers.add_parser("twist", help="Interact with twist API")

    return parser


def set_verbosity(args):
    '''determine the message level in the environment to set based on args.
    '''
    level = "INFO"

    if args.debug:
        level = "DEBUG"
    elif args.quiet:
        level = "QUIET"

    os.environ['MESSAGELEVEL'] = level
    os.putenv('MESSAGELEVEL', level)
    
    # Import logger to set
    from freegenes.logger import bot
    bot.debug('Logging level %s' % level)
    import freegenes

    bot.debug("FreeGenes Python Version: %s" % freegenes.__version__)


def version():
    '''version prints the version, both for the user and help output
    '''
    import freegenes
    return freegenes.__version__
    

def main():

    parser = get_parser()

    def print_help(return_code=0):
        '''print help, including the software version and active client 
           and exit with return code.
        '''
        v = version()
        print("\nFreeGenes Python [v%s]\n" %(v))
        parser.print_help()
        sys.exit(return_code)
    
    if len(sys.argv) == 1:
        print_help()
    try:
        # We capture all primary arguments, and take secondary to pass on
        args, options = parser.parse_known_args()
    except:
        sys.exit(0)

    # The main function
    func = None

    # If the user wants the version
    if args.version:
        print(version())
        sys.exit(0)

    # if environment logging variable not set, make silent
    set_verbosity(args)

    # Does the user want help for a subcommand?
    if args.command == 'shell': 
        from .shell import main as func
    elif args.command == 'twist': 
        from .twist import main as func
    else:
        print_help()

    # Pass on to the correct parser
    if args.command is not None:
        func(args=args, options=options, parser=parser)


if __name__ == '__main__':
    main()
