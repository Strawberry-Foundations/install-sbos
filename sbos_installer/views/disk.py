from sbos_installer import DEV_FLAG_SKIP_DISK_INPUT
from sbos_installer.cli.selection import ia_selection
from sbos_installer.cli.parser import parse_bool
from sbos_installer.core.ui.screen import Screen
from sbos_installer.steps.disk import get_block_device_size_in_gb, get_block_devices
from sbos_installer.utils.colors import *

from rich.text import Text
from rich.padding import Padding
from getpass import getpass


class DiskView(Screen):
    title = "Disk partitioning"

    def __init__(self):
        view = self.render
        super().__init__(title=self.title, view=view)

    def render(self):
        if DEV_FLAG_SKIP_DISK_INPUT:
            efi_disk = "/dev/sda1"
            system_disk = "/dev/strawberryos/system"
            user_disk = "/dev/strawberryos/user"
            swap_disk = "/dev/sda2"

            return {
                "disk": {
                    "custom_partitioning": False,
                    "/dev/sda": {
                        "efi": {
                            "block": efi_disk,
                            "size": get_block_device_size_in_gb(efi_disk)
                        },
                        "system": {
                            "block": system_disk,
                            "size": get_block_device_size_in_gb(system_disk)
                        },
                        "user": {
                            "block": user_disk,
                            "size": get_block_device_size_in_gb(user_disk)
                        },
                        "swap": {
                            "block": swap_disk,
                            "size": get_block_device_size_in_gb(swap_disk)
                        }
                    }
                }
            }, "/dev/sda"

        self.console.print(Padding(
            "Select a hard disk that you would like to use for the installation of StrawberryOS. "
            "Note that the hard disk will be completely erased during the installation.\n",
            (0, 8))
        )

        block, block_size, all_blocks = get_block_devices()

        disk = ia_selection(
            question="",
            options=block,
            flags=block_size,
            padding=8
        )

        print(CRESET)

        return ""
