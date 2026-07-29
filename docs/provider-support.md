# Provider Support

The repository keeps one canonical Agent Skills package and avoids provider-specific substantive copies.

| Provider | Install target | Status |
|---|---|---|
| Codex | `~/.codex/skills/finance-paper-writing` | Native package; locally tested by this repository |
| Claude Code | `~/.claude/skills/finance-paper-writing` | Agent Skills-compatible install path; verify in the target version |
| Cursor | `~/.cursor/skills/finance-paper-writing` | Agent Skills-compatible install path; verify in the target version |
| Other agents | Use the canonical `SKILL.md` and references as system or project instructions | Manual portability |

The installer defaults to Codex only. Other providers require explicit selection.

Symlink installation is the default because it remains current when the repository changes. Copy mode writes a managed-installation manifest and the verifier compares hashes against the canonical source.

The installer refuses to replace an unrecognized existing path, even with `--force`.

The canonical frontmatter includes a least-privilege `allowed-tools` hint. Providers that do not recognize that field may ignore it; the workflow itself does not depend on provider-specific tool names.
