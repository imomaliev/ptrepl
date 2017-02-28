r"""
https://www.gnu.org/software/bash/manual/bash.html#Controlling-the-Prompt

\a A bell character.

\d The date, in "Weekday Month Date" format (e.g., "Tue May 26").

\D{format} The format is passed to strftime(3) and the result is inserted into the prompt string; an empty format results in a locale-specific time representation. The braces are required.

\e An escape character.

\h The hostname, up to the first ‘.’.

\H The hostname.

\j The number of jobs currently managed by the shell.

\l The basename of the shell’s terminal device name.

\n A newline.

\r A carriage return.

\s The name of the shell, the basename of $0 (the portion following the final slash).

\t The time, in 24-hour HH:MM:SS format.

\T The time, in 12-hour HH:MM:SS format.

\@ The time, in 12-hour am/pm format.

\A The time, in 24-hour HH:MM format.

\u The username of the current user.

\v The version of Bash (e.g., 2.00)

\V The release of Bash, version + patchlevel (e.g., 2.00.0)

\w The current working directory, with $HOME abbreviated with a tilde (uses the $PROMPT_DIRTRIM variable).

\W The basename of $PWD, with $HOME abbreviated with a tilde.

\! The history number of this command.

\# The command number of this command.

\$ If the effective uid is 0, #, otherwise $.

\nnn The character whose ASCII code is the octal value nnn.

\\ A backslash.

\[ Begin a sequence of non-printing characters. This could be used to embed a terminal control sequence into the prompt.

\] End a sequence of non-printing characters.
"""
import datetime
import os
import re
import subprocess

from collections import OrderedDict

from prompt_toolkit.token import Token

CWD = r'\w'
DATETIME = r'\D'
NEWLINE = r'\n'
USER = r'\u'

regexes = OrderedDict((
    ('cwd', re.compile(r'^\\w')),
    ('cmd', re.compile(r'^\$\([^\)]*\)')),
    ('venv', re.compile(r'^\([^\)]*\)')),
    ('datetime', re.compile(r'^\\D\{[^\}]*\}')),
    ('color', re.compile(r'^\\\[\\e\[\d;\d{2}m\\\]')),
    ('nocolor', re.compile(r'^\\\[\\e\[m\\\]')),
    ('newline', re.compile(r'^\\n')),
    ('user', re.compile(r'^\\u')),
    ('string', re.compile(r'^[^\\\$]+')),
))


BASH_SCRIPT = """
source /etc/profile
source /etc/bash_completion.d/git-prompt
source ~/.bash_profile
source ~/.bashrc

echo "{cmd}"
"""

ANSI_COLORS = {
    '0;30': 'BLACK',
    '0;31': 'RED',
    '0;32': 'GREEN',
    '0;33': 'YELLOW',
    '0;34': 'BLUE',
    '0;35': 'PURPLE',
    '0;36': 'CYAN',
    '0;37': 'WHITE',
    '1;30': 'BOLD_BLACK',
    '1;31': 'BOLD_RED',
    '1;32': 'BOLD_GREEN',
    '1;33': 'BOLD_YELLOW',
    '1;34': 'BOLD_BLUE',
    '1;35': 'BOLD_PURPLE',
    '1;36': 'BOLD_CYAN',
    '1;37': 'BOLD_WHITE'
}


class Lexer(object):
    @staticmethod
    def regexec(regex, source):
        matches = regex.match(source)
        if matches:
            return (source[matches.start():matches.end()],) + matches.groups()
        return None

    def cwd(self):
        return os.getcwd().replace(os.path.expanduser('~'), '~')

    def cmd(self, cmd):
        script = BASH_SCRIPT.format(cmd=cmd)
        out = subprocess.check_output(
            ['bash', '-c', script], universal_newlines=True,
            stderr=subprocess.PIPE).strip('\n')
        return out

    def datetime(self, datetime_format):
        return datetime.datetime.now().strftime(datetime_format)

    def tokenize(self, source):
        style = getattr(Token, 'NO_COLOR')
        while True:
            for _type, regex in regexes.items():
                captures = self.regexec(regex, source)
                if captures:
                    raw_token = captures[0]
                    if _type == 'color':
                        style = getattr(Token, ANSI_COLORS[raw_token[5:9]])
                    if raw_token == CWD:
                        yield (style, getattr(self, 'cwd')())
                    elif raw_token.startswith(r'$(') and raw_token.endswith(')'):
                        yield (style, getattr(self, 'cmd')(raw_token))
                    elif raw_token.startswith(DATETIME):
                        yield (style, getattr(self, 'datetime')(raw_token[3:-1]))
                    elif raw_token.startswith('(') and raw_token.endswith(')') and os.getenv('VIRTUAL_ENV'):
                        yield (style, raw_token)
                    elif raw_token.startswith(NEWLINE):
                        yield (style, '\n')
                    elif raw_token == USER:
                        yield (style, os.getenv('USERNAME') or os.getenv('USER'))
                    elif raw_token[0] not in ('\\', '['):
                        yield (style, raw_token)
                    source = source[len(captures[0]):]
                    break
            else:
                break
