from sbos_installer.core.ui.screen import Screen
from sbos_installer.utils.colors import *

from rich.text import Text
from rich.padding import Padding


class HostnameView(Screen):
    title = "Configure hostname"
    hostname = ""

    def __init__(self):
        view = self.render
        super().__init__(title=self.title, view=view)

    def input(self):
        self.console.print(Padding(
            Text.from_ansi(f"{YELLOW}[!] {GRAY}'{GREEN}strawberryos{GRAY}' is automatically used if no input is made\n{CRESET}"),
            (0, 17))
        )

        self.hostname = input(f"        Hostname:  {GRAY}")

    def render(self):
        self.console.print(Padding(
            "Enter the hostname for your new system.\n"
            "The hostname can consist of numbers, upper and lower case letters.\n",
            (0, 8))
        )

        self.input()

        if self.hostname.strip() == "":
            return "strawberryos"

        print(CRESET)

        return self.hostname
