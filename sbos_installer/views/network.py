from sbos_installer.cli.parser import parse_bool
from sbos_installer.cli.selection import ia_selection
from sbos_installer.core.ui.screen import Screen
from sbos_installer.steps.network import \
    get_network_interfaces, get_connected_interface, check_internet_connection, \
    scan_wifi_networks, connect_to_wifi
from sbos_installer.utils.colors import *

from rich.text import Text
from rich.padding import Padding
from getpass import getpass

import sys
import subprocess
import time


class NetworkView(Screen):
    title = "Setup network connection"

    def __init__(self):
        view = self.render
        super().__init__(title=self.title, view=view)

    def render(self):
        self.console.print(Padding(
            "Next, an Internet connection must be established so that the necessary packages for "
            "StrawberryOS can be downloaded.\n",
            (0, 8))
        )

        # Get network interfaces
        interfaces = get_network_interfaces()
        connected_interface = get_connected_interface()

        if len(interfaces) > 1:
            connected_interface = ia_selection(
                question=f"Multiple network interfaces are available. Which one do you want to use?",
                options=interfaces,
                padding=8
            )
            print("")
        else:
            if not connected_interface:
                connected_interface = interfaces[0]

        if connected_interface:
            self.console.print(Padding(
                Text.from_ansi(f"You are connected to {CYAN}{connected_interface}{CRESET}"), (0, 8))
            )

            connection_available = check_internet_connection()

            if connection_available:
                self.console.print(Padding(
                    Text.from_ansi(f"Internet connection is {GREEN}{BOLD}available{CRESET}"), (0, 8)))
            else:
                self.console.print(Padding(
                    Text.from_ansi(f"{YELLOW}{BOLD}Internet connection is {RED}not {YELLOW}available{CRESET}"), (0, 8)))
                if "en" in connected_interface:
                    self.console.print(Padding(Text.from_ansi(
                        f"{YELLOW}{BOLD}No active internet connection is available. Please check your connection.{CRESET}"),
                        (0, 8)
                    ))
                    sys.exit(1)

            if "wl" in connected_interface:
                if connection_available:
                    print()
                    force_wifi_connect = parse_bool(ia_selection(
                        question=f"Your Wi-Fi connection already seems to be working.\n        "
                                 f"Would you still like to set up a connection?",
                        options=["No", "Yes"],
                        padding=8
                    ))

                    if force_wifi_connect:
                        print("")
                        self.establish_wifi()
                else:
                    self.establish_wifi()

            elif "en" in connected_interface:
                self.console.print(Padding(Text.from_ansi(
                    f"Connected via {CYAN}LAN{CRESET}"), (0, 8)
                ))
            else:
                self.console.print(Padding(Text.from_ansi(
                    f"{YELLOW}Unknown network interface{CRESET}"), (0, 8)
                ))
        else:
            self.console.print(Padding(Text.from_ansi(
                f"{YELLOW}{BOLD}No active network interface found. Setup cannot continue without a valid internet "
                f"connection!{CRESET}"), (0, 8)
            ))
            sys.exit(1)

        time.sleep(2)

        return connected_interface

    def establish_wifi(self):
        self.console.print(Padding(Text.from_ansi(
            f"Connected via {CYAN}Wi-Fi{CRESET}. Search for available Wi-Fi networks ..."), (0, 8)
        ))
        wifi_networks, wifi_freqs = scan_wifi_networks()

        if wifi_networks:
            print()
            ssid = ia_selection(
                question=f"Available {CYAN}Wi-Fi{CRESET} networks",
                options=wifi_networks,
                flags=wifi_freqs,
                padding=8
            )

            if ssid == "+ Add Wi-Fi":
                _input = True
                while _input:
                    ssid = input("\nSSID: ")
                    if ssid.strip() == "":
                        print(f"{YELLOW}{BOLD}SSID cannot be empty{CRESET}")
                    else:
                        _input = False

            print()
            show_password = parse_bool(ia_selection(
                question=f"Do you want the Wi-Fi password to be shown?",
                options=["No", "Yes"],
                padding=8
            ))

            if show_password:
                password = input(f"\n        Password for {ssid}:  {GRAY}")
            else:
                password = getpass(f"\n        Password for {ssid}:  {GRAY}")

            self.console.print(Padding(Text.from_ansi(
                f"Connection to {CYAN}{ssid}{CRESET} is being established ..."), (0, 8)
            ))
            connect_to_wifi(ssid, password)

        else:
            self.console.print(Padding(Text.from_ansi("No Wi-Fi networks found."), (0, 8)))

    def connect_to_wifi(self, ssid, password):
        try:
            subprocess.run(['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password], check=True)

            self.console.print(Padding(Text.from_ansi(
                f"Successfully {GREEN}connected{CRESET} with {CYAN}{ssid}{CRESET}"), (0, 8)
            ))
        except subprocess.CalledProcessError as e:
            self.console.print(Padding(Text.from_ansi(
                f"{RED}{BOLD}Error connecting to {ssid}: {e}{CRESET}"), (0, 8)
            ))
