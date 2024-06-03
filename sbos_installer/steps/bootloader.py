from sbos_installer.core.process import Runner
from sbos_installer.utils.colors import *

def configure_bootloader():
    print(f"{BOLD}{GREEN}Configuring GRUB ...{CRESET}")
    with open("/mnt/etc/default/grub", "+") as _grub_default:
        _content = _grub_default.read()
        _content = _content.replace('GRUB_CMDLINE_LINUX=""', 'GRUB_CMDLINE_LINUX="overlay=yes"')
        _grub_default.write(_content)