from sbos_installer.cli.selection import ia_selection
from sbos_installer.cli.parser import parse_bool
from sbos_installer.utils.colors import *
from getpass import getpass

import subprocess


def setup_user():
    print(f"\n{GREEN}{BOLD} -- User setup --{CRESET}")

    username = None
    password = None

    def setup_password(name="root"):
        _password = getpass(f"Password for {name}: ")
        _password_confirm = getpass(f"Confirm password for {name}: ")

        if _password != _password_confirm:
            print(f"{YELLOW}{BOLD}Passwords does not match{CRESET}")
            setup_password()

        return _password

    root_password = setup_password()

    new_user = parse_bool(ia_selection("Do you want to create a new user?", options=["Yes", "No"]))

    if new_user:
        uname = True
        while uname:
            username = input("Enter username: ")
            if username.strip() == "":
                print(f"{YELLOW}{BOLD}Username cannot be empty{CRESET}")
            else:
                uname = False

        pw = True
        while pw:
            password = setup_password(name=username)
            if password.strip() == "":
                print(f"{YELLOW}{BOLD}Password cannot be empty{CRESET}")
            else:
                pw = False

        add_to_sudo = parse_bool(ia_selection(
            question=f"\nWould you like to add '{CYAN}{BOLD}{username}{CRESET}' to the »{GREEN} sudo {CRESET}« group?",
            options=["Yes", "No"])
        )

        user_setup = {
            "users": {
                "root": root_password,
                username: {
                    "password": password,
                    "sudo_user": add_to_sudo
                }
            }
        }
    else:
        user_setup = {
            "users": {
                "root": root_password,
            }
        }

    return user_setup


def configure_users(user_data: dict):
    print(f"{BOLD}{GREEN}Configuring root user ...{CRESET}")
    command = f'echo "root:{user_data["users"]["root"]}" | chpasswd'

    subprocess.run(
        ['chroot', '/mnt', '/bin/bash', '-c', command],
        check=True,
        text=True,
        capture_output=True
    )

    if len(user_data["users"]) > 1:
        print(f"{BOLD}{GREEN}Configuring additional user ...{CRESET}")

        for username, password in user_data["users"].items():
            if username == "root":
                continue

            if user_data["users"][username]["sudo_user"]:
                command = f'useradd -m -G sudo -s /bin/bash {username}'
            else:
                command = f'useradd -m -s /bin/bash {username}'

            subprocess.run(
                ['chroot', '/mnt', '/bin/bash', '-c', command],
                check=True,
                text=True,
                capture_output=True
            )

            command = f'echo "{username}:{user_data["users"]["password"][username]}" | chpasswd'

            subprocess.run(
                ['chroot', '/mnt', '/bin/bash', '-c', command],
                check=True,
                text=True,
                capture_output=True
            )