from prompt_toolkit.completion import Completer, Completion

from .bash_completion import bash_completions

from .settings import settings


# https://github.com/xonsh/xonsh/blob/master/xonsh/ptk/completer.py
class BashCompleter(Completer):
    def __init__(self, command, aliases):
        self.command = command
        self.aliases = aliases

    def get_completions(self, document, complete_event):
        command = self.command
        subcommand = self.get_real_subcommand(document.text)
        word = document.get_word_before_cursor(WORD=True)
        if not subcommand:
            return
        line = ' '.join([command, subcommand])
        start_position = -len(word)
        split = line.split()
        if len(split) > 1 and not line.endswith(' '):
            prefix = split[-1]
            begidx = len(line.rsplit(prefix)[0])
        else:
            prefix = ''
            begidx = len(line)

        endidx = len(line)
        for completion in bash_completions(prefix, line, begidx, endidx)[0]:
            yield Completion(completion.strip('\'"'), start_position=start_position)
        if len(split) == 2:
            for a in self.aliases:
                if a.startswith('{} {}'.format(command, prefix)):
                    yield Completion(
                        a.replace('{} '.format(command), ''),
                        start_position=start_position,
                    )

    def get_real_subcommand(self, subcommand):
        """
        Strip preceding whitespaces, if subcommand starts with command ignore it,
        if subcommand is equal to exit return None
        """
        subcommand = subcommand.lstrip()
        if subcommand.strip() == settings.EXIT_COMMAND:
            return None
        command_with_space = '{} '.format(self.command)
        if subcommand.startswith(command_with_space):
            subcommand = subcommand.replace(command_with_space, '')
        return subcommand
