from sbos_installer.core.ui.screen import Screen
from sbos_installer.cli.parser import parse_bool
from sbos_installer.cli.selection import ia_selection
from sbos_installer.utils.colors import *

from rich.padding import Padding
from rich.text import Text

import sys


class OverviewScreenView(Screen):
    title = "Completing the installation"

    def __init__(self, data, disk):
        self.data = data
        self.disk = disk

        view = self.render
        super().__init__(title=self.title, view=view)

    def render(self):
        self.console.print(Padding(
            "Here you will find a brief overview of the entries you have made.\n",
            (0, 8))
        )

        file_system = self.data['disk']["file_system"]
        disk_data = self.data['disk'][self.disk]

        self.console.print(Padding(Text.from_ansi(
            f"{GRAY}{BOLD}* {CYAN}Hostname:{CRESET} {self.data['hostname']}"
        ), (0, 8)))
        self.console.print(Padding(Text.from_ansi(
            f"{GRAY}{BOLD}* {CYAN}Network interface:{CRESET} {self.data['net_interface']}"
        ), (0, 8)))
        self.console.print(Padding(Text.from_ansi(
            f"{GRAY}{BOLD}* {CYAN}Timezone:{CRESET} {self.data['timezone']['region']}/{self.data['timezone']['city']}"
        ), (0, 8)))
        self.console.print(Padding(Text.from_ansi(
            f"{GRAY}{BOLD}* {CYAN}Users:{CRESET}"
        ), (0, 8)))

        for user in self.data["users"]:
            suffix = ""
            if user != "root":
                if self.data["users"][f"{user}"]["sudo_user"]:
                    suffix = f"{CRESET}({YELLOW}sudo{CRESET})"
            self.console.print(Padding(Text.from_ansi(
                f"{GRAY}{BOLD}    * {CYAN}{user} {suffix}{CRESET}"
            ), (0, 8)))

        self.console.print(Padding(Text.from_ansi(
            f"{GRAY}{BOLD}* {CYAN}Disk:{CRESET} {self.disk}"
        ), (0, 8)))
        self.console.print(Padding(Text.from_ansi(
            f"{GRAY}{BOLD}    * {CYAN}EFI on {CYAN}{disk_data['efi']['block']}{CRESET}: "
            f"{disk_data['efi']['size'] / 1024}G ({disk_data['efi']['size']}M){CRESET}"
        ), (0, 8)))
        self.console.print(Padding(Text.from_ansi(
            f"{GRAY}{BOLD}    * {CYAN}Swap on {CYAN}{disk_data['swap']['block']}{CRESET}: "
            f"{disk_data['swap']['size'] / 1024}G ({disk_data['swap']['size']}M){CRESET}"
        ), (0, 8)))
        self.console.print(Padding(Text.from_ansi(
            f"{GRAY}{BOLD}    * {CYAN}System on {CYAN}{disk_data['system']['block']}{CRESET}: "
            f"{disk_data['system']['size'] / 1024}G ({disk_data['system']['size']}M){CRESET}"
        ), (0, 8)))
        self.console.print(Padding(Text.from_ansi(
            f"{GRAY}{BOLD}    * {CYAN}User on {CYAN}{disk_data['user']['block']}{CRESET}: "
            f"{disk_data['user']['size'] / 1024}G ({disk_data['user']['size']}M){CRESET}"
        ), (0, 8)))
        self.console.print(Padding(Text.from_ansi(
            f"{GRAY}{BOLD}    * {CYAN}File system:{CRESET} {file_system}"
        ), (0, 8)))
        self.console.print(Padding(Text.from_ansi(
            f"{GRAY}{BOLD}* {CYAN}Packages:{CRESET} {', '.join(self.data['packages'])}"
        ), (0, 8)))

        print()

        confirm = parse_bool(ia_selection(
            question="Do you want to continue the installation?",
            options=["Yes", "No"],
            padding=8
        ))

        if not confirm:
            print(f"\n{YELLOW}Exiting installation process{CRESET}")
            sys.exit()

        return None
