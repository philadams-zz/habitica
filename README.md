hrpg
====

Two tools for interacting with [HabitRPG](http://habitrpg.com):

1. Python wrapper for the RESTful Habit RPG api (`hrpg.api`)
2. Command-line interface with subcommands (e.g. `> hrpg todos`)

install
-------

First `pip install hrpg`. Then, using `hrpgrc.sample.json` as a template,
you'll want to add your API credentials to an `~/.hrpgrc` file in your home
directory.

Your userID and API token are available on the [HabitRPG options/setting/api
page](https://habitrpg.com/#/options/settings/api).

usage
-----

What's my character's status?

    > hrpg status
    --------------
    Level 62 Rogue
    --------------
    Health: 49/50
    XP: 471/1720
    Mana: 4/103

Show me my habits, and how well I'm doing with each:

    > hrpg habits
    [*******] 1 commit code
    [****] 2 drink water
    [******] 3 encourage others

Record improvement with a habit:

    > hrpg habits up 2
    incremented task 'drink water'
    [*******] 1 commit code
    [****] 2 drink water
    [******] 3 encourage others

Show me my dailies and each daily's state:

    > hrpg dailies
    [ ] 1 pushups (5x20)
    [ ] 2 clean dishes before bed
    [x] 3 2x90mins writing

Complete a daily task:

    > hrpg dailies done 1
    marked daily 'pushups (5x20)' completed
    [x] 1 pushups (5x20)
    [ ] 2 clean dishes before bed
    [x] 3 2x90mins writing

Show me my todo items:

    > hrpg todos
    [ ] update hrpg README with example instructions
    [ ] vacuum my car
    [ ] read Bell and Jofish "Designing technology for domestic spaces"

Complete a todo:

    > hrpg todos done 1
    marked todo 'update hrpg README with example instructions' complete
    [ ] vacuum my car
    [ ] read Bell and Jofish "Designing technology for domestic spaces"

Is the HabitRPG server up?

    > hrpg server
    Habit RPG server is up

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
