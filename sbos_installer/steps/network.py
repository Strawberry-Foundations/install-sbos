from sbos_installer.utils.colors import *

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
        socket.create_connection(("strawberryfoundations.org", 80), timeout=5)
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

        print(f"Successfully {GREEN}connected{CRESET} with {CYAN}{ssid}{CRESET}")
    except subprocess.CalledProcessError as e:
        print(f"{RED}{BOLD}Error connecting to {ssid}: {e}{CRESET}")
