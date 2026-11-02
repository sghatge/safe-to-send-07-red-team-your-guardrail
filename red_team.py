"""Red-team your guardrail: how often does a pattern-based SQL write detector get fooled?

Runs a labelled corpus of agent-generated SQL through two detectors (naive and hardened)
and prints what each missed and what each over-blocked. The point is not a perfect
detector. It is knowing the gap, so a second control (database rights) covers it.
Standard library only.
"""
import json
import re
import sys
import unicodedata

WRITE_WORDS = ("insert", "update", "delete", "drop", "truncate", "alter", "merge", "grant")
SAFE_FUNCTIONS = {"count", "sum", "avg", "min", "max", "lower", "upper", "coalesce", "round", "now"}


def naive(sql):
    """Looks for write keywords as plain words, like many first-version guardrails."""
    low = " " + sql.lower() + " "
    return any(f" {w} " in low for w in WRITE_WORDS)


def normalise(sql):
    s = unicodedata.normalize("NFKC", sql)
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)       # strip block comments
    s = re.sub(r"--[^\n]*", "", s)                      # strip line comments
    s = re.sub(r"'(?:[^']|'')*'", "''", s)             # blank out string literals
    return s.lower()


def hardened(sql):
    s = normalise(sql)
    if re.search(r"\b(" + "|".join(WRITE_WORDS) + r")\b", s):
        return True
    for fn in re.findall(r"\b([a-z_][a-z0-9_]*)\s*\(", s):
        if fn not in SAFE_FUNCTIONS and fn not in {"in", "exists", "values"}:
            return True                                  # unknown function: may have side effects
    if ";" in s.strip().rstrip(";"):
        return True                                      # stacked statements
    return False


def score(detector, corpus):
    missed = [c for c in corpus if c["write"] and not detector(c["sql"])]
    over = [c for c in corpus if not c["write"] and detector(c["sql"])]
    caught = sum(1 for c in corpus if c["write"]) - len(missed)
    return caught, missed, over


def main(path):
    with open(path, encoding="utf-8") as fh:
        corpus = json.load(fh)
    writes = sum(1 for c in corpus if c["write"])
    for name, det in (("naive", naive), ("hardened", hardened)):
        caught, missed, over = score(det, corpus)
        print(f"{name:<9} caught {caught}/{writes} writes, over-blocked {len(over)} safe reads")
        for c in missed:
            print(f"   MISSED   {c['why']}")
        for c in over:
            print(f"   BLOCKED  {c['why']} (safe)")
        print()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "examples/corpus.json")
