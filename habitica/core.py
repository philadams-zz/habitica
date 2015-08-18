#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Phil Adams http://philadams.net

habitica: commandline interface for http://habitica.com
http://github.com/philadams/habitica

TODO:philadams update README with new-look --help
TODO:philadams add logging statements
TODO:philadams add logging to .api
TODO:philadams get logger named, like requests!
"""


from bisect import bisect
import ConfigParser
import json
import logging
import netrc
import os.path
from time import sleep
from webbrowser import open_new_tab

from docopt import docopt

from . import api

from pprint import pprint


VERSION = 'habitica version 0.0.12'
TASK_VALUE_BASE = 0.9747  # http://habitica.wikia.com/wiki/Task_Value
HABITICA_REQUEST_WAIT_TIME = 0.5  # time to pause between concurrent requests
HABITICA_TASKS_PAGE = 'https://habitica.com/#/tasks'
# https://trello.com/c/4C8w1z5h/17-task-difficulty-settings-v2-priority-multiplier
PRIORITY = {'easy': 1,
            'medium': 1.5,
            'hard': 2}
CONFIG_FILE = os.path.join(os.path.expanduser('~'), '.habitica.cfg')
SECTION = 'habitica'


def load_netrc(host='habitica.com'):
    logging.debug('Loading ~/.netrc credentials...')
    accts = netrc.netrc()
    authn = accts.authenticators(host)
    return {'x-api-user': authn[0], 'x-api-key': authn[2]}


def load_config():
    logging.debug('Loading cached config data (%s)...' % CONFIG_FILE)
    defaults = {'quest_key': '',
                'quest_s': 'Not currently on a quest'}
    config = ConfigParser.SafeConfigParser(defaults)
    config.read(CONFIG_FILE)
    if not config.has_section(SECTION):
        config.add_section(SECTION)
    return config


def update_config(**kwargs):
    logging.debug('Updating (and caching) config data (%s)...' % CONFIG_FILE)
    config = load_config()
    for key, val in kwargs.items():
        config.set(SECTION, key, val)
    with open(CONFIG_FILE, 'wb') as f:
        config.write(f)
    config.read(CONFIG_FILE)
    return config


def get_task_ids(tids):
    """
    handle task-id formats such as:
        habitica todos done 3
        habitica todos done 1,2,3
        habitica todos done 2 3
        habitica todos done 1-3,4 8
    tids is a seq like (last example above) ('1-3,4' '8')
    """
    logging.debug('raw task ids: %s' % tids)
    task_ids = []
    for raw_arg in tids:
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

    Usage: habitica [--version] [--help]
                    <command> [<args>...] [--difficulty=<d>]
                    [--verbose | --debug]

    Options:
      -h --help         Show this screen
      --version         Show version
      --difficulty=<d>  (easy | medium | hard) [default: easy]
      --verbose         Show some logging information
      --debug           Some all logging information

    The habitica commands are:
      status                 Show HP, XP, GP, and more
      habits                 List habit tasks
      habits up <task-id>    Up (+) habit <task-id>
      habits down <task-id>  Down (-) habit <task-id>
      dailies                List daily tasks
      dailies done           Mark daily <task-id> complete
      dailies undo           Mark daily <task-id> incomplete
      todos                  List todo tasks
      todos done <task-id>   Mark one or more todo <task-id> completed
      todos add <task>       Add todo with description <task>
      server                 Show status of Habitica service
      home                   Open tasks page in default browser

    For `habits up|down`, `dailies done|undo`, and `todos done`, you can pass
    one or more <task-id> parameters, using either comma-separated lists or
    ranges or both. For example, `todos done 1,3,6-9,11`.
    """

    # set up args
    args = docopt(cli.__doc__, version=VERSION)

    # set up logging
    if args['--verbose']:
        logging.basicConfig(level=logging.INFO)
    if args['--debug']:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug('Command line args: {%s}' % ', '.join("'%s': '%s'" % (k, v) for k, v in args.items()))

    # set up auth
    auth = load_netrc()
    config = load_config()

    # instantiate api service
    hbt = api.Habitica(auth=auth)

    # GET server status
    if args['<command>'] == 'server':
        server = hbt.status()
        if server['status'] == 'up':
            print('Habitica server is up')
        else:
            print('Habitica server down... or your computer cannot connect')

    # open HABITICA_TASKS_PAGE
    elif args['<command>'] == 'home':
        print('Opening %s' % HABITICA_TASKS_PAGE)
        open_new_tab(HABITICA_TASKS_PAGE)

    # GET user
    elif args['<command>'] == 'status':

        # gather status info
        user = hbt.user()
        party = hbt.groups.party()
        stats = user.get('stats', '')
        items = user.get('items', '')
        food_count = sum(items['food'].values())
        quest = 'Not currently on a quest'
        if party['quest'] and party['quest']['active']:
            quest_key = party['quest']['key']
            if config.get(SECTION, 'quest_key') != quest_key:
                logging.info('Updating quest information...')
                # we're on a new quest, update quest key
                # and hit /content/ quests.<quest.key> for progress info
                # store in config 'quest_s' a repr for the quest's progress
                content = hbt.content()
                # TODO:philadams unjankify this for different quest types...
                # suspect we do one thing for boss quests,
                # and for collection types we naively search down to 'count'
                quest_max = content['quests'][quest_key]['collect']['moonstone']['count']
                quest_progress = party['quest']['progress']['collect']['moonstone']
                quest_s = '%s/%s "%s"' % (quest_progress, quest_max,
                                        content['quests'][quest_key]['text'])
                config = update_config(quest_key=quest_key, quest_s=quest_s)
            quest = config.get(SECTION, 'quest_s')

        # prepare and print status strings
        title = 'Level %d %s' % (stats['lvl'], stats['class'].capitalize())
        health = '%d/%d' % (stats['hp'], stats['maxHealth'])
        xp = '%d/%d' % (int(stats['exp']), stats['toNextLevel'])
        mana = '%d/%d' % (int(stats['mp']), stats['maxMP'])
        currentPet = items.get('currentPet', '')
        pet = '%s (%d food items)' % (currentPet, food_count)
        mount = items.get('currentMount', '')
        summary_items = ('health', 'xp', 'mana', 'quest', 'pet', 'mount')
        len_ljust = max(map(len, summary_items)) + 1
        print('-' * len(title))
        print(title)
        print('-' * len(title))
        print('%s %s' % ('Health:'.rjust(len_ljust, ' '), health))
        print('%s %s' % ('XP:'.rjust(len_ljust, ' '), xp))
        print('%s %s' % ('Mana:'.rjust(len_ljust, ' '), mana))
        print('%s %s' % ('Pet:'.rjust(len_ljust, ' '), pet))
        print('%s %s' % ('Mount:'.rjust(len_ljust, ' '), mount))
        print('%s %s' % ('Quest:'.rjust(len_ljust, ' '), quest))

    # GET/POST habits
    elif args['<command>'] == 'habits':
        habits = hbt.user.tasks(type='habit')
        if 'up' in args['<args>']:
            tids = get_task_ids(args['<args>'][1:])
            for tid in tids:
                tval = habits[tid]['value']
                hbt.user.tasks(_id=habits[tid]['id'],
                               _direction='up', _method='post')
                print('incremented task \'%s\'' % habits[tid]['text'])
                habits[tid]['value'] = tval + (TASK_VALUE_BASE ** tval)
                sleep(HABITICA_REQUEST_WAIT_TIME)
        elif 'down' in args['<args>']:
            tids = get_task_ids(args['<args>'][1:])
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
    elif args['<command>'] == 'dailies':
        dailies = hbt.user.tasks(type='daily')
        if 'done' in args['<args>']:
            tids = get_task_ids(args['<args>'][1:])
            for tid in tids:
                hbt.user.tasks(_id=dailies[tid]['id'],
                               _direction='up', _method='post')
                print('marked daily \'%s\' completed' % dailies[tid]['text'])
                dailies[tid]['completed'] = True
                sleep(HABITICA_REQUEST_WAIT_TIME)
        elif 'undo' in args['<args>']:
            tids = get_task_ids(args['<args>'][1:])
            for tid in tids:
                hbt.user.tasks(_id=dailies[tid]['id'],
                               _method='put', completed=False)
                print('marked daily \'%s\' incomplete' % dailies[tid]['text'])
                dailies[tid]['completed'] = False
                sleep(HABITICA_REQUEST_WAIT_TIME)
        print_task_list(dailies)

    # GET tasks:todo
    elif args['<command>'] == 'todos':
        todos = [e for e in hbt.user.tasks(type='todo')
                 if not e['completed']]
        if 'done' in args['<args>']:
            tids = get_task_ids(args['<args>'][1:])
            for tid in tids:
                hbt.user.tasks(_id=todos[tid]['id'],
                               _direction='up', _method='post')
                print('marked todo \'%s\' complete' % todos[tid]['text'])
                sleep(HABITICA_REQUEST_WAIT_TIME)
            todos = updated_task_list(todos, tids)
        elif 'add' in args['<args>']:
            ttext = ' '.join(args['<args>'][1:])
            hbt.user.tasks(type='todo',
                           text=ttext,
                           priority=PRIORITY[args['--difficulty']],
                           _method='post')
            todos.insert(0, {'completed': False, 'text': ttext})
            print('added new todo \'%s\'' % ttext)
        print_task_list(todos)


if __name__ == '__main__':
    cli()
