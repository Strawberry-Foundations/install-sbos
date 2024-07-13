from sbos_installer.utils.colors import *

import shutil


def clear_screen():
    print("\033[2J\033[H", end="")


def get_terminal_width():
    size = shutil.get_terminal_size()
    return size.columns


def line_of_chars(char='-', length=None):
    if length is None:
        length = get_terminal_width()
    return char * length


def text_centered(text, bg_color):
    width = get_terminal_width()
    text_length = len(text)
    padding_left = (width - text_length) // 2
    padding_right = width - padding_left - text_length

    output = bg_color + ' ' * padding_left + f"{RESET}{WHITE}{BOLD}{text}{RESET}" + ' ' * padding_right + CRESET
    return output


def set_cursor_position(row, col):
    print(f"\033[{row};{col}H", end='')


def set_background_color(row, col, length, color):
    print(f"\033[{row};{col}H", end='')
    print(f"\033[48;5;{color}m{' ' * length}\033[0m", end='')


def input_with_background(row, col, length, bg_color, fg_color=0):
    set_background_color(row, col, length, bg_color)
    set_cursor_position(row, col)
    text = input()
    return text
