from sbos_installer.core.process import Runner
from sbos_installer.utils.colors import *

import os


def list_zoneinfo(path="/usr/share/zoneinfo"):
    try:
        entries = os.listdir(path)

        timezones = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]

        formatted_output = f' {GRAY}{BOLD}-{CRESET} '.join(timezones)

        return formatted_output
    except Exception as e:
        print(f"Error occurred while listing timezones: {e}")
        return ""

def configure_timezone_system(region: str, city: str):
    location = "/mnt"
    runner = Runner(False)

    runner.run(f"chroot {location} ln -sf /usr/share/zoneinfo/{region}/{city} /etc/localtime")