from sbos_installer.core.ui.screen import Screen
from sbos_installer.utils.colors import *

from rich.text import Text
from rich.padding import Padding


class AboutView(Screen):
    title = "About StrawberryOS Installer"

    def __init__(self):
        view = self.render
        super().__init__(title=self.title, view=view)

    def render(self):
        self.console.print(Padding(Text.from_ansi(
            "Enter the hostname for your new system.\n"
            "The hostname can consist of numbers, upper and lower case letters.\n"),
            (0, 8))
        )

        print(CRESET)
        return None
