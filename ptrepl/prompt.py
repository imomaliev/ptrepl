import os

from functools import partial

from prompt_toolkit.application.current import get_app
from prompt_toolkit.shortcuts.prompt import (
    PromptSession,
    CompleteStyle,
    _split_multiline_prompt,
    _RPrompt,
)
from prompt_toolkit.key_binding.vi_state import InputMode
from prompt_toolkit.enums import EditingMode
from prompt_toolkit import ANSI

from prompt_toolkit.filters import (
    is_done,
    has_focus,
    renderer_height_is_known,
    is_true,
    Condition,
    has_arg,
)
from prompt_toolkit.layout import Window, HSplit, FloatContainer, Float
from prompt_toolkit.layout.containers import ConditionalContainer
from prompt_toolkit.layout.controls import (
    BufferControl,
    SearchBufferControl,
    FormattedTextControl,
)
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.menus import CompletionsMenu, MultiColumnCompletionsMenu
from prompt_toolkit.layout.processors import (
    DynamicProcessor,
    PasswordProcessor,
    ConditionalProcessor,
    AppendAutoSuggestion,
    HighlightIncrementalSearchProcessor,
    HighlightSelectionProcessor,
    DisplayMultipleCursors,
    ReverseSearchProcessor,
    merge_processors,
)
from prompt_toolkit.lexers import DynamicLexer
from prompt_toolkit.widgets.toolbars import (
    ValidationToolbar,
    SystemToolbar,
    SearchToolbar,
)

from .bash_prompt import Lexer
from .toolbars import CommandToolbar
from .settings import settings


def get_prompt_tokens(command):
    # https://github.com/jonathanslenders/python-prompt-toolkit/issues/247
    prompt = Lexer().render(os.getenv('PS1'))

    def _get_prompt_tokens():
        if not settings.PARSE_PS1:
            return ANSI('{} > '.format(command))

        app = get_app()

        _prompt, last_line = prompt.rsplit('\n')

        _command = '\x1b[1;36m{}\x1b[m'.format(command)
        if app.editing_mode == EditingMode.VI:
            in_insert_mode = app.vi_state.input_mode == InputMode.INSERT
            mode = settings.VI_NORMAL_MODE if in_insert_mode else settings.VI_EDIT_MODE
            mode = '{} '.format(mode)
            last_line = '{}{}{}'.format(mode, _command, last_line)
        else:
            last_line = '{}{}'.format(_command, last_line)

        _prompt = '{}\n{}'.format(_prompt, last_line)
        return ANSI(_prompt)

    return _get_prompt_tokens


class PtreplSession(PromptSession):
    def _create_layout(self):
        """
        Create `Layout` for this prompt.
        """
        dyncond = self._dyncond

        # Create functions that will dynamically split the prompt. (If we have
        # a multiline prompt.)
        has_before_fragments, get_prompt_text_1, get_prompt_text_2 = _split_multiline_prompt(
            self._get_prompt
        )

        default_buffer = self.default_buffer
        search_buffer = self.search_buffer

        # Create processors list.
        all_input_processors = [
            HighlightIncrementalSearchProcessor(),
            HighlightSelectionProcessor(),
            ConditionalProcessor(
                AppendAutoSuggestion(), has_focus(default_buffer) & ~is_done
            ),
            ConditionalProcessor(PasswordProcessor(), dyncond('is_password')),
            DisplayMultipleCursors(),
            # Users can insert processors here.
            DynamicProcessor(lambda: merge_processors(self.input_processors or [])),
        ]

        # Create bottom toolbars.
        bottom_toolbar = ConditionalContainer(
            Window(
                FormattedTextControl(
                    lambda: self.bottom_toolbar, style='class:bottom-toolbar.text'
                ),
                style='class:bottom-toolbar',
                dont_extend_height=True,
                height=Dimension(min=1),
            ),
            ~is_done
            & renderer_height_is_known
            & Condition(lambda: self.bottom_toolbar is not None),
        )

        search_toolbar = SearchToolbar(
            search_buffer, ignore_case=dyncond('search_ignore_case')
        )

        search_buffer_control = SearchBufferControl(
            buffer=search_buffer,
            input_processors=[ReverseSearchProcessor()],
            ignore_case=dyncond('search_ignore_case'),
        )

        system_toolbar = SystemToolbar(
            enable_global_bindings=dyncond('enable_system_prompt')
        )

        command_toolbar = CommandToolbar(enable_global_bindings=True)

        def get_search_buffer_control():
            " Return the UIControl to be focused when searching start. "
            if is_true(self.multiline):
                return search_toolbar.control
            else:
                return search_buffer_control

        default_buffer_control = BufferControl(
            buffer=default_buffer,
            search_buffer_control=get_search_buffer_control,
            input_processors=all_input_processors,
            include_default_input_processors=False,
            lexer=DynamicLexer(lambda: self.lexer),
            preview_search=True,
        )

        default_buffer_window = Window(
            default_buffer_control,
            height=self._get_default_buffer_control_height,
            get_line_prefix=partial(
                self._get_line_prefix, get_prompt_text_2=get_prompt_text_2
            ),
            wrap_lines=dyncond('wrap_lines'),
        )

        @Condition
        def multi_column_complete_style():
            return self.complete_style == CompleteStyle.MULTI_COLUMN

        # Build the layout.
        layout = HSplit(
            [
                # The main input, with completion menus floating on top of it.
                FloatContainer(
                    HSplit(
                        [
                            ConditionalContainer(
                                Window(
                                    FormattedTextControl(get_prompt_text_1),
                                    dont_extend_height=True,
                                ),
                                Condition(has_before_fragments),
                            ),
                            ConditionalContainer(
                                default_buffer_window,
                                Condition(
                                    lambda: get_app().layout.current_control
                                    != search_buffer_control
                                ),
                            ),
                            ConditionalContainer(
                                Window(search_buffer_control),
                                Condition(
                                    lambda: get_app().layout.current_control
                                    == search_buffer_control
                                ),
                            ),
                        ]
                    ),
                    [
                        # Completion menus.
                        Float(
                            xcursor=True,
                            ycursor=True,
                            content=CompletionsMenu(
                                max_height=16,
                                scroll_offset=1,
                                extra_filter=has_focus(default_buffer)
                                & ~multi_column_complete_style,
                            ),
                        ),
                        Float(
                            xcursor=True,
                            ycursor=True,
                            content=MultiColumnCompletionsMenu(
                                show_meta=True,
                                extra_filter=has_focus(default_buffer)
                                & multi_column_complete_style,
                            ),
                        ),
                        # The right prompt.
                        Float(
                            right=0,
                            top=0,
                            hide_when_covering_content=True,
                            content=_RPrompt(lambda: self.rprompt),
                        ),
                    ],
                ),
                ConditionalContainer(ValidationToolbar(), ~is_done),
                ConditionalContainer(
                    system_toolbar, dyncond('enable_system_prompt') & ~is_done
                ),
                ConditionalContainer(command_toolbar, ~is_done),
                # In multiline mode, we use two toolbars for 'arg' and 'search'.
                ConditionalContainer(
                    Window(FormattedTextControl(self._get_arg_text), height=1),
                    dyncond('multiline') & has_arg,
                ),
                ConditionalContainer(search_toolbar, dyncond('multiline') & ~is_done),
                bottom_toolbar,
            ]
        )

        return Layout(layout, default_buffer_window)
