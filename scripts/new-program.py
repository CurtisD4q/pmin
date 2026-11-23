#!/usr/bin/env python3
"""Give a pmin program everything it needs to be installed with one command.

    python3 scripts/new-program.py ../myprog --name myprog [--files "emacs/myprog.el"]
                                   [--targets "linux/amd64 ..."] [--force]

For a new program (no go.mod in the folder) it also writes go.mod, a
cmd/NAME/main.go that already answers `install` and `uninstall`, a README
with the standard Install section, a LICENSE and CI. For an existing one it
adds what is missing and prints what to add by hand:

  scripts/dist.sh               the shared build script (always kept identical)
  install.sh                    downloads, checks and installs the latest release
  Makefile                      build, test, install, uninstall, dist
  .github/workflows/release.yml a tag builds and publishes a release
  .github/workflows/ci.yml      the shared CI (new programs only)

It never overwrites a file without --force, except scripts/dist.sh, which
must match the template. Check a program afterwards with
scripts/check-program.py.
"""
import argparse, os, re, shutil, stat, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, "..", "templates", "program")
DEFAULT_TARGETS = "linux/amd64 linux/arm64 darwin/amd64 darwin/arm64"

MAIN = '''// Command {name} is a pmin program.
package main

import (
	"fmt"
	"os"

	"github.com/CurtisD4q/pmin-base/selfinstall"
)

// Version is set from the release tag by scripts/dist.sh.
var Version = "0.0.0-dev"

func main() {{
	// `{name} install` puts this program on the PATH; `{name} uninstall` takes it off.
	if ok, code := selfinstall.Handle(selfinstall.Program{{Name: "{name}", Files: {files}}}, os.Args[1:], os.Stdout, os.Stderr); ok {{
		os.Exit(code)
	}}
	fmt.Println("{name}", Version)
}}
'''

CI = '''name: ci
on:
  push:
  pull_request:
jobs:
  go:
    uses: CurtisD4q/pmin/.github/workflows/go.yml@main
    secrets: inherit
'''


def fill(text, name, files, targets):
    return text.replace("@NAME@", name).replace("@FILES@", files).replace("@TARGETS@", targets)


def write(path, text, force, mode=0o644, note=None):
    if os.path.exists(path) and not force:
        print(f"kept      {path}" + (f"  ({note})" if note else ""))
        return False
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        f.write(text)
    os.chmod(path, mode)
    print(f"wrote     {path}")
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("dir")
    ap.add_argument("--name", required=True)
    ap.add_argument("--files", default="", help="files to ship and install beside the program")
    ap.add_argument("--targets", default="", help="GOOS/GOARCH pairs; default Linux and macOS on amd64 and arm64")
    ap.add_argument("--force", action="store_true", help="replace files that are already there")
    a = ap.parse_args()
    if not re.fullmatch(r"[a-z][a-z0-9-]*", a.name):
        sys.exit("the name must be lower-case letters, digits and -")
    d = a.dir
    tpl = lambda f: open(os.path.join(TPL, f)).read()
    new = not os.path.exists(os.path.join(d, "go.mod"))
    os.makedirs(d, exist_ok=True)

    dist = os.path.join(d, "scripts", "dist.sh")
    os.makedirs(os.path.dirname(dist), exist_ok=True)
    shutil.copyfile(os.path.join(TPL, "dist.sh"), dist)
    os.chmod(dist, 0o755)
    print(f"wrote     {dist}")
    write(os.path.join(d, "install.sh"), fill(tpl("install.sh"), a.name, a.files, a.targets), True, 0o755)
    targets_line = a.targets or DEFAULT_TARGETS
    mk = fill(tpl("Makefile"), a.name, a.files, a.targets).replace(
        "TARGETS ?= " + DEFAULT_TARGETS, "TARGETS ?= " + targets_line)
    if not write(os.path.join(d, "Makefile"), mk, a.force, note="add build, test, install, uninstall and dist from templates/program/Makefile"):
        pass
    write(os.path.join(d, ".github", "workflows", "release.yml"), fill(tpl("release.yml"), a.name, a.files, a.targets), a.force)

    readme = fill(tpl("README-install.md"), a.name, a.files, a.targets)
    if new:
        files_go = "nil" if not a.files else "[]string{" + ", ".join(f'"{f}"' for f in a.files.split()) + "}"
        write(os.path.join(d, "go.mod"), f"module github.com/CurtisD4q/{a.name}\n\ngo 1.21\n", a.force)
        write(os.path.join(d, "cmd", a.name, "main.go"), MAIN.format(name=a.name, files=files_go), a.force)
        write(os.path.join(d, "README.md"), f"# {a.name}\n\nWhat {a.name} does, in a sentence.\n\n{readme}", a.force)
        write(os.path.join(d, "LICENSE"), open(os.path.join(HERE, "..", "LICENSE")).read(), a.force)
        write(os.path.join(d, ".github", "workflows", "ci.yml"), CI, a.force)
        print(f"\nNext: cd {d} && GOPRIVATE='github.com/CurtisD4q/*' go mod tidy && make install")
    else:
        print("\nBy hand, if not done already:")
        print(f"  1. In cmd/{a.name}/main.go, first thing in main():")
        print(f'       if ok, code := selfinstall.Handle(selfinstall.Program{{Name: "{a.name}", Files: ...}}, os.Args[1:], os.Stdout, os.Stderr); ok {{ os.Exit(code) }}')
        print("  2. Put this Install section in README.md (from templates/program/README-install.md):\n")
        print("     " + readme.replace("\n", "\n     "))
    print("Then: python3 scripts/check-program.py", d)


if __name__ == "__main__":
    main()
