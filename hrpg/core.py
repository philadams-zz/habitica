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
      hrpg tasks [--habit | --daily | --todo | --reward]
      hrpg habit|daily|todo|reward
      hrpg task <tid> [<uid>]
      hrpg --version
      hrpg server

    options:
      -h --help     Show this screen.
      --version     Show version.

    Subcommands:
      status        Show HP, XP, and GP for user
      tasks         List user tasks
      habit         List habit tasks
      daily         List daily tasks
      todo          List todo tasks
      reward        List reward tasks
      task          Show task <tid> details
      server        Show status of HabitRPG service
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
    if args['server']:
        req = requests.get(API_URI_BASE + '/status')
        if req.status_code == 200:
            res = req.json()
            if res['status'] == 'up':
                print('Up and running! All is well.')

    # GET user
    elif args['status']:
        req = requests.get(API_URI_BASE + '/user', headers=config)
        res = req.json()
        if req.status_code == 200:
            pprint(res['stats'])
            print('\n...and a whole crapload of other stuff')
        else:
            print('Unhandled HTTP status code')
            raise NotImplementedError

    # GET tasks:habit
    elif args['habit']:
        payload = {'type': 'habit'}
        req = requests.get(API_URI_BASE + '/user/tasks',
                headers=config,
                params=payload)
        res = req.json()
        if req.status_code == 200:
            pprint([e['text'] for e in res])
        else:
            print('Unhandled HTTP status code')
            raise NotImplementedError

    # GET tasks:daily
    elif args['daily']:
        payload = {'type': 'daily'}
        req = requests.get(API_URI_BASE + '/user/tasks',
                headers=config,
                params=payload)
        res = req.json()
        if req.status_code == 200:
            pprint([e['text'] for e in res])
        else:
            print('Unhandled HTTP status code')
            raise NotImplementedError

    # GET tasks:todo
    elif args['todo']:
        payload = {'type': 'todo'}
        req = requests.get(API_URI_BASE + '/user/tasks',
                headers=config,
                params=payload)
        res = req.json()
        if req.status_code == 200:
            pprint([e['text'] for e in res if not e['completed']])
        else:
            print('Unhandled HTTP status code')
            raise NotImplementedError

    elif args['tasks']:
        raise NotImplementedError

    # GET task
    elif args['task']:
        raise NotImplementedError


if __name__ == '__main__':
    cli()
