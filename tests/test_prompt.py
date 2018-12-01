from prompt_toolkit.application import current
from prompt_toolkit.application.dummy import DummyApplication
from prompt_toolkit.key_binding.vi_state import InputMode
from prompt_toolkit.enums import EditingMode

from ptrepl.prompt import _get_prompt_mode_token


def test_prompt_mode_token_emacs():
    app = DummyApplication()
    app.editing_mode = EditingMode.EMACS
    with current.set_app(app):
        assert _get_prompt_mode_token('@', '+', ':') == '@'


def test_prompt_mode_token_vi():
    app = DummyApplication()
    app.editing_mode = EditingMode.VI
    with current.set_app(app):
        assert _get_prompt_mode_token('@', '+', ':') == '+'


def test_prompt_mode_token_vi_ins():
    app = DummyApplication()
    app.editing_mode = EditingMode.VI
    app.vi_state.input_mode = InputMode.INSERT
    with current.set_app(app):
        assert _get_prompt_mode_token('@', '+', ':') == '+'


def test_prompt_mode_token_vi_cmd():
    app = DummyApplication()
    app.editing_mode = EditingMode.VI
    app.vi_state.input_mode = InputMode.NAVIGATION
    with current.set_app(app):
        assert _get_prompt_mode_token('@', '+', ':') == ':'
