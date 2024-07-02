from sbos_installer.core.process import Runner, run
from sbos_installer.utils.colors import *

import time


def get_partition_suffix(device):
    if "nvme" in device or "mmcblk" in device:
        return "p"
    return ""


def configure_lvm(device):
    runner = Runner(True)
    suffix = get_partition_suffix(device)

    print(f"\n{GREEN}{BOLD}Creating partitions ...{CRESET}")
    runner.run(f"parted -s {device} mklabel gpt")
    runner.run(f"parted -s -a optimal {device} mkpart primary fat32 1MiB 513MiB")
    runner.run(f"parted -s -a optimal {device} mkpart primary linux-swap 513MiB 2561MiB")
    runner.run(f"parted -s -a optimal {device} mkpart primary 2561MiB 100%")

    runner.run(f"sync")
    time.sleep(0.5)

    print(f"\n{GREEN}{BOLD}Formatting base partitions ...{CRESET}")
    runner.run(f"mkfs.fat -F 32 {device}{suffix}1")
    runner.run(f"mkswap {device}{suffix}2")

    print(f"\n{GREEN}{BOLD}Creating LVM group ...{CRESET}")
    runner.run(f"pvcreate {device}{suffix}3 -ff -y ")
    runner.run(f"vgcreate strawberryos {device}{suffix}3")
    runner.run(f"lvcreate -L 10G -n system strawberryos")
    runner.run(f"lvcreate -l 100%FREE -n user strawberryos")

    print(f"\n{GREEN}{BOLD}Formatting LVM volumes ...{CRESET}")
    runner.run(f"mkfs.ext4 /dev/strawberryos/system")
    runner.run(f"mkfs.ext4 /dev/strawberryos/user")

    print(f"\n{GREEN}{BOLD}Finished LVM configuration{CRESET}")