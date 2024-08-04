from sbos_installer.core.ui.screen import Screen
from sbos_installer.core.process import Runner
from sbos_installer.cli.parser import parse_bool
from sbos_installer.cli.selection import ia_selection
from sbos_installer.var import ROOT_MNT

from rich.padding import Padding


class DesktopView(Screen):
    title = "Additional post-install steps"

    def __init__(self):
        view = self.render
        super().__init__(title=self.title, view=view)

    def render(self):
        self.console.print(Padding(
            "A graphical desktop can be installed.\nThis is useful if you want to use this computer as a desktop.\n",
            (0, 8))
        )

        confirm = parse_bool(ia_selection(
            question="Would you like to install a graphical desktop?",
            options=["Yes", "No"],
            flags=["(Recommended for desktops)", "(Recommended for servers)"],
            padding=8
        ))

        if confirm:
            runner = Runner(True)
            runner.run(f"chroot {ROOT_MNT} tasksel")

        return None
