from sbos_installer.utils.colors import *
from sbos_installer.views.error import ErrorView

import subprocess
import os


def run(command):
    try:
        result = subprocess.run(command, shell=True, check=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Command '{command}' failed with error:\n{e.stderr}"


def check_root_permissions():
    return os.geteuid() == 0


def check_uefi_capability():
    return os.path.exists("/sys/firmware/efi/fw_platform_size")


def show_error(command: subprocess.CompletedProcess[bytes]):
    ErrorView(
        "Something went wrong during the installation of StrawberryOS and the installation cannot continue.\n\n"
        f"{YELLOW}{UNDERLINE}Error Details{CRESET}\n"
        f"Command '{GREEN}{command.args}{CRESET}' returned with return code {RED}{command.returncode}{CRESET}\n\n"
        f"{YELLOW}{UNDERLINE}Command Output{CRESET}\n{command.stdout}\n\n"
        f"{YELLOW}{UNDERLINE}Command Error{CRESET}\n{command.stderr}\n\n"
        f"{YELLOW}{UNDERLINE}Important{CRESET}\n"
        "This is not normal behavior and should be reported to the StrawberryOS team.\n"
        "Please provide the error details above and the output of the installer to the developers.\n"
        f"{LIGHT_BLUE}https://github.com/Strawberry-Foundations/install-sbos{CRESET}"
    )

class Runner:
    def __init__(self, show_logs: bool):
        self.show_logs = show_logs

    def run(self, run_command: str):
        try:
            if self.show_logs:
                command = subprocess.run(run_command, shell=True)

                if command.returncode != 0:
                    show_error(command)
                    
            else:
                command = subprocess.run(run_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                if command.returncode != 0:
                    show_error(command)
                    
                return command.stdout

        except subprocess.CalledProcessError as e:
            return f"Command '{run_command}' failed with error:\n{e.stderr}"
