from pathlib import Path

from .xdg import XDG_DATA_HOME

from .settings import settings


def get_history(command):
    command = command.replace(' ', '').replace('/', '')
    if settings.LOCAL_SHADA:
        history = Path(settings.LOCAL_SHADA_PATH, 'history/{}'.format(command))
    else:
        history = Path(XDG_DATA_HOME, 'ptrepl/history/{}'.format(command))
    if not history.exists():
        if not history.parent.exists():
            history.parent.mkdir(parents=True)
        history.touch()
    return str(history)
