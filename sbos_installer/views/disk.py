from sbos_installer.core.ui.screen import Screen
from sbos_installer.core.ui.single_select_button import SingleSelectButton, ia_selection as ssb_ia_selection
from sbos_installer.core.process import Runner
from sbos_installer.cli.selection import ia_selection
from sbos_installer.cli.parser import parse_bool
from sbos_installer.cli.input import parse_size
from sbos_installer.steps.disk import get_block_device_size_in_gb, get_block_devices
from sbos_installer.steps.lvm import get_partition_suffix
from sbos_installer.utils.colors import *
from sbos_installer.dev import DEV_FLAG_SKIP_DISK_INPUT

from rich.text import Text
from rich.padding import Padding

import time


class DiskView(Screen):
    title = "Disk partitioning"

    def __init__(self):
        view = self.render
        super().__init__(title=self.title, view=view)

    def finalize(self, disk, suffix, efi_disk_size, system_disk_size, user_disk_size, swap_disk_size, file_system):
        print()
        continue_installation = parse_bool(ia_selection(
            question=f"Continue installation? (Deletes all data on the selected disk)",
            options=["Yes", "No"],
            padding=8
        ))

        if continue_installation:
            print()
            wipe_disk = parse_bool(ia_selection(
                question=f"Completely erase your hard disk before continuing? [{disk}] (Required if data is still present)",
                options=["Yes", "No"],
                flags=[f"{GRAY}({YELLOW}{BOLD}ALL DATA WILL BE DELETED!{CRESET}{GRAY}){CRESET}", ""],
                padding=8
            ))

            if wipe_disk:
                runner = Runner(True)
                runner.run(f"dd if=/dev/zero of={disk} bs=512 count=1")
                time.sleep(0.5)

                return {
                    "disk": {
                        "custom_partitioning": False,
                        "file_system": file_system,
                        disk: {
                            "efi": {
                                "block": f"{disk}{suffix}1",
                                "size": efi_disk_size
                            },
                            "system": {
                                "block": "/dev/strawberryos/system",
                                "size": system_disk_size
                            },
                            "user": {
                                "block": "/dev/strawberryos/user",
                                "size": user_disk_size
                            },
                            "swap": {
                                "block": f"{disk}{suffix}2",
                                "size": swap_disk_size
                            }
                        }
                    }
                }, disk

            else:
                self.render()

        else:
            self.render()

    def modify_disk_setup(self, disk, suffix, efi_disk_size, system_disk_size, user_disk_size, swap_disk_size):
        file_system = "btrfs"
        while True:
            print()
            modify_partition = ia_selection(
                question=f"Select an action that you would like to perform",
                options=["Change EFI size", "Change Swap size", "Change System size", "Change file system", "-> Done"],
                flags=[f"({disk}{suffix}1)", f"({disk}{suffix}2)", "(/dev/strawberryos/system)"],
                padding=8
            )
            print()

            match modify_partition:
                case "Change EFI size":
                    while True:
                        _size = parse_size(
                            input(f"        Input new EFI disk ({CYAN}{BOLD}{disk}{suffix}1{CRESET}) size: "))
                        if _size:
                            efi_disk_size = _size
                            break
                    self.console.print(Padding(Text.from_ansi(
                        f"EFI disk size is now {GREEN}{BOLD}{_size / 1024}G{CRESET} ({GREEN}{BOLD}{_size}M{CRESET})"
                    ), (0, 8)))
                    continue

                case "Change Swap size":
                    while True:
                        _size = parse_size(
                            input(f"        Input new Swap disk ({CYAN}{BOLD}{disk}{suffix}2{CRESET}) size: "))
                        if _size:
                            swap_disk_size = _size
                            break
                    self.console.print(Padding(Text.from_ansi(
                        f"Swap disk size is now {GREEN}{BOLD}{_size / 1024}G{CRESET} ({GREEN}{BOLD}{_size}M{CRESET})"
                    ), (0, 8)))
                    continue

                case "Change System size":
                    while True:
                        _size = parse_size(
                            input(f"        Input new System disk ({CYAN}{BOLD}/dev/strawberryos/system{CRESET}) size: "))
                        if _size:
                            system_disk_size = _size
                            break
                    self.console.print(Padding(Text.from_ansi(
                        f"System disk size is now {GREEN}{BOLD}{_size / 1024}G{CRESET} ({GREEN}{BOLD}{_size}M{CRESET})"
                    ), (0, 8)))
                    continue

                case "Change file system":
                    group = []

                    SingleSelectButton(
                        label="BTRFS",
                        group=group
                    )

                    SingleSelectButton(
                        label="EXT4",
                        group=group
                    )

                    self.console.print(Padding(Text.from_ansi(
                        f"StrawberryOS uses the BTRFS file system by default. "
                        f"However, if you want to use EXT4 for whatever reason, you can change this here"
                    ), (0, 8)))

                    file_system = ssb_ia_selection(
                        question="",
                        options=group,
                        flags=["btrfs", "ext4"]
                    )
                    continue

                case "-> Done":
                    self.console.print(Padding(Text.from_ansi(
                        f"\nModified partition scheme for StrawberryOS\n"
                        f"   {GREEN}{BOLD}EFI on {CYAN}{disk}{suffix}1:{CRESET} {efi_disk_size / 1024}G ({efi_disk_size}M)\n"
                        f"   {GREEN}{BOLD}Swap on {CYAN}{disk}{suffix}2:{CRESET} {swap_disk_size / 1024}G ({swap_disk_size}M)\n"
                        f"   {GREEN}{BOLD}System ({file_system}) on {CYAN}/dev/strawberryos/system:{CRESET} {system_disk_size / 1024}G ({system_disk_size}M)\n"
                        f"   {GREEN}{BOLD}User ({file_system}) on {CYAN}/dev/strawberryos/user:{CRESET} {user_disk_size / 1024}G ({user_disk_size}M)"
                    ), (0, 8)))

            return self.finalize(
                disk=disk,
                suffix=suffix,
                efi_disk_size=efi_disk_size,
                system_disk_size=system_disk_size,
                user_disk_size=user_disk_size,
                swap_disk_size=swap_disk_size,
                file_system=file_system
            )

    def render(self):
        file_system = "btrfs"

        if DEV_FLAG_SKIP_DISK_INPUT:
            efi_disk = "/dev/sda1"
            system_disk = "/dev/strawberryos/system"
            user_disk = "/dev/strawberryos/user"
            swap_disk = "/dev/sda2"

            return {
                "disk": {
                    "custom_partitioning": False,
                    "file_system": file_system,
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
            "Note that the hard disk will be completely erased during the installation.",
            (0, 8))
        )

        block, block_size, all_blocks = get_block_devices()

        disk = ia_selection(
            question="",
            options=block,
            flags=block_size,
            padding=8
        )

        print()
        guided_disk_setup = parse_bool(ia_selection(
            question=f"Use guided LVM disk setup?",
            options=["Yes", "No"],
            flags=[
                f"{GRAY}({GREEN}Recommended{CRESET}{GRAY}){CRESET}",
                f"{GRAY}({YELLOW}Only for experts{CRESET}{GRAY}){CRESET}"
            ],
            padding=8
        ))

        if guided_disk_setup:
            suffix = get_partition_suffix(disk)

            disk_size_gb = float(str(all_blocks[disk]["size"]).strip("G").replace(",", "."))
            disk_size_mb = int(disk_size_gb * 1024)

            efi_disk_size = 512
            system_disk_size = 10240
            swap_disk_size = 2048
            user_disk_size = disk_size_mb - efi_disk_size - system_disk_size - swap_disk_size

            self.console.print(Padding(Text.from_ansi(
                f"\nPartition scheme for StrawberryOS\n"
                f"   {GREEN}{BOLD}EFI on {CYAN}{disk}{suffix}1:{CRESET} {efi_disk_size / 1024}G ({efi_disk_size}M)\n"
                f"   {GREEN}{BOLD}Swap on {CYAN}{disk}{suffix}2:{CRESET} {swap_disk_size / 1024}G ({swap_disk_size}M)\n"
                f"   {GREEN}{BOLD}System ({file_system}) on {CYAN}/dev/strawberryos/system:{CRESET} {system_disk_size / 1024}G ({system_disk_size}M)\n"
                f"   {GREEN}{BOLD}User ({file_system}) on {CYAN}/dev/strawberryos/user:{CRESET} {user_disk_size / 1024}G ({user_disk_size}M)"),
                (0, 8)
            ))

            print()
            modify_disk_setup = parse_bool(ia_selection(
                question=f"Modify partition scheme? (Size, file system, ..)",
                options=["No", "Yes"],
                padding=8
            ))

            print(CRESET, end="")

            if modify_disk_setup:
                return self.modify_disk_setup(disk, suffix, efi_disk_size, system_disk_size, user_disk_size, swap_disk_size)
            else:
                return self.finalize(
                    disk=disk,
                    suffix=suffix,
                    efi_disk_size=efi_disk_size,
                    system_disk_size=system_disk_size,
                    user_disk_size=user_disk_size,
                    swap_disk_size=swap_disk_size,
                    file_system=file_system
                )

        else:
            print()
            existing_partition = parse_bool(ia_selection(
                question=f"Does your disk already have a partitioning scheme that is suitable for StrawberryOS?\n"
                         f"        A suitable partitioning scheme should look like this:\n"
                         f"           EFI disk on {CYAN}{BOLD}/dev/sdxX{CRESET} ({GREEN}{BOLD}FAT32{CRESET})\n"
                         f"           Swap disk on {CYAN}{BOLD}/dev/sdxX{CRESET} ({GREEN}{BOLD}Linux swap{CRESET})\n"
                         f"           System disk on {CYAN}{BOLD}/dev/lvmgroup/system{CRESET} ({GREEN}{BOLD}ext4/btrfs{CRESET})\n"
                         f"           User disk on {CYAN}{BOLD}/dev/lvmgroup/user{CRESET} ({GREEN}{BOLD}ext4/btrfs{CRESET})",
                options=["Yes", "No"],
                padding=8
            ))

            if existing_partition:
                self.console.print(Padding(Text.from_ansi(
                    "Please enter the following partitions with the correct block device to continue the partitioning\n"),
                    (0, 8)
                ))

                efi_disk = input(f"        EFI disk (e.g. {CYAN}/dev/sda1{CRESET}):  ")
                swap_disk = input(f"        Swap disk (e.g. {CYAN}/dev/sda2{CRESET}):  ")
                system_disk = input(f"        System disk (e.g. {CYAN}/dev/strawberryos/system{CRESET}):  ")
                user_disk = input(f"        User disk (e.g. {CYAN}/dev/strawberryos/user{CRESET}):  ")

                print(CRESET, end="")

                return {
                    "disk": {
                        "custom_partitioning": True,
                        "file_system": file_system,
                        disk: {
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
                }, disk

            else:
                self.console.print(Padding(Text.from_ansi(
                    f"{YELLOW}{BOLD}Custom disk setup for non-suitable disks is currently not supported.{CRESET}"),
                    (0, 8)
                ))
                time.sleep(3)
                self.redraw()
