from sbos_installer.core.packages import package_list
from sbos_installer.core.ui.checkbox import Checkbox, ia_selection as chb_selection
from sbos_installer.core.ui.screen import Screen
from sbos_installer.utils.colors import *

from rich.text import Text


class PackageView(Screen):
    title = "Install additional packages"

    def __init__(self, os_type: str):
        self.packages = None
        self.os_type = os_type

        view = self.render
        super().__init__(title=self.title, view=view)

    def render(self):
        if self.os_type == "server":
            self.packages = ["base", "server"]
        else:
            self.packages = ["base"]

        self.console.print(
            "When installing StrawberryOS, you can choose whether you want to install additional packages. \n"
            "These can be utilities, but also development packages\n",
            justify="center"
        )

        self.console.print(
            Text.from_ansi(
                f"{YELLOW}[!] {GRAY}Use SPACE to select a package, ENTER to continue{CRESET}\n\n"
            ), justify="center"
        )

        groups = []
        flags = []

        for name, flag in package_list.items():
            Checkbox(
                label=name,
                group=groups
            )
            flags.append(flag)

        packages = chb_selection(
            question="",
            options=groups,
            flags=flags
        )

        self.packages.extend(packages)

        print(self.packages)

        return self.packages
