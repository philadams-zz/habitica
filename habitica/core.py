#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Phil Adams http://philadams.net

habitica: commandline interface for http://habitica.com
http://github.com/philadams/habitica

TODO: figure out cache solution (shelve-json?) and how/when to invalidate
"""


from bisect import bisect
import json
import netrc
import os
from time import sleep
from webbrowser import open_new_tab

from docopt import docopt

from . import api


VERSION = 'habitica version 0.0.11'
CACHE_FILE = '~/.habitica.cache'
TASK_VALUE_BASE = 0.9747  # http://habitica.wikia.com/wiki/Task_Value
HABITICA_REQUEST_WAIT_TIME = 0.5  # time to pause between concurrent requests
HABITICA_TASKS_PAGE = 'https://habitica.com/#/tasks'
# https://trello.com/c/4C8w1z5h/17-task-difficulty-settings-v2-priority-multiplier
PRIORITY = {'easy': 1,
            'medium': 1.5,
            'hard': 2}


def load_netrc(host='habitica.com'):
    accts = netrc.netrc()
    authn = accts.authenticators(host)
    return {'x-api-user': authn[0], 'x-api-key': authn[2]}

def clear_cache():
    """delete the cache file CACHE_FILE."""
    try:
        os.remove(os.path.expanduser(CACHE_FILE))
    except OSError:
        pass  # overwhelmingly, the cache file wasn't there
    print('cache file (%s) deleted' % CACHE_FILE)


def get_task_ids(args, key='<task-id>'):
    """
    handle task-id formats such as:
        habitica todos done 3
        habitica todos done 1,2,3
        habitica todos done 2 3
        habitica todos done 1-3,4
    """
    task_ids = []
    for raw_arg in args[key]:
        for bit in raw_arg.split(','):
            if '-' in bit:
                start, stop = [int(e) for e in bit.split('-')]
                task_ids.extend(range(start, stop + 1))
            else:
                task_ids.append(int(bit))
    return [e - 1 for e in set(task_ids)]


def updated_task_list(tasks, tids):
    for tid in sorted(tids, reverse=True):
        del(tasks[tid])
    return tasks


def print_task_list(tasks):
    for i, task in enumerate(tasks):
        completed = 'x' if task['completed'] else ' '
        print('[%s] %s %s' % (completed, i + 1, task['text']))


def qualitative_task_score_from_value(value):
    # task value/score info: http://habitica.wikia.com/wiki/Task_Value
    scores = ['*', '**', '***', '****', '*****', '******', '*******']
    breakpoints = [-20, -10, -1, 1, 5, 10]
    return scores[bisect(breakpoints, value)]


def cli():
    """Habitica command-line interface.

    usage:
      habitica status
      habitica habits|dailies|todos
      habitica habits up <task-id>
      habitica habits down <task-id>
      habitica dailies done <task-id>
      habitica dailies undo <task-id>
      habitica todos done <task-id>...
      habitica todos add <task>... [--difficulty=<d>]
      habitica server
      habitica home

    options:
      -h --help         Show this screen
      --version         Show version
      --difficulty=<d>  (easy | medium | hard) [default: easy]

    Subcommands:
      status                 Show HP, XP, GP, and more for user
      habits                 List habit tasks
      habits up <task-id>    Up (+) habit <task-id>
      habits down <task-id>  Down (-) habit <task-id>
      dailies                List daily tasks
      dailies done           Mark daily <task-id> complete
      dailies undo           Mark daily <task-id> incomplete
      todos                  List todo tasks
      todos done <task-id>   Mark todo <task-id> completed
      todos add <task>       Add todo with description <task>
      server                 Show status of Habitica service
      home                   Open tasks page in default browser
    """

    # set up auth
    auth = load_netrc()

    # set up args
    args = docopt(cli.__doc__, version=VERSION)

    # instantiate api service
    hbt = api.Habitica(auth=auth)

    # GET server status
    if args['server']:
        server = hbt.status()
        if server['status'] == 'up':
            print('Habitica server is up')
        else:
            print('Habitica server down... or your computer cannot connect')

    # open HOME
    elif args['home']:
        print('Opening %s' % HABITICA_TASKS_PAGE)
        open_new_tab(HABITICA_TASKS_PAGE)

    # GET user
    elif args['status']:
        user = hbt.user()
        stats = user.get('stats', '')
        items = user.get('items', '')
        food_count = sum(items['food'].values())
        party = user.get('party', '')
        quest = party['quest'].get('key', '')
        quest_progress = party['quest'].get('progress', '')
        title = 'Level %d %s' % (stats['lvl'], stats['class'].capitalize())
        health = '%d/%d' % (stats['hp'], stats['maxHealth'])
        xp = '%d/%d' % (int(stats['exp']), stats['toNextLevel'])
        mana = '%d/%d' % (int(stats['mp']), stats['maxMP'])
        currentPet = items.get('currentPet', '')
        pet = '%s (%d food items)' % (currentPet, food_count)
        mount = items.get('currentMount', '')
        len_ljust = max(map(len, ('health', 'xp', 'mana', 'pet', 'mount'))) + 1
        print('-' * len(title))
        print(title)
        print('-' * len(title))
        print('%s %s' % ('Health:'.rjust(len_ljust, ' '), health))
        print('%s %s' % ('XP:'.rjust(len_ljust, ' '), xp))
        print('%s %s' % ('Mana:'.rjust(len_ljust, ' '), mana))
        print('%s %s' % ('Pet:'.rjust(len_ljust, ' '), pet))
        print('%s %s' % ('Mount:'.rjust(len_ljust, ' '), mount))

    # GET/POST habits
    elif args['habits']:
        tids = get_task_ids(args)
        habits = hbt.user.tasks(type='habit')
        if args['up']:
            for tid in tids:
                tval = habits[tid]['value']
                hbt.user.tasks(_id=habits[tid]['id'],
                               _direction='up', _method='post')
                print('incremented task \'%s\'' % habits[tid]['text'])
                habits[tid]['value'] = tval + (TASK_VALUE_BASE ** tval)
                sleep(HABITICA_REQUEST_WAIT_TIME)
        elif args['down']:
            for tid in tids:
                tval = habits[tid]['value']
                hbt.user.tasks(_id=habits[tid]['id'],
                               _direction='down', _method='post')
                print('decremented task \'%s\'' % habits[tid]['text'])
                habits[tid]['value'] = tval - (TASK_VALUE_BASE ** tval)
                sleep(HABITICA_REQUEST_WAIT_TIME)
        for i, task in enumerate(habits):
            score = qualitative_task_score_from_value(task['value'])
            print('[%s] %s %s' % (score, i + 1, task['text']))

    # GET/PUT tasks:daily
    elif args['dailies']:
        tids = get_task_ids(args)
        dailies = hbt.user.tasks(type='daily')
        if args['done']:
            for tid in tids:
                hbt.user.tasks(_id=dailies[tid]['id'],
                               _direction='up', _method='post')
                print('marked daily \'%s\' completed' % dailies[tid]['text'])
                dailies[tid]['completed'] = True
                sleep(HABITICA_REQUEST_WAIT_TIME)
        elif args['undo']:
            for tid in tids:
                hbt.user.tasks(_id=dailies[tid]['id'],
                               _method='put', completed=False)
                print('marked daily \'%s\' incomplete' % dailies[tid]['text'])
                dailies[tid]['completed'] = False
                sleep(HABITICA_REQUEST_WAIT_TIME)
        print_task_list(dailies)

    # GET tasks:todo
    elif args['todos']:
        tids = get_task_ids(args)
        todos = [e for e in hbt.user.tasks(type='todo')
                 if not e['completed']]
        if args['done']:
            for tid in tids:
                hbt.user.tasks(_id=todos[tid]['id'],
                               _direction='up', _method='post')
                print('marked todo \'%s\' complete' % todos[tid]['text'])
                sleep(HABITICA_REQUEST_WAIT_TIME)
            todos = updated_task_list(todos, tids)
        elif args['add']:
            ttext = ' '.join(args['<task>'])
            hbt.user.tasks(type='todo',
                           text=ttext,
                           priority=PRIORITY[args['--difficulty']],
                           _method='post')
            todos.insert(0, {'completed': False, 'text': ttext})
            print('added new todo \'%s\'' % ttext)
        print_task_list(todos)


if __name__ == '__main__':
    cli()
