#!/usr/bin/env python3
"""Check that a repository keeps to the pmin layering rules.

Run from a repository's root, after its Go modules can be fetched. It reads
the repository's pmin.json and go.mod, and the pmin.json of each family
library it requires (from the Go module cache, so no other access is
needed), then checks:

1. pmin.json names a known tier.
2. pmin.json "requires" lists exactly the family libraries go.mod requires
   directly, so the catalogue tells the truth.
3. Each requirement is allowed for this tier:
     foundation  -> foundation
     engine      -> foundation
     function    -> foundation, engine, function (sibling, as listed)
     wrap        -> foundation, wrap
     frameworks  -> foundation, engine, function, wrap
     program     -> anything but another program
   No library ever requires a program, and nothing requires frameworks
   except a program.

usage: python3 check-layering.py [REPO_DIR]
"""
import json
import os
import re
import subprocess
import sys

FAMILY = re.compile(r"^github\.com/CurtisD4q/(pmin-[a-z]+)(/v\d+)?$")
ALLOWED = {
    "foundation": {"foundation"},
    "engine": {"foundation"},
    "function": {"foundation", "engine", "function"},
    "wrap": {"foundation", "wrap"},
    "frameworks": {"foundation", "engine", "function", "wrap"},
    "program": {"foundation", "engine", "function", "wrap", "frameworks"},
}


def go_json(args, cwd):
    out = subprocess.run(["go"] + args, cwd=cwd, capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit("go " + " ".join(args) + ": " + out.stderr.strip())
    return json.loads(out.stdout)


def main():
    repo = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    problems = []
    meta_path = os.path.join(repo, "pmin.json")
    if not os.path.isfile(meta_path):
        raise SystemExit("no pmin.json: every pmin repository describes itself in one")
    meta = json.load(open(meta_path, encoding="utf-8"))
    tier = meta.get("tier")
    if tier not in ALLOWED:
        raise SystemExit(f"pmin.json: unknown tier {tier!r}; one of {', '.join(sorted(ALLOWED))}")

    mod = go_json(["mod", "edit", "-json"], repo)
    direct = {}
    for r in mod.get("Require") or []:
        m = FAMILY.match(r["Path"])
        if m and not r.get("Indirect"):
            direct[m.group(1)] = r["Path"]

    listed = set(meta.get("requires", []))
    if listed != set(direct):
        missing = sorted(set(direct) - listed)
        extra = sorted(listed - set(direct))
        if missing:
            problems.append("pmin.json requires is missing " + ", ".join(missing) + " (go.mod requires them)")
        if extra:
            problems.append("pmin.json requires lists " + ", ".join(extra) + " (go.mod does not require them)")

    for name, path in sorted(direct.items()):
        info = go_json(["list", "-m", "-json", path], repo)
        dep_meta = os.path.join(info.get("Dir") or "", "pmin.json")
        if not info.get("Dir") or not os.path.isfile(dep_meta):
            problems.append(f"{name}: no pmin.json in the required version, so its tier is unknown (update the requirement)")
            continue
        dep_tier = json.load(open(dep_meta, encoding="utf-8")).get("tier")
        if dep_tier not in ALLOWED[tier]:
            problems.append(f"{meta['name']} ({tier}) may not require {name} ({dep_tier})")

    if problems:
        print("Layering check failed:")
        for p in problems:
            print("  - " + p)
        sys.exit(1)
    print(f"Layering check passed: {meta['name']} ({tier}) requires {', '.join(sorted(direct)) or 'nothing from the family'}")


if __name__ == "__main__":
    main()
