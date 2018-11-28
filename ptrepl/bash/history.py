"""
http://structure.usc.edu/bash/bashref_9.html#SEC115

9.3.1 Event Designators

An event designator is a reference to a command line entry in the history list.

! Start a history substitution, except when followed by a space, tab, the end of the line, `=' or `('.

!n Refer to command line n.

!-n Refer to the command n lines back.

!! Refer to the previous command. This is a synonym for `!-1'.

!string Refer to the most recent command starting with string.

!?string[?] Refer to the most recent command containing string. The trailing `?' may be omitted if the string is followed immediately by a newline.

^string1^string2^ Quick Substitution. Repeat the last command, replacing string1 with string2. Equivalent to !!:s/string1/string2/.

!# The entire command line typed so far.


9.3.2 Word Designators

Word designators are used to select desired words from the event. A `:' separates the event specification from the word designator. It may be omitted if the word designator begins with a `^', `$', `*', `-', or `%'. Words are numbered from the beginning of the line, with the first word being denoted by 0 (zero). Words are inserted into the current line separated by single spaces.

For example,

!! designates the preceding command. When you type this, the preceding command is repeated in toto.

!!:$ designates the last argument of the preceding command. This may be shortened to !$.

!fi:2 designates the second argument of the most recent command starting with the letters fi.


Here are the word designators:

0 (zero) The 0th word. For many applications, this is the command word.

n The nth word.

^ The first argument; that is, word 1.

$ The last argument.

% The word matched by the most recent `?string?' search.

x-y A range of words; `-y' abbreviates `0-y'.

* All of the words, except the 0th. This is a synonym for `1-$'. It is not an error to use `*' if there is just one word in the event; the empty string is returned in that case.

x* Abbreviates `x-$'

x- Abbreviates `x-$' like `x*', but omits the last word.

If a word designator is supplied without an event specification, the previous command is used as the event.


9.3.3 Modifiers

After the optional word designator, you can add a sequence of one or more of the following modifiers, each preceded by a `:'.

h Remove a trailing pathname component, leaving only the head.

t Remove all leading pathname components, leaving the tail.

r Remove a trailing suffix of the form `.suffix', leaving the basename.

e Remove all but the trailing suffix.

p Print the new command but do not execute it.

q Quote the substituted words, escaping further substitutions.

x Quote the substituted words as with `q', but break into words at spaces, tabs, and newlines.

s/old/new/ Substitute new for the first occurrence of old in the event line. Any delimiter may be used in place of `/'. The delimiter may be quoted in old and new with a single backslash. If `&' appears in new, it is replaced by old. A single backslash will quote the `&'. The final delimiter is optional if it is the last character on the input line.

& Repeat the previous substitution.

g Cause changes to be applied over the entire event line. Used in conjunction with `s', as in gs/old/new/, or with `&'.
"""

import re


class BashHistoryIndexError(IndexError):
    pass


def expand_history(command, history):
    history_num = re.compile(r'(?<!\\)!-?\d+')
    res = history_num.search(command)
    while res is not None:
        match = res.group(0)
        history_index = int(match[1:])
        history_index -= 1
        try:
            history_command = history[history_index]
        except IndexError:
            raise BashHistoryIndexError(match)
        span = res.span()
        command = command[: span[0]] + history_command + command[span[1] :]
        res = history_num.search(command)
    try:
        command = command.replace('!!', history[-2])
    except IndexError:
        pass
    return command, True
