from sbos_installer.utils.screen import line_of_chars
from sbos_installer.utils.colors import *

from rich.console import Console
from rich.text import Text


class Header:
    border_style = "cyan on white"
    text_style = "on cyan"

    def __init__(self, title):
        self.title = title
        console = Console()

        console.print(line_of_chars("▄"), style=self.border_style)
        console.print(Text.from_ansi(f"{WHITE}{BOLD}{title}"), style=self.text_style, justify="center")
        console.print(line_of_chars("▀"), style=self.border_style)
