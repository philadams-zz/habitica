hrpg
====

Three tools for interacting with [HabitRPG](http://habitrpg.com):

1. Python wrapper for the RESTful Habit RPG api (`hrpg.api`)
2. Command-line interface with subcommands (e.g. `> hrpg habits`)
3. An interactive command-line interface (`hrpg --interactive` - in
   development)

install
-------

First `pip install hrpg`. Then you'll want to TODO API credentials.

help
----

Via `hrpg --help`:

TODO

thanks
------

Much thanks to the following excellent projects:

- docopt
- requests

future
------

- figure out the cleanest way to select a task for an action (tid sucks)
- test harness
- prettify with [clint](https://github.com/kennethreitz/clint)
- POST endpoints
