import subprocess

import click

from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.contrib.completers import SystemCompleter

from pygments.lexers import BashLexer


EXIT_COMMAND = 'exit'

@click.command()
@click.argument('command')
def main(command):
    history = InMemoryHistory()

    while True:
        try:
            subcommand = prompt('{command} > '.format(command=command),
                                lexer=BashLexer, completer=SystemCompleter(),
                                history=history)
            if subcommand == EXIT_COMMAND:
                break
            subcommand = subcommand.split()
            call_command = command.split()
            call_command.extend(subcommand)
            subprocess.call(call_command)
        except EOFError:
            break  # Control-D pressed.
        except KeyboardInterrupt:
            pass
    print('GoodBye!')


if __name__ == '__main__':
    main()
