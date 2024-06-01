from sbos_installer.utils.colors import *


def setup_hostname():
    print(f"{GREEN}{BOLD} -- Hostname configuration --{CRESET}")
    hostname = input("Enter system hostname [strawberryos]: ")

    if hostname.strip() == "":
        return "strawberryos"

    return hostname
