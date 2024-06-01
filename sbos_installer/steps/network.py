from sbos_installer.cli.selection import ia_selection
from sbos_installer.utils.colors import *
from sbos_installer.cli.parser import parse_bool
from getpass import getpass

import sys
import socket
import subprocess


def check_internet_connection():
    try:
        socket.create_connection(("strawberryfoundations.xyz", 80), timeout=5)
        return True
    except OSError:
        return False


def get_network_interfaces():
    result = subprocess.run(['ip', 'link'], capture_output=True, text=True)
    interfaces = [line.split(": ")[1].split("@")[0] for line in result.stdout.splitlines() if ": " in line]
    return interfaces


def get_connected_interface():
    result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if "default" in line:
            return line.split()[4]
    return None


def scan_wifi_networks():
    result = subprocess.run(['nmcli', '-t', '-f', 'SSID,FREQ', 'dev', 'wifi'], capture_output=True, text=True)
    networks = result.stdout.splitlines()
    ssids = []
    freqs = []
    for network in networks:
        ssid, freq = network.split(':')
        ssids.append(ssid)
        freq = int(str(freq).replace(" MHz", "").strip())
        if freq < 3000:
            freqs.append("[2.4 GHz]")
        else:
            freqs.append("[5 GHz]")
    return ssids, freqs


def connect_to_wifi(ssid, password):
    try:
        subprocess.run(['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password], check=True)
        print(f"Successfully connected with {ssid}.")
    except subprocess.CalledProcessError as e:
        print(f"Error connecting to {ssid}: {e}")


def setup_network():
    print(f"\n{GREEN}{BOLD} -- Setup network --{CRESET}")
    connected_interface = get_connected_interface()

    if connected_interface:
        print(f"You are connected to {CYAN}{connected_interface}{CRESET}")

        if check_internet_connection():
            print(f"Internet connection is {GREEN}{BOLD}available{CRESET}")
        else:
            print(f"{YELLOW}{BOLD}Internet connection is {RED}not {YELLOW}available")

        if "wl" in connected_interface:
            print(f"Connected via {CYAN}Wi-Fi{CRESET}. Search for available Wi-Fi networks...")
            wifi_networks, wifi_freqs = scan_wifi_networks()

            if wifi_networks:
                ssid = ia_selection("Available Wi-Fi networks", options=wifi_networks, flags=wifi_freqs)
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
