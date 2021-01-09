import os

from ptrepl.config import get_config_file


def test_config_file_created(mocker, tmp_path):
    mocker.patch("ptrepl.config.XDG_CONFIG_HOME", tmp_path)
    get_config_file()
    assert os.path.exists(os.path.join(tmp_path, "ptrepl/config.json"))
