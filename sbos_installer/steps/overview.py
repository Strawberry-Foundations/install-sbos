from sbos_installer.cli.selection import ia_selection
from sbos_installer.cli.parser import parse_bool
from sbos_installer.utils.colors import *


def overview(data, disk):
    print(f"\n{GREEN}{BOLD} -- Install overview --{CRESET}")

    print(f"{GRAY}{BOLD}* {CYAN}Hostname:{CRESET} {data['hostname']}")
    print(f"{GRAY}{BOLD}* {CYAN}Network interface:{CRESET} {data['net_interface']}")
    print(f"{GRAY}{BOLD}* {CYAN}Timezone:{CRESET} {data['timezone']['region']}/{data['timezone']['city']}")
    print(f"{GRAY}{BOLD}* {CYAN}Users:{CRESET}")
    for user in data["users"]:
        print(f"{GRAY}{BOLD}    * {CYAN}{user}{CRESET}")
    print(f"{GRAY}{BOLD}* {CYAN}Disk:{CRESET} {disk}")
    print(f"{GRAY}{BOLD}    * {CYAN}EFI:{CRESET} {data['disk'][disk]['efi_disk_size']}G{CRESET}")
    print(f"{GRAY}{BOLD}    * {CYAN}System:{CRESET} {data['disk'][disk]['system_disk_size']}G{CRESET}")
    print(f"{GRAY}{BOLD}    * {CYAN}User:{CRESET} {data['disk'][disk]['user_disk_size']}G{CRESET}")
    print(f"{GRAY}{BOLD}    * {CYAN}Swap:{CRESET} {data['disk'][disk]['swap_disk_size']}G{CRESET}")
    print(f"{GRAY}{BOLD}* {CYAN}Packages:{CRESET} {', '.join(data['packages'])}")

    confirm = parse_bool(ia_selection("\nDo you want to continue?", options=["Yes", "No"]))

    if not confirm:
        print(f"\n{YELLOW}Exiting installation process{CRESET}")