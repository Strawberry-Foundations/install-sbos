from sbos_installer.core.process import Runner
from sbos_installer.steps.lvm import get_partition_suffix
from sbos_installer.cli.selection import ia_selection
from sbos_installer.cli.parser import parse_bool
from sbos_installer.cli.input import parse_size
from sbos_installer.utils.colors import *
from sbos_installer.dev import DEV_FLAG_SKIP_DISK_INPUT
from sbos_installer.var import Setup

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


def configure_partitions(setup: Setup):
    disk_data = setup.disk_data[setup.disk]

    efi_disk_size = disk_data["efi"]["size"] + 1
    swap_disk_size = disk_data["swap"]["size"] + efi_disk_size

    runner = Runner(True)

    print(f"\n{GREEN}{BOLD}Creating partitions ...{CRESET}")
    runner.run(f"parted -s {setup.disk} mklabel gpt")
    runner.run(f"parted -s -a optimal {setup.disk} mkpart primary fat32 1MiB {efi_disk_size}MiB")
    runner.run(f"parted -s -a optimal {setup.disk} mkpart primary linux-swap {efi_disk_size}MiB {swap_disk_size}MiB")
    runner.run(f"parted -s -a optimal {setup.disk} mkpart primary {swap_disk_size}MiB 100%")
    runner.run(f"sync")
