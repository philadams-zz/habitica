#
# Phil Adams http://philadams.net
# habitica: commandline interface for http://habitica.com
# http://github.com/philadams/habitica
#
# habitica shell completion script
# copy to /etc/bash_completion.d/
# or source in .bashrc/.zshrc
#

_habitica() 
{
    local cur prev opts base
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    #
    #  The basic options we'll complete.
    #
    opts="status habits dailies todos server home --help --version --verbose --debug"


    #
    #  Complete the arguments to some of the basic commands.
    #
    case "${prev}" in
        habits)
            local habitsopt="up down"
            COMPREPLY=( $(compgen -W "${habitsopt}" -- ${cur}) )
            return 0
            ;;
        dailies)
            local dailiesopt="done undo"
            COMPREPLY=( $(compgen -W "${dailiesopt}" -- ${cur}) )
            return 0
            ;;
        todos)
            local todosopt="done add"
            COMPREPLY=( $(compgen -W "${todosopt}" -- ${cur}) )
            return 0
            ;;
        *)
        ;;
    esac

   COMPREPLY=($(compgen -W "${opts}" -- ${cur}))  
   return 0
}

complete -F _habitica habitica
