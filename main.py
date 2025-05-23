import sys
from modules.utils import extract_settings
from modules.api import run


def main(args):
    run(extract_settings(args))


if __name__ == '__main__':
    main(sys.argv)