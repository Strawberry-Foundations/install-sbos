from sbos_installer.core.ui.radiobutton import RadioButton
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

        btn_desktop = RadioButton(
            label="StrawberryOS Desktop",
            description="The standard version of StrawberryOS - With all the necessary tools from us"
            "and a selection of desktops",
            state=True,
            group=group
        )

        btn_desktop_sod = RadioButton(
            label="StrawberryOS Desktop with Open Directory",
            description="StrawberryOS with configured Open Directory. Useful for schools, workplaces,"
            "and also the one or other private use",
            state=False,
            group=group
        )

        btn_server = RadioButton(
            label="StrawberryOS Server",
            description="A minimal environment of StrawberryOS without a desktop. Includes additional server utilities",
            state=False,
            group=group
        )


        for button in group:
            btn, description = button.build()
            rprint(btn)
            rprint(description)
            rprint(" " * 90)

        input()
        return ""
