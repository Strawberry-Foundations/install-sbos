from sbos_installer import clear_screen
from sbos_installer.core.ui.header import Header
from sbos_installer.utils.colors import *

from rich.console import Console
from rich.text import Text

import sys


class ErrorView:
    class Header(Header):
        border_style = "red"
        text_style = "on red"

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

        try:
            input()
        except KeyboardInterrupt:
            self.console.clear()
            self.console.print(Text.from_ansi(
                f"-- {YELLOW}{BOLD}Exited installation process{CRESET} --"
            ), justify="center")
            self.console.show_cursor(True)
            sys.exit(1)

        print(CRESET)
        self.console.show_cursor(True)
        self.console.clear()
        sys.exit(1)
