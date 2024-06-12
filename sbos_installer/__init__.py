from sbos_installer.core.process import run, check_root_permissions, Runner
from sbos_installer.core.bootstrap import bootstrap
from sbos_installer.core.initramfs import setup_initramfs
from sbos_installer.cli.selection import ia_selection
from sbos_installer.utils.colors import *
from sbos_installer.dev import DEV_FLAG_SKIP_BOOTSTRAP, DEV_FLAG_SKIP_INITRAMFS, DEV_FLAG_SKIP_POST_SETUP

from sbos_installer.steps.disk import disk_partitioning
from sbos_installer.steps.hostname import setup_hostname
from sbos_installer.steps.network import setup_network
from sbos_installer.steps.locale import setup_timezone, configure_timezone_system
from sbos_installer.steps.user import setup_user, configure_users
from sbos_installer.steps.package import setup_packages
from sbos_installer.steps.overview import overview
from sbos_installer.steps.bootloader import configure_bootloader
from sbos_installer.steps.general import configure_desktop

import sys

version = "1.0.4"

if not check_root_permissions():
    print(f"{BOLD}{RED}Requires root permissions{CRESET}")
    sys.exit(1)

print(f"{GREEN}{BOLD}Welcome to StrawberryOS Installer v{version}!\n{CRESET}Thanks for installing StrawberryOS on "
      f"your computer.\n")

print(f"{YELLOW}{BOLD}Warning: The installer does not currently support BIOS/legacy systems.{CRESET}")
print(f"{YELLOW}{BOLD}Warning: The installer does not currently support automatic disk partitioning.{CRESET}\n")

try:
    runner = Runner(False)
    location = "/mnt"

    input("Press Enter to continue the installation ... \n")

    """
    -- Required Steps
    * Hostname
    * Network setup
    * Timezone setup
    * User setup (root password, additional user ...) (todo: add groups, login shell)
    * Disk setup
    * Package selection (base, base-dev, python3, utils, ...)
    * Bootloader
    * Additional steps (graphical user interface)
    """

    hostname = setup_hostname()  # Setup hostname
    net_stat = setup_network()  # Setup network
    region, city = setup_timezone()  # Setup timezone
    user_setup = setup_user()  # Setup user
    disk_data, disk = disk_partitioning()  # Setup disk
    packages = setup_packages()  # Setup packages

    install_data = {
        "hostname": hostname,
        "net_interface": net_stat,
        "timezone": {
            "region": region,
            "city": city
        },
        "packages": packages
    }

    install_data.update(user_setup)
    install_data.update(disk_data)

    overview(install_data, disk)

    run(f"mount --mkdir {install_data['disk'][disk]['system']['block']} /mnt")
    run(f"mount --mkdir {install_data['disk'][disk]['efi']['block']} /mnt/boot/efi")

    if not DEV_FLAG_SKIP_BOOTSTRAP:
        bootstrap(packages)
    if not DEV_FLAG_SKIP_INITRAMFS:
        setup_initramfs(install_data['disk'][disk]['user']['block'])

    print(f"\n -- {GREEN}{BOLD} StrawberryOS base installation completed --{CRESET}")
    print(f"{CYAN}{BOLD} Starting post-installation ... {CRESET}\n")

    runner.run(f"mount --bind /dev {location}/dev")
    runner.run(f"mount --bind /sys {location}/sys")
    runner.run(f"mount --bind /proc {location}/proc")

    if not DEV_FLAG_SKIP_POST_SETUP:
        configure_timezone_system(region, city)  # Configure timezone
        configure_users(user_setup)  # Configure users
        configure_bootloader(disk)  # Install & configure bootloader
        configure_desktop()  # Install desktop

    runner.run("chroot /mnt somgr update")  # Update StrawberryOS and lock system

    with open("/mnt/root/.bashrc", "a") as _file:
        _file.write(r"PS1='\[\e[92;1m\][ System ] \[\e[91m\]\u\[\e[93m\]@\[\e[91m\]\H\[\e[0m\] \[\e[96;1m\]\w\[\e[0m\] \[\e[2m\]\$\[\e[0m\] '")

    runner.run(f"cp /etc/os-release /mnt/etc/os-release")

    runner.run(f"umount {location}/dev")
    runner.run(f"umount {location}/sys")
    runner.run(f"umount {location}/proc")


    print(f"\n -- {GREEN}{BOLD} StrawberryOS post installation completed --{CRESET}")

except KeyboardInterrupt:
    print(f"\n{YELLOW}Exited installation process{CRESET}")
