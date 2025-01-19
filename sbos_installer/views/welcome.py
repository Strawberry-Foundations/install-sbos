from sbos_installer.core.ui.screen import Screen
from sbos_installer.core.ui.select_button import SelectButton, SelectButtonGroup
from sbos_installer.core.process import run
from sbos_installer.views.about import AboutView
from sbos_installer.views.info import InfoView
from sbos_installer.utils.colors import *

from rich.text import Text

import sys
import os


class WelcomeView(Screen):
    title = "Welcome to the StrawberryOS Installer!"

    def __init__(self):
        view = self.render
        super().__init__(title=self.title, view=view)

    def render(self):
        self.console.show_cursor(False)
        self.console.print(
            f"Thanks for choosing StrawberryOS!\n"
            f"The StrawberryOS Installer will guide you through the installation process.\n",
            justify="center"
        )

        self.console.print(
            Text.from_ansi(
                f"{GREEN}{BOLD}! {CRESET}Use UP and DOWN to navigate, ENTER to continue\n\n"
            ), justify="center"
        )

        group = SelectButtonGroup()
        
        group.append(
            SelectButton(
                label=f"(->) Start installation",
                description="Start with the installation of StrawberryOS"
            )
        )
        
        group.append(
            SelectButton(
                label=f"(>_) Open a console",
                description="Open a console if you need to make changes beforehand. "
                            "You can start the installer again using 'setup-strawberryos'"
            )
        )

        group.append(
            SelectButton(
                label=f"(?) About StrawberryOS Installer",
                description="Learn more about the new StrawberryOS Installer (NucleusV2)"
            )
        )

        group.append(
            SelectButton(
                label=f"(!) Update StrawberryOS Installer",
                description="Check whether there is a new update for the installer"
            )
        )
        
        group.append(
            SelectButton(
                label=f"(->) Reboot",
                description="Restart your computer"
            )
        )
        
        group.append(
            SelectButton(
                label=f"(^) Shutdown",
                description="Turn off your computer"
            )
        )
        
        group.append(
            SelectButton(
                label=f"(x) Exit",
                description="Exit the installer"
            )
        )

        selection = group.selection(flags=["start", "console", "about", "update", "reboot", "shutdown", "exit"])

        match selection:
            case "console":
                self.console.clear()

                try:
                    with open("/etc/motd", 'r') as _motd:
                        print(_motd.read(), end="")

                except (FileNotFoundError, Exception):
                    pass

                self.console.show_cursor(True)
                sys.exit(0)

            case "about":
                AboutView()
                self.console.clear()
                self.redraw()

            case "update":
                run("update-installer")
                self.console.clear()
                python = sys.executable
                os.execv(python, ['python3'] + sys.argv)
                
            case "reboot":
                run("reboot")
                
            case "shutdown":
                run("shutdown now")
                
            case "exit":
                InfoView(f"Exited installation process.\nYou can start the installer again using '{GRAY}setup-strawberryos{CRESET}'")
                self.console.show_cursor(True)
                self.console.clear()
                sys.exit(0)

        self.console.show_cursor(True)
        return None
