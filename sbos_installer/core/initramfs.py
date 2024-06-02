from sbos_installer.core.process import Runner
from sbos_installer.cli.selection import ia_selection
from sbos_installer.cli.parser import parse_bool
from sbos_installer.utils.colors import *

import os


def setup_initramfs(data_block_device):
    show_logs = parse_bool(ia_selection(
        "The next step is to configure the initramfs. Would you like to view the logs during the installation?",
        options=["No", "Yes"]
    ))

    runner = Runner(show_logs)

    location = "/mnt"
    binder = f"bwrap --bind {location} / --dev /dev --bind /sys /sys --bind /proc /proc --bind /tmp /tmp"

    print("\nConfiguring StrawberryOS initramfs ... ")

    print("Downloading initramfs tools ...")
    runner.run("wget https://github.com/Strawberry-Foundations/sbos-scripts/archive/refs/heads/main.tar.gz")

    print("Extracting initramfs tools ...")
    runner.run("tar xfz main.tar.gz")

    print("Patching initramfs init script ...")

    with open(f"{os.getcwd()}/sbos-scripts-main/overlay-init", "r") as _initramfs_script:
        initramfs_init = _initramfs_script.read()

    patched_initramfs_init = initramfs_init.replace("/dev/data_partition", data_block_device)

    with open(f"{os.getcwd()}/sbos-scripts-main/overlay-init", "w") as _initramfs_script:
        _initramfs_script.write(patched_initramfs_init)

    print(f"Installing initramfs-tools to {location}")

    runner.run(f"mv sbos-scripts-main/overlay-hook {location}/etc/initramfs-tools/hooks/overlay")
    runner.run(f"mv sbos-scripts-main/overlay-init {location}/etc/initramfs-tools/scripts/init-bottom/overlay")

    runner.run(f"mv sbos-scripts-main/regen-initramfs {location}/usr/local/bin/regen-initramfs")
    runner.run(f"chmod a+x {location}/usr/local/bin/regen-initramfs")
    runner.run(f"chmod a+x {location}/etc/initramfs-tools/hooks/overlay")
    runner.run(f"chmod a+x {location}/etc/initramfs-tools/scripts/init-bottom/overlay")
    runner.run(f"chmod 775 {location}/etc/initramfs-tools/hooks/overlay")
    runner.run(f"chmod 775 {location}/etc/initramfs-tools/scripts/init-bottom/overlay")

    print(f"Updating initramfs")
    runner.run(binder + " regen-initramfs")

    print(f"Cleaning up ...")
    runner.run(f"rm -rf sbos-scripts-main")
    runner.run(f"rm -rf main.tar* ")

    print(f"Finished initramfs configuration ")