from sbos_installer.core.process import Runner
from sbos_installer.utils.colors import *


def get_partition_suffix(device):
    if any(device_type in device for device_type in ('nvme', 'mmcblk', 'nbd')):
        return "p"
    else:
        return ""


def configure_lvm(disk, disk_data):
    runner = Runner(True)
    suffix = get_partition_suffix(disk)
    disk_data = disk_data['disk'][disk]

    print(f"\n{GREEN}{BOLD}Formatting base partitions ...{CRESET}")
    runner.run(f"mkfs.fat -F 32 {disk}{suffix}1")
    runner.run(f"mkswap {disk}{suffix}2")

    print(f"\n{GREEN}{BOLD}Creating LVM group ...{CRESET}")
    runner.run(f"pvcreate {disk}{suffix}3 -ff -y ")
    runner.run(f"vgcreate strawberryos {disk}{suffix}3")
    runner.run(f"lvcreate -L {disk_data['system']['size']}M -n system strawberryos")
    runner.run(f"lvcreate -l 100%FREE -n user strawberryos")

    print(f"\n{GREEN}{BOLD}Formatting LVM volumes ...{CRESET}")
    runner.run(f"mkfs.ext4 /dev/strawberryos/system")
    runner.run(f"mkfs.ext4 /dev/strawberryos/user")

    print(f"\n{GREEN}{BOLD}Finished LVM configuration{CRESET}")