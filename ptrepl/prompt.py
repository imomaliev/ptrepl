import os

from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding.vi_state import InputMode
from prompt_toolkit.enums import EditingMode
from prompt_toolkit import ANSI

from .bash_prompt import Lexer
from .settings import settings


def get_prompt_tokens(command):
    # https://github.com/jonathanslenders/python-prompt-toolkit/issues/247
    prompt = Lexer().render(os.getenv('PS1'))

    def _get_prompt_tokens():
        if not settings.PARSE_PS1:
            return ANSI('{} > '.format(command))

        app = get_app()

        _prompt, last_line = prompt.rsplit('\n')

        _command = '\x1b[1;36m{}\x1b[m'.format(command)
        if app.editing_mode == EditingMode.VI:
            in_insert_mode = app.vi_state.input_mode == InputMode.INSERT
            mode = settings.VI_NORMAL_MODE if in_insert_mode else settings.VI_EDIT_MODE
            mode = '{} '.format(mode)
            last_line = ''.join((mode, _command, last_line))
        else:
            last_line = ''.join((_command, last_line))

        _prompt = '\n'.join((_prompt, last_line))
        return ANSI(_prompt)

    return _get_prompt_tokens
