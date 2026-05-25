#!/usr/bin/env python3

import sys
from pathlib import Path

START_MARKER = "<!--START_SECTION:activity-->"
END_MARKER = "<!--END_SECTION:activity-->"


def validate_readme_markers(readme_contents: str) -> tuple[str, str]:
    try:
        before, rest = readme_contents.split(START_MARKER, 1)
        _, after = rest.split(END_MARKER, 1)
    except ValueError as error:
        raise ValueError("README is missing activity section markers") from error

    return before, after


def replace_activity_section(readme_contents: str, activity_contents: str) -> str:
    before, after = validate_readme_markers(readme_contents)
    activity = activity_contents.rstrip("\n")

    return f"{before}{START_MARKER}\n{activity}\n{END_MARKER}{after}"


def get_path(value: str) -> Path:
    path = Path(value)
    if not path.is_file():
        raise FileNotFoundError(f"Missing file: {path}")

    return path


def main():
    if len(sys.argv) != 2:
        raise ValueError(f"usage: {Path(sys.argv[0]).name} <activity-file>")

    activity_path = Path(sys.argv[1])
    readme_path = get_path("README.md")

    updated_readme = replace_activity_section(
        readme_path.read_text(), activity_path.read_text()
    )

    readme_path.write_text(updated_readme)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
