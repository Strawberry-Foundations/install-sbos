from sbos_installer.core.ui.screen import clear_screen
from sbos_installer.core.process import run
from sbos_installer.core.ui.select_button import SelectButton, ia_selection
from sbos_installer.core.ui.screen import Screen
from sbos_installer.utils.colors import *

from rich.text import Text
from rich.padding import Padding

import sys


class FinishView(Screen):
    title = "Installation finished"

    def __init__(self):
        view = self.render
        super().__init__(title=self.title, view=view)

    def render(self):
        self.console.show_cursor(False)
        self.console.print(Padding(Text.from_ansi(
            f"The installation was completed successfully.\n"
            f"You can now restart your system or open a shell to make further configurations"
        )))

        self.console.show_cursor(False)

        group = []

        SelectButton(
            label=f"(->) Reboot",
            description="Restart your computer to start your new system",
            group=group
        )

        SelectButton(
            label=f"(>_) Open a console",
            description="Open a console if you need to make changes to your new system."
                        "You can restart your computer by using the 'reboot' command",
            group=group
        )

        action = ia_selection(
            question="",
            options=group,
            flags=["reboot", "console"]
        )

        match action:
            case "reboot":
                run("reboot")
            case "console":
                clear_screen()
                self.console.show_cursor(True)
                print(CRESET)

                try:
                    with open("/etc/motd", 'r') as _file:
                        print(_file.read(), end="")
                except:
                    pass

                sys.exit(0)

        return None
