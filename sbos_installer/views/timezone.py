from sbos_installer.core.ui.screen import Screen
from sbos_installer.steps.locale import list_zoneinfo
from sbos_installer.utils.colors import *

from rich.text import Text
from rich.padding import Padding

import os


class TimezoneView(Screen):
    title = "Timezone configuration"

    def __init__(self):
        view = self.render
        super().__init__(title=self.title, view=view)

    def render(self):
        self.console.print(Padding(
            "To display the time correctly, you must specify the time zone in which you are located.\n",
            (0, 8)
        ))

        region = self.setup_region()
        city = self.setup_city(region)

        print(CRESET)

        return region, city

    def setup_region(self):
        region_input = "Europe"

        while True:
            _region_input = input(f"        Which region are you in? (? for list) [Europe]:  {GRAY}")
            print(CRESET)
            if _region_input == "?":
                self.console.print(Padding(list_zoneinfo(path="/usr/share/zoneinfo"), (0, 8)))
                continue

            elif _region_input.strip() == "":
                region_input = "Europe"
                break

            else:
                if not os.path.exists(f"/usr/share/zoneinfo/{_region_input}"):
                    self.console.print(Padding(
                        f"{YELLOW}{BOLD}Region '{_region_input}' does not exists{CRESET}", (0, 8)
                    ))
                    continue
                region_input = _region_input
                break

        return region_input

    def setup_city(self, _region):
        city_input = "Berlin"

        while True:
            _city_input = input(f"        Which city are you in? (? for list) [Berlin]:  {GRAY}")
            print(CRESET)
            if _city_input == "?":
                try:
                    entries = os.listdir(f"/usr/share/zoneinfo/{_region}")

                    timezones = [entry for entry in entries if
                                 os.path.isfile(os.path.join(f"/usr/share/zoneinfo/{_region}", entry))]

                    formatted_output = ' '.join(timezones)

                    self.console.print(Padding(formatted_output), (0, 8))
                except Exception as e:
                    self.console.print(Padding(
                        f"{YELLOW}{BOLD}Error occurred while listing timezones: {e}{CRESET}", (0, 8)
                    ))
                    return ""

                continue
            elif _city_input.strip() == "":
                city_input = "Berlin"
                break

            else:
                if not os.path.exists(f"/usr/share/zoneinfo/{_region}/{_city_input}"):
                    self.console.print(Padding(
                        f"{YELLOW}{BOLD}City '{_city_input}' does not exists{CRESET}", (0, 8)
                    ))
                    continue
                city_input = _city_input
                break

        return city_input
