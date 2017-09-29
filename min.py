#!/usr/bin/env python3

import argparse
import time
import os

def main():

    # load configuration
    # TODO: Push this to a YAML file
    config = {
            'path': os.path.expanduser('~/notes'),
            'default_min': 'personal',
            'default_ref': 'quick',
            'ext': 'md',
            'followup_tag': '#FU',
            'done_tag': '#X'
            }

    # create arg parser
    parser = argparse.ArgumentParser(description="minimal note management")
    subparsers = parser.add_subparsers(dest='command')

    # open command
    open_parser = subparsers.add_parser('open', help='open/create notes')
    open_parser.set_defaults(func=cmd_open)

    ## open: ref or min?
    open_parser.add_argument(
        '--ref', '-r',
        help='is it a ref note type? (default: min type)',
        dest='is_min_type',
        action='store_false',
        default=True,
     )

    ## open: date (only for mins)
    open_parser.add_argument(
        '--date', '-d',
        help='for min: date to open (default: today, format: 20170329)',
        dest='min_date',
        type=validate_date_string,
        default=str(time.strftime('%Y-%m-%d'))
     )

    ## open: title
    open_parser.add_argument(
        'title',
        help='title for note (defaults in config)',
        nargs='?'
     )

    # list (maybe use a menu?)
    # * [OPT] search: mins or refs or all
    # * [OPT] only followups?
    # * [OPT] search text

    # list command
    list_parser = subparsers.add_parser('list', help='list notes')
    list_parser.set_defaults(func=cmd_list)

    # TODO: Create list options

    # parse arguments
    args = parser.parse_args()

    ## post-parsing: open/title has conditional defaults
    if args.title == '':
        args.title = config['default_min'] if args.is_min_type else config['default_ref']

    # run function
    args.func(**vars(args), config=config)

def validate_date_string(string):
    try:
        return time.strftime('%Y-%m-%d', time.strptime(string, '%Y-%m-%d'))
    except:
        raise argparse.ArgumentTypeError('Invalid date, expecting format YYYYMMDDD')

def cmd_open(is_min_type, min_date, title, config, **kwargs):

    # dir path
    note_path_parts = []
    note_path_parts.append(config['path'])
    note_path_parts.append('mins' if is_min_type else 'refs')
    if is_min_type:
        note_path_parts.append(title)
    note_path = os.path.join(*note_path_parts)

    # note filename
    note_filename = '{}.{}'.format(min_date if is_min_type else title, config['ext'])

    # full path
    note_fullpath = os.path.join(note_path, note_filename)

    # create dir and open
    os.makedirs(note_path, exist_ok=True)
    os.system('cd {}; {} "{}"'.format(config['path'], os.getenv('EDITOR'), note_fullpath))

def cmd_list(**kwargs):
    pass

if __name__ == "__main__":
    main()
