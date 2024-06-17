import sys

args = sys.argv[1:]

DEV_FLAG_DEV_MODE = False
DEV_FLAG_SKIP_DISK_INPUT = False
DEV_FLAG_SKIP_BOOTSTRAP = False
DEV_FLAG_SKIP_INITRAMFS = False
DEV_FLAG_SKIP_POST_SETUP = False

if '--enable-dev' in args:
    ENABLE_DEV_MODE = True

if any(arg.startswith('-f') and 'DEV_FLAG_SKIP_BOOTSTRAP' in arg for arg in args):
    DEV_FLAG_SKIP_BOOTSTRAP = True

if any(arg.startswith('-f') and 'DEV_FLAG_SKIP_INITRAMFS' in arg for arg in args):
    DEV_FLAG_SKIP_INITRAMFS = True

if any(arg.startswith('-f') and 'DEV_FLAG_SKIP_DISK_INPUT' in arg for arg in args):
    DEV_FLAG_SKIP_DISK_INPUT = True

if any(arg.startswith('-f') and 'DEV_FLAG_SKIP_POST_SETUP' in arg for arg in args):
    DEV_FLAG_SKIP_POST_SETUP = True

if DEV_FLAG_DEV_MODE:
    DEV_FLAG_SKIP_BOOTSTRAP = True
    DEV_FLAG_SKIP_INITRAMFS = True
    DEV_FLAG_SKIP_DISK_INPUT = True
    DEV_FLAG_SKIP_POST_SETUP = True