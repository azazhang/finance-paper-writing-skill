# Provider Support

The repository keeps one canonical Agent Skills package and avoids provider-specific substantive copies.

| Provider / surface | Install target | Status |
|---|---|---|
| OpenAI Agent Skills | `~/.agents/skills/finance-paper-writing` | Portable Agent Skills target; install alongside the Codex compatibility path when desired |
| Codex | `~/.codex/skills/finance-paper-writing` | Locally tested compatibility path |
| Claude Code | `~/.claude/skills/finance-paper-writing` | Agent Skills-compatible install path; locally verified when the target CLI is present |
| Cursor | `~/.cursor/skills/finance-paper-writing` | Agent Skills-compatible install path; locally verified when the target CLI is present |
| Other agents | Use the canonical `SKILL.md` and references only after confirming that agent's skill-discovery path | Manual portability; do not guess install directories |

The installer defaults to Codex only. Other targets require explicit selection, for example:

```bash
python3 scripts/install_local.py --providers agents,codex,claude,cursor
```

Symlink installation is the default because it remains current when the repository changes. Copy mode writes a managed-installation manifest and the verifier compares hashes against the canonical source. Generated Python cache files are excluded from those hashes.

The installer refuses to replace an unrecognized existing path, even with `--force`. For a recognized managed copy, `--force` also refuses to discard post-install local edits unless `--discard-local-changes` is supplied explicitly.

The canonical frontmatter includes a least-privilege `allowed-tools` hint. Providers that do not recognize that field may ignore it; the workflow itself does not depend on provider-specific tool names.
