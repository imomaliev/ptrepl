from .utils import get_xdg_json_data


DEFAULTS = {
    "EXIT_COMMAND": "exit",
    "BASH_EXEC": "$",
    "VI_MODE": False,
    "PREPEND_SPACE": False,
    "VI_EDIT_MODE": ":",
    "VI_NORMAL_MODE": "+",
    "PARSE_PS1": False  # experimental
}


USER_SETTINGS = get_xdg_json_data('settings.json')


class Settings(object):
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
            raise AttributeError("Invalid API setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Cache the result
        setattr(self, attr, val)
        return val

settings = Settings(USER_SETTINGS, DEFAULTS)
