# ptrepl

Make REPL out of any bash command

 - has bash completion
 - has vi mode
 - has PS1 parsing(experimental)
 - stores history in XDG_DATA_HOME/ptrepl/history

## Installation
Requires `python3` and `prompt_toolkit==2.0.0`
```bash
pip install --process-dependency-links git+https://github.com/imomaliev/ptrepl.git
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
git $
# to call "git status"
git $ status
# if you need execute some other bash command prepend it with '$'
git $ $echo 123
```

### Custom prompt command
```bash
$ ptrepl git --prompt g
g $
```

### Multiword command
```bash
$ ptrepl "echo prefix"
echo prefix $ 1
echo prefix 1
```

## Settings
Place settings file in `XDG_CONFIG_HOME/ptrepl/settings.json`

```json
{
  "PARSE_PS1": true,
  "VI_MODE": true
}
```
### Available settings
 - EXIT_COMMAND - change exit command
 - PREPEND_SPACE - prepend space before prompt command
 - VI_MODE - enable VI mode
 - VI_EDIT_MODE - set VI edit mode prompt string
 - VI_NORMAL_MODE - set VI normal mode prompt string
 - PARSE_PS1 {experimental} - will try to adgust ptrepl's prompt according to your PS1 setting

### Default settings
```json
{
  "EXIT_COMMAND": "exit",
  "PREPEND_SPACE": false,
  "VI_MODE": false,
  "VI_EDIT_MODE": ":",
  "VI_NORMAL_MODE": "+",
  "PARSE_PS1": false
}
```

### Parsing PS1
Here is how my bash prompt(PS1) looks like by default
```bash
 {ptrepl} ~/Development/Python/ptrepl [master] |19:18:36 07-Feb-18|
+ ❯ ptrepl git
 {ptrepl} ~/Development/Python/ptrepl [master] |19:20:15 07-Feb-18|
+ git ❯
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
