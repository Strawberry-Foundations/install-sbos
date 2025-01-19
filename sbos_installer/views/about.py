from sbos_installer.core.ui.screen import Screen
from sbos_installer.var import VERSION
from sbos_installer.utils.colors import *

from rich.text import Text


class AboutView(Screen):
    title = "About StrawberryOS Installer"

    def __init__(self):
        view = self.render
        super().__init__(title=self.title, view=view)

    def render(self):
        self.console.show_cursor(False)
        self.console.print(Text.from_ansi(
            f"StrawberryOS Installer {CYAN}v{VERSION}{RESET} (Nucleus)\n\n"
            "The StrawberryOS Installer is an easy to use installer \n"
            "that allows you to install StrawberryOS according to your preferences.\n\n"
            "This installer is a part of the StrawberryOS project.\n"
            f"{LIGHT_BLUE}https://github.com/Strawberry-Foundations/install-sbos{CRESET}\n\n"
            "StrawberryOS Installer uses open source libraries, the main ones being:\n"
            f"* {LIGHT_BLUE}https://github.com/Textualize/rich{CRESET}"
        ), justify="center")

        self.console.print("\nPress Enter to return", justify="center")

        input()

        print(CRESET)
        self.console.show_cursor(True)
        return None
