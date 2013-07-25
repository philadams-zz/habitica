#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Phil Adams http://philadams.net

hrpg: commandline interface for http://habitrpg.com
http://github.com/philadams/hrpg
"""


import json
import os

from docopt import docopt
from pprint import pprint
import requests

VERSION = 'hrpg version 0.0.4'
CONFIG_FILE = '~/.hrpgrc'
API_URI_BASE = 'https://habitrpg.com/api/v1'
API_CONTENT_TYPE = 'application/json'


def cli():
    """HabitRPG command-line interface.

    usage:
      hrpg status
      hrpg user [<uid>]
      hrpg tasks [--habit | --daily | --todo | --reward] [<uid>]
      hrpg task <tid> [<uid>]
      hrpg
      hrpg --version

    options:
      -h --help     Show this screen.
      --version     Show version.

    Subcommands:
      status        Get status of HabitRPG service
      user          Get user <uid> status
      tasks         Get user <uid> tasks
      task          Get task <tid> details
      <none>        Get user status for this user (convenience)
    """

    # load config
    config = None
    try:
        config = json.load(open(os.path.expanduser(CONFIG_FILE), 'r'))
        uid, key = config['x-api-user'], config['x-api-key']
    except IOError as err:
        print('No config file at %s' % CONFIG_FILE)
        exit()
    except ValueError as err:
        print('Malformed config file at %s\n' % CONFIG_FILE)
        print(err.msg)
        exit()
    except KeyError as err:
        print('Missing config key,value in %s\n' % CONFIG_FILE)
        print(err.msg)
        exit()

    # set up args
    args = docopt(cli.__doc__, version=VERSION)

    # GET status
    if args['status']:
        req = requests.get(API_URI_BASE + '/status')
        if req.status_code == 200:
            res = req.json()
            if res['status'] == 'up':
                print('Up and running! All is well.')

    # GET user
    # TODO fix hackish default setting - might be a docopt config opt?
    elif args['user'] or not (args['tasks'] or args['task']):
        req = requests.get(API_URI_BASE + '/user', headers=config)
        if req.status_code == 200:
            res = req.json()
            pprint(res['stats'])
            print('\n...and a whole crapload of other stuff...')
        else:
            print('Unhandled HTTP status code')
            raise NotImplementedError

    # GET tasks
    elif args['tasks']:
        raise NotImplementedError

    # GET task
    elif args['task']:
        raise NotImplementedError


if __name__ == '__main__':
    cli()
