#!/usr/bin/env python3

import subprocess


def notify(message):
    subprocess.Popen(['notify-send', 'CertChecker', message])
