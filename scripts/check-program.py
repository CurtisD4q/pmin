#!/usr/bin/env python3
"""Check that a pmin program can be installed with one command.

    python3 scripts/check-program.py ../jobwatch [../cairn ...]

Fails (exit 1) and says what is missing when a program lacks: the shared
scripts/dist.sh (identical to the template), install.sh (the template for
its name), a Makefile with build, test, install, uninstall and dist, a
release workflow that calls pmin's, `install`/`uninstall` handled in its
main, or a README that says how to install, uninstall and build over SSH.
scripts/new-program.py adds most of these.
"""
import glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, "..", "templates", "program")


def check(d):
    bad = []
    rel = os.path.join(d, ".github", "workflows", "release.yml")
    name = None
    if os.path.exists(rel):
        s = open(rel).read()
        if "CurtisD4q/pmin/.github/workflows/release.yml" not in s:
            bad.append("release.yml does not call pmin's shared release workflow")
        m = re.search(r'^\s+name:\s*"?([a-z0-9-]+)"?\s*$', s, re.M)
        name = m.group(1) if m else None
    else:
        bad.append("no .github/workflows/release.yml")
    name = name or os.path.basename(os.path.abspath(d))

    dist = os.path.join(d, "scripts", "dist.sh")
    if not os.path.exists(dist):
        bad.append("no scripts/dist.sh")
    elif open(dist).read() != open(os.path.join(TPL, "dist.sh")).read():
        bad.append("scripts/dist.sh differs from pmin/templates/program/dist.sh")

    inst = os.path.join(d, "install.sh")
    want = open(os.path.join(TPL, "install.sh")).read().replace("@NAME@", name)
    if not os.path.exists(inst):
        bad.append("no install.sh")
    else:
        if open(inst).read() != want:
            bad.append("install.sh differs from the template for " + name)
        if not os.access(inst, os.X_OK):
            bad.append("install.sh is not executable")

    mk = os.path.join(d, "Makefile")
    if not os.path.exists(mk):
        bad.append("no Makefile")
    else:
        targets = set(re.findall(r"^([a-z]+):", open(mk).read(), re.M))
        for t in ("build", "test", "install", "uninstall", "dist"):
            if t not in targets:
                bad.append(f"the Makefile has no {t} target")

    mains = glob.glob(os.path.join(d, "cmd", name, "*.go"))
    if not any("selfinstall.Handle" in open(f).read() for f in mains if not f.endswith("_test.go")):
        bad.append(f"cmd/{name} does not handle install and uninstall (selfinstall.Handle)")

    rd = os.path.join(d, "README.md")
    s = open(rd).read() if os.path.exists(rd) else ""
    for what, needle in (("an Install section", "## Install"), ("the install.sh one-liner", "install.sh"),
                         ("how to uninstall", f"{name} uninstall"), ("how to build over SSH", "insteadOf")):
        if needle not in s:
            bad.append(f"README.md lacks {what}")
    return name, bad


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    failed = False
    for d in sys.argv[1:]:
        name, bad = check(d)
        if bad:
            failed = True
            print(f"{name}: not ready")
            for b in bad:
                print("  - " + b)
        else:
            print(f"{name}: ready")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
