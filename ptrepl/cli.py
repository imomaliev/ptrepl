import subprocess

import click

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory

from .completion import BashCompleter
from .prompt import style, get_prompt_tokens
from .settings import settings
from .history import get_history
from .utils import get_xdg_json_data


@click.command()
@click.argument('command')
@click.option('--prompt', help='Override prompt')
def main(command, **kwargs):
    history = FileHistory(get_history(command))
    completer = BashCompleter(command)
    aliases = get_xdg_json_data('aliases.json')

    prompt_str = kwargs.get('prompt') or command

    while True:
        try:
            _get_prompt_tokens = get_prompt_tokens(prompt_str)
            subcommand = prompt('',
                                completer=completer, history=history,
                                complete_while_typing=False, vi_mode=True,
                                style=style, get_prompt_tokens=_get_prompt_tokens)
            subcommand = completer.get_real_subcommand(subcommand)
            if subcommand is None:
                break
            if subcommand and subcommand[0] == settings.BASH_EXEC:
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
