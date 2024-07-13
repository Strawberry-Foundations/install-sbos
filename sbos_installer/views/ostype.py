from sbos_installer.core.ui.select_button import SelectButton, ia_selection
from sbos_installer.core.ui.screen import Screen

from rich import print as rprint


class OSTypeView(Screen):
    title = "Choose the type of installation"

    def __init__(self):
        view = self.render
        super().__init__(title=self.title, view=view)

    def render(self):
        self.console.print("StrawberryOS has different editions to choose from\n", justify="center")

        group = []

        SelectButton(
            label="StrawberryOS Desktop",
            description="The standard version of StrawberryOS - With all the necessary tools "
                        "from us and a selection of desktops",
            group=group
        )

        SelectButton(
            label="StrawberryOS Desktop with Open Directory",
            description="StrawberryOS with configured Open Directory. Useful for schools, workplaces, and "
            "also the one or other private use",
            group=group
        )

        SelectButton(
            label="StrawberryOS Server",
            description="A minimal environment of StrawberryOS without a desktop. Includes additional server utilities",
            group=group
        )

        ostype_select = ia_selection(
            question="",
            options=group,
            flags=["desktop", "desktop_sod", "server"]
        )

        return ostype_select
