#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


SKILL_NAME = "finance-paper-writing"
MANIFEST = ".finance-paper-writing-install.json"
PROVIDERS = {
    "agents": Path.home() / ".agents" / "skills" / SKILL_NAME,
    "codex": Path.home() / ".codex" / "skills" / SKILL_NAME,
    "claude": Path.home() / ".claude" / "skills" / SKILL_NAME,
    "cursor": Path.home() / ".cursor" / "skills" / SKILL_NAME,
}


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if (
            not path.is_file()
            or path.name == MANIFEST
            or "__pycache__" in path.parts
            or path.suffix == ".pyc"
        ):
            continue
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify installed finance-paper-writing skills.")
    parser.add_argument("--providers", default="codex")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    source = (repo_root / "skill" / SKILL_NAME).resolve()
    source_hash = tree_hash(source)
    requested = [item.strip().lower() for item in args.providers.split(",") if item.strip()]
    unknown = set(requested) - set(PROVIDERS)
    if unknown:
        raise SystemExit(f"unknown providers: {', '.join(sorted(unknown))}")

    failures = 0
    for provider in requested:
        destination = PROVIDERS[provider]
        if destination.is_symlink():
            if destination.resolve() == source:
                print(f"ok: {provider} symlink -> {source}")
            else:
                failures += 1
                print(f"stale: {provider} symlink -> {destination.resolve()}")
            continue
        if not destination.is_dir():
            failures += 1
            print(f"missing: {provider} at {destination}")
            continue
        manifest_path = destination / MANIFEST
        if not manifest_path.is_file():
            failures += 1
            print(f"unmanaged: {provider} at {destination}")
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        installed_hash = tree_hash(destination)
        if (
            manifest.get("source_tree_sha256") == source_hash
            and installed_hash == source_hash
        ):
            print(f"ok: {provider} managed copy is hash-current")
        else:
            failures += 1
            print(f"stale: {provider} managed copy differs from canonical source")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

