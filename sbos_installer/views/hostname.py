from sbos_installer.core.ui.screen import Screen


class HostnameView(Screen):
    title = "Configure hostname"

    def __init__(self):
        view = self.render
        super().__init__(title=self.title, view=view)

    def render(self):
        hostname = input("Enter system hostname [strawberryos]: ")
        if hostname.strip() == "":
            return "strawberryos"

        return hostname
