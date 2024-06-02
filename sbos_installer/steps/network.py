from sbos_installer.cli.selection import ia_selection
from sbos_installer.utils.colors import *
from sbos_installer.cli.parser import parse_bool
from getpass import getpass

import sys
import os
import socket
import subprocess


def get_network_interfaces():
    """Get a list of all network interfaces, excluding virtual interfaces."""
    virtual_interfaces_prefixes = ('docker', 'veth', 'br-', 'lo', 'virbr', 'vmnet', 'vboxnet')
    interfaces = []
    for interface in os.listdir('/sys/class/net/'):
        if not interface.startswith(virtual_interfaces_prefixes):  # Exclude virtual interfaces
            interfaces.append(interface)
    return interfaces


def get_connected_interface():
    result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if "default" in line:
            return line.split()[4]
    return None


def check_internet_connection():
    """Check if the machine is connected to the internet."""
    try:
        socket.create_connection(("strawberryfoundations.xyz", 80), timeout=5)
        return True
    except OSError:
        return False


def scan_wifi_networks():
    """List available Wi-Fi networks."""
    result = subprocess.run(['nmcli', '-t', '-f', 'SSID,FREQ', 'dev', 'wifi'], capture_output=True, text=True)
    networks = result.stdout.splitlines()
    ssids = []
    freqs = []
    for network in networks:
        ssid, freq = network.split(':')
        ssids.append(ssid)
        freq = int(str(freq).replace(" MHz", "").strip())
        if freq < 3000:
            freqs.append(f"{YELLOW}[2.4 GHz]{RESET}")
        else:
            freqs.append(f"{GREEN}[5 GHz]{RESET}")

    ssids.extend(["+ Add Wi-Fi"])
    return ssids, freqs


def connect_to_wifi(ssid, password):
    try:
        subprocess.run(['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password], check=True)
        print(f"Successfully connected with {ssid}.")
    except subprocess.CalledProcessError as e:
        print(f"Error connecting to {ssid}: {e}")


def setup_network():
    print(f"\n{GREEN}{BOLD} -- Setup network --{CRESET}")

    interfaces = get_network_interfaces()
    connected_interface = get_connected_interface()

    if len(interfaces) > 1:
        connected_interface = ia_selection(
            question=f"Multiple network interfaces are available. Which one do you want to use?",
            options=interfaces
        )
        print("")
    else:
        if connected_interface == "":
            connected_interface = interfaces[0]

    if connected_interface:
        print(f"You are connected to {CYAN}{connected_interface}{CRESET}")

        if check_internet_connection():
            print(f"Internet connection is {GREEN}{BOLD}available{CRESET}")
        else:
            print(f"{YELLOW}{BOLD}Internet connection is {RED}not {YELLOW}available")
            if "en" in connected_interface:
                print(f"{YELLOW}{BOLD}No active internet connection is available. Please check your connection.{CRESET}")
                sys.exit(1)

        if "wl" in connected_interface:
            print(f"Connected via {CYAN}Wi-Fi{CRESET}. Search for available Wi-Fi networks...")
            wifi_networks, wifi_freqs = scan_wifi_networks()

            if wifi_networks:
                ssid = ia_selection(f"\nAvailable {CYAN}Wi-Fi{CRESET} networks", options=wifi_networks, flags=wifi_freqs)

                if ssid == "+ Add Wi-Fi":
                    _input = True
                    while _input:
                        ssid = input("\nSSID: ")
                        if ssid.strip() == "":
                            print(f"{YELLOW}{BOLD}SSID cannot be empty{CRESET}")
                        else:
                            _input = False

                show_password = parse_bool(ia_selection(
                    question=f"\nDo you want the Wi-Fi password to be shown?",
                    options=["No", "Yes"]
                ))

                if show_password:
                    password = input(f"\nPassword for {ssid}: ")
                else:
                    password = getpass(f"\nPassword for {ssid}: ")

                connect_to_wifi(ssid, password)

            else:
                print("No Wi-Fi networks found.")

        elif "en" in connected_interface:
            print(f"Connected via {CYAN}LAN{CRESET}")
        else:
            print("Unknown network interface.")

    else:
        print(
            f"{YELLOW}{BOLD}No active network interface found. Setup cannot continue without a valid internet "
            f"connection!{CRESET}"
        )
        sys.exit(1)

    return connected_interface
