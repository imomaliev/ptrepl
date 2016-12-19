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


class BashCompleter(Completer):
    def __init__(self, command):
        self.command = command

    def get_completions(self, document, complete_event):
        text = document.text.lstrip()
        word = document.get_word_before_cursor(WORD=True)
        if text[0] == BASH_EXEC:
            command_for_completion = text[1:]
        else:
            command_for_completion = ' '.join([self.command, text])
        start_position = -len(document.get_word_before_cursor(WORD=True))
        if text == word and word[0] == BASH_EXEC:
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
            if subcommand == EXIT_COMMAND:
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
