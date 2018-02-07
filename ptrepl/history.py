from pathlib import Path

from .xdg import XDG_DATA_HOME


def get_history(command):
    command = command.replace(' ', '').replace('/', '')
    history = Path(XDG_DATA_HOME, 'ptrepl/history/{}'.format(command))
    if not history.exists():
        if not history.parent.exists():
            history.parent.mkdir(parents=True)
        history.touch()
    return str(history)
