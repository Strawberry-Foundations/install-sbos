from sbos_installer.cli.parser import parse_bool
from sbos_installer.cli.selection import ia_selection
from sbos_installer.core.process import Runner
from sbos_installer.utils.colors import *


def _modify_grub_config(file_path, search_string, replace_string):
    with open(file_path, 'r') as file:
        content = file.read()

    modified_content = content.replace(search_string, replace_string)

    with open(file_path, 'w') as file:
        file.write(modified_content)


def configure_bootloader(disk: str):
    selection = parse_bool(ia_selection(
        question="What bootloader would you like to use?",
        options=["GRUB", "systemd-boot"],
        flags=["(Recommended)", "(Experimental support)", ])
    )

    if selection == "systemd-boot":
        _configure_systemd_boot()
    else:
        _configure_grub(disk)


def _configure_grub(disk: str):
    runner = Runner(True)

    _modify_grub_config("/mnt/etc/default/grub", 'GRUB_CMDLINE_LINUX=""', 'GRUB_CMDLINE_LINUX="overlay=yes"')
    _modify_grub_config("/mnt/etc/default/grub", 'Debian', 'StrawberryOS')

    print(f"{BOLD}{GREEN}Installing GRUB ...{CRESET}")
    runner.run(
        f"grub-install --efi-directory=/mnt/boot/efi --boot-directory=/mnt/boot/ --bootloader-id=StrawberryOS {disk}")
    runner.run(f"chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg")


def _configure_systemd_boot():
    runner = Runner(True)
    print(f"{BOLD}{GREEN}Installing systemd-boot ...{CRESET}")
    runner.run(f"bootctl --esp-path=/mnt/boot/efi install")
    print(f"{BOLD}{GREEN}Configuring systemd-boot ...{CRESET}")
    with open("/mnt/boot/loader/loader.conf", "w+") as _loader_conf:
        _loader_conf.write("default strawberryos.conf\n")
        _loader_conf.write("timeout 3\n")
        _loader_conf.write("editor 0\n")
