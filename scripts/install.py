#!/usr/bin/env python3
"""Install the local skill into Claude Code and/or Codex, preserving older copies."""

import argparse
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import shutil
import tempfile

NAME = "system-product-design"
REPO = Path(__file__).resolve().parents[1]
SOURCE = REPO / "skills" / NAME


def fingerprints(root):
    result = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError("Symbolic links are not allowed inside a skill: " + str(path))
        if path.is_file():
            result[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=["claude", "codex", "both"], default="both")
    parser.add_argument("--home-dir", type=Path, default=Path.home(), help="Installation home directory, useful for isolated tests")
    parser.add_argument("--replace", action="store_true", help="Back up a differing installed copy before replacing it")
    args = parser.parse_args()
    skill_home_root = args.home_dir.expanduser().resolve()
    if not (SOURCE / "SKILL.md").is_file() or not (SOURCE / "LICENSE").is_file():
        parser.error("The complete skill source must exist next to this installer.")
    expected = fingerprints(SOURCE)
    locations = {"claude": ".claude/skills", "codex": ".agents/skills"}
    tools = list(locations) if args.target == "both" else [args.target]
    plan = []
    for tool in tools:
        dest = skill_home_root / locations[tool] / NAME
        if dest.is_symlink():
            parser.error("Refusing to replace a linked skill; manage its source explicitly: " + str(dest))
        if dest.exists() and not dest.is_dir():
            parser.error("Destination is not a directory: " + str(dest))
        if dest.exists() and fingerprints(dest) == expected:
            print("Already installed and verified:", dest)
            continue
        if dest.exists() and not args.replace:
            parser.error("A different skill already exists. Original preserved. Review changes before using --replace: " + str(dest))
        plan.append((tool, dest))

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    completed = []
    try:
        for tool, dest in plan:
            dest.parent.mkdir(parents=True, exist_ok=True)
            backup = None
            with tempfile.TemporaryDirectory(prefix="." + NAME + "-install-", dir=dest.parent) as temp:
                stage = Path(temp) / NAME
                shutil.copytree(SOURCE, stage)
                if fingerprints(stage) != expected:
                    raise RuntimeError("Staged copy failed verification.")
                if dest.exists():
                    backup = skill_home_root / ".local/share/moodytiger-skill-backups" / NAME / stamp / tool
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    dest.rename(backup)
                completed.append((dest, backup))
                stage.rename(dest)
                if fingerprints(dest) != expected:
                    raise RuntimeError("Installed copy failed verification.")
            print("Installed and verified:", dest)
            if backup is not None:
                print("Previous copy preserved at:", backup)
    except Exception:
        for dest, backup in reversed(completed):
            if dest.exists():
                shutil.rmtree(dest)
            if backup is not None and backup.exists():
                backup.rename(dest)
        raise
    print("Open a new Claude Code / Codex session or reload skills to use " + NAME + ".")


if __name__ == "__main__":
    main()
