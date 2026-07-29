#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


SKILL_NAME = "finance-paper-writing"
PROVIDERS = {
    "codex": Path.home() / ".codex" / "skills" / SKILL_NAME,
    "claude": Path.home() / ".claude" / "skills" / SKILL_NAME,
    "cursor": Path.home() / ".cursor" / "skills" / SKILL_NAME,
}
MANIFEST = ".finance-paper-writing-install.json"


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name == MANIFEST:
            continue
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install the finance-paper-writing skill.")
    parser.add_argument(
        "--providers",
        default="codex",
        help="Comma-separated providers: codex, claude, cursor. Default: codex.",
    )
    parser.add_argument("--mode", choices=("symlink", "copy"), default="symlink")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def provider_list(raw: str) -> list[str]:
    values = [item.strip().lower() for item in raw.split(",") if item.strip()]
    unknown = set(values) - set(PROVIDERS)
    if unknown:
        raise SystemExit(f"unknown providers: {', '.join(sorted(unknown))}")
    return values


def is_managed_copy(destination: Path, source: Path) -> bool:
    manifest_path = destination / MANIFEST
    if not manifest_path.is_file():
        return False
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    return (
        manifest.get("skill") == SKILL_NAME
        and Path(manifest.get("source", "")).expanduser().resolve() == source.resolve()
    )


def install_one(
    provider: str,
    source: Path,
    mode: str,
    force: bool,
    dry_run: bool,
) -> str:
    destination = PROVIDERS[provider]
    if destination.is_symlink() and destination.resolve() == source.resolve():
        return f"kept current symlink: {destination}"

    if destination.exists() or destination.is_symlink():
        managed = (
            destination.is_symlink() and destination.resolve() == source.resolve()
        ) or (destination.is_dir() and is_managed_copy(destination, source))
        if not managed:
            raise SystemExit(
                f"refusing to replace unrecognized installation: {destination}"
            )
        if not force:
            return f"skipped managed installation without --force: {destination}"
        if not dry_run:
            if destination.is_symlink() or destination.is_file():
                destination.unlink()
            else:
                shutil.rmtree(destination)

    if dry_run:
        return f"would install {provider}: {source} -> {destination} via {mode}"

    destination.parent.mkdir(parents=True, exist_ok=True)
    if mode == "symlink":
        destination.symlink_to(source, target_is_directory=True)
        return f"linked {destination} -> {source}"

    shutil.copytree(source, destination)
    manifest = {
        "skill": SKILL_NAME,
        "source": str(source.resolve()),
        "source_tree_sha256": tree_hash(source),
        "mode": "copy",
    }
    (destination / MANIFEST).write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return f"copied {source} -> {destination}"


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    source = repo_root / "skill" / SKILL_NAME
    if not (source / "SKILL.md").is_file():
        raise SystemExit(f"canonical skill not found: {source}")

    for provider in provider_list(args.providers):
        print(install_one(provider, source, args.mode, args.force, args.dry_run))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

