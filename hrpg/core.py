#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Phil Adams http://philadams.net

hrpg: commandline interface for http://habitrpg.com
http://github.com/philadams/hrpg
"""


import json
import os
from pprint import pprint

from docopt import docopt
from . import api

VERSION = 'hrpg version 0.0.4'
CONFIG_FILE = '~/.hrpgrc'
CACHE_FILE = '~/.hrpg.cache'


def load_config(fname):
    config = None
    try:
        config = json.load(open(os.path.expanduser(fname), 'r'))
    except IOError as err:
        raise IOError('No config file at %s' % fname)
    except ValueError as err:
        print('Malformed config file at %s\n' % fname)
        raise ValueError(err.msg)
    except KeyError as err:
        raise KeyError('Missing config key,value in %s\n' % fname)
    return config


def cache(key, data):
    """cache (short term!) data in file, accessible at key"""
    cached = {}
    try:
        cached = json.load(open(os.path.expanduser(CACHE_FILE), 'r'))
    except IOError as err:
        pass  # the cache file might not exist, and that's okay
    except ValueError as err:
        print('Malformed cache file at %s\n' % CONFIG_FILE)
        raise ValueError(err.msg)
    cached[key] = data
    try:
        out = open(os.path.expanduser(CACHE_FILE), 'w')
        out.write(json.dumps(cached))
        out.close()
    except IOError as err:
        raise(IOError('Problem writing to cache file at %s\n' % CACHE_FILE))


def from_cache(key):
    """return data from cache file by key.
    if key doesn't exist, cache error."""
    return json.load(open(os.path.expanduser(CACHE_FILE), 'r'))[key]


def cli():
    """HabitRPG command-line interface.

    usage:
      hrpg status
      hrpg habit|daily|todo
      hrpg yay <tid>
      hrpg doh <tid>
      hrpg server

    options:
      -h --help          Show this screen
      --version          Show version

    Subcommands:
      daily         List daily tasks
      doh           Down (-) habit <tid>
      done          Mark <tid> task as completed
      habit         List habit tasks
      show          Show task <tid> details
      server        Show status of HabitRPG service
      status        Show HP, XP, and GP for user
      tasks         List user tasks of all types
      todo          List todo tasks
      undo          Mark <tid> task as incomplete
      yay           Up (+) habit <tid>
    """

    # load config and set auth
    config = load_config(CONFIG_FILE)
    authkeys = ['x-api-user', 'x-api-key']
    auth = dict([(k, config[k]) for k in authkeys])
    #auth = dict([(k, config[k]) for k in authkeys if k in config])

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
        cache('habit', habits)
        pprint([e['text'] for e in habits])

    # GET tasks:daily
    elif args['daily']:
        dailies = hbt.user.tasks(type='daily')
        pprint([e['text'] for e in dailies])

    # POST yay
    elif args['yay']:
        habits = from_cache('habit')
        cache_id = int(args['<tid>'])
        res = hbt.user.tasks(_id=habits[cache_id]['id'],
                             _direction='up', _method='post')
        print('success!')
        pprint(res)

    # POST doh
    elif args['doh']:
        habits = from_cache('habit')
        cache_id = int(args['<tid>'])
        res = hbt.user.tasks(_id=habits[cache_id]['id'],
                             _direction='down', _method='post')
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
