from sbos_installer.core.process import Runner
from sbos_installer.utils.colors import *

import os


def list_zoneinfo(path="/usr/share/zoneinfo"):
    try:
        entries = os.listdir(path)

        timezones = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]

        formatted_output = ' '.join(timezones)

        return formatted_output
    except Exception as e:
        print(f"Error occurred while listing timezones: {e}")
        return ""


def setup_timezone():
    print(f"\n{GREEN}{BOLD} -- Timezone configuration --{CRESET}")

    def setup_region():
        _region = input("Which region are you in? (? for list) [Europe]: ")
        if _region == "?":
            print(list_zoneinfo(path="/usr/share/zoneinfo"))
            setup_region()
        elif _region.strip() == "":
            _region = "Europe"

        if not os.path.exists(f"/usr/share/zoneinfo/{_region}"):
            print(f"{YELLOW}{BOLD}Region '{_region}' does not exists{CRESET}")
            setup_region()

        return _region

    def setup_city(_region):
        _city = input("Which city are you in? (? for list) [Berlin]: ")
        if _city == "?":
            try:
                entries = os.listdir(f"/usr/share/zoneinfo/{_region}")

                timezones = [entry for entry in entries if os.path.isfile(os.path.join(f"/usr/share/zoneinfo/{_region}", entry))]

                formatted_output = ' '.join(timezones)

                print(formatted_output)
            except Exception as e:
                print(f"{YELLOW}{BOLD}Error occurred while listing timezones: {e}{CRESET}")
                return ""

            setup_city(_region)
        elif _city.strip() == "":
            _city = "Berlin"

        if not os.path.exists(f"/usr/share/zoneinfo/{_region}/{_city}"):
            print(f"{YELLOW}{BOLD}City '{_city}' does not exists{CRESET}")
            setup_city(_region)

        return _city

    region = setup_region()
    city = setup_city(region)

    return region, city


def configure_timezone_system(region: str, city: str):
    location = "/mnt"
    runner = Runner(False)

    print(f"{BOLD}{GREEN}Configuring timezone ...{CRESET}")

    runner.run(f"mount --bind /dev {location}/dev")
    runner.run(f"mount --bind /sys {location}/sys")
    runner.run(f"mount --bind /proc {location}/proc")

    runner.run(f"chroot {location} ln -sf /usr/share/zoneinfo/{region}/{city} /etc/localtime")

    runner.run(f"umount {location}/dev")
    runner.run(f"umount {location}/sys")
    runner.run(f"umount {location}/proc")