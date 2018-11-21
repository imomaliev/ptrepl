# ptrepl

Make REPL out of any bash command

 - has bash completion
 - has vi mode
 - has PS1 parsing(experimental)
 - stores history in XDG_DATA_HOME/ptrepl/history
 - bash like history expansion
 - list history
 - command mode

## Installation
Requires `python3`, `click` and `prompt_toolkit>2.0.7`
```bash
pip install git+https://github.com/imomaliev/ptrepl.git
```

## Usage
## Basic Usage
```bash
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
```

### Custom prompt command
```bash
$ ptrepl git --prompt g
$ g >
```

### Multiword command
```bash
$ ptrepl "echo prefix"
$ echo prefix > 1
echo prefix 1
```

## Settings
Place settings file in `XDG_CONFIG_HOME/ptrepl/settings.json`

```json
{
  "PARSE_PS1": true,
  "VI_MODE": true,
  "LOCAL_SHADA": true
}
```
### Available settings
 - EXIT_COMMAND - change exit command
 - VI_MODE - enable VI mode
 - VI_EDIT_MODE - set VI edit mode prompt string
 - VI_NORMAL_MODE - set VI normal mode prompt string
 - PARSE_PS1 {experimental} - will try to adgust ptrepl's prompt according to your PS1 setting
 - LOCAL_SHADA - store shada(history) in LOCAL_SHADA_PATH
 - LOCAL_SHADA_PATH - path to local shada

### Default settings
```json
{
  "EXIT_COMMAND": "exit",
  "VI_MODE": false,
  "VI_EDIT_MODE": ":",
  "VI_NORMAL_MODE": "+",
  "PARSE_PS1": false,
  "LOCAL_SHADA": false,
  "LOCAL_SHADA_PATH": ".direnv/ptrepl/",
}
```

## Features

### Parsing PS1
Here is how my bash prompt(PS1) looks like by default
```bash
 {ptrepl} ~/Development/Python/ptrepl [master] |19:18:36 07-Feb-18|
+ ❯ ptrepl git
 {ptrepl} ~/Development/Python/ptrepl [master] |19:20:15 07-Feb-18|
+ git ❯
```
### Completion
```bash
$ ptrepl git
$ git > st (press TAB)
# result
$ git > st
          status
          stage
          stash
```

### System mode
```bash
$ ptrepl git
$ git > (press Escape + !)
# result
# you could enter your shell commands here
Shell command: ls
```

### Command mode
```bash
$ ptrepl git
$ git > (press Escape + :)
# result
# you could enter your command mode commands here
# to list history
Command mode: history
```

### Bash like history expansion
```bash
$ ptrepl git
$ git > status
# repeat last command
$ git > !!
# repeat 10th command
$ git > !10
# repeat 10th command from bottom of history stack
$ git > !-10
```

## Similar projects
### Written in Ruby
https://github.com/defunkt/repl

### Written in Bash
https://github.com/joh6nn/shrepl

https://github.com/mchav/with

### Written in Python
https://github.com/mbr/repl

https://github.com/renanivo/with
