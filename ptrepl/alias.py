import json

from pathlib import Path

from .xdg import XDG_CONFIG_HOME


def get_aliases():
    aliases = Path(XDG_CONFIG_HOME, 'ptrepl/aliases.json')
    if aliases.exists():
        with aliases.open('r') as a:
            return json.load(a)
    return {}
