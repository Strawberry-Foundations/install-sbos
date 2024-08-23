from sbos_installer.core.process import run, check_root_permissions, check_uefi_capability, Runner
from sbos_installer.core.bootstrap import bootstrap
from sbos_installer.core.initramfs import setup_initramfs
from sbos_installer.core.ui.select_button import SelectButton, ia_selection
from sbos_installer.core.ui.header import Header
from sbos_installer.utils import modify_file_entry
from sbos_installer.utils.colors import *
from sbos_installer.utils.screen import *
from sbos_installer.dev import *
from sbos_installer.var import *

from sbos_installer.views.about import AboutView
from sbos_installer.views.error import ErrorView
from sbos_installer.views.warning import WarningView
from sbos_installer.views.kbd import KeyboardLayout
from sbos_installer.views.ostype import OSTypeView
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
from rich.text import Text

import sys
import time
import os


console = Console()
v = Vars()

if not check_root_permissions():
    ErrorView(error_message="The Installer requires root permissions to continue.")

if not check_uefi_capability():
    ErrorView(error_message="The StrawberryOS Installer currently only supports UEFI-capable computers")

if DEV_FLAG_DEV_MODE:
    WarningView("Developer mode is enabled!\nSome functions could possibly be skipped. Only use this if you are sure!")

try:
    runner = Runner(True)


    def _selection():
        clear_screen()

        Header("Welcome to the StrawberryOS Installer!")

        console.show_cursor(False)

        console.print(
            f"Thanks for choosing StrawberryOS!\n"
            f"The StrawberryOS Installer will guide you through the installation process.\n",
            justify="center"
        )

        console.print(
            Text.from_ansi(
                f"{GREEN}{BOLD}! {CRESET}Use UP and DOWN to navigate, ENTER to continue\n\n"
            ), justify="center"
        )

        group = []

        SelectButton(
            label=f"(->) Start installation",
            description="Start with the installation of StrawberryOS",
            group=group
        )

        SelectButton(
            label=f"(>_) Open a console",
            description="Open a console if you need to make changes beforehand. "
                        "You can start the installer again using 'setup-strawberryos'",
            group=group
        )

        SelectButton(
            label=f"(?) About StrawberryOS Installer",
            description="Learn more about the new StrawberryOS Installer (NucleusV2)",
            group=group
        )

        SelectButton(
            label=f"(!) Update StrawberryOS Installer",
            description="Check whether there is a new update for the installer",
            group=group
        )

        try:
            selection = ia_selection(
                question="",
                options=group,
                flags=["start", "console", "about", "update"]
            )
        except KeyboardInterrupt:
            console.clear()
            console.print(Text.from_ansi(
                f"-- {YELLOW}{BOLD}Exited installation process{CRESET} --"
            ), justify="center")
            console.show_cursor(True)
            sys.exit(0)

        console.show_cursor(True)

        match selection:
            case "console":
                clear_screen()

                try:
                    with open("/etc/motd", 'r') as _motd:
                        print(_motd.read(), end="")

                except (FileNotFoundError, Exception):
                    pass

                sys.exit(0)

            case "about":
                AboutView()
                clear_screen()
                _selection()

            case "update":
                run("update-installer")
                clear_screen()
                python = sys.executable
                os.execv(python, ['python3'] + sys.argv)


    _selection()

    # todo:
    #  - add StrawberryOS recovery
    #  - replace installation of custom files (e.g. /etc/motd) with binpkg

    KeyboardLayout()

    # General installation config steps
    v.os_type = OSTypeView().val  # Choose which edition of StrawberryOS you want to install
    v.hostname = HostnameView().val  # Setup hostname
    v.net_stat = NetworkView().val  # Setup network
    v.region, v.city = TimezoneView().val  # Setup timezone
    v.user_setup = UserView().val  # Setup user
    v.packages = PackageView(v.os_type).val  # Setup packages
    v.disk_data, disk = DiskView().val  # Setup disk

    install_data = {
        "hostname": v.hostname,
        "net_interface": v.net_stat,
        "timezone": {
            "region": v.region,
            "city": v.city
        },
        "packages": v.packages
    }

    install_data.update(v.user_setup)
    install_data.update(v.disk_data)

    # Show overview of installation config
    OverviewScreenView(install_data, disk)

    clear_screen()
    Header("Creating disk partitions ...")

    # Create disk partitions and mount disk
    if not v.disk_data["disk"]["custom_partitioning"]:
        configure_partitions(disk, install_data)
        time.sleep(0.5)
        configure_lvm(disk, install_data)

        run(f"mount --mkdir /dev/strawberryos/system {ROOT_MNT}")
        run(f"mount --mkdir {install_data['disk'][disk]['efi']['block']} {ROOT_MNT}boot/efi")

    else:
        run(f"mount --mkdir {install_data['disk'][disk]['system']['block']} {ROOT_MNT}")
        run(f"mount --mkdir {install_data['disk'][disk]['efi']['block']} {ROOT_MNT}boot/efi")

    if not DEV_FLAG_SKIP_BOOTSTRAP:
        clear_screen()
        Header("Installing base system ...")

        bootstrap(v.packages)
    if not DEV_FLAG_SKIP_INITRAMFS:
        clear_screen()
        Header("Installing & configuring Initramfs ...")

        setup_initramfs(install_data['disk'][disk]['user']['block'])

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
        configure_timezone_system(v.region, v.city)  # Configure timezone

        clear_screen()
        Header("Configuring users ...")
        configure_users(v.user_setup)  # Configure users

        clear_screen()
        Header("Configuring hostname ...")
        configure_hostname(v.hostname)  # Configure users

        match v.os_type:
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

        BootloaderView(disk)  # Install & configure bootloader
        if not v.os_type == "server":
            DesktopView()  # Install desktop

    # Mount userspace & copy root's .bashrc from systemspace to userspace
    run(f"mount --mkdir {install_data['disk'][disk]['user']['block']} {ROOT_MNT}user")
    run(f"mkdir -p {ROOT_MNT}user/data/root")
    run(f"cp {ROOT_MNT}/root/.bashrc {ROOT_MNT}user/data/root")

    # Modify root's userspace PS1 variable
    with open(f"{ROOT_MNT}user/data/root/.bashrc", "a") as _file:
        _file.write(
            r"PS1='\[\e[0m\][\[\e[0;1;91m\]\u\[\e[0;1;38;5;226m\]@\[\e[0;1;96m\]\H \[\e[0;1;38;5;161m\]\w\[\e[0m\]] \[\e[0;1m\]\$ \[\e[0m\]'"
        )
        _file.write("\n")

    # Modify root's systemspace PS1 variable
    with open(f"{ROOT_MNT}root/.bashrc", "a") as _file:
        _file.write(
            r"PS1='\[\e[92;1m\][ System ] \[\e[91m\]\u\[\e[93m\]@\[\e[91m\]\H\[\e[0m\] \[\e[96;1m\]\w\[\e[0m\] \[\e[2m\]\$\[\e[0m\] '"
        )
        _file.write("\n")

    # Add custom /etc/issue
    with open(f"{ROOT_MNT}etc/issue", 'w') as file:
        file.write(r"StrawberryOS Chocolate Crisps \n \l"
                   "\n\n"
                   r"")

    # Add custom /etc/motd
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
    console.clear()
    console.print(Text.from_ansi(
        f"-- {YELLOW}{BOLD}Exited installation process{CRESET} --"
    ), justify="center")
    console.show_cursor(True)
    sys
