#!/usr/bin/env python3
"""Split a tar archive into several smaller, independently extractable archives.

Each output part is a complete, valid tar archive: no reassembly needed.
Members are never cut in half; a member larger than the size limit simply
gets a part of its own.

Usage:
    tarsplit.py ARCHIVE --size 100M [--out-dir DIR] [--prefix NAME]
    tarsplit.py ARCHIVE --parts 4   [--out-dir DIR] [--prefix NAME]

Examples:
    tarsplit.py backup.tar.gz --size 2G
    tarsplit.py backup.tar --parts 5 --out-dir /tmp/chunks
"""

import argparse
import os
import sys
import tarfile

SUFFIXES = {"k": 1024, "m": 1024**2, "g": 1024**3, "t": 1024**4}


def parse_size(text):
    text = text.strip().lower().rstrip("b")
    if text and text[-1] in SUFFIXES:
        return int(float(text[:-1]) * SUFFIXES[text[-1]])
    return int(text)


def split_name(path):
    """Return (stem, extension) so part names keep the original suffixes."""
    base = os.path.basename(path)
    for ext in (".tar.gz", ".tar.bz2", ".tar.xz", ".tar.zst", ".tgz", ".tbz2", ".txz"):
        if base.endswith(ext):
            return base[: -len(ext)], ext
    stem, ext = os.path.splitext(base)
    return stem, ext or ".tar"


def write_mode(ext):
    if ext in (".tar.gz", ".tgz"):
        return "w:gz"
    if ext in (".tar.bz2", ".tbz2"):
        return "w:bz2"
    if ext in (".tar.xz", ".txz"):
        return "w:xz"
    return "w"


def pack(sizes, limit):
    """Greedily assign each member index to a part number."""
    assignment = []
    part, used = 1, 0
    for size in sizes:
        if used and used + size > limit:
            part += 1
            used = 0
        assignment.append(part)
        used += size
    return assignment


def plan(sizes, limit=None, parts=None):
    if limit is not None:
        return pack(sizes, limit)
    # Smallest limit that still fits everything into `parts` archives.
    lo, hi = max(sizes + [1]), max(sum(sizes), 1)
    while lo < hi:
        mid = (lo + hi) // 2
        if pack(sizes, mid)[-1] <= parts:
            hi = mid
        else:
            lo = mid + 1
    return pack(sizes, lo)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("archive")
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--size", help="max size per part, e.g. 500M, 2G")
    group.add_argument("--parts", type=int, help="target number of parts")
    ap.add_argument("--out-dir", default=".", help="where to write parts (default: .)")
    ap.add_argument("--prefix", help="base name for parts (default: source name)")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    stem, ext = split_name(args.archive)
    prefix = args.prefix or stem
    os.makedirs(args.out_dir, exist_ok=True)

    # Pass 1: read the index so we can plan the parts up front.
    with tarfile.open(args.archive, "r:*") as src:
        members = src.getmembers()
    if not members:
        sys.exit("archive contains no members")

    sizes = [m.size if m.isfile() else 0 for m in members]
    assignment = plan(sizes,
                      limit=parse_size(args.size) if args.size else None,
                      parts=args.parts)
    total_parts = assignment[-1]
    width = max(3, len(str(total_parts)))

    # Pass 2: copy members into their part.
    out, current, written = None, None, 0
    try:
        with tarfile.open(args.archive, "r:*") as src:
            for member, part in zip(members, assignment):
                if part != current:
                    if out:
                        out.close()
                    current = part
                    path = os.path.join(
                        args.out_dir, f"{prefix}.part{part:0{width}d}{ext}")
                    out = tarfile.open(path, write_mode(ext))
                    if not args.quiet:
                        print(f"-> {path}")
                data = src.extractfile(member) if member.isfile() else None
                out.addfile(member, data)
                written += 1
    finally:
        if out:
            out.close()

    if not args.quiet:
        print(f"{written} members written to {total_parts} part(s)")


if __name__ == "__main__":
    main()
