import subprocess


def configure_users(user_data: dict):
    command = f'echo "root:{user_data["users"]["root"]["password"]}" | chpasswd'

    subprocess.run(
        ['chroot', '/mnt', '/bin/bash', '-c', command],
        check=True,
        text=True,
        capture_output=True
    )

    if len(user_data["users"]) > 1:

        for username, password in user_data["users"].items():
            if username == "root":
                continue

            if user_data["users"][username]["sudo_user"]:
                command = f'useradd -m -G sudo -s /bin/bash {username}'
            else:
                command = f'useradd -m -s /bin/bash {username}'

            subprocess.run(
                ['chroot', '/mnt', '/bin/bash', '-c', command],
                check=True,
                text=True,
                capture_output=True
            )

            command = f'echo "{username}:{user_data["users"][username]["password"]}" | chpasswd'

            subprocess.run(
                ['chroot', '/mnt', '/bin/bash', '-c', command],
                check=True,
                text=True,
                capture_output=True
            )
