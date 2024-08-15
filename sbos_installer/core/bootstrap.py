from sbos_installer.core.packages import base_package_list, init_package
from sbos_installer.core.process import Runner
from sbos_installer.core.ui.screen import clear_screen
from sbos_installer.core.ui.header import Header
from sbos_installer.utils.colors import *
from sbos_installer.var import ROOT_MNT


def bootstrap(install_packages: list):
    runner = Runner(True)

    packages = ["base"]
    binder = f"bwrap --bind {ROOT_MNT} / --dev /dev --bind /sys /sys --bind /proc /proc --bind /tmp /tmp"

    packages.extend(install_packages)

    print(
        f"\n{CYAN}{BOLD}The installation program will now start the bootstrap process. "
        f"This may take some time. Get yourself a coffee in the meantime!{CRESET}"
    )

    install_args = f"""/usr/sbin/debootstrap \
        --include={init_package} trixie \
        {ROOT_MNT} https://deb.debian.org/debian"""

    runner.run(install_args)

    clear_screen()
    Header("Configuring apt ...")
    print("Configuring /etc/apt/sources.list")

    with open(f"{ROOT_MNT}etc/apt/sources.list", 'w') as file:
        file.write(
            f'deb https://deb.debian.org/debian trixie main contrib non-free non-free-firmware\n'
            f'deb http://security.debian.org/debian-security trixie-security main non-free-firmware\n'
            f'deb http://deb.debian.org/debian/ trixie-updates main non-free-firmware\n'
            f'deb https://dl.strawberryfoundations.org/deb mainstream main'
        )

    print("Fetching StrawberryOS apt repo key ...")
    runner.run(binder + " wget https://dl.strawberryfoundations.org/deb/key.public -O /etc/apt/trusted.gpg.d/strawberryos.asc")
    print("Updating apt ...")
    runner.run(binder + " apt update")

    clear_screen()
    Header("Installing additional packages ...")

    i = 1
    for package in packages:
        clear_screen()
        Header(f"Installing additional packages ({i}/{len(packages)}) ...")
        runner.run(binder + " apt install -y " + base_package_list.get(package))

        i += 1
        print("")

    clear_screen()
    Header("Cleaning up system ...")
    runner.run(binder + " apt update")
    runner.run(binder + " apt upgrade -y")
    runner.run(binder + " apt clean all")
    runner.run(binder + " apt autoclean")
    runner.run(binder + " apt autoremove -y")

    clear_screen()
    Header("Post-package setup ...")

    print(f"\n{GREEN}{BOLD}Installing StrawberryOS utils ...{CRESET}")

    runner.run(
        binder + " wget https://raw.githubusercontent.com/Strawberry-Foundations/sbos-scripts/main/update-utils -O "
                 "/usr/local/bin/update-utils",
    )

    runner.run(binder + " chmod a+x /usr/local/bin/update-utils")
    runner.run(binder + " update-utils")

    print(f"\n{GREEN}{BOLD}Installing spkg ...{CRESET}")

    runner.run(binder + " wget https://spkg.strawberryfoundations.org/setup/spkg-git.deb -O /root/spkg-git.deb")
    runner.run(binder + " apt install /root/spkg-git.deb")
    runner.run(binder + " rm /root/spkg-git.deb")

    print(f"\n{CYAN}{BOLD}Finished bootstrap of base system{CRESET}")
