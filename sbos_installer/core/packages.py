init_package = (
    "dbus,dbus-bin,dbus-daemon,dbus-session-bus-common,dbus-system-bus-common,dbus-user-session,"
    "libpam-systemd,apt-utils,apt-transport-https,ca-certificates,bash,bzip2,initramfs-tools-core,"
    "initramfs-tools,linux-image-amd64,busybox-static,network-manager,wget,curl"
)

package_list = {
    "base": "zstd grub-efi kbd locales locales-all bash-completion sudo lvm2",
    "base-dev": "git gcc make g++ build-essential linux-headers-amd64",
    "utils": "neofetch htop btop",
    "python3": "python3 python3-dev python3-pip python-is-python3"
}
