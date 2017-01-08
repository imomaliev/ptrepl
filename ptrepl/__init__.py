#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import datetime

import click

from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.token import Token
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.key_binding.vi_state import InputMode

from .completion import BashCompleter
from .settings import *


style = style_from_dict({
    Token.Prompt.Venv: '#ansilightgray bold',
    Token.Prompt.Path: '#ansiblue bold',
    Token.Prompt.Branch: '#ansiyellow bold',
    Token.Prompt.Command: '#ansiturquoise bold',
    Token.Prompt.DateTime: '#ansigreen bold'
})


def _get_venv():
    if os.getenv('VIRTUAL_ENV'):
        ps1 = os.getenv('PS1')
        venv = ps1.split('(', 1)[1].split(')', 1)[0]
        return '({}) '.format(venv)
    else:
        return ''


def _get_cwd():
    cwd = os.getcwd().replace(os.path.expanduser('~'), '~')
    return '{} '.format(cwd)


def _get_branch():
    branch_commnads = [
        'git rev-parse --abbrev-ref HEAD',
        'hg branch'
    ]
    for cmd in branch_commnads:
        try:
            branch = subprocess.check_output(
                cmd, shell=True,
                stderr=subprocess.DEVNULL
            )
            return '[{}] '.format(branch.strip().decode())
        except subprocess.CalledProcessError as e:
            pass
    else:
        return ''


def _get_datetime():
    return '|{}| '.format(datetime.datetime.now().strftime(DATETIME_FORMAT))


@click.command()
@click.argument('command')
def main(command):
    history = InMemoryHistory()
    completer = BashCompleter(command)
    venv = _get_venv()
    cwd = _get_cwd()

    def get_prompt_tokens(cli):
        mode = VI_NORMAL_MODE if cli.vi_state.input_mode == InputMode.INSERT else VI_EDIT_MODE
        return [
            (Token.Prompt, ' '),
            (Token.Prompt.Venv, venv),
            (Token.Prompt.Path, cwd),
            (Token.Prompt.Branch, _get_branch()),
            (Token.Prompt.DateTime, _get_datetime()),
            (Token.Prompt, '\n'),
            (Token.Prompt, '{mode} '.format(mode=mode)),
            (Token.Prompt.Command, '{command} '.format(command=command)),
            (Token.Prompt, '❯ '.format(mode=mode, command=command)),
        ]

    while True:
        try:
            subcommand = prompt('',
                                completer=completer, history=history,
                                complete_while_typing=False, vi_mode=True,
                                style=style, get_prompt_tokens=get_prompt_tokens)
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
