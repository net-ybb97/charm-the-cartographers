#!/usr/bin/env python3
"""Entry program for make.fun "Charm the Cartographers".

The treasure map is composed ahead of time by build/label_map.py and
stored in assets/map.png. This program's only job is to publish those
exact bytes to /output/entry.png, so every run of the entry produces
the identical map.
"""
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "assets" / "map.png"
DEST_DIR = Path("/output")
DEST = DEST_DIR / "entry.png"


def publish() -> int:
    if not SOURCE.is_file():
        print(f"source image missing: {SOURCE}", file=sys.stderr)
        return 1
    payload = SOURCE.read_bytes()
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    with DEST.open("wb") as fh:
        fh.write(payload)
    written = DEST.read_bytes()
    if hashlib.sha256(written).digest() != hashlib.sha256(payload).digest():
        print("verification failed: written bytes differ from source",
              file=sys.stderr)
        return 1
    print(f"published {DEST} ({len(written)} bytes, sha256 verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(publish())
