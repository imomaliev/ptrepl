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
    branch_commnads = [
        'git rev-parse --abbrev-ref HEAD',
        'hg branch'
    ]
    for cmd in branch_commnads:
        try:
            branch = subprocess.check_output(
                cmd, shell=True,
                stderr=subprocess.DEVNULL
            )
            return '[{}] '.format(branch.strip().decode())
        except subprocess.CalledProcessError as e:
            pass
    else:
        return ''


def _get_datetime():
    return '|{}| '.format(datetime.datetime.now().strftime(DATETIME_FORMAT))


def get_prompt_tokens(command):
    venv = _get_venv()
    cwd = _get_cwd()

    def _get_prompt_tokens(cli):
        mode = VI_NORMAL_MODE if cli.vi_state.input_mode == InputMode.INSERT else VI_EDIT_MODE
        return [
            (Token.Prompt, ' '),
            (Token.Prompt.Venv, venv),
            (Token.Prompt.Path, cwd),
            (Token.Prompt.Branch, _get_branch()),
            (Token.Prompt.DateTime, _get_datetime()),
            (Token.Prompt, '\n'),
            (Token.Prompt, '{mode} '.format(mode=mode)),
            (Token.Prompt.Command, '{command} '.format(command=command)),
            (Token.Prompt, '❯ '.format(mode=mode, command=command)),
        ]

    return _get_prompt_tokens
