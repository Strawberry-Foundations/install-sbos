from sbos_installer.core.process import Runner
from sbos_installer.utils.colors import *


def get_partition_suffix(device):
    if "nvme" in device:
        return "p"
    return ""


def configure_lvm(device):
    suffix = get_partition_suffix(device)
    runner = Runner(True)

    print(f"\n{GREEN}{BOLD}Creating partitions ...{CRESET}")
    runner.run(f"parted -s {device} mklabel gpt")
    runner.run(f"parted -s -a optimal {device} mkpart primary fat32 1MiB 513MiB")
    runner.run(f"parted -s -a optimal {device} mkpart primary linux-swap 513MiB 2561MiB")
    runner.run(f"parted -s -a optimal {device} mkpart primary 2561MiB 100%")

    print(f"\n{GREEN}{BOLD}Formatting base partitions ...{CRESET}")
    runner.run(f"mkfs.fat -F 32 /dev/{device}{suffix}1")
    runner.run(f"mkswap /dev/{device}{suffix}2")

    print(f"\n{GREEN}{BOLD}Creating LVM group ...{CRESET}")
    runner.run(f"pvcreate {device}{suffix}3")
    runner.run(f"vgcreate strawberryos {device}{suffix}3")
    runner.run(f"lvcreate -L 10G -n system strawberryos")
    runner.run(f"lvcreate -l 100%FREE -n user strawberryos")

    print(f"\n{GREEN}{BOLD}Formatting LVM volumes ...{CRESET}")
    runner.run(f"mkfs.ext4 /dev/strawberryos/system")
    runner.run(f"mkfs.ext4 /dev/strawberryos/user")

    print(f"\n{GREEN}{BOLD}Finished LVM configuration{CRESET}")