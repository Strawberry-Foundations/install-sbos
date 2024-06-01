from sbos_installer.cli.selection import get_user_input, ia_selection
from sbos_installer.utils.colors import *

from sbos_installer.steps.disk import disk_partitioning
from sbos_installer.steps.hostname import setup_hostname
from sbos_installer.steps.network import setup_network
from sbos_installer.steps.locale import setup_timezone
from sbos_installer.steps.user import setup_user
from sbos_installer.steps.package import setup_packages
from sbos_installer.steps.overview import overview

print(f"{GREEN}{BOLD}Welcome to StrawberryOS Installer!\n{CRESET}Thanks for installing StrawberryOS on your computer.\n")

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

except KeyboardInterrupt:
    print(f"\n{YELLOW}Exited installation process{CRESET}")
