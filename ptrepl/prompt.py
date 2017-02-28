import datetime
import os

from prompt_toolkit.token import Token
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.key_binding.vi_state import InputMode

from .bash_prompt import Lexer
from .settings import *


style = style_from_dict({
    Token.Prompt.Venv: '#ansilightgray bold',
    Token.Prompt.Cwd: '#ansiblue bold',
    Token.Prompt.Branch: '#ansiyellow bold',
    Token.Prompt.Command: '#ansiturquoise bold',
    Token.Prompt.DateTime: '#ansigreen bold'
})


def get_prompt_tokens(command):
    # https://github.com/jonathanslenders/python-prompt-toolkit/issues/247
    tokens = Lexer().tokenize(os.getenv('PS1'))
    tokens_pre = []
    new_line = False
    tokens_post = [
        (Token.Prompt.Command, command),
    ]

    for token in tokens:
        if new_line:
            tokens_post.append(token)
        else:
            tokens_pre.append(token)
        if token[1] == '\n':
            new_line = True

    def _get_prompt_tokens(cli):
        mode = VI_NORMAL_MODE if cli.vi_state.input_mode == InputMode.INSERT else VI_EDIT_MODE
        _prompt_tokens = tokens_pre[:]
        _prompt_tokens.append((
            Token.Prompt, '{mode} '.format(mode=mode)
        ))
        _prompt_tokens.extend(tokens_post)
        return _prompt_tokens

    return _get_prompt_tokens
