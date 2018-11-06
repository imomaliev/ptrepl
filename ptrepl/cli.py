import subprocess

import click

from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from .bash_history import expand_history, BashHistoryIndexError
from .completion import BashCompleter
from .prompt import get_prompt_tokens, PtreplSession
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

    session = PtreplSession(
        '',
        completer=completer,
        history=history,
        complete_while_typing=False,
        enable_system_prompt=True,
        enable_suspend=True,
        vi_mode=settings.VI_MODE,
        auto_suggest=AutoSuggestFromHistory(),
        enable_history_search=True,
    )

    while True:
        try:
            _get_prompt_tokens = get_prompt_tokens(prompt_str)
            subcommand = session.prompt(_get_prompt_tokens)
            try:
                subcommand, execute = expand_history(
                    subcommand, session.default_buffer.history.get_strings()
                )
            except BashHistoryIndexError as e:
                click.echo(
                    '{command}: {event}: event not found'.format(
                        command=command, event=e
                    )
                )
                continue
            if not execute:
                click.echo(subcommand)
                continue
            session.default_buffer.history.get_strings()[-1] = subcommand
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
    click.echo('GoodBye!')
