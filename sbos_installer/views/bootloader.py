from sbos_installer.core.ui.screen import Screen
from sbos_installer.cli.selection import ia_selection
from sbos_installer.steps.bootloader import configure_systemd_boot, configure_grub

from rich.padding import Padding


class BootloaderView(Screen):
    title = "Install a bootloader"

    def __init__(self, disk):
        self.disk = disk

        view = self.render
        super().__init__(title=self.title, view=view)

    def render(self):
        self.console.print(Padding(
            "The bootloader is important for starting the operating system.\n"
            "Please select one of our available bootloaders",
            (0, 8))
        )

        selection = ia_selection(
            question="",
            options=["GRUB", "systemd-boot"],
            flags=["(Recommended)", "(Experimental support)"],
            padding=8
        )

        if selection == "systemd-boot":
            configure_systemd_boot()
        else:
            configure_grub(self.disk)

        return None
