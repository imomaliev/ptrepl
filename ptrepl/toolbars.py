import sys

import click

from prompt_toolkit.application.application import _do_wait_for_enter
from prompt_toolkit.application.current import get_app
from prompt_toolkit.application.run_in_terminal import run_coroutine_in_terminal
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.eventloop import From, run_in_executor
from prompt_toolkit.filters import (
    emacs_mode,
    has_focus,
    to_filter,
    vi_mode,
    vi_navigation_mode,
)
from prompt_toolkit.key_binding.key_bindings import (
    ConditionalKeyBindings,
    KeyBindings,
    merge_key_bindings,
)
from prompt_toolkit.key_binding.vi_state import InputMode
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.containers import ConditionalContainer, Window
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.processors import BeforeInput
from prompt_toolkit.lexers import SimpleLexer
from prompt_toolkit.renderer import print_formatted_text
from prompt_toolkit.widgets.toolbars import SystemToolbar


COMMAND_BUFFER = 'COMMAND_BUFFER'


class CommandToolbar(SystemToolbar):
    def __init__(
        self, command, aliases, prompt='Command mode: ', enable_global_bindings=True
    ):
        self.command = command
        self.aliases = aliases
        self._app = get_app()
        self.prompt = prompt
        self.enable_global_bindings = to_filter(enable_global_bindings)

        self.system_buffer = Buffer(name=COMMAND_BUFFER)

        self._bindings = self._build_key_bindings()

        self.buffer_control = BufferControl(
            buffer=self.system_buffer,
            lexer=SimpleLexer(style='class:system-toolbar.text'),
            input_processors=[
                BeforeInput(lambda: self.prompt, style='class:system-toolbar')
            ],
            key_bindings=self._bindings,
        )

        self.window = Window(
            self.buffer_control, height=1, style='class:system-toolbar'
        )

        self.container = ConditionalContainer(
            content=self.window, filter=has_focus(self.system_buffer)
        )

    def print_text(self, text, style=None):
        """
        Print a list of (style_str, text) tuples to the output.
        (When the UI is running, this method has to be called through
        `run_in_terminal`, otherwise it will destroy the UI.)

        :param text: List of ``(style_str, text)`` tuples.
        :param style: Style class to use. Defaults to the active style in the CLI.
        """
        print_formatted_text(
            output=self._app.output,
            formatted_text=text,
            style=style or self._app._merged_style,
            color_depth=self._app.color_depth,
            style_transformation=self._app.style_transformation,
        )

    def run(
        self,
        app,
        command,
        wait_for_enter=True,
        display_before_text='',
        wait_text='Press ENTER to continue...',
    ):
        """
        Run command (While hiding the prompt. When finished, all the
        output will scroll above the prompt.)

        :param command: Shell command to be executed.
        :param wait_for_enter: FWait for the user to press enter, when the
            command is finished.
        :param display_before_text: If given, text to be displayed before the
            command executes.
        :return: A `Future` object.
        """
        assert isinstance(wait_for_enter, bool)

        def _run():
            # Try to use the same input/output file descriptors as the one,
            # used to run this application.
            try:
                input_fd = self.input.fileno()
            except AttributeError:
                input_fd = sys.stdin.fileno()
            try:
                output_fd = self.output.fileno()
            except AttributeError:
                output_fd = sys.stdout.fileno()

            # Run sub process.
            def run_command():
                self.print_text(display_before_text)
                if command == 'history':
                    for index, item in enumerate(
                        app.layout.get_buffer_by_name(
                            DEFAULT_BUFFER
                        ).history.get_strings()
                    ):
                        click.echo(f'{index} {item}')
                elif command == 'alias':
                    for alias, alias_command in self.aliases.items():
                        click.echo(f'alias "{alias}"="{alias_command}"')

            yield run_in_executor(run_command)

            # Wait for the user to press enter.
            if wait_for_enter:
                yield From(_do_wait_for_enter(wait_text))

        return run_coroutine_in_terminal(_run)

    def _build_key_bindings(self):
        focused = has_focus(self.system_buffer)

        # Emacs
        emacs_bindings = KeyBindings()
        handle = emacs_bindings.add

        @handle('escape', filter=focused)
        @handle('c-g', filter=focused)
        @handle('c-c', filter=focused)
        def _(event):
            """Hide system prompt."""
            self.system_buffer.reset()
            event.app.layout.focus_last()

        @handle('enter', filter=focused)
        def _(event):
            """Run command."""
            self.run(
                event.app,
                self.system_buffer.text,
                display_before_text=self._get_display_before_text(),
            )
            self.system_buffer.reset(append_to_history=True)
            event.app.layout.focus_last()

        # Vi.
        vi_bindings = KeyBindings()
        handle = vi_bindings.add

        @handle('escape', filter=focused)
        @handle('c-c', filter=focused)
        def _(event):
            """Hide command prompt."""
            event.app.vi_state.input_mode = InputMode.NAVIGATION
            self.system_buffer.reset()
            event.app.layout.focus_last()

        @handle('enter', filter=focused)
        def _(event):
            """Run command."""
            event.app.vi_state.input_mode = InputMode.NAVIGATION
            self.run(
                event.app,
                self.system_buffer.text,
                display_before_text=self._get_display_before_text(),
            )
            self.system_buffer.reset(append_to_history=True)
            event.app.layout.focus_last()

        # Global bindings. (Listen to these bindings, even when this widget is
        # not focussed.)
        global_bindings = KeyBindings()
        handle = global_bindings.add

        @handle(Keys.Escape, ':', filter=~focused & emacs_mode, is_global=True)
        def _(event):
            """M-'!' will focus this user control."""
            event.app.layout.focus(self.window)

        @handle(':', filter=~focused & vi_mode & vi_navigation_mode, is_global=True)
        def _(event):
            """Focus."""
            event.app.vi_state.input_mode = InputMode.INSERT
            event.app.layout.focus(self.window)

        return merge_key_bindings(
            [
                ConditionalKeyBindings(emacs_bindings, emacs_mode),
                ConditionalKeyBindings(vi_bindings, vi_mode),
                ConditionalKeyBindings(global_bindings, self.enable_global_bindings),
            ]
        )
