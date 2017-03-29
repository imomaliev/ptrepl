import json
import os
from .xdg import XDG_CONFIG_HOME

def get_aliases():
    filename = os.path.join(XDG_CONFIG_HOME, 'ptrepl/aliases.json')
    if os.path.isfile(filename):
        with open(filename, 'r') as pa:
            return json.load(pa)
    return {}
