import os

from ptrepl.history import get_history_file


def test_get_history_file(mocker, tmp_path):
    command = 'git'
    mocker.patch('ptrepl.history.XDG_DATA_HOME', tmp_path)
    history = get_history_file(command)
    assert history == os.path.join(tmp_path, 'ptrepl/history/git')


def test_get_history_file_local_shada(monkeypatch, tmp_path):
    command = 'git'
    monkeypatch.setenv('DIRENV_DIR', tmp_path)
    history = get_history_file(command, local_shada_path='$DIRENV_DIR/.direnv/ptrepl')
    assert history == os.path.join(tmp_path, '.direnv/ptrepl/history/git')
