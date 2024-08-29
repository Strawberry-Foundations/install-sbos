from sbos_installer import clear_screen
from sbos_installer.core.ui.header import Header
from sbos_installer.utils.colors import *

from rich.console import Console
from rich.text import Text

import sys


class WarningView:
    class Header(Header):
        border_style = "yellow"
        text_style = "on yellow"

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
            self.console.show_cursor(True)
            sys.exit(1)

        print(CRESET)
        self.console.show_cursor(True)
