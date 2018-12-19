import os

from ptrepl.vendor.xdg import XDG_DATA_HOME
from ptrepl.history import get_history_file


def test_get_history_file():
    command = 'git'
    history = get_history_file(command)
    assert history == os.path.join(XDG_DATA_HOME, 'ptrepl/history/git')


def test_get_history_file_local_shada(monkeypatch):
    command = 'git'
    monkeypatch.setenv('DIRENV_DIR', '.direnv/')
    history = get_history_file(command, local_shada_path='$DIRENV_DIR/ptrepl')
    assert history == '.direnv/ptrepl/history/git'
