#!/usr/bin/env python3
"""Copy scripts/check-layering.py into .github/workflows/go.yml.

The shared workflow carries the checker inside it, so a repository using
the workflow needs no access to this one. Run this after changing the
checker; --check fails if the copy is out of date (CI runs that).
"""
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WF = os.path.join(HERE, ".github", "workflows", "go.yml")
SRC = os.path.join(HERE, "scripts", "check-layering.py")
BEGIN = "# BEGIN check-layering.py"
END = "# END check-layering.py"
INDENT = " " * 10


def main():
    wf = open(WF, encoding="utf-8").read().split("\n")
    b = next(i for i, l in enumerate(wf) if l.strip().startswith(BEGIN))
    e = next(i for i, l in enumerate(wf) if l.strip().startswith(END))
    body = [(INDENT + l) if l.strip() else "" for l in open(SRC, encoding="utf-8").read().rstrip("\n").split("\n")]
    new = "\n".join(wf[: b + 1] + body + wf[e:])
    if "--check" in sys.argv:
        if new != "\n".join(wf):
            sys.exit("go.yml's copy of check-layering.py is out of date: run scripts/embed-layering.py")
        print("go.yml's copy of check-layering.py is up to date")
        return
    open(WF, "w", encoding="utf-8").write(new)
    print("copied check-layering.py into go.yml")


if __name__ == "__main__":
    main()
