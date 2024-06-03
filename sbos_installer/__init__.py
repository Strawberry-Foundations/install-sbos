from sbos_installer.core.process import run, check_root_permissions
from sbos_installer.core.bootstrap import bootstrap
from sbos_installer.core.initramfs import setup_initramfs
from sbos_installer.cli.selection import ia_selection
from sbos_installer.utils.colors import *

from sbos_installer.steps.disk import disk_partitioning
from sbos_installer.steps.hostname import setup_hostname
from sbos_installer.steps.network import setup_network
from sbos_installer.steps.locale import setup_timezone
from sbos_installer.steps.user import setup_user
from sbos_installer.steps.package import setup_packages
from sbos_installer.steps.overview import overview
from sbos_installer.dev import DEV_FLAG_SKIP_BOOTSTRAP, DEV_FLAG_SKIP_INITRAMFS

import sys

version = "0.2.1"

if not check_root_permissions():
    print(f"{BOLD}{RED}Requires root permissions{CRESET}")
    sys.exit(1)

print(f"{GREEN}{BOLD}Welcome to StrawberryOS Installer v{version}!\n{CRESET}Thanks for installing StrawberryOS on "
      f"your computer.\n")

print(f"{YELLOW}{BOLD}Warning: The installer does currently not support BIOS/Legacy systems.{CRESET}\n")

try:
    input("Press Enter to continue the installation ... \n")

    """
    -- Required Steps
    * Hostname
    * Network setup
    * Timezone setup
    * User setup (root password, additional user ...) (todo: add groups, login shell)
    * Disk setup
    * Package selection (base, base-dev, python3, utils, ...)
    * (Bootloader)
    * Additional steps (graphical user interface)
    """

    hostname = setup_hostname()             # Setup hostname
    net_stat = setup_network()              # Setup network
    region, city = setup_timezone()         # Setup timezone
    user_setup = setup_user()               # Setup user
    disk_data, disk = disk_partitioning()   # Setup disk
    packages = setup_packages()             # Setup packages
    # ... bootloader
    # ... additional steps

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

    print(f" -- {GREEN}{BOLD} StrawberryOS base installation completed --{CRESET}")
    print(f"{CYAN}{BOLD} Starting post-installation ... {CRESET}")


except KeyboardInterrupt:
    print(f"\n{YELLOW}Exited installation process{CRESET}")
