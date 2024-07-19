from sbos_installer.core.ui.screen import Screen
from sbos_installer.cli.selection import ia_selection
from sbos_installer.cli.parser import parse_bool
from sbos_installer.utils.colors import *

from rich.text import Text
from rich.padding import Padding
from getpass import getpass


class UserView(Screen):
    title = "Setting up users"

    def __init__(self):
        view = self.render
        super().__init__(title=self.title, view=view)

    def render(self):
        self.console.print(Padding(Text.from_ansi(
            "User accounts are an important part of the installation of the operating system. "
            "First enter a new root password, which is used for the root user.\n\n"
            f"{YELLOW}[!]{GRAY} The password is not displayed for security reasons\n\n"
        ), (0, 8)))

        root_password = None

        username = None
        password = None

        while True:
            root_password = self.setup_password()
            if root_password.strip() == "":
                self.console.print(Padding(Text.from_ansi(f"{YELLOW}{BOLD}Password cannot be empty{CRESET}"), (0, 8)))
                print()
                continue
            break

        print()
        new_user = parse_bool(ia_selection("Do you want to create a new user?", options=["Yes", "No"], padding=8))

        if new_user:
            _username = True
            while _username:
                username = input(f"        {CRESET}Enter username:  {GRAY}")
                if username.strip() == "":
                    self.console.print(Padding(Text.from_ansi(f"{YELLOW}{BOLD}Username cannot be empty{CRESET}"), (0, 8)))
                    print()
                else:
                    _username = False

            pw = True
            while pw:
                password = self.setup_password(name=username)
                if password.strip() == "":
                    self.console.print(Padding(Text.from_ansi(f"{YELLOW}{BOLD}Password cannot be empty{CRESET}"), (0, 8)))
                    print()
                else:
                    pw = False

            print()
            add_to_sudo = parse_bool(ia_selection(
                question=f"Would you like to add '{CYAN}{BOLD}{username}{CRESET}' to the »{GREEN} sudo {CRESET}« group?",
                options=["Yes", "No"],
                padding=8
            ))

            user_setup = {
                "users": {
                    "root": {
                        "password": root_password
                    },
                    username: {
                        "password": password,
                        "sudo_user": add_to_sudo
                    }
                }
            }
        else:
            user_setup = {
                "users": {
                    "root": {
                        "password": root_password
                    },
                }
            }

        print(CRESET)

        return user_setup

    def setup_password(self, name="root"):
        _password = getpass(f"{CRESET}        Password for {name}: ")
        _password_confirm = getpass(f"        Confirm password for {name}: ")

        if _password != _password_confirm:
            self.console.print(Padding(Text.from_ansi(f"{YELLOW}{BOLD}Passwords does not match{CRESET}"), (0, 8)))
            print()
            self.setup_password()

        return _password
