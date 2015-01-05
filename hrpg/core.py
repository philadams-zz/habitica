#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Phil Adams http://philadams.net

hrpg: commandline interface for http://habitrpg.com
http://github.com/philadams/hrpg

TODO: pretty format task-ids
TODO: handle ranges and lists for done/undone
TODO: figure out cache solution (shelve-json?) and how/when to invalidate
"""


import json
import os
from collections import defaultdict
from pprint import pprint

from docopt import docopt
from . import api

VERSION = 'hrpg version 0.0.5'
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


def clear_cache():
    """delete the cache file CACHE_FILE."""
    try:
        os.remove(os.path.expanduser(CACHE_FILE))
    except OSError:
        pass  # overwhelmingly, the cache file wasn't there
    print('cache file (%s) deleted' % CACHE_FILE)


def get_task_id(args, key='<task-id>'):
    return int(args[key]) - 1 if args[key] is not None else -1


def print_task_list(tasks):
    for i, task in enumerate(tasks):
        completed = 'x' if task['completed'] else ' '
        print('[%s] %s %s' % (completed, i + 1, task['text']))


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
      hrpg todos add <task>
      hrpg server
      hrpg clear-cache

    options:
      -h --help          Show this screen
      --version          Show version

    Subcommands:
      status                 Show HP, XP, and GP for user
      habits                 List habit tasks
      habits up <task-id>    Up (+) habit <task-id>
      habits down <task-id>  Up (+) habit <task-id>
      dailies                List daily tasks
      dailies done           Mark daily <task-id> complete
      dailies undo           Mark daily <task-id> incomplete
      todos                  List todo tasks
      todos done <task-id>   Mark todo <task-id> completed
      todos add <task>       Add todo with description <task>
      server                 Show status of HabitRPG service
      clear-cache            Wipe out local (home dir) cache
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
        tid = get_task_id(args)
        habits = hbt.user.tasks(type='habit')
        if args['up']:
            hbt.user.tasks(_id=habits[tid]['id'],
                           _direction='up', _method='post')
            print('incremented!')
        elif args['down']:
            hbt.user.tasks(_id=habits[tid]['id'],
                           _direction='down', _method='post')
            print('decremented!')
        else:
            for i, task in enumerate(habits):
                pprint(task); exit()
                # TODO figure out strength to show here
                strength = 'x' if task['completed'] else ' '
                print('[%s] %s %s' % (completed, i + 1, task['text']))

    # GET/PUT tasks:daily
    elif args['dailies']:
        tid = get_task_id(args)
        dailies = hbt.user.tasks(type='daily')
        if args['done']:
            hbt.user.tasks(_id=dailies[tid]['id'],
                           _direction='up', _method='post')
            print('marked daily \'%s\' completed' % dailies[tid]['text'])
            dailies[tid]['completed'] = True
        elif args['undo']:
            hbt.user.tasks(_id=dailies[tid]['id'],
                           _method='put', completed=False)
            print('marked daily \'%s\' incomplete' % dailies[tid]['text'])
            dailies[tid]['completed'] = False
        print_task_list(dailies)

    # GET tasks:todo
    elif args['todos']:
        tid = get_task_id(args)
        todos = [e for e in hbt.user.tasks(type='todo')
                if not e['completed']]
        if args['done']:
            hbt.user.tasks(_id=todos[tid]['id'],
                           _direction='up', _method='post')
            print('marked todo \'%s\' complete' % todos[tid]['text'])
            del(todos[tid])
        elif args['add']:
            ttext = args['<task>']
            hbt.user.tasks(type='todo', text=ttext,
                           _method='post')
            todos.insert(0, {'completed': False, 'text': ttext})
            print('added new todo \'%s\'' % ttext)
        print_task_list(todos)


if __name__ == '__main__':
    cli()
