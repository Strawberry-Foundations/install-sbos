from sbos_installer import clear_screen
from sbos_installer.utils.screen import line_of_chars
from sbos_installer.utils.colors import *

from rich.console import Console
from rich.text import Text

import sys


class ErrorView:
    class Header:
        border_style = "red on black"
        text_style = "on red"

        def __init__(self, title):
            self.title = title
            console = Console()

            console.print(line_of_chars("▄"), style=self.border_style)
            console.print(Text.from_ansi(f"{WHITE}{BOLD}{title}"), style=self.text_style, justify="center")
            console.print(line_of_chars("▀"), style=self.border_style)

    title = "An error occurred"
    console = Console()

    def __init__(self, error_message):
        self.error = error_message

        clear_screen()
        ErrorView.Header(self.title)

        self.render()

    def render(self):
        self.console.show_cursor(False)
        self.console.print(Text.from_ansi(
            f"{self.error}"
        ), justify="center")

        self.console.print("\nPress Enter to exit the installer", justify="center")
        input()

        print(CRESET)
        self.console.show_cursor(True)
        sys.exit(1)
