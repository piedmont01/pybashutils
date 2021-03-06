#!/usr/bin/env python
"""
recursively find video files based on extension.

"""
from pathlib import Path
import subprocess
from argparse import ArgumentParser


def findvid(path: Path):
    """
    recursive file search in Pure Python.
    about 10 times slower than Linux find, but platform-independent.
    """
    ext = ['avi', 'mov', 'mp4', 'mpg', 'mpeg', 'webm', 'ogv', 'mkv', 'wmv']
    path = Path(path).expanduser()

    for e in ext:
        print(f'searching *.{e}\r', end="", flush=True)
        # need sorted() for "if not flist" to work.
        flist = sorted(path.glob(f'**/*.{e}'))
        if not flist:
            continue

        print('\n'.join(map(str, flist)))
# %% clear last line before returning
    print('\r                         \r', end="")


def findvid_linux(path: Path, verbose: bool=False):
    """
    recursive file search using GNU find
    """
    path = Path(path).expanduser()

    cmd = ['find', str(path), '-type', 'f',
           '-regextype', 'posix-egrep',
           '-iregex', '.*\.(avi|mov|mp4|mpg|mpeg|webm|ogv|mkv|wmv)$']

    if verbose:
        print(' '.join(cmd))

    ret = subprocess.run(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL,
                         universal_newlines=True)

    returncode: int = ret.returncode
    if returncode in (0, 1):
        pass
    elif returncode == 2:
        raise OSError('GNU find error or not found')
    else:
        raise OSError(returncode)

    vids = ret.stdout.split('\n')
    if vids:
        print('\n'.join(vids), end="")


def main():
    p = ArgumentParser()
    p.add_argument('path', help='root path to start recursive search',
                   nargs='?', default='.')
    p.add_argument('-v', '--verbose', action='store_true')
    P = p.parse_args()

    try:
        findvid_linux(P.path, P.verbose)
    except OSError:
        findvid(P.path)


if __name__ == '__main__':
    main()
