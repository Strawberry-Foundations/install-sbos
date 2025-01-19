from sbos_installer.utils.colors import *
from sbos_installer.utils.screen import get_terminal_width
from sbos_installer.cli.selection import KeyGetter

from itertools import zip_longest


class Checkbox:
    def __init__(self, label):
        self.label = label

    def __str__(self):
        return f"{self.label}"


class CheckboxGroup:
    def __init__(self):
        self.checkboxes = []

    def append(self, checkbox):
        self.checkboxes.append(checkbox)

    def __iter__(self):
        return iter(self.checkboxes)

    def __getitem__(self, index):
        return self.checkboxes[index]

    def __len__(self):
        return len(self.checkboxes)

    def selection(self, question: str = "", flags: list = None) -> str:
        print(question)
        return self._draw_ia_selection(self.checkboxes, flags)


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
        __SPACE = 32

        __SELECTS = []

        if flags is None:
            flags = []

        def spaces(length: int):
            return " " * length

        def _choices_print():
            for i, (option, flag) in enumerate(zip_longest(options, flags, fillvalue='')):
                if i == __INDEX:
                    len_label = len(option.label)
                    remaining = 33 - len_label
                    print(f" {__POINTED}{BLACK}[{selected(flag)}] [ {option.label}{spaces(remaining)}]{CRESET}")

                else:
                    len_label = len(option.label)
                    remaining = 33 - len_label
                    print(f" {__UNPOINTED} [{selected(flag)}] [ {option.label}{spaces(remaining)}]{CRESET}")

        def selected(flag: str):
            nonlocal __SELECTS
            if flag in __SELECTS:
                return "X"
            return " "

        def check(index: int):
            nonlocal __SELECTS
            obj = enumerate(zip_longest(options, flags, fillvalue=''))
            
            for i, (_, flag) in obj:
                if i == index:
                    if flag in __SELECTS:
                        disable(index)
                    else:
                        enable(index)

        def enable(index: int):
            nonlocal __SELECTS
            obj = enumerate(zip_longest(options, flags, fillvalue=''))
            
            for i, (_, flag) in obj:
                if i == index:
                    __SELECTS.append(flag)

        def disable(index: int):
            nonlocal __SELECTS
            obj = enumerate(zip_longest(options, flags, fillvalue=''))
            
            for i, (_, flag) in obj:
                if i == index:
                    __SELECTS.remove(flag)

        def _choices_clear():
            nonlocal __LENGTH
            print(f"\033[{__LENGTH}A\033[J", end='')

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
                
                if key == __SPACE:
                    check(__INDEX)
                    _choices_clear()
                    _choices_print()
                    
                if key == __ENTER:
                    _choices_clear()
                    _choices_print()
                    break

        _main_loop()
        return __SELECTS
