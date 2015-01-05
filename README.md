hrpg
====

Two tools for interacting with [HabitRPG](http://habitrpg.com):

1. Python wrapper for the RESTful Habit RPG api (`hrpg.api`)
2. Command-line interface with subcommands (e.g. `> hrpg todos`)

install
-------

First `pip install hrpg`. Then you'll want to TODO API credentials.

examples
--------

Coming soon.

help
----

Via `hrpg --help`:

    HabitRPG command-line interface.

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

thanks
------

Many thanks to the following excellent projects:

- [docopt](https://github.com/docopt/docopt)
- [requests](https://github.com/kennethreitz/requests)
