from sbos_installer.core.process import Runner
from sbos_installer.cli.selection import ia_selection
from sbos_installer.cli.parser import parse_bool
from sbos_installer.utils.colors import *


def configure_desktop():
    confirm = parse_bool(ia_selection(
        question="Would you like to install a graphical desktop?",
        options=["Yes", "No"],
        flags=["(Recommended for desktops)", "(Recommended for servers)",])
    )

    if confirm:
        runner = Runner(True)

        print(f"{CYAN}{BOLD}Running tasksel{CRESET}")
        runner.run(f"chroot /mnt tasksel")
