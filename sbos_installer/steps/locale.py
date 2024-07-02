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


def setup_timezone():
    print(f"\n{GREEN}{BOLD} -- Timezone configuration --{CRESET}")

    def setup_region():
        region_input = "Europe"

        while True:
            _region_input = input("Which region are you in? (? for list) [Europe]: ")

            if _region_input == "?":
                print(list_zoneinfo(path="/usr/share/zoneinfo"))
                continue

            elif _region_input.strip() == "":
                region_input = "Europe"
                break

            else:
                if not os.path.exists(f"/usr/share/zoneinfo/{_region_input}"):
                    print(f"{YELLOW}{BOLD}Region '{_region_input}' does not exists{CRESET}")
                    continue
                region_input = _region_input
                break

        return region_input

    def setup_city(_region):
        city_input = "Berlin"

        while True:
            _city_input = input("Which city are you in? (? for list) [Berlin]: ")

            if _city_input == "?":
                try:
                    entries = os.listdir(f"/usr/share/zoneinfo/{_region}")

                    timezones = [entry for entry in entries if os.path.isfile(os.path.join(f"/usr/share/zoneinfo/{_region}", entry))]

                    formatted_output = ' '.join(timezones)

                    print(formatted_output)
                except Exception as e:
                    print(f"{YELLOW}{BOLD}Error occurred while listing timezones: {e}{CRESET}")
                    return ""

                continue
            elif _city_input.strip() == "":
                city_input = "Berlin"
                break

            else:
                if not os.path.exists(f"/usr/share/zoneinfo/{_region}/{_city_input}"):
                    print(f"{YELLOW}{BOLD}City '{_city_input}' does not exists{CRESET}")
                    continue
                city_input = _city_input
                break

        return city_input

    region = setup_region()
    city = setup_city(region)

    return region, city


def configure_timezone_system(region: str, city: str):
    location = "/mnt"
    runner = Runner(False)

    print(f"{BOLD}{GREEN}Configuring timezone ...{CRESET}")
    runner.run(f"chroot {location} ln -sf /usr/share/zoneinfo/{region}/{city} /etc/localtime")