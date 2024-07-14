from sbos_installer.core.process import run, check_root_permissions, check_uefi_capability, Runner
from sbos_installer.core.bootstrap import bootstrap
from sbos_installer.core.initramfs import setup_initramfs
from sbos_installer.core.ui.select_button import SelectButton, ia_selection
from sbos_installer.core.ui.header import Header
from sbos_installer.utils.colors import *
from sbos_installer.utils.screen import *
from sbos_installer.dev import *

from sbos_installer.views.about import AboutView
from sbos_installer.views.error import ErrorView
from sbos_installer.views.warning import WarningView
from sbos_installer.views.ostype import OSTypeView
from sbos_installer.views.hostname import HostnameView
from sbos_installer.views.network import NetworkView
from sbos_installer.views.timezone import TimezoneView
from sbos_installer.views.user import UserView
from sbos_installer.views.disk import DiskView
from sbos_installer.views.package import PackageView
from sbos_installer.views.overview import OverviewScreenView

from sbos_installer.steps.disk import disk_partitioning, configure_partitions
from sbos_installer.steps.lvm import configure_lvm
from sbos_installer.steps.hostname import setup_hostname
from sbos_installer.steps.network import setup_network
from sbos_installer.steps.locale import setup_timezone, configure_timezone_system
from sbos_installer.steps.user import setup_user, configure_users
from sbos_installer.steps.package import setup_packages
from sbos_installer.steps.overview import overview
from sbos_installer.steps.bootloader import configure_bootloader
from sbos_installer.steps.general import configure_desktop

from rich.console import Console
from rich.text import Text

import sys
import time

console = Console()

if not check_root_permissions():
    ErrorView(error_message="The Installer requires root permissions to continue.")

if not check_uefi_capability():
    ErrorView(error_message="The StrawberryOS Installer currently only supports UEFI-capable computers")

if DEV_FLAG_DEV_MODE:
    WarningView("Developer mode is enabled!\nSome functions could possibly be skipped. Only use this if you are sure!")

try:
    runner = Runner(True)
    location = "/mnt"

    def _selection():
        clear_screen()

        Header("Welcome to the StrawberryOS Installer!")

        console.show_cursor(False)

        console.print(
            f"Thanks for choosing StrawberryOS!\n"
            f"The StrawberryOS Installer will guide you through the installation process.\n",
            justify="center"
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

        try:
            selection = ia_selection(
                question="",
                options=group,
                flags=["start", "console", "about"]
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
                    with open("/etc/motd", 'r') as _file:
                        print(_file.read())
                except:
                    pass

                sys.exit(0)

            case "about":
                AboutView()
                clear_screen()
                _selection()

    _selection()

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

    os_type = OSTypeView().val  # Choose which edition of StrawberryOS you want to install
    hostname = HostnameView().val  # Setup hostname
    net_stat = NetworkView().val  # Setup network
    region, city = TimezoneView().val  # Setup timezone
    user_setup = UserView().val  # Setup user
    disk_data, disk = DiskView().val  # Setup disk
    packages = PackageView().val  # Setup packages

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

    OverviewScreenView(install_data, disk)

    if not disk_data["disk"]["custom_partitioning"]:
        configure_partitions(disk, install_data)
        time.sleep(0.5)
        configure_lvm(disk, install_data)

        run(f"mount --mkdir /dev/strawberryos/system /mnt")
        run(f"mount --mkdir {install_data['disk'][disk]['efi']['block']} /mnt/boot/efi")

    else:
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

    # Mount userspace & copy root's .bashrc from systemspace to userspace
    run(f"mount --mkdir {install_data['disk'][disk]['user']['block']} /mnt/user")
    run(f"mkdir -p /mnt/user/data/root")
    run(f"cp /mnt/root/.bashrc /mnt/user/data/root")

    # Modify root's userspace PS1 variable
    with open("/mnt/user/data/root/.bashrc", "a") as _file:
        _file.write(
            r"PS1='\[\e[0m\][\[\e[0;1;91m\]\u\[\e[0;1;38;5;226m\]@\[\e[0;1;96m\]\H \[\e[0;1;38;5;161m\]\w\[\e[0m\]] \[\e[0;1m\]\$ \[\e[0m\]'")
        _file.write("\n")

    # Modify root's systemspace PS1 variable
    with open("/mnt/root/.bashrc", "a") as _file:
        _file.write(
            r"PS1='\[\e[92;1m\][ System ] \[\e[91m\]\u\[\e[93m\]@\[\e[91m\]\H\[\e[0m\] \[\e[96;1m\]\w\[\e[0m\] \[\e[2m\]\$\[\e[0m\] '")
        _file.write("\n")

    with open("/mnt/etc/issue", 'w') as file:
        file.write(r"StrawberryOS Chocolate Crisps \n \l"
                   "\n\n"
                   r"")

    # todo: Add StrawberryOS recovery (custom initramfs?)

    runner.run(f"cp /etc/os-release /mnt/etc/os-release")

    runner.run(f"umount {location}/dev")
    runner.run(f"umount {location}/sys")
    runner.run(f"umount {location}/proc")

    print(f"\n -- {GREEN}{BOLD} StrawberryOS post installation completed {CRESET}--")

except KeyboardInterrupt:
    console.clear()
    console.print(Text.from_ansi(
        f"-- {YELLOW}{BOLD}Exited installation process{CRESET} --"
    ), justify="center")
    console.show_cursor(True)
    sys.exit(0)