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


def clear_cache():
    """delete the cache file CACHE_FILE."""
    try:
        os.remove(os.path.expanduser(CACHE_FILE))
    except OSError:
        pass  # overwhelmingly, the cache file wasn't there
    print('cache file (%s) deleted' % CACHE_FILE)


def cli():
    """HabitRPG command-line interface.

    usage:
      hrpg status
      hrpg habits|dailies|todos
      hrpg habits up <task-id>
      hrpg habits down <task-id>
      hrpg dailies done <task-id>
      hrpg dailies undo <task-id>
      hrpg todos done <task-id>
      hrpg server
      hrpg clear-cache

    options:
      -h --help          Show this screen
      --version          Show version

    Subcommands:
      status               Show HP, XP, and GP for user
      habits               List habit tasks
      habits up <task-id>  Up (+) habit <task-id>
      habits down <task-id>  Up (+) habit <task-id>
      dailies              List daily tasks
      dailies done         Mark daily <task-id> complete
      dailies undo         Mark daily <task-id> incomplete
      todos                List todo tasks
      todos done <task-id> Mark todo <task-id> completed
      server               Show status of HabitRPG service
      clear-cache          Wipe out local (home dir) cache
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

    # clear cache
    if args['clear-cache']:
        clear_cache()

    # GET server status
    elif args['server']:
        server = hbt.status()
        pprint(server)

    # GET user
    elif args['status']:
        status = hbt.user()
        pprint(status['stats'])

    # GET/POST habits
    elif args['habits']:
        if args['up']:
            habits = from_cache('habits')
            cache_id = int(args['<task-id>'])
            res = hbt.user.tasks(_id=habits[cache_id]['id'],
                                 _direction='up', _method='post')
            print('success!')
        elif args['down']:
            habits = from_cache('habits')
            cache_id = int(args['<task-id>'])
            res = hbt.user.tasks(_id=habits[cache_id]['id'],
                                 _direction='down', _method='post')
            print('success!')
        else:
            habits = hbt.user.tasks(type='habit')
            cache('habits', habits)
            pprint([e['text'] for e in habits])

    # GET/PUT tasks:daily
    elif args['dailies']:
        if args['done']:
            dailies = from_cache('dailies')
            cache_id = int(args['<task-id>'])
            # you'd think this'd work, but you don't get rewards!
            #res = hbt.user.tasks(_id=dailies[cache_id]['id'],
            #                     _method='put', completed=True)
            res = hbt.user.tasks(_id=dailies[cache_id]['id'],
                                 _direction='up', _method='post')
            print('success!')
        elif args['undo']:
            dailies = from_cache('dailies')
            cache_id = int(args['<task-id>'])
            res = hbt.user.tasks(_id=dailies[cache_id]['id'],
                                 _method='put', completed=False)
            print('success!')
        else:
            dailies = hbt.user.tasks(type='daily')
            cache('dailies', dailies)
            pprint([e['text'] for e in dailies])

    # GET tasks:todo
    elif args['todos']:
        if args['done']:
            todos = from_cache('todos')
            cache_id = int(args['<task-id>'])
            # you'd think this'd work, but you don't get rewards!
            #res = hbt.user.tasks(_id=todos[cache_id]['id'],
            #                     _method='put', completed=True)
            res = hbt.user.tasks(_id=todos[cache_id]['id'],
                                 _direction='up', _method='post')
            print('marked completed')
        else:
            todos = hbt.user.tasks(type='todo')
            cache('todos', todos)
            pprint([e['text'] for e in todos if not e['completed']])


if __name__ == '__main__':
    cli()
