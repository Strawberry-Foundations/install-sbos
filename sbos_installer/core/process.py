from sbos_installer.utils.colors import *

import subprocess
import os
import sys


def run(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Command '{command}' failed with error:\n{e.stderr}"


def check_root_permissions():
    return os.geteuid() == 0


class Runner:
    def __init__(self, show_logs: bool):
        self.show_logs = show_logs

    def run(self, run_command: str):
        try:
            if self.show_logs:
                command = subprocess.run(run_command, shell=True)

                if command.returncode != 0:
                    print(f"{YELLOW}{BOLD}Something went wrong while installing StrawberryOS ...{CRESET}")
                    sys.exit(1)
            else:
                result = subprocess.run(run_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        text=True)
                return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Command '{run_command}' failed with error:\n{e.stderr}"
