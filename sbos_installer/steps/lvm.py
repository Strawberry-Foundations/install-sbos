from sbos_installer.core.process import Runner
from sbos_installer.utils.colors import *
from sbos_installer.views.error import ErrorView


def get_partition_suffix(device):
    if any(device_type in device for device_type in ('nvme', 'mmcblk', 'nbd')):
        return "p"
    else:
        return ""


def configure_lvm(disk, disk_data):
    runner = Runner(True)
    suffix = get_partition_suffix(disk)
    file_system = disk_data["disk"]["file_system"]
    disk_data = disk_data["disk"][disk]

    print(f"\n{GREEN}{BOLD}Formatting base partitions ...{CRESET}")
    runner.run(f"mkfs.fat -F 32 {disk}{suffix}1")
    runner.run(f"mkswap {disk}{suffix}2")

    print(f"\n{GREEN}{BOLD}Creating LVM group ...{CRESET}")
    runner.run(f"pvcreate {disk}{suffix}3 -ff -y ")
    runner.run(f"vgcreate strawberryos {disk}{suffix}3")
    runner.run(f"lvcreate -L {disk_data['system']['size']}M -n system strawberryos")
    runner.run(f"lvcreate -l 100%FREE -n user strawberryos")

    print(f"\n{GREEN}{BOLD}Formatting LVM volumes ({file_system}) ...{CRESET}")

    match file_system:
        case "btrfs":
            runner.run(f"mkfs.btrfs /dev/strawberryos/system")
            runner.run(f"mkfs.btrfs /dev/strawberryos/user")
        case "ext4":
            runner.run(f"mkfs.ext4 /dev/strawberryos/system")
            runner.run(f"mkfs.ext4 /dev/strawberryos/user")
        case _:
            ErrorView(error_message="Invalid file system")

    print(f"\n{GREEN}{BOLD}Finished LVM configuration{CRESET}")
