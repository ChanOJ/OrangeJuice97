#!/usr/bin/env python3
"""One-time import: download every file of the storage zone (site.json) into site/.

Refuses to run if site/ already holds files, so a later run cannot overwrite the
repository with the remote copy. Each file is checked against its SHA-256.

Usage:  pass-cli run --env-file infra/secrets.env -- python3 scripts/import_storage.py
"""

from __future__ import annotations

import hashlib
import sys
from concurrent.futures import ThreadPoolExecutor

import bunny


def main() -> int:
    zone = bunny.site_config()["storage_zone"]
    if bunny.SITE_DIR.exists() and any(p.is_file() for p in bunny.SITE_DIR.rglob("*")):
        sys.exit(f"{bunny.SITE_DIR} is not empty: refusing to overwrite it.")
    storage = bunny.Storage(zone)
    files, _ = storage.list_recursive()
    print(f"{len(files)} files in storage zone {zone!r}.")

    def fetch(rel: str) -> None:
        data = storage.download(rel)
        expected = files[rel]
        if expected and hashlib.sha256(data).hexdigest().upper() != expected:
            raise RuntimeError(f"Checksum mismatch: {rel}")
        dest = bunny.SITE_DIR / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)

    with ThreadPoolExecutor(8) as pool:
        list(pool.map(fetch, sorted(files)))
    print(f"Downloaded to {bunny.SITE_DIR}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
