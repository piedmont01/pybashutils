#!/usr/bin/env python
"""
gets interface IPv4 and IPv6 public addresses using libCURL
This uses the "reflector" method, which I feel is more reliable for finding public-facing IP addresses,
WITH THE CAVEAT that man-in-the-middle, etc. attacks can defeat the reflector method.

PyCurl does not have a context manager.

https://ident.me  ipv6 and ipv4
https://api.ipify.org # ipv4 only
"""
from argparse import ArgumentParser
from pybashutils.getIP import getip


def main():
    p = ArgumentParser()
    p.add_argument('iface', help='network interface to use', nargs='?')
    p.add_argument('--url', help='plain text server',
                   default='https://ident.me')
    P = p.parse_args()

    addr = getip(P.url, P.iface)
    for a in addr:
        print(a)


if __name__ == '__main__':
    main()
