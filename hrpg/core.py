#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Phil Adams http://philadams.net

hrpg: commandline interface for http://habitrpg.com
http://github.com/philadams/hrpg
"""


import json
import os
import cmd
from pprint import pprint

from docopt import docopt
from . import api

VERSION = 'hrpg version 0.0.4'
CONFIG_FILE = '~/.hrpgrc'


def cli():
    """HabitRPG command-line interface.

    usage:
      hrpg status
      hrpg tasks|habit|daily|todo|reward
      hrpg history <tid>
      hrpg (-i | --interactive)
      hrpg --version
      hrpg server

    options:
      -h --help          Show this screen
      --version          Show version
      -i, --interactive  Interactive mode

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
        authkeys = ['x-api-user', 'x-api-key']
        auth = dict([(k, config[k]) for k in authkeys])
        #auth = dict([(k, config[k]) for k in authkeys if k in config])
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

    # instantiate api service
    hbt = api.HRPG(auth=auth)

    # GET server status
    if args['server']:
        server = hbt.status()
        pprint(server)

    # GET user
    elif args['status']:
        status = hbt.user()
        pprint(status['stats'])

    # GET tasks:habit
    elif args['habit']:
        habits = hbt.user.tasks(type='habit')
        pprint([e['text'] for e in habits])

    # GET tasks:daily
    elif args['daily']:
        dailies = hbt.user.tasks(type='daily')
        pprint([e['text'] for e in dailies])

    # GET tasks:todo
    elif args['todo']:
        todos = hbt.user.tasks(type='todo')
        pprint([e['text'] for e in todos if not e['completed']])

    elif args['tasks']:
        raise NotImplementedError  # no hurry on this one...

    # GET task
    elif args['task']:
        raise NotImplementedError  # only really useful for the history...


if __name__ == '__main__':
    cli()
