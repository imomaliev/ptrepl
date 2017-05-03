import json

from pathlib import Path

from .xdg import XDG_CONFIG_HOME


BASE_DIR = 'ptrepl'


def get_xdg_json_data(filename):
    path = Path(XDG_CONFIG_HOME, BASE_DIR, filename)
    if path.exists():
        with path.open('r') as a:
            return json.load(a)
    return {}
