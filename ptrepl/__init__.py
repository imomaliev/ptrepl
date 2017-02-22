#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

import click

from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory

from .completion import BashCompleter
from .prompt import style, get_prompt_tokens
from .settings import *


@click.command()
@click.argument('command')
def main(command):
    history = InMemoryHistory()
    completer = BashCompleter(command)

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
            subprocess.call(call_command, shell=True)
        except EOFError:
            break  # Control-D pressed.
        except KeyboardInterrupt:
            pass
    print('GoodBye!')


if __name__ == '__main__':
    main()
