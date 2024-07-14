from sbos_installer.core.ui.screen import Screen
from sbos_installer.var import version
from sbos_installer.utils.colors import *

from rich.text import Text

import sys


class AboutView(Screen):
    title = "About StrawberryOS Installer"

    def __init__(self):
        view = self.render
        super().__init__(title=self.title, view=view)

    def render(self):
        self.console.show_cursor(False)
        self.console.print(Text.from_ansi(
            f"StrawberryOS Installer v{version} (Nucleus)\n\n"
            "The StrawberryOS Installer is an easy to use installer \n"
            "that allows you to install StrawberryOS according to your preferences.\n\n"
            f"{LIGHT_BLUE}https://github.com/Strawberry-Foundations/install-sbos{CRESET}"
        ), justify="center")

        self.console.print("\nPress Enter to return", justify="center")

        try:
            input()
        except KeyboardInterrupt:
            self.console.clear()
            self.console.print(Text.from_ansi(f"{YELLOW}{BOLD}Exited installation process{CRESET}"), justify="center")
            self.console.show_cursor(True)
            sys.exit(1)

        print(CRESET)
        self.console.show_cursor(True)
        return None
