#!/usr/bin/env python3
"""Publish the finished treasure map as the competition entry.

The map itself is composed ahead of time by build/label_map.py and
committed as assets/map.png. This entry program performs no drawing:
it copies those committed bytes to /output/entry.png and then reads
the copy back to confirm its SHA-256 matches the source, guaranteeing
the judged file is exactly the map that was reviewed.

Exit status is 0 on success, 1 if the source is missing or the copy
does not verify.
"""
import hashlib
import sys
from pathlib import Path

ENTRY_DIR = Path(__file__).resolve().parent
MAP_FILE = ENTRY_DIR / "assets" / "map.png"
OUT_DIR = Path("/output")
OUT_FILE = OUT_DIR / "entry.png"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run() -> int:
    if not MAP_FILE.exists():
        print(f"error: committed map not found at {MAP_FILE}",
              file=sys.stderr)
        return 1

    blob = MAP_FILE.read_bytes()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_bytes(blob)

    copied = OUT_FILE.read_bytes()
    if digest(copied) != digest(blob):
        print("error: /output/entry.png failed SHA-256 verification",
              file=sys.stderr)
        return 1

    print(f"entry.png written: {len(copied)} bytes, "
          f"sha256 {digest(copied)}")
    return 0


if __name__ == "__main__":
    sys.exit(run())
