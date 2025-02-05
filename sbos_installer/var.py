VERSION = "2.3.0"

ROOT_MNT = "/mnt/"

CODENAME_FULL = "Lemon Tea"
CODENAME_LOWER = "lemontea"


class Versions:
    desktop = "2025.01"
    desktop_sod = "2025.01"
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
