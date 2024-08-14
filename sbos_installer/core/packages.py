init_package = (
    "dbus,dbus-bin,dbus-daemon,dbus-session-bus-common,dbus-system-bus-common,dbus-user-session,"
    "libpam-systemd,apt-utils,apt-transport-https,ca-certificates,bash,bzip2,initramfs-tools-core,"
    "initramfs-tools,linux-image-amd64,busybox-static,network-manager,wget,curl"
)

base_package_list = {
    "base": "zstd grub-efi kbd locales locales-all bash-completion sudo lvm2",
    "server": "git curl wget htop net-tools fail2ban openssh-server rsync screen openssl",
    "base-dev": "git gcc make g++ build-essential linux-headers-amd64",
    "utils": "neofetch htop btop",
    "python3": "python3 python3-dev python3-pip python-is-python3",
    "firmware-linux-free": "firmware-linux-free",
    "firmware-linux-non-free": "firmware-linux-non-free firmware-misc-non-free",
    "amd-graphics": "firmware-amd-graphics libgl1-mesa-dri libglx-mesa0 mesa-vulkan-drivers xserver-xorg-video-all",
}


package_list = {
    "Development Utilities": "base-dev",
    "General Utilities": "utils",
    "Python Runtime": "python3",
    "Open Source Firmware": "firmware-linux-free",
    "AMD Graphics": "amd-graphics",
}
