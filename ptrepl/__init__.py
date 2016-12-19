#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

import click

from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import Completer, Completion

from bash_completion import get_completions

EXIT_COMMAND = 'exit'
BASH_EXEC = '$'


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
