#!/usr/bin/env python3

import argparse
import sys

from certchecker.expiration import get_cert_expiration_from_file
from certchecker.expiration import get_cert_expiration_from_host
from certchecker.expiration import get_days_to_expiration


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, default=None,
                        help='path to local file to verify')
    parser.add_argument('-t', '--host', type=str, default=None,
                        help='host with certificate to verify')
    parser.add_argument('-p', '--port', type=int, default=443,
                        help='port on host with certificate, default 443')
    args = parser.parse_args()

    if not (args.file or args.host):
        parser.error('At least one of --file or --host is required.')

    if args.file is not None:
        date = get_cert_expiration_from_file(args.file)
    if args.host is not None:
        date = get_cert_expiration_from_host(args.host, args.port)

    days = get_days_to_expiration(date)

    print(days)

    if days < 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
