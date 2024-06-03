from sbos_installer.core.process import Runner
from sbos_installer.utils.colors import *


def configure_bootloader(disk: str):
    runner = Runner(True)
    print(f"{BOLD}{GREEN}Configuring GRUB ...{CRESET}")
    with open("/mnt/etc/default/grub", "w+") as _grub_default:
        _content = _grub_default.read()
        _content = _content.replace('GRUB_CMDLINE_LINUX=""', 'GRUB_CMDLINE_LINUX="overlay=yes"')
        _grub_default.write(_content)

    print(f"{BOLD}{GREEN}Installing GRUB ...{CRESET}")
    runner.run(f"grub-install --efi-directory=/mnt/boot/efi --boot-directory=/mnt/boot/ --bootloader-id=StrawberryOS {disk}")
    runner.run(f"chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg")