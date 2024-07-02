from sbos_installer.cli.selection import ia_selection
from sbos_installer.cli.parser import parse_bool
from sbos_installer.utils.colors import *
from sbos_installer.dev import DEV_FLAG_SKIP_DISK_INPUT
from sbos_installer.steps.lvm import get_partition_suffix
from sbos_installer.core.process import Runner

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

    print(f"\n{GREEN}{BOLD} -- Disk partitioning --{CRESET}")
    block, block_size, all_blocks = get_block_devices()

    disk = ia_selection("Select the disk you want to use for Strawberry OS", options=block, flags=block_size)

    guided_disk_setup = parse_bool(ia_selection(
        question=f"\nUse guided LVM disk setup?",
        options=["Yes", "No"],
        flags=[
            f"{GRAY}({GREEN}Recommended{CRESET}{GRAY}){CRESET}",
            f"{GRAY}({YELLOW}Only for experts{CRESET}{GRAY}){CRESET}"
        ]
    ))

    if guided_disk_setup:
        suffix = get_partition_suffix(disk)

        disk_size = float(str(all_blocks[disk]["size"]).strip("G").replace(",", "."))

        efi_disk_size = 0.512
        system_disk_size = 10
        swap_disk_size = 4
        user_disk_size = disk_size - efi_disk_size - system_disk_size - swap_disk_size

        confirm_partitioning = parse_bool(ia_selection(
            question=f"\nContinue with the following partitioning:\n"
                     f"   {GREEN}{BOLD}EFI on {CYAN}{disk}{suffix}1:{CRESET} {efi_disk_size}G\n"
                     f"   {GREEN}{BOLD}Swap on {CYAN}{disk}{suffix}2:{CRESET} {swap_disk_size}G"
                     f"   {GREEN}{BOLD}System on {CYAN}/dev/strawberryos/system:{CRESET} {system_disk_size.__round__()}G\n"
                     f"   {GREEN}{BOLD}User on {CYAN}/dev/strawberryos/user:{CRESET} {user_disk_size.__round__()}G\n",
            options=["Yes", "No"]
        ))

        if not confirm_partitioning:
            disk_partitioning()

        wipe_disk = parse_bool(ia_selection(
            question=f"\nErase your hard disk before continuing? [{disk}] (Required if data is still present)",
            options=["Yes", "No"],
            flags=[f"{GRAY}({YELLOW}{BOLD}ALL DATA WILL BE DELETED!{CRESET}{GRAY}){CRESET}", ""]
        ))

        if wipe_disk:
            runner = Runner(True)
            runner.run(f"dd if=/dev/zero of={disk} bs=512 count=1")

        return {
            "disk": {
                "custom_partitioning": False,
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
        existing_partition = parse_bool(ia_selection(
            question=f"\nDoes your disk already have a partitioning scheme that is suitable for StrawberryOS?\n"
                     f"A suitable partitioning scheme should look like this:\n"
                     f"EFI disk on {CYAN}{BOLD}/dev/sdxX{CRESET} ({GREEN}{BOLD}FAT32{CRESET})\n"
                     f"Swap disk on {CYAN}{BOLD}/dev/sdxX{CRESET} ({GREEN}{BOLD}Linux swap{CRESET})\n"
                     f"System disk on {CYAN}{BOLD}/dev/lvmgroup/system{CRESET} ({GREEN}{BOLD}ext4/btrfs{CRESET})\n"
                     f"User disk on {CYAN}{BOLD}/dev/lvmgroup/user{CRESET} ({GREEN}{BOLD}ext4/btrfs{CRESET})\n",
            options=["Yes", "No"]
        ))

        if existing_partition:
            print("Please enter the following partitions with the correct block device to continue the partitioning\n")

            efi_disk = input(f"EFI disk (e.g. {CYAN}/dev/sda1{CRESET}): ")
            swap_disk = input(f"Swap disk (e.g. {CYAN}/dev/sda2{CRESET}): ")
            system_disk = input(f"System disk (e.g. {CYAN}/dev/strawberryos/system{CRESET}): ")
            user_disk = input(f"User disk (e.g. {CYAN}/dev/strawberryos/user{CRESET}): ")

            return {
                "disk": {
                    "custom_partitioning": True,
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
            print(f"{YELLOW}{BOLD}Custom disk setup for non-suitable disks is currently not supported.{CRESET}")
            disk_partitioning()
