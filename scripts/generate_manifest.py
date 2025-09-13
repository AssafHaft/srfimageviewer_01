#!/usr/bin/env python3
"""
Generate images/manifest.json listing images for the TV viewer.

Usage:
  python scripts/generate_manifest.py            # one-off generate
  python scripts/generate_manifest.py --watch    # regenerate on changes

Options:
  --dir PATH     Source images directory (default: repo/images)
  --out PATH     Output manifest path (default: <dir>/manifest.json)
  --interval N   Watch poll interval seconds (default: 2.0)

Manifest format:
  { "images": ["file1.jpg", "sub/f2.png", ...] }

The viewer prefixes entries that do not start with "images/" automatically.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

SUPPORTED_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"}


def is_image(path: Path) -> bool:
    return path.suffix.lower() in SUPPORTED_EXT


def enumerate_images(root: Path) -> List[str]:
    """Return a sorted list of relative image paths under root (recursive)."""
    images: List[str] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.name.lower() == "manifest.json":
            continue
        if not is_image(p):
            continue
        rel = p.relative_to(root).as_posix()
        images.append(rel)
    images.sort(key=lambda s: s.lower())
    return images


def write_manifest(out_path: Path, images: Iterable[str]) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "count": len(list(images)),
        "images": list(images),
    }
    # Write atomically
    tmp = out_path.with_suffix(out_path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    tmp.replace(out_path)


def snapshot(root: Path) -> Dict[str, Tuple[int, int]]:
    """Return a map of relpath -> (size, mtime_ns) to detect changes."""
    snap: Dict[str, Tuple[int, int]] = {}
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.name.lower() == "manifest.json":
            continue
        if not is_image(p):
            continue
        try:
            st = p.stat()
        except OSError:
            continue
        snap[p.relative_to(root).as_posix()] = (st.st_size, getattr(st, "st_mtime_ns", int(st.st_mtime * 1e9)))
    return snap


def run_once(images_dir: Path, out_path: Path) -> None:
    imgs = enumerate_images(images_dir)
    write_manifest(out_path, imgs)
    print(f"Wrote {out_path} with {len(imgs)} image(s)")


def run_watch(images_dir: Path, out_path: Path, interval: float) -> None:
    print(f"Watching {images_dir} for changes (interval {interval:.1f}s)...")
    prev = {}  # type: Dict[str, Tuple[int, int]]
    while True:
        try:
            snap = snapshot(images_dir)
            if snap != prev:
                prev = snap
                imgs = sorted(snap.keys(), key=lambda s: s.lower())
                write_manifest(out_path, imgs)
                print(f"Updated {out_path} with {len(imgs)} image(s)")
        except KeyboardInterrupt:
            print("\nStopped.")
            return
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(interval)


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    default_images = (script_dir.parent / "images").resolve()
    parser = argparse.ArgumentParser(description="Generate images/manifest.json for the viewer")
    parser.add_argument("--dir", dest="images_dir", type=Path, default=default_images, help="Images directory (default: repo/images)")
    parser.add_argument("--out", dest="out_path", type=Path, default=None, help="Output manifest path (default: <dir>/manifest.json)")
    parser.add_argument("--watch", action="store_true", help="Watch for changes and regenerate")
    parser.add_argument("--interval", type=float, default=2.0, help="Watch poll interval seconds (default: 2.0)")
    args = parser.parse_args()

    images_dir: Path = args.images_dir.resolve()
    out_path: Path = (args.out_path if args.out_path else images_dir / "manifest.json").resolve()

    if not images_dir.exists():
        raise SystemExit(f"Images directory not found: {images_dir}")

    if args.watch:
        run_watch(images_dir, out_path, args.interval)
    else:
        run_once(images_dir, out_path)


if __name__ == "__main__":
    main()

