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

        SingleSelectButton(
            label=f"Deutsch (German)",
            group=group
        )

        SingleSelectButton(
            label=f"English (English)",
            group=group
        )

        SingleSelectButton(
            label=f"Netherlands (Dutch)",
            group=group
        )

        kbd_layout = ia_selection(
            question="",
            options=group,
            flags=["desktop", "desktop_sod", "server"]
        )

        self.console.show_cursor(True)

        return kbd_layout
