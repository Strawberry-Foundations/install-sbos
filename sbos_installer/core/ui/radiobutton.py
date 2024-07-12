from sbos_installer.utils.colors import *

from rich.padding import Padding
from rich.text import Text


class RadioButton:
    def __init__(self, label, description, state=False, group=None):
        self.label = label
        self.description_text = Text.from_ansi(f"{GRAY}{description}{RESET}")
        self.description = Padding(self.description_text, (0, 17))
        self.state = state
        self.group = group

        if group is not None:
            group.append(self)

    def set_state(self, state):
        if state and self.group:
            for button in self.group:
                button.state = False
        self.state = state

    def build(self):
        marker = "(X)" if self.state else "( )"
        return f"           {marker}   {self.label}\n", self.description

    def __str__(self):
        marker = "(X)" if self.state else "( )"
        return f"           {marker}   {self.label}\n\n                 ", {self.description}
