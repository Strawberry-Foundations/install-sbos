from sbos_installer.cli.selection import ia_selection
from sbos_installer.cli.parser import parse_bool
from sbos_installer.utils.colors import *

import sys


def overview(data, disk):
    print(f"\n{GREEN}{BOLD} -- Install overview --{CRESET}")

    disk_data = data['disk'][disk]

    print(f"{GRAY}{BOLD}* {CYAN}Hostname:{CRESET} {data['hostname']}")
    print(f"{GRAY}{BOLD}* {CYAN}Network interface:{CRESET} {data['net_interface']}")
    print(f"{GRAY}{BOLD}* {CYAN}Timezone:{CRESET} {data['timezone']['region']}/{data['timezone']['city']}")
    print(f"{GRAY}{BOLD}* {CYAN}Users:{CRESET}")
    for user in data["users"]:
        print(f"{GRAY}{BOLD}    * {CYAN}{user}{CRESET}")
    print(f"{GRAY}{BOLD}* {CYAN}Disk:{CRESET} {disk}")
    print(f"{GRAY}{BOLD}    * {CYAN}EFI on {CYAN}{disk_data['efi']['block']}{CRESET}: {disk_data['efi']['size']:.2f}G{CRESET}")
    print(f"{GRAY}{BOLD}    * {CYAN}System on {CYAN}{disk_data['system']['block']}{CRESET}: {disk_data['system']['size']:.2f}G{CRESET}")
    print(f"{GRAY}{BOLD}    * {CYAN}User on {CYAN}{disk_data['user']['block']}{CRESET}: {disk_data['user']['size']:.2f}G{CRESET}")
    print(f"{GRAY}{BOLD}    * {CYAN}Swap on {CYAN}{disk_data['swap']['block']}{CRESET}: {disk_data['swap']['size']:.2f}G{CRESET}")
    print(f"{GRAY}{BOLD}* {CYAN}Packages:{CRESET} {', '.join(data['packages'])}")

    confirm = parse_bool(ia_selection("\nDo you want to continue?", options=["Yes", "No"]))

    if not confirm:
        print(f"\n{YELLOW}Exiting installation process{CRESET}")
        sys.exit()
