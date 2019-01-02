======
ptrepl
======

.. image:: https://travis-ci.com/imomaliev/ptrepl.svg?branch=master
    :target: https://travis-ci.com/imomaliev/ptrepl
.. image:: https://badge.fury.io/py/ptrepl.svg
    :target: https://badge.fury.io/py/ptrepl

About
-----
Make REPL out of any bash command

- has bash completion
- has vi mode
- has PS1 parsing(experimental)
- stores history in ``$XDG_DATA_HOME/ptrepl/history``
- bash like history expansion
- list history
- command mode
- aliases

Installation
------------
Requires ``python>=3.6``, ``prompt_toolkit>=2.0.7``, ``pygments``

.. code:: bash

    pip install ptrepl

``ptrepl`` vendors https://github.com/xonsh/py-bash-completion

Usage
-----
Basic Usage
^^^^^^^^^^^
.. code:: bash

    $ ptrepl --help
    Usage: ptrepl [OPTIONS] COMMAND

    Options:
    --prompt TEXT  Override prompt
    --help         Show this message and exit.
    $ ptrepl git
    $ git >
    # to call "git status"
    $ git > status
    # if you need execute some other bash command see system mode below

Custom prompt command
^^^^^^^^^^^^^^^^^^^^^
.. code:: bash

    $ ptrepl git --prompt g
    $ g >

Multiword command
^^^^^^^^^^^^^^^^^
.. code:: bash

    $ ptrepl "echo prefix"
    $ echo prefix > 1
    echo prefix 1

Config
------
Place settings file in :bash:``$XDG_CONFIG_HOME/ptrepl/config.json``

Here is example of config with enabled vi mode and git alias

.. code:: json

    {
        "settings": {
            "EXIT_COMMAND": "exit",
            "EDITING_MODE": "vi",
            "SHOW_MODE_IN_PROMPT": true,
            "EMACS_MODE_STRING": "@",
            "VI_INS_MODE_STRING": "+",
            "VI_CMD_MODE_STRING": ":",
            "READLINE_COMPLETION": false,
            "PARSE_PS1": false,
            "LOCAL_SHADA": false,
            "LOCAL_SHADA_PATH": "$PWD/.ptrepl/",
        },
        "alias": {
            "git st": "git status"
        }
    }

Available settings
^^^^^^^^^^^^^^^^^^
- EXIT_COMMAND - change exit command
- EDITING_MODE - choose mode vi/emacs
- SHOW_MODE_IN_PROMPT - show editing mode string in prompt
- EMACS_MODE_STRING - set emacs mode prompt string
- VI_INS_MODE_STRING - set vi insert mode prompt string
- VI_CMD_MODE_STRING - set vi command mode prompt string
- READLINE_COMPLETION: use readline like completion instead of dropdown one
- PARSE_PS1 {experimental} - will try to adgust ptrepl's prompt according to your PS1 setting
- LOCAL_SHADA - store shada(history) in LOCAL_SHADA_PATH
- LOCAL_SHADA_PATH - path to local shada

Default settings
^^^^^^^^^^^^^^^^
.. code:: json

    {
        "EXIT_COMMAND": "exit",
        "EDITING_MODE": "emacs",
        "SHOW_MODE_IN_PROMPT": false,
        "EMACS_MODE_STRING": "@",
        "VI_INS_MODE_STRING": "(ins)",
        "VI_CMD_MODE_STRING": "(cmd)",
        "READLINE_COMPLETION": false,
        "PARSE_PS1": false,
        "LOCAL_SHADA": false,
        "LOCAL_SHADA_PATH": "$DIRENV_DIR/.direnv/ptrepl/",
    }

Features
--------

Parsing PS1(requires PARSE_PS1 set to true)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Here is how my bash prompt(PS1) looks like by default

.. code:: bash

    {ptrepl} ~/Development/Python/ptrepl [master] |19:18:36 07-Feb-18|
    + ❯ ptrepl git
    {ptrepl} ~/Development/Python/ptrepl [master] |19:20:15 07-Feb-18|
    + git ❯

Completion
^^^^^^^^^^
.. code:: bash

    $ ptrepl git
    $ git > sta (press TAB)
    # result
    $ git > sta
            status
            stage
            stash

Readline like completion(requires READLINE_COMPLETION set to true)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
.. code:: bash

    $ ptrepl git
    $ git > sta (press TAB)
    # result
    $ git > sta
    stage  stash  status


System mode
^^^^^^^^^^^
.. code:: bash

    $ ptrepl git
    $ git > (press Escape + !)
    # result
    # you could enter your shell commands here
    Shell command: ls

Command mode
^^^^^^^^^^^^
.. code:: bash

    $ ptrepl git
    $ git > (press Escape + :)
    # result
    # you could enter your command mode commands here
    # to list history
    Command mode: history

Bash like history expansion
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: bash

    $ ptrepl git
    $ git > status
    # repeat last command
    $ git > !!
    # repeat 10th command
    $ git > !10
    # repeat 10th command from bottom of history stack
    $ git > !-10

Bash like aliases
^^^^^^^^^^^^^^^^^
.. code:: bash

    $ ptrepl git
    $ git > (press Escape + :)
    # you could enter your command mode commands here
    # to list alias
    Command mode: alias
    alias "git st"="git status"
    $ git > st

Similar projects
-------------------
Written in Ruby
^^^^^^^^^^^^^^^
https://github.com/defunkt/repl

Written in Bash
^^^^^^^^^^^^^^^
https://github.com/joh6nn/shrepl

https://github.com/mchav/with

Written in Python
^^^^^^^^^^^^^^^^^
https://github.com/mbr/repl

https://github.com/renanivo/with
