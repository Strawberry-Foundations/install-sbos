from sbos_installer.core.ui.select_button import SelectButton, SelectButtonGroup
from sbos_installer.core.ui.screen import Screen
from sbos_installer.var import Versions


class EditionView(Screen):
    title = "Choose the type of installation"

    def __init__(self):
        view = self.render
        super().__init__(title=self.title, view=view)

    def render(self):
        self.console.print("StrawberryOS has different editions to choose from\n", justify="center")
        self.console.show_cursor(False)

        group = SelectButtonGroup()

        group.append(
            SelectButton(
                label=f"StrawberryOS Desktop ({Versions.desktop})",
                description="The standard version of StrawberryOS - With all the necessary tools "
                "from us and a selection of desktops"
            )
        )

        group.append(
            SelectButton(
                label=f"StrawberryOS Desktop with Open Directory ({Versions.desktop_sod})",
                description="StrawberryOS with configured Open Directory. Useful for schools, workplaces, and "
                "also the one or other private use"
            )
        )

        group.append(
            SelectButton(
                label=f"StrawberryOS Server ({Versions.server})",
                description="A minimal environment of StrawberryOS without a desktop. Includes additional server utilities",
                group=group
            )
        )


        edition_select = group.selection(flags=["desktop", "desktop_sod", "server"])

        self.console.show_cursor(True)

        return edition_select
