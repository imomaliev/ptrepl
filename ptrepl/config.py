import json

from pathlib import Path

from .vendor.xdg import XDG_CONFIG_HOME


DEFAULTS = {
    "EXIT_COMMAND": "exit",
    "EDITING_MODE": "emacs",
    "SHOW_MODE_IN_PROMPT": False,
    "READLINE_COMPLETION": False,
    "EMACS_MODE_STRING": "@",
    "VI_INS_MODE_STRING": "(ins)",
    "VI_CMD_MODE_STRING": "(cmd)",
    "PARSE_PS1": False,  # experimental
    "LOCAL_SHADA": False,
    "LOCAL_SHADA_PATH": "$DIRENV_DIR/.direnv/ptrepl/",
}


def get_config_file():
    path = Path(XDG_CONFIG_HOME, 'ptrepl', 'config.json')
    if path.exists():
        with path.open('r') as _config_file:
            config = json.load(_config_file)
    else:
        with open(path, 'w') as _config_file:
            config = {'settings': {}}
            _config_file.write(json.dumps(config))
    return config


def get_config(config_file_, name):
    return config_file_.get(name, {})


class Settings:
    """
    A settings object, that allows settings to be accessed as properties.
    For example:

        from .settings import settings
        print settings.EXIT_COMMAND
    """

    def __init__(self, user_settings=None, defaults=None):
        self.user_settings = user_settings or {}
        self.defaults = defaults or {}

    def __getattr__(self, attr):
        if attr not in self.defaults.keys():
            raise AttributeError("Invalid setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Cache the result
        setattr(self, attr, val)
        return val


config_file = get_config_file()
settings = Settings(
    user_settings=get_config(config_file, 'settings'), defaults=DEFAULTS
)


def get_aliases(command):
    command = f'{command} '
    return {
        k: v
        for k, v in get_config(config_file, 'alias').items()
        if k.startswith(command)
    }
