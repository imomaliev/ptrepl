import os

from pathlib import Path

from xdg import XDG_DATA_HOME


def get_history_file(command, local_shada_path=None):
    command = command.replace(' ', '').replace('/', '')
    if local_shada_path:
        path = os.path.expandvars(local_shada_path)
        assert '$' not in path, f"Not all environment variables were expanded {path}"
        # FIXME: fox some reason expansion gives path '-/...'
        if path.startswith('-'):
            path = path[1:]
        history = Path(path, f'history/{command}')
    else:
        history = Path(XDG_DATA_HOME, f'ptrepl/history/{command}')
    if not history.exists():
        if not history.parent.exists():
            history.parent.mkdir(parents=True)
        history.touch()
    return str(history)
