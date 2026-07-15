"""Small source checks used before delivery."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    main_tex = (ROOT / "main.tex").read_text(encoding="utf-8")
    missing = []
    for match in re.finditer(r"(?:include|input)\{([^}]+)\}", main_tex):
        target = ROOT / (match.group(1) + ".tex")
        if not target.exists():
            missing.append(str(target.relative_to(ROOT)))
    if missing:
        raise SystemExit("Missing TeX files: " + ", ".join(missing))

    for path in (ROOT / "chapters").glob("*.tex"):
        text = path.read_text(encoding="utf-8")
        if "TODO" in text or "FIXME" in text:
            raise SystemExit(f"Unresolved marker in {path}")
    print("Project source checks passed.")


if __name__ == "__main__":
    main()
