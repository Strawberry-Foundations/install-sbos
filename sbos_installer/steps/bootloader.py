from sbos_installer.core.process import Runner
from sbos_installer.cli.selection import ia_selection
from sbos_installer.utils import modify_file_entry
from sbos_installer.utils.colors import *


def configure_bootloader(disk: str):
    selection = ia_selection(
        question="What bootloader would you like to use?",
        options=["GRUB", "systemd-boot"],
        flags=["(Recommended)", "(Experimental support)", ]
    )

    if selection == "systemd-boot":
        configure_systemd_boot()
    else:
        configure_grub(disk)


def configure_grub(disk: str):
    runner = Runner(True)

    modify_file_entry("/mnt/etc/default/grub", 'GRUB_CMDLINE_LINUX=""', 'GRUB_CMDLINE_LINUX="overlay=yes"')
    modify_file_entry("/mnt/etc/default/grub", 'Debian', 'StrawberryOS')

    print(f"{BOLD}{GREEN}Installing GRUB ...{CRESET}")
    runner.run(
        f"grub-install --efi-directory=/mnt/boot/efi --boot-directory=/mnt/boot/ --bootloader-id=StrawberryOS {disk}")
    runner.run(f"chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg")

    modify_file_entry("/mnt/boot/grub/grub.cfg", 'GNU/Linux', '(Chocolate Crisps)')


def configure_systemd_boot():
    runner = Runner(True)

    print(f"{BOLD}{GREEN}Installing systemd-boot ...{CRESET}")

    runner.run(f"apt install -y systemd-boot")
    runner.run(f"bootctl --esp-path=/mnt/boot/efi install")

    print(f"{BOLD}{GREEN}Configuring systemd-boot ...{CRESET}")
    with open("/mnt/boot/loader/loader.conf", "w+") as _loader_conf:
        _loader_conf.write("default strawberryos.conf\n")
        _loader_conf.write("timeout 3\n")
        _loader_conf.write("editor 0\n")
