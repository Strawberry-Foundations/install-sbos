from sbos_installer.var import ROOT_MNT


def configure_hostname(hostname: str):
    with open(f"{ROOT_MNT}etc/hostname", 'w') as file:
        file.write(hostname)
