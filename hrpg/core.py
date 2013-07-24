#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Phil Adams http://philadams.net

hrpg: commandline interface for http://habitrpg.com
http://github.com/philadams/hrpg
"""


import json

import requests
from docopt import docopt
from pprint import pprint

API_URI_BASE = 'https://habitrpg.com/api/v1'


def cli():
    """HabitRPG command-line interface.

    usage:
      hrpg status
      hrpg user [<uid>]
      hrpg tasks (--habit | --daily | --todo | --reward) [<uid>]
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
    args = docopt(cli.__doc__, version='hrpg version 0.0.2')

    if args['status']:
        req = requests.get(API_URI_BASE + '/status')
        if req.status_code == 200:
            res = json.loads(req.text)
            if res['status'] == 'up':
                print('Up and running! All is well.')
    elif args['user']:
        raise NotImplementedError
    elif args['tasks']:
        raise NotImplementedError
    elif args['task']:
        raise NotImplementedError


if __name__ == '__main__':
    cli()
