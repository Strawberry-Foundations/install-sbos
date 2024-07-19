from sbos_installer.core.ui.header import Header
from sbos_installer.utils.screen import clear_screen

from rich.console import Console


class Screen:
    title = ""
    console = Console()

    def __init__(self, title, view):
        self.val = None
        self.title = title
        self.view = view

        clear_screen()
        Header(self.title)

        self.val = self.render()

    def render(self):
        return self.view()

    def redraw(self):
        self.console.clear()
        Header(self.title)
        self.val = self.render()
