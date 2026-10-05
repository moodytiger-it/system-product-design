#!/usr/bin/env python3
"""Check package structure, local references, scenarios, and accidental private content."""

import json
from pathlib import Path
import re

from install import NAME, REPO, SOURCE, fingerprints

EXCLUDED = {".git", ".verification", "dist", "__pycache__"}


def main():
    fingerprints(SOURCE)
    skill = (SOURCE / "SKILL.md").read_text(encoding="utf-8")
    if not skill.startswith("---\n") or "\n---\n" not in skill[4:]:
        raise SystemExit("Missing YAML frontmatter.")
    front = skill.split("---\n", 2)[1]
    if not re.search(r"^name: " + NAME + r"$", front, re.M):
        raise SystemExit("Canonical skill name must match the folder.")
    description = re.search(r'^description: (".*")$', front, re.M)
    if not description or not 1 <= len(json.loads(description.group(1))) <= 1024:
        raise SystemExit("Expected a nonempty quoted description of at most 1024 characters.")
    version = re.search(r'^  version: "(\d+\.\d+\.\d+)"$', front, re.M)
    if not version or version.group(1) not in (REPO / "README.md").read_text(encoding="utf-8"):
        raise SystemExit("Version must match README.")
    if (SOURCE / "LICENSE").read_bytes() != (REPO / "LICENSE").read_bytes():
        raise SystemExit("Missing or differing license.")
    scenarios = json.loads((SOURCE / "evals/evals.json").read_text(encoding="utf-8"))
    ids = [item["id"] for item in scenarios["evals"]]
    if scenarios["skill_name"] != NAME or len(ids) != len(set(ids)):
        raise SystemExit("Scenario names/IDs are inconsistent.")
    for item in scenarios["evals"]:
        if not item.get("prompt") or not item.get("expected_output") or item.get("files"):
            raise SystemExit("Scenarios must have prompts/expectations and no private file dependencies.")

    checks = [
        ("personal absolute path", re.compile("/" + r"Users/[^/\s]+|[A-Z]:\\Users\\")),
        ("internal business link", re.compile(r"https?://[^\s)]*(?:feishu\.cn|larksuite\.com|moodytiger\.work)/")),
        ("private chat/user identifier", re.compile(r"\b(?:oc_|ou_|on_)[a-f0-9]{20,}\b")),
        ("private network address", re.compile(r"\b(?:10\.\d+|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d+\.\d+\b")),
        ("API credential", re.compile(r"\b(?:ghp_|github_pat_|sk-proj-)[A-Za-z0-9_\-]{20,}\b")),
        ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ]
    count = 0
    for path in sorted(REPO.rglob("*")):
        relative = path.relative_to(REPO)
        if any(part in EXCLUDED for part in relative.parts) or not path.is_file():
            continue
        if path.is_symlink():
            raise SystemExit("Public source must not include symlinks: " + str(relative))
        if path.suffix not in {".md", ".py", ".json"} and path.name not in {"LICENSE", ".gitignore", ".gitattributes"}:
            raise SystemExit("Review unexpected public file: " + str(relative))
        content = path.read_text(encoding="utf-8")
        for label, pattern in checks:
            if pattern.search(content):
                raise SystemExit("Review " + label + " in " + str(relative))
        if path.suffix == ".md":
            for target in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", content):
                if target.startswith(("https://", "http://", "#", "mailto:")):
                    continue
                resolved = (path.parent / target.split("#", 1)[0]).resolve()
                if REPO not in resolved.parents or not resolved.is_file():
                    raise SystemExit("Broken or external local reference in " + str(relative) + ": " + target)
        count += 1
    print("Validated:", count, "public files;", len(ids), "scenario definitions; version", version.group(1))
    print("Structure, references, license, and private-content checks passed. Scenario outputs were not run.")


if __name__ == "__main__":
    main()
