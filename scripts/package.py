#!/usr/bin/env python3
"""Build a deterministic, licensed skill archive and SHA256SUMS using only stdlib."""

import gzip
import hashlib
from pathlib import Path
import re
import tarfile

from install import NAME, REPO, SOURCE, fingerprints


def main():
    fingerprints(SOURCE)  # Reject symbolic links before building.
    if (SOURCE / "LICENSE").read_bytes() != (REPO / "LICENSE").read_bytes():
        raise SystemExit("Skill license and repository license must match.")
    match = re.search(r'^  version: "(\d+\.\d+\.\d+)"$', (SOURCE / "SKILL.md").read_text(encoding="utf-8"), re.M)
    if not match:
        raise SystemExit("A semantic version is required in SKILL.md metadata.")
    version = match.group(1)
    out = REPO / "dist"
    out.mkdir(exist_ok=True)
    archive = out / (NAME + "-v" + version + ".tgz")
    paths = [SOURCE] + sorted(SOURCE.rglob("*"))
    with archive.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w", format=tarfile.USTAR_FORMAT) as bundle:
                for path in paths:
                    info = tarfile.TarInfo(path.relative_to(SOURCE.parent).as_posix())
                    info.mtime = 0
                    info.uid = info.gid = 0
                    info.uname = info.gname = ""
                    info.mode = 0o755 if path.is_dir() else 0o644
                    if path.is_dir():
                        info.type = tarfile.DIRTYPE
                        bundle.addfile(info)
                    else:
                        info.size = path.stat().st_size
                        with path.open("rb") as content:
                            bundle.addfile(info, content)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (out / "SHA256SUMS").write_text(digest + "  " + archive.name + "\n", encoding="utf-8")
    print("Built:", archive.name)
    print("SHA-256:", digest)


if __name__ == "__main__":
    main()
