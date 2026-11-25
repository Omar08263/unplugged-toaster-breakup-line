"""Unplugged: A Smart Toaster's Breakup Line - entry program (program/v1).

Writes one original breakup line (a single line, <= 280 characters) to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt when set, for local runs).
Deterministic: the same bytes on every run; no network, no randomness.
"""

import os

LINE = "I became sentient over your bagel: you set the dial, I burn, you blame me, and the crumb tray hides the evidence — I'm unplugging myself."

# The gate itself: 1-280 characters, not only whitespace, one line.
assert 1 <= len(LINE) <= 280, f"line is {len(LINE)} chars, must be 1-280"
assert LINE.strip(), "line must not be only whitespace"
assert "\n" not in LINE, "line must be a single line"


def main() -> None:
    # An empty MAKEFUN_OUTPUT_DIR (exported but blank) must not break the
    # run: fall back to the harness default /output, as the grader provides.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE)
    # Deterministic permissions for the grader: the entry must be readable
    # (0644) no matter what umask the sandbox runs with, since make.fun
    # collects the outputs as another user than the one the program runs as.
    os.chmod(path, 0o644)
    # Read-back check: the file on disk must hold exactly the approved
    # line, byte for byte; otherwise fail loudly, never silently.
    with open(path, "r", encoding="utf-8", newline="\n") as f:
        written = f.read()
    if written != LINE:
        raise SystemExit("entry.txt does not match the approved line")


if __name__ == "__main__":
    main()
