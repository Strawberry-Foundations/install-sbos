from sbos_installer.core.ui import KeyGetter
from itertools import zip_longest

def ia_selection(question: str, options: list = None, flags: list = None, padding: int = 0) -> str:
    print(" " * padding + question)
    return _draw_ia_selection(options, flags, padding)


def _draw_ia_selection(options: list, flags: list = None, padding: int = 0):
    __UNPOINTED = " "
    __POINTED = ">"
    __INDEX = 0
    __LENGTH = len(options)
    __ARROWS = __UP, _ = 65, 66
    __ENTER = 10

    if flags is None:
        flags = []

    def _choices_print():
        for i, (option, flag) in enumerate(zip_longest(options, flags, fillvalue='')):
            if i == __INDEX:
                print(" " * padding + f" {__POINTED} {{0}}{option} {flag}{{1}}".format('\033[94m', '\033[0m'))
            else:
                print(" " * padding + f" {__UNPOINTED} {option} {flag}")

    def _choices_clear():
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
            if key == __ENTER:
                _choices_clear()
                _choices_print()
                break

    _main_loop()
    return options[__INDEX]