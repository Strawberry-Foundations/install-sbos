from sbos_installer import clear_screen
from sbos_installer.utils.screen import line_of_chars
from sbos_installer.utils.colors import *

from rich.console import Console
from rich.text import Text

import sys


class WarningView:
    class Header:
        border_style = "yellow on black"
        text_style = "on yellow"

        def __init__(self, title):
            self.title = title
            console = Console()

            console.print(line_of_chars("▄"), style=self.border_style)
            console.print(Text.from_ansi(f"{WHITE}{BOLD}{title}"), style=self.text_style, justify="center")
            console.print(line_of_chars("▀"), style=self.border_style)

    title = "Warning!"
    console = Console()

    def __init__(self, warning_message):
        self.warning = warning_message

        clear_screen()
        WarningView.Header(self.title)

        self.render()

    def render(self):
        self.console.show_cursor(False)
        self.console.print(Text.from_ansi(
            f"{self.warning}"
        ), justify="center")

        self.console.print("\nPress Enter to continue", justify="center")

        try:
            input()
        except KeyboardInterrupt:
            self.console.clear()
            print(f"\n{YELLOW}Exited installation process{CRESET}")
            self.console.show_cursor(True)

        print(CRESET)
        self.console.show_cursor(True)
