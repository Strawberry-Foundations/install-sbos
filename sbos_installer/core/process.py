import subprocess
import os


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

    def run(self, command):
        try:
            if self.show_logs:
                command = subprocess.run(command, shell=True)
                if command.returncode != 0:
                    print(f"Something went wrong while executing '{command}' ...")
                    exit(1)
            else:
                result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        text=True)
                return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Command '{command}' failed with error:\n{e.stderr}"