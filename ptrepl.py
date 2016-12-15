import subprocess

import click

from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.contrib.completers import WordCompleter

from bash_completion import get_completions

EXIT_COMMAND = 'exit'


@click.command()
@click.argument('command')
def main(command):
    history = InMemoryHistory()
    completions = get_completions(command)
    completer = WordCompleter(completions[0])

    while True:
        try:
            subcommand = prompt('{command} > '.format(command=command),
                                completer=completer, history=history)
            if subcommand == EXIT_COMMAND:
                break
            if subcommand[0] == '$':
                call_command = subcommand[1:].split()
            else:
                call_subcommand = subcommand.split()
                call_command = command.split()
                call_command.extend(call_subcommand)
            subprocess.call(call_command)
        except EOFError:
            break  # Control-D pressed.
        except KeyboardInterrupt:
            pass
    print('GoodBye!')


if __name__ == '__main__':
    main()
