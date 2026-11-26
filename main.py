#!/usr/bin/env python3
"""Ship the finished front-page image to the output folder.

The entry image lives next to this script. This script copies it into
the directory named by MAKEFUN_OUTPUT_DIR (or /output when that
variable is unset), checks the copy is byte-for-byte the same size as
the original, and reports where it wrote the file.
"""

import os
import shutil
import sys

DEFAULT_OUT_DIR = "/output"
SOURCE_NAME = "entry.png"


def source_path():
    """Path of the bundled image sitting beside this script."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, SOURCE_NAME)


def destination_path():
    """Target path inside the configured output directory."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUT_DIR)
    return os.path.join(out_dir, SOURCE_NAME)


def deliver():
    """Copy the image and confirm the copy matches the original."""
    origin = source_path()
    target = destination_path()
    if not os.path.isfile(origin):
        # Fail loudly rather than silently producing an empty output dir.
        print(f"ERROR: bundled image not found: {origin}", file=sys.stderr)
        sys.exit(1)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copyfile(origin, target)
    expected = os.path.getsize(origin)
    actual = os.path.getsize(target)
    if actual != expected:
        print(f"ERROR: copied file is {actual} bytes, expected {expected}",
              file=sys.stderr)
        sys.exit(1)
    print(f"Wrote {target}")
    return target


if __name__ == "__main__":
    deliver()
