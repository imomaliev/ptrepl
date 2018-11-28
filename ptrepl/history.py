from pathlib import Path

from .vendor.xdg import XDG_DATA_HOME

from .config import settings


def get_history_file(command):
    command = command.replace(' ', '').replace('/', '')
    if settings.LOCAL_SHADA:
        history = Path(settings.LOCAL_SHADA_PATH, f'history/{command}')
    else:
        history = Path(XDG_DATA_HOME, f'ptrepl/history/{command}')
    if not history.exists():
        if not history.parent.exists():
            history.parent.mkdir(parents=True)
        history.touch()
    return str(history)
