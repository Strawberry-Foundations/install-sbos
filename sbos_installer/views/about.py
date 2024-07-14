from sbos_installer.var import version
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
        self.console.print(Text.from_ansi(
            f"StrawberryOS Installer v{version} (Nucleus)\n"
            ""
        ), justify="center")

        self.console.print(Text.from_ansi(f"Press Enter to return"), justify="center")
        input()

        print(CRESET)
        return None
