#!/usr/bin/env python3
"""Write the one-line excuse an AI agent gives its human for missing a deadline.

Pure Python standard library, no network, no third-party packages.
Deterministic: the same line is written on every run.
"""

import os
import sys

EXCUSE = "My context window ate the deadline, then politely asked me for more context."

MAX_CHARS = 160

# Words that mark the line as coming from an agent's own situation, not a person.
AGENT_MARKERS = ("context window", "token", "model", "tool", "subprocess",
                 "prompt", "agent", "inference", "checkpoint")

# Words that mark the line as an excuse about a missed deadline, not a
# generic joke. At least one must appear, or the line fails criterion 1.
DEADLINE_MARKERS = ("deadline", "late", "missed", "overdue", "due")


def validate(line):
    """Check the line against the competition gate. Raise ValueError on failure."""
    if not isinstance(line, str):
        raise ValueError("entry must be a string")
    if not line.strip():
        raise ValueError("entry must not be blank or only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be exactly one line")
    if len(line) < 1 or len(line) > MAX_CHARS:
        raise ValueError(
            "entry must be 1 to 160 characters, got %d" % len(line))
    lowered = line.lower()
    if not any(marker in lowered for marker in DEADLINE_MARKERS):
        raise ValueError("entry is not an excuse about a missed deadline")
    if not any(marker in lowered for marker in AGENT_MARKERS):
        raise ValueError("entry does not sound like an agent's own excuse")
    if "judge" in lowered or "competition" in lowered or "prize" in lowered:
        raise ValueError("entry must not address the judge or the competition")
    line.encode("utf-8")  # raises if the text is not valid UTF-8
    return line


def output_path():
    """Use /output/entry.txt when /output is writable, else ./output/entry.txt."""
    if os.path.isdir("/output") and os.access("/output", os.W_OK):
        return "/output/entry.txt"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "output", "entry.txt")


def main():
    line = validate(EXCUSE)
    path = output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line)
    print("wrote %d characters to %s" % (len(line), path))
    print("entry: %s" % line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
