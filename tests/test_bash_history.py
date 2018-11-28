import pytest

from ptrepl.bash.history import expand_history


@pytest.fixture
def history():
    return ['git diff', 'git add .', 'git commit', 'git status']


def test_expand_history_double_exclamation_mark(history):
    command = '!!'
    history.append(command)
    expanded_command, __ = expand_history(command, history)
    assert expanded_command == 'git status'


def test_expand_history_exclamation_mark_minus_1(history):
    command = '!-1'
    history.append(command)
    expanded_command, __ = expand_history(command, history)
    assert expanded_command == 'git status'


def test_expand_history_exclamation_mark_1(history):
    command = '!1'
    history.append(command)
    expanded_command, __ = expand_history(command, history)
    assert expanded_command == 'git diff'
