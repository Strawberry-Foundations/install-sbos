from sbos_installer.core.process import Runner
from sbos_installer.utils import modify_file_entry
from sbos_installer.utils.colors import *


def configure_grub(disk: str):
    runner = Runner(True)

    modify_file_entry("/mnt/etc/default/grub", 'GRUB_CMDLINE_LINUX=""', 'GRUB_CMDLINE_LINUX="overlay=yes"')
    modify_file_entry("/mnt/etc/default/grub", 'Debian', 'StrawberryOS')
    modify_file_entry(
        file_path="/mnt/etc/grub.d/10_linux",
        search_string='${GRUB_DISTRIBUTOR} GNU/Linux',
        replace_string='${GRUB_DISTRIBUTOR} (Chocolate Crisps)'
    )

    print(f"{BOLD}{GREEN}Installing GRUB ...{CRESET}")
    runner.run(
        f"grub-install --efi-directory=/mnt/boot/efi --boot-directory=/mnt/boot/ --bootloader-id=StrawberryOS {disk}")
    runner.run(f"chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg")


def configure_systemd_boot(disk: str):
    runner = Runner(True)

    print(f"{BOLD}{GREEN}Installing systemd-boot ...{CRESET}")
    print(f"{BOLD}{YELLOW}systemd-boot is currently not supported.{CRESET}")
    configure_grub(disk)

    runner.run(f"apt install -y systemd-boot")
    runner.run(f"bootctl --esp-path=/mnt/boot/efi install")

    print(f"{BOLD}{GREEN}Configuring systemd-boot ...{CRESET}")
    with open("/mnt/boot/loader/loader.conf", "w+") as _loader_conf:
        _loader_conf.write("default strawberryos.conf\n")
        _loader_conf.write("timeout 3\n")
        _loader_conf.write("editor 0\n")
