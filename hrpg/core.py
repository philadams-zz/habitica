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
      hrpg yay <tid>
      hrpg doh <tid>
      hrpg server

    options:
      -h --help          Show this screen
      --version          Show version
      -i, --interactive  Interactive mode

    Subcommands:
      daily         List daily tasks
      doh           Down (-) habit <tid>
      done          Mark <tid> task as completed
      habit         List habit tasks
      show          Show task <tid> details
      reward        List reward tasks
      server        Show status of HabitRPG service
      status        Show HP, XP, and GP for user
      tasks         List user tasks of all types
      todo          List todo tasks
      undo          Mark <tid> task as incomplete
      yay           Up (+) habit <tid>
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

    # POST yay
    elif args['yay']:
        res = hbt.user.tasks(_id=args['<tid>'], _direction='up', _method='post')
        pprint(res)

    # POST doh
    elif args['doh']:
        res = hbt.user.tasks(_id=args['<tid>'], _direction='down', _method='post')
        pprint(res)

    # TODO PUT done
    #elif args['done']:
    #    res = hbt.user.task(_id=args['<tid>'], _method='put', completed=True)
    #    pprint(res)

    # TODO PUT undo

    # GET tasks:todo
    elif args['todo']:
        todos = hbt.user.tasks(type='todo')
        pprint([e['text'] for e in todos if not e['completed']])

    elif args['tasks']:
        raise NotImplementedError  # no hurry on this one...


if __name__ == '__main__':
    cli()
