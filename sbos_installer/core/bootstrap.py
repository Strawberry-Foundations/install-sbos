from sbos_installer.core.packages import package_list, init_package
from sbos_installer.core.process import Runner
from sbos_installer.cli.selection import ia_selection
from sbos_installer.cli.parser import parse_bool
from sbos_installer.utils.colors import *

import subprocess
import sys


def bootstrap(install_packages: list):
    show_logs = parse_bool(ia_selection(
        "The next step is to start the installation. Would you like to view the logs during the installation?",
        options=["No", "Yes"]
    ))

    runner = Runner(show_logs)

    packages = ["base"]
    location = "/mnt"
    binder = f"bwrap --bind {location} / --dev /dev --bind /sys /sys --bind /proc /proc --bind /tmp /tmp"

    packages.extend(install_packages)

    print(
        f"\n{CYAN}{BOLD}The installation program will now start the bootstrap process. "
        f"This may take some time. Get yourself a coffee in the meantime!{CRESET}"
    )

    install_args = f"""/usr/sbin/debootstrap \
        --include={init_package} trixie \
        {location} https://deb.debian.org/debian"""

    runner.run(install_args)

    print(f"\n{GREEN}{BOLD}Installing additional packages ...{CRESET}")

    i = 1
    for package in packages:
        command = runner.run(binder + " apt install -y " + package_list.get(package))

        i += 1
        print("")

    print(f"\n{MAGENTA}{BOLD}Cleaning up system ...{CRESET}")
    runner.run(binder + " apt update")
    runner.run(binder + " apt upgrade -y")
    runner.run(binder + " apt clean all")
    runner.run(binder + " apt autoclean")
    runner.run(binder + " apt autoremove -y")

    print(f"\n{GREEN}{BOLD}Installing StrawberryOS utils ...{CRESET}")

    runner.run(
        binder + " wget https://raw.githubusercontent.com/Strawberry-Foundations/sbos-scripts/main/update-utils -O "
                 "/usr/local/bin/update-utils",
    )

    runner.run(binder + " chmod a+x /usr/local/bin/update-utils")
    runner.run(binder + " update-utils")

    print(f"Finished bootstrap of base system")
