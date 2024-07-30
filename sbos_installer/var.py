version = "2.2.0"

ROOT_MNT = "/mnt/"


class Versions:
    desktop = "2024.08"
    desktop_sod = "2024.08"
    server = "2024.1"


class Vars:
    def __init__(self):
        self.os_type = None
        self.hostname = None
        self.net_stat = None
        self.region = None
        self.city = None
        self.user_setup = None
        self.disk_data = None
        self.disk = None
        self.packages = None
