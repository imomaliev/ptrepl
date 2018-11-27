import subprocess

import click

from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory

from .bash.history import BashHistoryIndexError, expand_history

from .completion import BashCompleter
from .config import settings, get_aliases
from .history import get_history_file
from .prompt import PtreplSession, get_prompt_tokens


@click.command()
@click.argument('command')
@click.option('--prompt', help='Override prompt')
def main(command, **kwargs):
    history = FileHistory(get_history_file(command))
    aliases = get_aliases(command)
    completer = BashCompleter(command, aliases)

    prompt_str = kwargs.get('prompt') or command

    session = PtreplSession(
        command,
        aliases,
        message='',
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
                click.echo(f'{command}: {e}: event not found')
                continue
            if not execute:
                click.echo(subcommand)
                continue
            session.default_buffer.history.get_strings()[-1] = subcommand
            subcommand = completer.get_real_subcommand(subcommand)
            if subcommand is None:
                break

            call_command = f'{command} {subcommand}'
            for alias, alias_command in aliases.items():
                if call_command.startswith(alias):
                    if call_command != alias:
                        alias = f'{alias} '
                        alias_command = f'{alias_command} '
                    call_command = call_command.replace(alias, alias_command)
            subprocess.call(call_command, shell=True)
        except EOFError:
            break  # Control-D pressed.
        except KeyboardInterrupt:
            pass
    click.echo('GoodBye!')
