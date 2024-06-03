import atexit
import termios
import tty
import sys
from itertools import zip_longest


class KeyGetter:
    def arm(self):
        self.old_term = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin)

        atexit.register(self.disarm)

    def disarm(self):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_term)

    def getch(self):
        self.arm()
        ch = sys.stdin.read(1)[0]
        self.disarm()
        return ch


def ia_selection(question: str, options: list = None, flags: list = None) -> str:
    print(question)
    return _draw_ia_selection(options, flags)


def _draw_ia_selection(options: list, flags: list = None):
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
                print(f" {__POINTED} {{0}}{option} {flag}{{1}}".format('\033[94m', '\033[0m'))
            else:
                print(f" {__UNPOINTED} {option} {flag}")

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