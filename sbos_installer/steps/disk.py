from sbos_installer.cli.selection import ia_selection
from sbos_installer.cli.parser import parse_bool
from sbos_installer.utils.colors import *
from sbos_installer.dev import DEV_FLAG_SKIP_DISK_INPUT

import subprocess
import os


def get_block_devices():
    block = []
    block_size = []
    all_blocks = {}

    lsblk_output = subprocess.check_output(["lsblk", "-o", "NAME,SIZE,TYPE", "-n", "-l", "-e", "7"]).decode("utf-8")

    for line in lsblk_output.splitlines():
        columns = line.split()

        if len(columns) >= 3:
            name = columns[0]
            size = columns[1]
            device_type = columns[2]

            if device_type == "disk":
                block.append(f"/dev/{name}")
                block_size.append(f"({size})")

                all_blocks.update({f"/dev/{name}": {"size": size, "type": device_type}})

    return block, block_size, all_blocks


def get_block_device_size_in_gb(device_path):
    if not os.path.exists(device_path):
        raise FileNotFoundError(f"The device {device_path} does not exist.")

    try:
        with open(device_path, 'rb') as device:
            device.seek(0, os.SEEK_END)
            size = device.tell()
            size_gb = size / (1024 ** 3)
            return size_gb
    except Exception as e:
        raise RuntimeError(f"Failed to get the size of the device {device_path}. Error: {e}")


def disk_partitioning():
    print(f"\n{GREEN}{BOLD} -- Disk partitioning --{CRESET}")
    block, block_size, all_blocks = get_block_devices()

    disk = ia_selection("Select the disk you want to use for Strawberry OS", options=block, flags=block_size)

    if DEV_FLAG_SKIP_DISK_INPUT:
        efi_disk = "/dev/sda1"
        system_disk = "/dev/sda2"
        user_disk = "/dev/sda4"
        swap_disk = "/dev/sda3"

        return {
            "disk": {
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

    own_partitioning = ia_selection(
        question=f"\nWould you like to create your own partitioning for {disk}?",
        options=["No", "Yes"],
        flags=["", "(Only for experts)"]
    )

    if not parse_bool(own_partitioning):
        disk_size = float(str(all_blocks[disk]["size"]).strip("G").replace(",", "."))

        efi_disk_size = 0.512
        system_disk_size = disk_size * 10 / 100
        swap_disk_size = 4
        user_disk_size = disk_size - efi_disk_size - system_disk_size - swap_disk_size

        confirm_partitioning = ia_selection(
            question=f"\nContinue with the following partitioning:\n"
                     f"   {GREEN}{BOLD}EFI:{CRESET} {efi_disk_size}G\n"
                     f"   {GREEN}{BOLD}System:{CRESET} {system_disk_size.__round__()}G\n"
                     f"   {GREEN}{BOLD}User:{CRESET} {user_disk_size.__round__()}G\n"
                     f"   {GREEN}{BOLD}Swap:{CRESET} {swap_disk_size}G",
            options=["Yes", "No"]
        )

        if not confirm_partitioning:
            disk_partitioning()

        return {
            "disk": {
                disk: {
                    "efi": {
                        "block": None,
                        "size": efi_disk_size
                    },
                    "system": {
                        "block": None,
                        "size": system_disk_size
                    },
                    "user": {
                        "block": None,
                        "size": user_disk_size
                    },
                    "swap": {
                        "block": None,
                        "size": swap_disk_size
                    }
                }
            }
        }, disk

    else:
        existing_partition = ia_selection(
            question=f"\nDoes your hard disk already have a partitioning scheme that is suitable for StrawberryOS?",
            options=["Yes", "No"]
        )

        if existing_partition:
            print("Please enter the following partitions with the correct block device to continue the partitioning.\n")

            efi_disk = input(f"EFI disk (e.g. {CYAN}/dev/sda1{CRESET}): ")
            system_disk = input(f"System disk (e.g. {CYAN}/dev/sda2{CRESET}): ")
            user_disk = input(f"User disk (e.g. {CYAN}/dev/sda3{CRESET}): ")
            swap_disk = input(f"Swap disk (e.g. {CYAN}/dev/sda4{CRESET}): ")

            return {
                "disk": {
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
            print("not supported")
            disk_partitioning()
