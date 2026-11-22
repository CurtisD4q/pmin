#!/usr/bin/env python3
"""Check that a repository keeps to the pmin layering rules.

Run from a repository's root, after its Go modules can be fetched. It reads
the repository's pmin.json and go.mod, and the pmin.json of each family
library it requires (from the Go module cache, so no other access is
needed), then checks:

1. pmin.json names a known tier.
2. pmin.json "requires" lists exactly the family libraries go.mod requires
   directly, so the catalogue tells the truth.
3. Each requirement is allowed for this tier. The rule is that modules
   depend only on the foundation, and programs wire modules together:
     foundation  -> a lower foundation layer only (pmin.json "layer":
                    1 base, 2 sys, 3 kit, 4 tools, 5 contracts)
     engine, function, wrap, frameworks -> foundation only
     program     -> anything but another program
   While STRICT is False (the move to this rule), a module that still
   requires another module is reported as a warning and does not fail;
   everything else fails as before.

usage: python3 check-layering.py [REPO_DIR]
"""
import json
import os
import re
import subprocess
import sys

FAMILY = re.compile(r"^github\.com/CurtisD4q/(pmin-[a-z]+)(/v\d+)?$")
# STRICT turns the modules-depend-only-on-the-foundation warnings into
# failures. It becomes True once every module has moved over.
STRICT = False

ALLOWED = {
    "foundation": {"foundation"},
    "engine": {"foundation"},
    "function": {"foundation"},
    "wrap": {"foundation"},
    "frameworks": {"foundation"},
    "program": {"foundation", "engine", "function", "wrap", "frameworks"},
}

# OLD is what each tier could require before the rule; while STRICT is
# False, a requirement OLD allows and ALLOWED does not is only a warning.
OLD = {
    "engine": {"foundation"},
    "function": {"foundation", "engine", "function"},
    "wrap": {"foundation", "wrap"},
    "frameworks": {"foundation", "engine", "function", "wrap"},
}


def go_json(args, cwd):
    out = subprocess.run(["go"] + args, cwd=cwd, capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit("go " + " ".join(args) + ": " + out.stderr.strip())
    return json.loads(out.stdout)


def main():
    repo = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    problems = []
    warnings = []
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
        dep = json.load(open(dep_meta, encoding="utf-8"))
        dep_tier = dep.get("tier")
        if dep_tier not in ALLOWED[tier]:
            msg = f"{meta['name']} ({tier}) may not require {name} ({dep_tier}): modules use only the foundation"
            if not STRICT and dep_tier in OLD.get(tier, set()):
                warnings.append(msg)
            else:
                problems.append(msg)
        elif tier == "foundation":
            mine, theirs = meta.get("layer"), dep.get("layer")
            if not isinstance(mine, int) or not isinstance(theirs, int):
                problems.append(f"{name}: foundation repositories give their layer in pmin.json")
            elif theirs >= mine:
                problems.append(f"{meta['name']} (layer {mine}) may not require {name} (layer {theirs}): a layer uses only the ones below it")

    for w in warnings:
        print("warning: " + w)
    if problems:
        print("Layering check failed:")
        for p in problems:
            print("  - " + p)
        sys.exit(1)
    print(f"Layering check passed: {meta['name']} ({tier}) requires {', '.join(sorted(direct)) or 'nothing from the family'}")


if __name__ == "__main__":
    main()
