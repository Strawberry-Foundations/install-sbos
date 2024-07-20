from sbos_installer.core.ui.single_select_button import SingleSelectButton, ia_selection
from sbos_installer.core.ui.screen import Screen


class KeyboardLayout(Screen):
    title = "Welcome to the StrawberryOS Installer!"

    def __init__(self):
        view = self.render
        super().__init__(title=self.title, view=view)

    def render(self):
        self.console.print("Please select your keyboard layout\n", justify="center")
        self.console.show_cursor(False)

        group = []

        layouts = {
            "Deutsch (German)": "de-latin1",
            "British English (English)": "uk",
            "American English (English)": "us",
            "Netherlands (Dutch)": "nl",
        }

        for lang, kbd in layouts.items():
            SingleSelectButton(
                label=lang,
                group=group
            )

        kbd_layout = ia_selection(
            question="",
            options=group,
            flags=[layouts.values()]
        )

        self.console.show_cursor(True)

        return kbd_layout
