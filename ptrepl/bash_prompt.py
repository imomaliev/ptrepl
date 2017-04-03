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


regexes = OrderedDict((
    ('cwd', re.compile(r'^\\w')),
    ('cmd', re.compile(r'^\$\([^\)]*\)')),
    ('array', re.compile(r'^\$\{[^\}]*\}')),
    ('venv', re.compile(r'^\([^\)]*\)')),
    ('datetime', re.compile(r'^\\D\{[^\}]*\}')),
    ('color', re.compile(r'^\\\[(\\e|\\033)\[\d{1,2};\d{2}m\\\]')),
    ('nocolor', re.compile(r'^\\\[(\\e|\\033)\[\d{0,2}m\\\]')),
    ('newline', re.compile(r'^\\n')),
    ('user', re.compile(r'^\\u')),
    ('hostname', re.compile(r'^\\h')),
    ('dollar', re.compile(r'^\\\$')),
    ('string', re.compile(r'^.')),
))


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
            end = matches.end()
            return source[:end], source[end:]
        return None

    def cwd(self, raw_token):
        return os.getcwd().replace(os.path.expanduser('~'), '~')

    def _get_git_branch(self):
        if os.path.exists('.git'):
            branch = self.cmd("git symbolic-ref HEAD 2> /dev/null || git describe --tags --exact-match HEAD", is_script=False)
            if 'refs/heads/' in branch:
                branch = branch.replace('refs/heads/', '')
            else:
                branch = '({})'.format(branch)
        else:
            return ''
        return '[{}] '.format(branch)

    def _get_hg_branch(self):
        if os.path.exists('.hg'):
            return '[{}] '.format(self.cmd("$(hg prompt '{branch}')", is_script=True))
        else:
            return ''

    def cmd(self, raw_token, is_script=True):
        if '__git_ps1' in raw_token:
            return self._get_git_branch()
        if '__hg_ps1' in raw_token:
            return self._get_hg_branch()
        cmd = 'echo "{}"'.format(raw_token) if is_script else raw_token
        return subprocess.check_output(
            ['bash', '-c', cmd], universal_newlines=True,
            stderr=subprocess.PIPE
        ).strip('\n')

    def venv(self, raw_token):
        return raw_token

    def datetime(self, raw_token):
        return datetime.datetime.now().strftime(raw_token[3:-1])

    def newline(self, raw_token):
        return '\n'

    def user(self, raw_token):
        return os.getenv('USERNAME') or os.getenv('USER')

    def hostname(self, raw_token):
        return os.uname()[1]

    def dollar(self, raw_token):
        return '$'

    def string(self, raw_token):
        return raw_token

    def array(self, raw_token):
        return ''

    def tokenize(self, source):
        style = getattr(Token, 'NO_COLOR')
        while True:
            for _type, regex in regexes.items():
                captures = self.regexec(regex, source)
                if captures:
                    raw_token, source = captures
                    if _type == 'color':
                        style = getattr(Token, ANSI_COLORS[raw_token[-7:-3]])
                        break
                    elif _type == 'venv' and not os.getenv('VIRTUAL_ENV'):
                        _type = 'string'
                    elif _type == 'nocolor':
                        break
                    yield (style, getattr(self, _type, lambda t: t)(raw_token))
                    break
            else:
                break
