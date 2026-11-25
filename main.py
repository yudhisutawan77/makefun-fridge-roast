"""Midnight Fridge Roast — one line, written to the entry file.

The program takes no arguments and needs no network. It writes a
single roast line (under the 200-character gate) to the place the
grader reads, then prints the same line to stdout.

Where the line goes, first match wins:

- ``$ENTRY_OUT`` — a file path, or a directory (then entry.txt
  inside it);
- ``$MAKEFUN_OUTPUT_DIR`` — always a directory, entry.txt inside;
- ``$ENTRY_OUT_DIR`` / ``$OUTPUT`` — same file-or-directory rule;
- otherwise ``/output/entry.txt``.

Stdlib only.
"""

import os
import sys
from pathlib import Path

CHAR_LIMIT = 200
DEFAULT_ENTRY = Path("/output/entry.txt")

# Env vars the harness may set, in priority order. The second entry is
# always a directory; the rest may be a file or a directory.
OUTPUT_VARS = ("ENTRY_OUT", "MAKEFUN_OUTPUT_DIR", "ENTRY_OUT_DIR", "OUTPUT")


def _as_entry_file(raw_value: str, directory_only: bool = False) -> Path:
    """Turn one env value into the entry.txt path it points at."""
    candidate = Path(raw_value)
    if directory_only or candidate.is_dir() or candidate.suffix != ".txt":
        return candidate / "entry.txt"
    return candidate


def pick_output_path() -> Path:
    """Choose the entry destination from the environment."""
    for index, name in enumerate(OUTPUT_VARS):
        value = os.environ.get(name)
        if not value:
            continue
        return _as_entry_file(value, directory_only=(index == 1))
    return DEFAULT_ENTRY


MIDNIGHT_ROAST = (
    "My fridge locks at midnight and beeps like I broke in \u2014 "
    "I bought the fridge, the leftovers, and the house it's standing in."
)


def checked_line() -> str:
    """Return the roast, refusing anything that would fail the gate."""
    line = MIDNIGHT_ROAST.strip()
    if not line or line != line.strip():
        raise ValueError("roast line is blank")
    if len(line) > CHAR_LIMIT:
        raise ValueError(f"roast is {len(line)} chars, over {CHAR_LIMIT}")
    if any(ch in line for ch in ("\n", "\r")):
        raise ValueError("roast must stay on one line")
    return line


def deliver() -> Path:
    """Write the checked roast to its destination and echo it."""
    line = checked_line()
    target = pick_output_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(line, encoding="utf-8")
    print(line)
    print(f"wrote {len(line)} chars to {target}", file=sys.stderr)
    return target


def main() -> int:
    deliver()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
