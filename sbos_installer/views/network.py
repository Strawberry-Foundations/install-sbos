from sbos_installer.core.ui.screen import Screen
from sbos_installer.utils.colors import *

from rich.text import Text
from rich.padding import Padding


class NetworkView(Screen):
    title = "Setup network connection"

    def __init__(self):
        view = self.render
        super().__init__(title=self.title, view=view)

    def render(self):
        self.console.print(Padding(
            "Next, an Internet connection must be established so that the necessary packages for "
            "StrawberryOS can be downloaded.",
            (0, 8))
        )

        return ""
