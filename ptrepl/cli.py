import subprocess

import click

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory

from .completion import BashCompleter
from .prompt import style, get_prompt_tokens
from .settings import *
from .alias import get_aliases
from .history import get_history


@click.command()
@click.argument('command')
def main(command):
    history = FileHistory(get_history(command))
    completer = BashCompleter(command)
    aliases = get_aliases()

    while True:
        try:
            _get_prompt_tokens = get_prompt_tokens(command)
            subcommand = prompt('',
                                completer=completer, history=history,
                                complete_while_typing=False, vi_mode=True,
                                style=style, get_prompt_tokens=_get_prompt_tokens)
            subcommand = completer.get_real_subcommand(subcommand)
            if subcommand is None:
                break
            if subcommand and subcommand[0] == BASH_EXEC:
                call_command = subcommand[1:]
            else:
                call_command = ' '.join([command, subcommand])
            if call_command in aliases:
                call_command = aliases[call_command]
            subprocess.call(call_command, shell=True)
        except EOFError:
            break  # Control-D pressed.
        except KeyboardInterrupt:
            pass
    print('GoodBye!')
