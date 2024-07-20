from sbos_installer.core.ui.single_select_button import SingleSelectButton, ia_selection
from sbos_installer.core.ui.screen import Screen
from sbos_installer.core.process import Runner
from sbos_installer.utils.colors import *

from rich.padding import Padding
from rich.text import Text


class KeyboardLayout(Screen):
    title = "Welcome to the StrawberryOS Installer!"

    def __init__(self):
        view = self.render
        super().__init__(title=self.title, view=view)

    def render(self):
        self.console.print("Please select your keyboard layout\n", justify="center")
        self.console.show_cursor(False)

        runner = Runner(True)

        group = []

        layouts = {
            "Deutsch (German)": "de-latin1",
            "British English (English)": "uk",
            "American English (English)": "us",
            "Netherlands (Dutch)": "nl",
            "-> Manual input": "own_layout",
        }

        for lang, kbd in layouts.items():
            SingleSelectButton(
                label=lang,
                group=group
            )

        kbd_layout = ia_selection(
            question="",
            options=group,
            flags=list(layouts.values())
        )

        self.console.show_cursor(True)

        if kbd_layout == "own_layout":
            print()
            self.console.print(Padding(
                Text.from_ansi(
                    f"{YELLOW}[!] {GRAY}The entry of a non-existent keyboard layout is ignored and the default "
                    f"layout is automatically used{CRESET}\n\n"),
                (0, 8)
            ))
            while True:
                kbd_layout = input(f"{CRESET}        Keyboard Layout:  {GRAY}")
                if kbd_layout.strip() != "":
                    break
                print(f"\033[1A\033[J", end='')

        runner.run(f"loadkeys {kbd_layout}")

        return kbd_layout
