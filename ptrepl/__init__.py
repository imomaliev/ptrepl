#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

import click

from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.token import Token
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.key_binding.vi_state import InputMode

from bash_completion import get_completions

EXIT_COMMAND = 'exit'
BASH_EXEC = '$'
VI_EDIT_MODE = ':'
VI_NORMAL_MODE = '+'


style = style_from_dict({
    # need space after bg for applying to text
    Token.Prompt.Venv: 'bg: #ansilightgray bold',
    Token.Prompt.Path: 'bg: #ansiblue bold',
    Token.Prompt.Branch: 'bg: #ansiyellow bold',
    Token.Prompt.Command: 'bg: #0088a8 bold'
})


def _get_real_subcommand(command, subcommand):
    """
    Strip preceding whitespaces, if subcommand starts with command ignore it,
    if subcommand is equal to exit return None
    """
    subcommand = subcommand.lstrip()
    if subcommand.strip() == EXIT_COMMAND:
        return None
    command_with_space = '{} '.format(command)
    if subcommand.startswith(command_with_space):
        subcommand = subcommand.replace(command_with_space, '')
    return subcommand


class BashCompleter(Completer):
    def __init__(self, command):
        self.command = command

    def get_completions(self, document, complete_event):
        subcommand = _get_real_subcommand(self.command, document.text)
        word = document.get_word_before_cursor(WORD=True)
        if subcommand[0] == BASH_EXEC:
            command_for_completion = subcommand[1:]
        else:
            command_for_completion = ' '.join([self.command, subcommand])
        start_position = -len(word)
        if subcommand == word and word[0] == BASH_EXEC:
            start_position += 1
        for completion in get_completions(command_for_completion)[0]:
            yield Completion(completion, start_position=start_position)


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


@click.command()
@click.argument('command')
def main(command):
    history = InMemoryHistory()
    completer = BashCompleter(command)
    venv = _get_venv()
    cwd = _get_cwd()
    branch = _get_branch()

    def get_prompt_tokens(cli):
        mode = VI_NORMAL_MODE if cli.vi_state.input_mode == InputMode.INSERT else VI_EDIT_MODE
        return [
            (Token.Prompt, ' '),
            (Token.Prompt.Venv, venv),
            (Token.Prompt.Path, cwd),
            (Token.Prompt.Branch, branch),
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
            subcommand = _get_real_subcommand(command, subcommand)
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
