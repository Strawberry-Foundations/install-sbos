from sbos_installer.core.packages import package_list
from sbos_installer.cli.selection import ia_selection
from sbos_installer.cli.parser import parse_bool
from sbos_installer.utils.colors import *


def setup_packages():
    packages = ["base"]
    print(f"\n{GREEN}{BOLD} -- Package selection --{CRESET}")

    confirm = parse_bool(ia_selection(
        "Would you like to install other packages in addition to init & base?",
        options=["Yes", "No"])
    )

    if confirm:
        _packages = None
        _flag = True
        while _flag:
            print(f"Available packages: {' '.join(package_list)}")

            _packages = input("Provide additional packages [init,base]: ").split(",")

            for package in _packages:
                if package == '':
                    _flag = False
                if package not in package_list:
                    print(f"{YELLOW}{BOLD}Package '{package}' is not available{CRESET}")
                else:
                    _flag = False

        packages.extend(_packages)

    return packages
