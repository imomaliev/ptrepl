import subprocess
import argparse

from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.history import FileHistory

from .bash.history import BashHistoryIndexError, expand_history

from .completion import BashCompleter
from .config import settings, get_aliases
from .history import get_history_file
from .prompt import PtreplSession, get_prompt_tokens


def main(command, prompt=None):
    local_shada_path = settings.LOCAL_SHADA_PATH if settings.LOCAL_SHADA else None
    history = FileHistory(get_history_file(command, local_shada_path=local_shada_path))
    aliases = get_aliases(command)
    completer = BashCompleter(command, aliases)

    complete_style = (
        CompleteStyle.READLINE_LIKE
        if settings.READLINE_COMPLETION
        else CompleteStyle.COLUMN
    )
    vi_mode = settings.EDITING_MODE == 'vi'

    session = PtreplSession(
        command,
        aliases,
        message='',
        completer=completer,
        complete_style=complete_style,
        history=history,
        enable_system_prompt=True,
        enable_suspend=True,
        vi_mode=vi_mode,
        auto_suggest=AutoSuggestFromHistory(),
        enable_history_search=True,
    )

    prompt = prompt if prompt is not None else command

    while True:
        try:
            _get_prompt_tokens = get_prompt_tokens(
                prompt,
                settings.PARSE_PS1,
                settings.SHOW_MODE_IN_PROMPT,
                settings.EMACS_MODE_STRING,
                settings.VI_INS_MODE_STRING,
                settings.VI_CMD_MODE_STRING,
            )
            subcommand = session.prompt(_get_prompt_tokens)
            try:
                expanded_subcommand, execute = expand_history(
                    subcommand, session.default_buffer.history.get_strings()
                )
            except BashHistoryIndexError as e:
                print(f'{command}: {e}: event not found')
                continue
            if not execute:
                print(expanded_subcommand)
                continue
            if subcommand != expanded_subcommand:
                session.default_buffer.history.get_strings()[-1] = expanded_subcommand
            subcommand = completer.get_real_subcommand(expanded_subcommand)
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
    print('GoodBye!')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('--prompt')
    args = parser.parse_args()
    main(args.command, prompt=args.prompt)
