import datetime
import os

from prompt_toolkit.token import Token
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.key_binding.vi_state import InputMode

from .bash_prompt import Lexer
from .settings import settings


style = style_from_dict({
    Token.BOLD_BLUE: '#ansiblue bold',
    Token.BOLD_YELLOW: '#ansiyellow bold',
    Token.BOLD_CYAN: '#ansiturquoise bold',
    Token.BOLD_BLACK: '#ansiblack bold',
    Token.BOLD_GREEN: '#ansigreen bold',
    Token.BOLD_PURPLE: '#ansipurple bold'
})


def get_prompt_tokens(command):
    # https://github.com/jonathanslenders/python-prompt-toolkit/issues/247
    new_line = 0
    tokens = []
    for i, token in enumerate(Lexer().tokenize(os.getenv('PS1'))):
        tokens.append(token)
        if token[1] == '\n':
            new_line = i + 1

    def _get_prompt_tokens(cli):
        if not settings.PARSE_PS1:
            return ((Token.Prompt, command), (Token.Prompt, ' > '))
        mode = settings.VI_NORMAL_MODE if cli.vi_state.input_mode == InputMode.INSERT else settings.VI_EDIT_MODE
        _prompt_tokens = tokens[:]
        _prompt_tokens.insert(new_line, (
            Token.Prompt, mode
        ))
        _prompt_tokens.insert(new_line + 1, (
            Token.BOLD_CYAN, ' {command}'.format(command=command)
        ))
        return _prompt_tokens

    return _get_prompt_tokens
