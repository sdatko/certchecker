#!/usr/bin/env python3

import argparse
import sched
import signal
import sys
import time

from certchecker.expiration import get_cert_expiration_from_file
from certchecker.expiration import get_cert_expiration_from_host
from certchecker.expiration import get_days_to_expiration
from certchecker.utils import notify


continuous_interval = 10
continuous_scheduler = sched.scheduler(time.time, time.sleep)


def single_step(args):
    if args.file is not None:
        date = get_cert_expiration_from_file(args.file)
        identifier = args.file
    if args.host is not None:
        date = get_cert_expiration_from_host(args.host, args.port)
        identifier = '{}:{}'.format(args.host, args.port)

    days = get_days_to_expiration(date)

    return identifier, days


def single_run(args):
    identifier, days = single_step(args)

    print(days)

    if days < 0:
        sys.exit(1)


def continuous_step(scheduler, args):
    continuous_scheduler.enter(delay=continuous_interval, priority=1,
                               action=continuous_step,
                               argument=(continuous_scheduler, args))

    identifier, days = single_step(args)

    print(identifier, days)

    if days < 0:
        notify(f'The {identifier} certificate has expired!')


def continuous_run(args):
    notify('Started daemon.')

    try:
        continuous_scheduler.enter(delay=continuous_interval, priority=1,
                                   action=continuous_step,
                                   argument=(continuous_scheduler, args))
        continuous_scheduler.run()
    except KeyboardInterrupt:
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--daemon', action="store_true", default=False,
                        help='run continuously in background')
    parser.add_argument('-f', '--file', type=str, default=None,
                        help='path to local file to verify')
    parser.add_argument('-t', '--host', type=str, default=None,
                        help='host with certificate to verify')
    parser.add_argument('-p', '--port', type=int, default=443,
                        help='port on host with certificate, default 443')
    args = parser.parse_args()

    if not (args.file or args.host):
        parser.error('At least one of --file or --host is required.')

    if args.daemon:
        continuous_run(args)
    else:
        single_run(args)


def handle_sigterm(*args):
    raise KeyboardInterrupt()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, handle_sigterm)
    main()
