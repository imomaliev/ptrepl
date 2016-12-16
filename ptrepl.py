import subprocess

import click

from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import Completer, Completion

from bash_completion import get_completions

EXIT_COMMAND = 'exit'


class BashCompleter(Completer):
    def __init__(self, command):
        self.command = command

    def get_completions(self, document, complete_event):
        subcommand = document.text.rsplit(' ', 1)
        start_position = -len(subcommand) if subcommand else 0
        for completion in get_completions(' '.join([self.command, document.text]))[0]:
            yield Completion(completion, start_position=start_position)


@click.command()
@click.argument('command')
def main(command):
    history = InMemoryHistory()
    completer = BashCompleter(command)
    while True:
        try:
            subcommand = prompt('{command} > '.format(command=command),
                                completer=completer, history=history,
                                complete_while_typing=False)
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
