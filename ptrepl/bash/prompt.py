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

from pygments.token import Token


regexes = OrderedDict(
    (
        ('cwd', re.compile(r'^\\w')),
        ('cmd', re.compile(r'^\$\([^\)]*\)')),
        ('array', re.compile(r'^\$\{[^\}]*\}')),
        ('datetime', re.compile(r'^\\D\{[^\}]*\}')),
        ('newline', re.compile(r'^\\n')),
        ('user', re.compile(r'^\\u')),
        ('hostname', re.compile(r'^\\h')),
        ('dollar', re.compile(r'^\\\$')),
        ('string', re.compile(r'^.')),
    )
)


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
            branch = self.cmd(
                "git symbolic-ref HEAD 2> /dev/null || git describe --tags --exact-match HEAD 2> /dev/null || git rev-parse HEAD",
                is_script=False,
            )
            if 'refs/heads/' in branch:
                branch = branch.replace('refs/heads/', '')
            else:
                branch = f'({branch})'
        else:
            return ''
        return f'[{branch}] '

    def _get_hg_branch(self):
        if os.path.exists('.hg'):
            branch = self.cmd("$(hg prompt '{branch}')", is_script=True)
            return f'[{branch}] '
        else:
            return ''

    def _get_direnv(self):
        if os.path.exists('.direnv'):
            return f'{{{os.path.basename(os.getcwd())}}} '
        else:
            return ''

    def cmd(self, raw_token, is_script=True):
        if '__git_ps1' in raw_token:
            return self._get_git_branch()
        if '__hg_ps1' in raw_token:
            return self._get_hg_branch()
        if '__venv_ps1' in raw_token:
            return self._get_venv()
        if '__dotfiles_ps1' in raw_token:
            return self._get_direnv()
        cmd = f'echo "{raw_token}"' if is_script else raw_token
        return subprocess.check_output(
            ['bash', '-c', cmd], universal_newlines=True, stderr=subprocess.PIPE
        ).strip('\n')

    def _get_venv(self):
        venv = os.getenv('VIRTUAL_ENV') or ''
        venv = os.getcwd() if venv.endswith('.venv') else venv
        if venv:
            return f'({os.path.basename(venv)}) '
        else:
            return ''

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
                    yield getattr(self, _type, lambda t: t)(raw_token)
                    break
            else:
                break

    def render(self, source):
        source = ''.join(self.tokenize(source))
        source = source.replace('\\e', '\x1b')
        source = source.replace('\\[', '')
        source = source.replace('\\]', '')
        return source
