from sbos_installer.core.ui.single_select_button import SingleSelectButton, SingleSelectButtonGroup
from sbos_installer.core.ui.screen import Screen
from sbos_installer.core.process import Runner
from sbos_installer.core.locales import kbd_layouts
from sbos_installer.utils.colors import *

from rich.padding import Padding
from rich.text import Text


class KeyboardLayout(Screen):
    title = "Welcome to the StrawberryOS Installer!"

    def __init__(self):
        view = self.render
        super().__init__(title=self.title, view=view)

    def render(self):
        self.console.print("Please select your keyboard layout\nThis is used only during installation\n", justify="center")
        self.console.show_cursor(False)

        self.console.print(
            Text.from_ansi(
                f"{GREEN}? {LIGHT_GRAY}Can't see your layout? Open an issue on our GitHub with your requested layout "
                f"and we'll add it!\n"
            ),
            justify="center"
        )

        self.console.print(Text.from_ansi(f"URL: {LIGHT_BLUE}https://github.com/Strawberry-Foundations/install-sbos{CRESET}\n\n"), justify="center")

        runner = Runner(True)
        
        group = SingleSelectButtonGroup()

        for lang, _ in kbd_layouts.items():
            group.append(SingleSelectButton(label=lang))

        kbd_layout = group.selection(flags=list(kbd_layouts.values()))

        self.console.show_cursor(True)

        if kbd_layout == "own_layout":
            print()
            self.console.print(Padding(
                Text.from_ansi(
                    f"{YELLOW}[!] {GRAY}The entry of a non-existent keyboard layout can cause problems{CRESET}\n\n"
                ),
                (0, 8)
            ))
            while True:
                kbd_layout = input(f"{CRESET}        Keyboard Layout:  {GRAY}")
                if kbd_layout.strip() != "":
                    break
                print(f"\033[1A\033[J", end='')

        runner.run(f"loadkeys {kbd_layout}")

        return kbd_layout
