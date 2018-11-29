from prompt_toolkit.application import current
from prompt_toolkit.application.dummy import DummyApplication
from prompt_toolkit.key_binding.vi_state import InputMode
from prompt_toolkit.enums import EditingMode

from ptrepl import config
from ptrepl import prompt
from ptrepl.prompt import _get_prompt_command_token


def test_prompt_command_token(monkeypatch):
    monkeypatch.setattr(config, 'settings', config.Settings(defaults=config.DEFAULTS))
    from ptrepl.config import settings

    assert not settings.VI_MODE
    assert _get_prompt_command_token('git') == '\x1b[1;36mgit\x1b[m'


def test_prompt_command_token_vi_mode(monkeypatch):
    monkeypatch.setattr(
        config,
        'settings',
        config.Settings(user_settings={'VI_MODE': True}, defaults=config.DEFAULTS),
    )
    from ptrepl.config import settings

    app = DummyApplication()
    app.editing_mode = EditingMode.VI
    with current.set_app(app):
        assert settings.VI_MODE
        assert current.get_app().editing_mode == EditingMode.VI
        assert _get_prompt_command_token('git') == '+ \x1b[1;36mgit\x1b[m'


MOCK_SETTINGS = {
    'VI_MODE': True,
    'VI_INS_MODE_STRING': '(ins)',
    'VI_CMD_MODE_STRING': '(cmd)',
}


def test_prompt_command_token_vi_ins_mode_string(monkeypatch):
    monkeypatch.setattr(
        config,
        'settings',
        config.Settings(user_settings=MOCK_SETTINGS, defaults=config.DEFAULTS),
    )
    monkeypatch.setattr(
        prompt,
        'settings',
        config.Settings(user_settings=MOCK_SETTINGS, defaults=config.DEFAULTS),
    )
    from ptrepl.config import settings

    app = DummyApplication()
    app.editing_mode = EditingMode.VI
    with current.set_app(app):
        assert settings.VI_MODE
        assert settings.VI_INS_MODE_STRING == '(ins)'
        assert current.get_app().editing_mode == EditingMode.VI
        assert _get_prompt_command_token('git') == '(ins) \x1b[1;36mgit\x1b[m'


def test_prompt_command_token_vi_cmd_mode_string(monkeypatch):
    monkeypatch.setattr(
        config,
        'settings',
        config.Settings(user_settings=MOCK_SETTINGS, defaults=config.DEFAULTS),
    )
    monkeypatch.setattr(
        prompt,
        'settings',
        config.Settings(user_settings=MOCK_SETTINGS, defaults=config.DEFAULTS),
    )
    from ptrepl.config import settings

    app = DummyApplication()
    app.editing_mode = EditingMode.VI
    app.vi_state.input_mode = InputMode.NAVIGATION
    with current.set_app(app):
        assert settings.VI_MODE
        assert settings.VI_CMD_MODE_STRING == '(cmd)'
        assert current.get_app().editing_mode == EditingMode.VI
        assert _get_prompt_command_token('git') == '(cmd) \x1b[1;36mgit\x1b[m'
