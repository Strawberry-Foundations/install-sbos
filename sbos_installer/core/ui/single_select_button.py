from sbos_installer.utils.colors import *
from sbos_installer.utils.screen import get_terminal_width
from sbos_installer.cli.selection import KeyGetter

from itertools import zip_longest


class SingleSelectButton:
    def __init__(self, label):
        self.label = label

    def __str__(self):
        return f"{self.label}"


class SingleSelectButtonGroup:
    def __init__(self):
        self.buttons = []

    def append(self, button: SingleSelectButton):
        self.buttons.append(button)

    def __iter__(self):
        return iter(self.buttons)

    def selection(self, question: str = "", flags: list = None) -> str:
        print(question)
        return self._draw_ia_selection(options=self.buttons, flags=flags)

    def _draw_ia_selection(self, options: list, flags: list = None):
        width = get_terminal_width()
        text_length = len("                                    ")
        padding_left = (width - text_length) // 2

        __UNPOINTED = " " * (padding_left - 2)
        __POINTED = " " * (padding_left - 1) + f"{BACK_WHITE}"
        __INDEX = 0
        __LENGTH = len(options)
        __ARROWS = __UP, _ = 65, 66
        __ENTER = 10

        if flags is None:
            flags = []

        def spaces(length: int):
            return " " * length

        def _choices_print():
            for i, (option, flag) in enumerate(zip_longest(options, flags, fillvalue='')):
                if i == __INDEX:
                    len_label = len(option.label)
                    remaining = 33 - len_label
                    print(f" {__POINTED}{BLACK}[ {option.label}{spaces(remaining)}]{CRESET}")

                else:
                    len_label = len(option.label)
                    remaining = 33 - len_label
                    print(f" {__UNPOINTED} [ {option.label}{spaces(remaining)}]{CRESET}")

        def _choices_clear():
            nonlocal __LENGTH
            print(f"\033[{__LENGTH}A\033[J", end='')

        def _move_pointer(ch_ord: int):
            nonlocal __INDEX
            __INDEX = max(
                0, __INDEX - 1) if ch_ord == __UP else min(__INDEX + 1, __LENGTH - 1)

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
