from sbos_installer.core.process import run, check_root_permissions, check_uefi_capability, Runner
from sbos_installer.core.bootstrap import bootstrap
from sbos_installer.core.initramfs import setup_initramfs
from sbos_installer.core.ui.header import Header
from sbos_installer.utils.colors import *
from sbos_installer.utils.screen import *
from sbos_installer.dev import *
from sbos_installer.var import *

from sbos_installer.views.error import ErrorView
from sbos_installer.views.warning import WarningView
from sbos_installer.views.info import InfoView
from sbos_installer.views.welcome import WelcomeView
from sbos_installer.views.kbd import KeyboardLayout
from sbos_installer.views.edition import EditionView
from sbos_installer.views.hostname import HostnameView
from sbos_installer.views.network import NetworkView
from sbos_installer.views.timezone import TimezoneView
from sbos_installer.views.user import UserView
from sbos_installer.views.disk import DiskView
from sbos_installer.views.package import PackageView
from sbos_installer.views.overview import OverviewScreenView
from sbos_installer.views.bootloader import BootloaderView
from sbos_installer.views.desktop import DesktopView
from sbos_installer.views.finished import FinishView

from sbos_installer.steps.disk import configure_partitions
from sbos_installer.steps.lvm import configure_lvm
from sbos_installer.steps.hostname import configure_hostname
from sbos_installer.steps.locale import configure_timezone_system
from sbos_installer.steps.user import configure_users

from rich.console import Console

import sys
import time
import traceback


console = Console()
setup = Setup()

if not check_root_permissions():
    ErrorView("The Installer requires root permissions to continue.")

if not check_uefi_capability():
    ErrorView("The StrawberryOS Installer currently only supports UEFI-capable computers")

if DEV_FLAG_DEV_MODE:
    WarningView("Developer mode is enabled!\nSome functions could possibly be skipped. Only use this if you are sure!")

"""
# Todo:
  - Add StrawberryOS recovery
  - Add custom /etc/motd (via binpkg)
  - Replace installation of custom files (e.g. /etc/motd) with binpkg
"""

try:
    runner = Runner(True)

    WelcomeView()
    KeyboardLayout()

    # General installation config steps
    setup.edition = EditionView().val
    setup.hostname = HostnameView().val  # Setup hostname
    setup.net_interface = NetworkView().val  # Setup network
    setup.region, setup.city = TimezoneView().val  # Setup timezone
    setup.user_setup = UserView().val  # Setup user
    setup.packages = PackageView(setup.edition).val  # Setup packages
    setup.disk_data, setup.disk = DiskView().val  # Setup disk

    # Show overview of installation config
    OverviewScreenView(setup)

    clear_screen()
    Header("Creating disk partitions ...")

    # Create disk partitions and mount disk
    if not setup.disk_data["disk"]["custom_partitioning"]:
        configure_partitions(setup)
        time.sleep(0.5)
        configure_lvm(setup)

        run(f"mount --mkdir /dev/strawberryos/system {ROOT_MNT}")
        run(f"mount --mkdir {setup.disk_data[setup.disk]['efi']['block']} {ROOT_MNT}boot/efi")

    else:
        run(f"mount --mkdir {setup.disk_data[setup.disk]['system']['block']} {ROOT_MNT}")
        run(f"mount --mkdir {setup.disk_data[setup.disk]['efi']['block']} {ROOT_MNT}boot/efi")

    if not DEV_FLAG_SKIP_BOOTSTRAP:
        clear_screen()
        Header("Installing base system ...")
        bootstrap(setup.packages)
        
    if not DEV_FLAG_SKIP_INITRAMFS:
        clear_screen()
        Header("Installing & configuring Initramfs ...")
        setup_initramfs(setup.disk_data[setup.disk]['user']['block'])

    print(f"{GREEN}Finished.{CRESET}")
    time.sleep(0.85)

    clear_screen()
    Header("Post-installation")

    runner.run(f"mount --bind /dev {ROOT_MNT}dev")
    runner.run(f"mount --bind /sys {ROOT_MNT}sys")
    runner.run(f"mount --bind /proc {ROOT_MNT}proc")

    time.sleep(0.85)

    if not DEV_FLAG_SKIP_POST_SETUP or not DEV_DRY_RUN:
        clear_screen()
        Header("Configuring timezone ...")
        configure_timezone_system(setup.region, setup.city)  # Configure timezone

        clear_screen()
        Header("Configuring users ...")
        configure_users(setup.user_setup)  # Configure users

        clear_screen()
        Header("Configuring hostname ...")
        configure_hostname(setup.hostname)  # Configure users

        match setup.edition:
            case "desktop":
                os_release_version = Versions.desktop
            case "desktop_sod":
                os_release_version = Versions.desktop_sod
            case "server":
                os_release_version = Versions.server
            case _:
                os_release_version = Versions.desktop

        with open(f"{ROOT_MNT}etc/os-release", 'w') as file:
            file.write(
                f'''PRETTY_NAME="StrawberryOS {os_release_version}"
NAME="StrawberryOS"
VERSION_ID="{os_release_version}"
VERSION="{os_release_version} ({CODENAME_FULL})"
VERSION_CODENAME={CODENAME_LOWER}
ID=strawberryos
ID_LIKE=debian
HOME_URL="https://strawberryfoundations.org"
SUPPORT_URL="https://github.com/Strawberry-Foundations/sbos-live-iso"
BUG_REPORT_URL="https://github.com/Strawberry-Foundations/sbos-live-iso"
'''
            )

        BootloaderView(setup.disk)  # Install & configure bootloader
        
        if not setup.edition == "server":
            DesktopView()  # Install desktop

    # Mount userspace & copy root's .bashrc from systemspace to userspace
    run(f"mount --mkdir {setup.disk_data[setup.disk]['user']['block']} {ROOT_MNT}user")
    run(f"mkdir -p {ROOT_MNT}user/data/root")
    run(f"cp {ROOT_MNT}/root/.bashrc {ROOT_MNT}user/data/root")

    # Modify root's userspace PS1 variable
    with open(f"{ROOT_MNT}user/data/root/.bashrc", "a") as _file:
        _file.write(r"PS1='\[\e[0m\][\[\e[0;1;91m\]\u\[\e[0;1;38;5;226m\]@\[\e[0;1;96m\]\H \[\e[0;1;38;5;161m\]\w\[\e[0m\]] \[\e[0;1m\]\$ \[\e[0m\]'")
        _file.write("\n")

    # Modify root's systemspace PS1 variable
    with open(f"{ROOT_MNT}root/.bashrc", "a") as _file:
        _file.write(r"PS1='\[\e[92;1m\][ System ] \[\e[91m\]\u\[\e[93m\]@\[\e[91m\]\H\[\e[0m\] \[\e[96;1m\]\w\[\e[0m\] \[\e[2m\]\$\[\e[0m\] '")
        _file.write("\n")

    # Add custom /etc/issue
    with open(f"{ROOT_MNT}etc/issue", 'w') as file:
        file.write(r"StrawberryOS Chocolate Crisps \n \l"
                   "\n\n"
                   r"")

    # Add /etc/strawberryos_version for easier version validation
    with open(f"{ROOT_MNT}etc/strawberryos_version", 'w') as file:
        file.write(CODENAME_LOWER)

    runner.run(f"umount {ROOT_MNT}dev")
    runner.run(f"umount {ROOT_MNT}sys")
    runner.run(f"umount {ROOT_MNT}proc")

    runner.run(f"umount {ROOT_MNT}boot/efi")
    runner.run(f"umount {ROOT_MNT}user")
    runner.run(f"umount {ROOT_MNT}")

    FinishView()

except KeyboardInterrupt:
    InfoView(
        f"Exited installation process.\nYou can start the installer again using '{GRAY}setup-strawberryos{CRESET}'"
    )
    console.clear()
    console.show_cursor(True)
    sys.exit(0)

except Exception as e:
    error_trace = traceback.format_exc()
    ErrorView(
        "Something went wrong during the installation of StrawberryOS and the installation cannot continue.\n\n"
        f"{YELLOW}Error Details{CRESET}\n"
        f"Exception in sbos_installer: {e}\n\n"
        f"Full traceback:\n{error_trace}\n\n"
        f"{YELLOW}Important{CRESET}\n"
        "This is not normal behavior and should be reported to the StrawberryOS team.\nTry updating the installer to the latest version.\n"
        "If the issue persists, please report it to the developers.\n\n"
        "Please provide the error details above and the output of the installer to the developers.\n"
        f"{LIGHT_BLUE}https://github.com/Strawberry-Foundations/install-sbos{CRESET}"
    )