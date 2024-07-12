from sbos_installer.utils.screen import line_of_chars

from rich.console import Console


class Header:
    border_style = "cyan on black"
    text_style = "bold white on cyan"

    def __init__(self, title):
        self.title = title
        console = Console()

        console.print(line_of_chars("▄"), style=self.border_style)
        console.print(title, style=self.text_style, justify="center")
        console.print(line_of_chars("▀"), style=self.border_style)
