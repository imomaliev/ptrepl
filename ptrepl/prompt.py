import os
import datetime
import subprocess

from prompt_toolkit.token import Token
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.key_binding.vi_state import InputMode

from .settings import *


style = style_from_dict({
    Token.Prompt.Venv: '#ansilightgray bold',
    Token.Prompt.Path: '#ansiblue bold',
    Token.Prompt.Branch: '#ansiyellow bold',
    Token.Prompt.Command: '#ansiturquoise bold',
    Token.Prompt.DateTime: '#ansigreen bold'
})


def _get_venv():
    if os.getenv('VIRTUAL_ENV'):
        ps1 = os.getenv('PS1')
        venv = ps1.split('(', 1)[1].split(')', 1)[0]
        return '({}) '.format(venv)
    else:
        return ''


def _get_cwd():
    cwd = os.getcwd().replace(os.path.expanduser('~'), '~')
    return '{} '.format(cwd)


def _get_branch():
    if os.path.exists('.git'):
        cmd = 'git rev-parse --abbrev-ref HEAD'
    elif os.path.exists('.hg'):
        cmd = 'hg branch'
    else:
        return ''
    branch = subprocess.check_output(
        cmd, shell=True,
        stderr=subprocess.DEVNULL
    )
    return '[{}] '.format(branch.strip().decode())


def _get_datetime():
    return '|{}| '.format(datetime.datetime.now().strftime(DATETIME_FORMAT))


def get_prompt_tokens(command):
    # https://github.com/jonathanslenders/python-prompt-toolkit/issues/247
    tokens_pre = [
        (Token.Prompt, ' '),
        (Token.Prompt.Venv, _get_venv()),
        (Token.Prompt.Path, _get_cwd()),
        (Token.Prompt.Branch, _get_branch()),
        (Token.Prompt.DateTime, _get_datetime()),
        (Token.Prompt, '\n')
    ]

    tokens_post = [
        (Token.Prompt.Command, '{command} '.format(command=command)),
        (Token.Prompt, '❯ '),
    ]

    def _get_prompt_tokens(cli):
        mode = VI_NORMAL_MODE if cli.vi_state.input_mode == InputMode.INSERT else VI_EDIT_MODE
        _prompt_tokens = tokens_pre[:]
        _prompt_tokens.append((
            Token.Prompt, '{mode} '.format(mode=mode)
        ))
        _prompt_tokens.extend(tokens_post)
        return _prompt_tokens

    return _get_prompt_tokens
