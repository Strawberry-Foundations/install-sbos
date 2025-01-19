from sbos_installer.utils.colors import *
from sbos_installer.cli.selection import KeyGetter

from rich.padding import Padding
from rich.text import Text
from rich.console import Console

from io import StringIO
from itertools import zip_longest

import sys


class SelectButton:
    def __init__(self, label, description):
        self.label = label
        self.raw_description_text = description
        self.description_text = Text.from_ansi(f"{GRAY}{description}{RESET}")
        self.description = Padding(self.description_text, (0, 8))

    def __str__(self):
        return f"{self.label}"


class SelectButtonGroup:
    def __init__(self):
        self.buttons = []

    def append(self, button):
        self.buttons.append(button)

    def selection(self, question: str = "", flags: list = None) -> str:
        print(question)
        return self._draw_ia_selection(self.buttons, flags)

    def _print_and_measure_text(self, text):
        console = Console()
        rich_text = Text.from_ansi(f"{GRAY}{text}{RESET}")
        rich_text = Padding(rich_text, (0, 8))

        buffer = StringIO()
        console.file = buffer

        console.print(rich_text)

        buffer.seek(0)
        num_lines = buffer.getvalue().count('\n')

        console.file = sys.stdout
        console.print(rich_text)

        return num_lines

    def _measure_text(self, options):
        length = 0

        console = Console()
        for option in options:
            rich_text = Text.from_ansi(f"{GRAY}{option.raw_description_text}{RESET}")
            rich_text = Padding(rich_text, (0, 8))

            buffer = StringIO()
            console.file = buffer

            console.print(rich_text)

            buffer.seek(0)
            num_lines = buffer.getvalue().count('\n')

            length += num_lines

            console.file = sys.stdout

        return length

    def _draw_ia_selection(self, options: list, flags: list = None):
        __UNPOINTED = "      "
        __POINTED = f"       {BACK_WHITE}"
        __INDEX = 0
        __LENGTH = len(options)
        __LENGTH_2 = len(options) + (len(options) * 2) + self._measure_text(options)
        __ARROWS = __UP, _ = 65, 66
        __ENTER = 10

        if flags is None:
            flags = []

        def _choices_print():
            for i, (option, _) in enumerate(zip_longest(options, flags, fillvalue='')):
                if i == __INDEX:
                    print(f" {__POINTED}{BLACK}[ {option.label} ]{CRESET}\n")
                    self._print_and_measure_text(option.raw_description_text)
                    print()

                else:
                    print(f" {__UNPOINTED} [ {option.label} ]{CRESET}\n")
                    self._print_and_measure_text(option.raw_description_text)
                    print()

        def _choices_clear():
            nonlocal __LENGTH_2
            print(f"\033[{__LENGTH_2}A\033[J", end='')

        def _move_pointer(ch_ord: int):
            nonlocal __INDEX
            __INDEX = max(0, __INDEX - 1) if ch_ord == __UP else min(__INDEX + 1, __LENGTH - 1)

        def _main_loop():
            kg = KeyGetter()
            _choices_print()
            
            while True:
                key = ord(kg.getch())
                
                if key in __ARROWS:
                    _move_pointer(key)
                    
                _choices_clear()
                _choices_print()
                
                if key == __ENTER:
                    _choices_clear()
                    _choices_print()
                    break

        _main_loop()
        return flags[__INDEX]
