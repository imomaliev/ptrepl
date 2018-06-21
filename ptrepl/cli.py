import subprocess

import click

from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from .completion import BashCompleter
from .prompt import get_prompt_tokens
from .settings import settings
from .history import get_history
from .utils import get_xdg_json_data


@click.command()
@click.argument('command')
@click.option('--prompt', help='Override prompt')
def main(command, **kwargs):
    history = FileHistory(get_history(command))
    aliases = get_xdg_json_data('aliases.json')
    completer = BashCompleter(command, aliases)

    prompt_str = kwargs.get('prompt') or command

    application = PromptSession(
        '',
        completer=completer,
        history=history,
        complete_while_typing=False,
        enable_system_prompt=True,
        enable_suspend=True,
        vi_mode=settings.VI_MODE,
        auto_suggest=AutoSuggestFromHistory(),
        enable_history_search=True
    )

    while True:
        try:
            _get_prompt_tokens = get_prompt_tokens(prompt_str)
            subcommand = application.prompt(_get_prompt_tokens)
            if subcommand.strip() == '!!':
                subcommand = application.default_buffer.history.get_strings()[-2]
                application.default_buffer.history.get_strings()[-1] = subcommand
            subcommand = completer.get_real_subcommand(subcommand)
            if subcommand is None:
                break

            call_command = ' '.join([command, subcommand])
            if call_command in aliases:
                call_command = aliases[call_command]
            subprocess.call(call_command, shell=True)
        except EOFError:
            break  # Control-D pressed.
        except KeyboardInterrupt:
            pass
    print('GoodBye!')
