from sbos_installer.core.ui.select_button import SelectButton, ia_selection
from sbos_installer.core.ui.screen import Screen


class OSTypeView(Screen):
    title = "Choose the type of installation"

    def __init__(self):
        view = self.render
        super().__init__(title=self.title, view=view)

    def render(self):
        self.console.print("StrawberryOS has different editions to choose from\n", justify="center")
        self.console.show_cursor(False)

        group = []

        SelectButton(
            label=f"StrawberryOS Desktop (2024.07)",
            description="The standard version of StrawberryOS - With all the necessary tools "
                        "from us and a selection of desktops",
            group=group
        )

        SelectButton(
            label=f"StrawberryOS Desktop with Open Directory (2024.07)",
            description="StrawberryOS with configured Open Directory. Useful for schools, workplaces, and "
            "also the one or other private use",
            group=group
        )

        SelectButton(
            label=f"StrawberryOS Server (2024.1)",
            description="A minimal environment of StrawberryOS without a desktop. Includes additional server utilities",
            group=group
        )

        ostype_select = ia_selection(
            question="",
            options=group,
            flags=["desktop", "desktop_sod", "server"]
        )

        self.console.show_cursor(True)

        return ostype_select
