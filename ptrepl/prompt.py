import datetime
import os

from pygments.token import Token

from prompt_toolkit.application.current import get_app
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding.vi_state import InputMode

from .bash_prompt import Lexer
from .settings import settings


style = Style.from_dict({
    'pygments.bold_blue': '#ansiblue bold',
    'pygments.bold_yellow': '#ansiyellow bold',
    'pygments.bold_cyan': '#ansiturquoise bold',
    'pygments.bold_black': '#ansiblack bold',
    'pygments.bold_green': '#ansigreen bold',
    'pygments.bold_purple': '#ansipurple bold'
})


def get_prompt_tokens(command):
    # https://github.com/jonathanslenders/python-prompt-toolkit/issues/247
    new_line = 0
    tokens = []
    for i, token in enumerate(Lexer().tokenize(os.getenv('PS1'))):
        tokens.append(token)
        if token[1] == '\n':
            new_line = i + 1

    def _get_prompt_tokens():
        app = get_app()
        if not settings.PARSE_PS1:
            return ((Token.Prompt, command), (Token.Prompt, ' > '))
        mode = settings.VI_NORMAL_MODE if app.vi_state.input_mode == InputMode.INSERT else settings.VI_EDIT_MODE
        _prompt_tokens = tokens[:]
        _prompt_tokens.insert(new_line, (
            Token.Prompt, mode
        ))
        _prompt_tokens.insert(new_line + 1, (
            Token.BOLD_CYAN, ' {command}'.format(command=command)
        ))
        return PygmentsTokens(_prompt_tokens)

    return _get_prompt_tokens
