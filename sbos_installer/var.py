VERSION = "2.3.1"

ROOT_MNT = "/mnt/"

CODENAME_FULL = "Spicy Latte"
CODENAME_LOWER = "spicylatte"


class Versions:
    desktop = "2025.07"
    desktop_sod = "2025.07"
    server = "2025.1.0"


class Setup:
    def __init__(self):
        self.edition = None
        self.hostname = None
        self.net_interface = None
        self.region = None
        self.city = None
        self.user_setup = None
        self.disk_data = None
        self.disk = None
        self.packages = None
