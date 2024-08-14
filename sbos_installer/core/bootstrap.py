from sbos_installer.core.packages import base_package_list, init_package
from sbos_installer.core.process import Runner
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

    print(f"\n{GREEN}{BOLD}Configuring apt ...{CRESET}")
    with open(f"{ROOT_MNT}etc/apt/sources.list", 'w') as file:
        file.write(f'deb https://deb.debian.org/debian trixie main contrib non-free non-free-firmware"')
    runner.run(binder + " apt update")

    print(f"\n{GREEN}{BOLD}Installing additional packages ...{CRESET}")

    i = 1
    for package in packages:
        command = runner.run(binder + " apt install -y " + base_package_list.get(package))

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

    print(f"\n{GREEN}{BOLD}Installing spkg ...{CRESET}")

    runner.run(binder + " wget https://spkg.strawberryfoundations.org/setup/spkg-git.deb -O /root/spkg-git.deb")
    runner.run(binder + " apt install /root/spkg-git.deb")
    runner.run(binder + " rm /root/spkg-git.deb")

    print(f"\n{CYAN}{BOLD}Finished bootstrap of base system{CRESET}")
