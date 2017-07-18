import subprocess

import click

from prompt_toolkit.shortcuts import create_prompt_application, run_application
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from .completion import BashCompleter
from .prompt import style, get_prompt_tokens
from .settings import settings
from .history import get_history
from .utils import get_xdg_json_data


def prompt(application, **kwargs):
    """
    Operate on application
    """

    patch_stdout = kwargs.pop('patch_stdout', False)
    return_asyncio_coroutine = kwargs.pop('return_asyncio_coroutine', False)
    true_color = kwargs.pop('true_color', False)
    refresh_interval = kwargs.pop('refresh_interval', 0)
    eventloop = kwargs.pop('eventloop', None)

    return run_application(application,
        patch_stdout=patch_stdout,
        return_asyncio_coroutine=return_asyncio_coroutine,
        true_color=true_color,
        refresh_interval=refresh_interval,
        eventloop=eventloop
    )


@click.command()
@click.argument('command')
@click.option('--prompt', help='Override prompt')
def main(command, **kwargs):
    history = FileHistory(get_history(command))
    aliases = get_xdg_json_data('aliases.json')
    completer = BashCompleter(command, aliases)

    prompt_str = kwargs.get('prompt') or command

    while True:
        try:
            _get_prompt_tokens = get_prompt_tokens(prompt_str)

            application = create_prompt_application('',
                completer=completer, history=history,
                complete_while_typing=False, vi_mode=True,
                style=style, get_prompt_tokens=_get_prompt_tokens,
                auto_suggest=AutoSuggestFromHistory()
            )
            subcommand = prompt(application)
            if subcommand.strip() == '!!':
                subcommand = application.buffer.history.strings[-2]
                application.buffer.history.strings[-1] = subcommand
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
