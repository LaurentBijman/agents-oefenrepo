"""Controleer de YAML-frontmatter van agent-, skill- en instructiebestanden.

Gebruik: ``python scripts/check_frontmatter.py`` (of ``make check-agents``).
Templates (``*.template.agent.md``) hoeven alleen geldige YAML te zijn.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".venv", "venv", "node_modules"}

REQUIRED_KEYS: dict[str, tuple[str, ...]] = {
    ".agent.md": ("name", "description", "tools"),
    "SKILL.md": ("name", "description"),
    ".instructions.md": ("applyTo",),
}


def kind_of(path: Path) -> str | None:
    return next((suffix for suffix in REQUIRED_KEYS if path.name.endswith(suffix)), None)


def read_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("bestand begint niet met '---'")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("afsluitende '---' van de frontmatter ontbreekt")
    data = yaml.safe_load(text[4:end]) or {}
    if not isinstance(data, dict):
        raise ValueError("frontmatter is geen YAML-mapping (key: value)")
    return data


def check(path: Path) -> list[str]:
    kind = kind_of(path)
    try:
        data = read_frontmatter(path)
    except (ValueError, yaml.YAMLError) as exc:
        return [f"ongeldige frontmatter: {exc}"]
    if ".template." in path.name:
        return []

    errors = [
        f"veld '{key}' ontbreekt of is leeg" for key in REQUIRED_KEYS[kind] if not data.get(key)
    ]
    if kind == ".agent.md" and "tools" in data and not isinstance(data["tools"], list):
        errors.append("'tools' moet een lijst zijn, bv. ['read', 'search']")
    if kind == "SKILL.md" and data.get("name") != path.parent.name:
        errors.append(f"'name' moet gelijk zijn aan de mapnaam '{path.parent.name}'")
    return errors


def main() -> int:
    files = sorted(
        path
        for path in ROOT.rglob("*.md")
        if kind_of(path) and not SKIP_DIRS & set(path.relative_to(ROOT).parts)
    )
    failures = 0
    for path in files:
        errors = check(path)
        label = path.relative_to(ROOT).as_posix()
        print(f"{'FOUT' if errors else 'ok  '} {label}")
        for error in errors:
            print(f"     - {error}")
        failures += bool(errors)
    print(f"\n{len(files)} bestanden gecontroleerd, {failures} met fouten.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
