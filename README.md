habitica
========

Two tools for interacting with [Habitica](http://habitica.com):

1. Python wrapper for the RESTful Habitica API (`habitica.api`)
2. Command-line interface with subcommands (e.g. `> habitica todos`)

install
-------

First `pip install habitica`. Then, using `habiticarc.sample.json` as a
template, you'll want to add your API credentials to an `~/.habiticarc` file in
your home directory.

Your userID and API token are available on the [Habitica options/setting/api
page](https://habitica.com/#/options/settings/api).

usage
-----

What's my character's status?

    > habitica status
    --------------
    Level 83 Rogue
    --------------
    Health: 50/50
    XP: 904/2690
    Mana: 133/218
    Pet: Gryphon-Base (11 food items)
    Mount: FlyingPig-Base

Show me my todo items:

    > habitica todos
    [ ]  1 update habitica README with example instructions
    [ ]  2 vacuum the car
    [ ]  3 read Bell and Jofish "Designing technology for domestic spaces"
    [ ]  4 order new contact lenses
    [ ]  5 complete Keppi project report and share with Geri
    [ ]  6 set up dinner with friends at Agava for Saturday night

Complete a todo:

    > habitica todos done 1
    marked todo 'update habitica README with example instructions' complete
    [ ] 1 vacuum the car
    [ ] 2 read Bell and Jofish "Designing technology for domestic spaces"
    [ ] 3 order new contact lenses
    [ ] 4 complete Keppi project report and share with Geri
    [ ] 5 make reservation at Agava for Saturday night

Complete multiple todos. All `done`, `undo`, `up`, `down` commands can take 1
or more tasks as arguments, using either comma-separated lists or ranges or
both:

    > habitica todos done 1,3-5
    marked todo 'update habitica README with example instructions' complete
    marked todo 'vacuum the car' complete
    marked todo 'order new contact lenses' complete
    marked todo 'complete Keppi project report and share with Geri' complete
    marked todo 'make reservation at Agava for Saturday night' complete
    [ ] 1 read Bell and Jofish "Designing technology for domestic spaces"

Add a new (hard!) todo. By default `--difficulty=easy`:

    > habitica todos add finish dissertation --difficulty=hard
    added new todo 'finish dissertation'
    [ ] 1 finish dissertation
    [ ] 2 read Bell and Jofish "Designing technology for domestic spaces"

Show me my habits, and how well I'm doing with each:

    > habitica habits
    [*******] 1 commit code
    [****] 2 drink water
    [******] 3 encourage others

Record improvement with some habits:

    > habitica habits up 2,3
    incremented task 'drink water'
    incremented task 'encourage others'
    [*******] 1 commit code
    [****] 2 drink water
    [******] 3 encourage others

Show me my dailies and each daily's state:

    > habitica dailies
    [ ] 1 pushups (5x20)
    [ ] 2 clean dishes before bed
    [x] 3 2x90mins writing

Complete a daily task:

    > habitica dailies done 1
    marked daily 'pushups (5x20)' completed
    [x] 1 pushups (5x20)
    [ ] 2 clean dishes before bed
    [x] 3 2x90mins writing

Is the Habitica server up?

    > habitica server
    Habit RPG server is up

help
----

Via `habitica --help`:

    Habitica command-line interface.

        usage:
          habitica status
          habitica habits|dailies|todos
          habitica habits up <task-id>
          habitica habits down <task-id>
          habitica dailies done <task-id>
          habitica dailies undo <task-id>
          habitica todos done <task-id>...
          habitica todos add <task>...
          habitica server
          habitica home

        options:
          -h --help          Show this screen
          --version          Show version

        Subcommands:
          status                 Show HP, XP, GP, and more for user
          habits                 List habit tasks
          habits up <task-id>    Up (+) habit <task-id>
          habits down <task-id>  Up (+) habit <task-id>
          dailies                List daily tasks
          dailies done           Mark daily <task-id> complete
          dailies undo           Mark daily <task-id> incomplete
          todos                  List todo tasks
          todos done <task-id>   Mark todo <task-id> completed
          todos add <task>       Add todo with description <task>
          server                 Show status of Habitica service
          home                   Open Habitica tasks page in default browser

thanks
------

Many thanks to the following excellent projects:

- [docopt](https://github.com/docopt/docopt)
- [requests](https://github.com/kennethreitz/requests)
