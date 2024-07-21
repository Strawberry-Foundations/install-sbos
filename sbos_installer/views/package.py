from sbos_installer.core.ui.screen import Screen
from sbos_installer.core.ui.checkbox import Checkbox, ia_selection as chb_selection
from sbos_installer.core.packages import package_list
from sbos_installer.cli.parser import parse_bool
from sbos_installer.cli.selection import ia_selection
from sbos_installer.utils.colors import *

from rich.text import Text
from rich.padding import Padding


class PackageView(Screen):
    title = "Install additional packages"

    def __init__(self):
        self.packages = None
        view = self.render
        super().__init__(title=self.title, view=view)

    def render(self):
        self.packages = ["base"]
        self.console.print(
            "When installing StrawberryOS, you can choose whether you want to install additional packages. \n"
            "These can be utilities, but also development packages\n",
            justify="center"
        )

        groups = []
        flags = []

        for name, flag in package_list.items():
            Checkbox(
                label=name,
                group=groups
            )
            flags.append(flag)

        self.packages = chb_selection(
            question="",
            options=groups,
            flags=flags
        )

        return self.packages


"""                
            _packages = None
            _flag = True
            while _flag:
                self.console.print(Padding(Text.from_ansi(f"\nAvailable packages: {GRAY}{' '.join(package_list)}{CRESET}"), (0, 8)))

                _packages = input(f"        Provide additional packages [init,base]:  {GRAY}").split(",")
                print(CRESET, end="")

                for package in _packages:
                    if package == '':
                        _flag = False
                    if package not in package_list:
                        self.console.print(Padding(Text.from_ansi(
                            f"{YELLOW}{BOLD}Package '{package}' is not available{CRESET}"), (0, 8)
                        ))
                    else:
                        _flag = False

            self.packages.extend(_packages)"""
