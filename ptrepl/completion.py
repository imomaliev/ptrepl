from prompt_toolkit.completion import Completer, Completion

from bash_completion import get_completions

from .settings import *


class BashCompleter(Completer):
    def __init__(self, command):
        self.command = command

    def get_completions(self, document, complete_event):
        subcommand = self.get_real_subcommand(document.text)
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

    def get_real_subcommand(self, subcommand):
        """
        Strip preceding whitespaces, if subcommand starts with command ignore it,
        if subcommand is equal to exit return None
        """
        subcommand = subcommand.lstrip()
        if subcommand.strip() == EXIT_COMMAND:
            return None
        command_with_space = '{} '.format(self.command)
        if subcommand.startswith(command_with_space):
            subcommand = subcommand.replace(command_with_space, '')
        return subcommand
