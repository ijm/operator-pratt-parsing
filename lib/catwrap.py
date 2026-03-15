#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Concatenate files with <file/> tag wrapping.

Usage:
    catfiles.py [-p PREFIX_FILE] [-o OUTPUT_FILE] [FILE ...]

The prefix file (-p) is output first, verbatim and unwrapped.
Each remaining file is wrapped in <file name="filename">...</file> tags.
Output goes to stdout unless -o is specified.
"""

import argparse
import sys


def write_ensuring_newline(data: bytes, out) -> None:
    out.write(data)
    if data and not data.endswith(b"\n"):
        out.write(b"\n")


def write_verbatim(path: str, out) -> None:
    with open(path, "rb") as f:
        write_ensuring_newline(f.read(), out)


def write_wrapped(path: str, out) -> None:
    out.write(f'<file name="{path}">'.encode())
    with open(path, "rb") as f:
        write_ensuring_newline(f.read(), out)
    out.write(b"</file>\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Concatenate files, wrapping general files in <file/> tags."
    )
    parser.add_argument("-p", metavar="PREFIX", help="prefix file, output verbatim first")
    parser.add_argument("-o", metavar="OUTPUT", type=argparse.FileType("wb"),
                        default=sys.stdout.buffer, help="output file (default: stdout)")
    parser.add_argument("files", nargs="*", metavar="FILE", help="files to wrap and concatenate")
    args = parser.parse_args()

    if args.p:
        write_verbatim(args.p, args.o)
        args.o.write(b"\n")
    for path in args.files:
        write_wrapped(path, args.o)


if __name__ == "__main__":
    main()
