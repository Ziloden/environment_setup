#!/usr/bin/env python3
import argparse
from lib.config_management import backup, restore

def main():
    parser = argparse.ArgumentParser(
        prog='Config Manager',
        description='Tool for maintaining system configurations between installs.',
    )
    mode_group = parser.add_mutually_exclusive_group()
    parser.add_argument(
        '-t',
        '--target',
        choices=['common', 'laptop', 'desktop'],
        default='common',
        help="Target environment."
    )
    parser.add_argument(
        '-m',
        '--manifest',
        default='./configuration/backup_manifests/common.json',
        help='The path to a manifest of what to process.',
    )
    parser.add_argument(
        '-u',
        '--user',
        help="User to target for home directory operations."
    )
    mode_group.add_argument(
        '-b',
        '--backup',
        dest='mode',
        action='store_const',
        const='backup',
        help='Mode to backup configuration.',
    )
    mode_group.add_argument(
        '-r',
        '--restore',
        dest='mode',
        action='store_const',
        const='restore',
        help='Mode to restore configuration.',
    )
    options = parser.parse_args()

    match options.mode:
        case 'backup':
            print("Running backup...")
            backup(options.manifest, options.target, options.user)
        case 'restore':
            print("Running restore...")
            restore(options.manifest, options.target, options.user)


if __name__ == "__main__":
    main()