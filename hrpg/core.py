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


def call_api(endpoint, headers=None, params=None):
    """make a call to the hrpg api and, on success, return json"""
    url = '%s%s' % (API_URI_BASE, endpoint)
    req = requests.get(url, headers=headers, params=params)
    if req.status_code == 200:
        return req.json()
    else:
        print('Unhandled HTTP status code')
        raise NotImplementedError


def cli():
    """HabitRPG command-line interface.

    usage:
      hrpg status
      hrpg tasks|habit|daily|todo|reward
      hrpg task <tid> [<uid>]
      hrpg --version
      hrpg server

    options:
      -h --help     Show this screen.
      --version     Show version.

    Subcommands:
      status        Show HP, XP, and GP for user
      habit         List habit tasks
      daily         List daily tasks
      todo          List todo tasks
      reward        List reward tasks
      tasks         List user tasks of all types
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
        res = call_api('/status')
        if res['status'] == 'up':
            print('Up and running! All is well.')
        else:
            print('HRPG server is down...')

    # GET user
    elif args['status']:
        res = call_api('/user', headers=config)
        pprint(res['stats'])

    # GET tasks:habit
    elif args['habit']:
        payload = {'type': 'habit'}
        res = call_api('/user/tasks', headers=config, params=payload)
        pprint([e['text'] for e in res])

    # GET tasks:daily
    elif args['daily']:
        payload = {'type': 'daily'}
        res = call_api('/user/tasks', headers=config, params=payload)
        pprint([e['text'] for e in res])

    # GET tasks:todo
    elif args['todo']:
        payload = {'type': 'todo'}
        res = call_api('/user/tasks', headers=config, params=payload)
        pprint([e['text'] for e in res if not e['completed']])

    elif args['tasks']:
        raise NotImplementedError  # no hurry on this one...

    # GET task
    elif args['task']:
        raise NotImplementedError  # only really useful for the history...


if __name__ == '__main__':
    cli()
