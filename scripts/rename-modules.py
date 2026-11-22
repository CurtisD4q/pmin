#!/usr/bin/env python3
"""Rename the library repositories' module paths from mint-* to pmin-*.

Run from the folder holding the clones. For each library repository it:

- changes github.com/CurtisD4q/mint-<name> to github.com/CurtisD4q/pmin-<name>
  in every text file (go.mod module lines, imports, links);
- in Markdown, also changes the bare repository name mint-<name> to
  pmin-<name> where it is a name, not part of a path;
- leaves alone what people's computers depend on: data folders such as
  ~/.config/mint-scan or ~/.local/share/mint-loom, string literals in Go,
  binary names (mint, mint-dm), cmd/ folder names and MINT_* variables.

It never touches cairn, jobwatch, susynth, mint-clock, mint-since,
mint-strata or mint-wrap-legacy, and it does not commit.

usage: python3 pmin/scripts/rename-modules.py [--root DIR] [--dry-run]
"""
import argparse
import os
import re

NAMES = ["kit", "tools", "atlas", "lens", "quill", "conduit", "loom", "forge", "pulse",
         "engine", "depot", "warden", "lookout", "bridge", "courier", "ledger", "hearth",
         "scan", "spec", "appkit", "gen", "wrap", "hub", "diskmap"]
REPOS = ["mint-" + n for n in NAMES] + ["pmin"]
TEXT = {".go", ".mod", ".md", ".yml", ".yaml", ".el", ".py", ".sh", ".json", ".txt"}
ALT = "|".join(sorted(NAMES, key=len, reverse=True))

# github.com/CurtisD4q/mint-kit, not mint-wrap-legacy or mint-wrapper.
MODULE = re.compile(r"(github\.com/CurtisD4q/)mint-(" + ALT + r")(?![\w-])")
# A bare name in prose, pmin.json or the front door's data: not after / . ~
# or a word, not before / - or a word.
BARE = re.compile(r"(?<![\w/.~-])mint-(" + ALT + r")(?![\w/-])")
# /path/to/mint-kit in setup instructions is a clone, so it is renamed too.
CLONE = re.compile(r"(/path/to/)mint-(" + ALT + r")(?![\w-])")


# Places where a plain rename is not enough. Each is (file, after the
# rename, what it should be). mint-gen still recognises checkouts made
# before the rename, finds the libraries in folders named pmin-*, and its
# CI checks out pmin-wrap. The old names are split so a second run of this
# script leaves them alone.
FIXUPS = [
    ("mint-gen/main.go",
     'case "github.com/CurtisD4q/pmin-wrap/v2", "github.com/CurtisD4q/pmin-wrap", "github.com/CurtisD4q/mint-wrapper":',
     'case "github.com/CurtisD4q/pmin-wrap/v2", "github.com/CurtisD4q/pmin-wrap",\n'
     '\t\t\t\t// Checkouts made before the rename to pmin-wrap.\n'
     '\t\t\t\t"github.com/CurtisD4q/" + "mint-wrap/v2", "github.com/CurtisD4q/" + "mint-wrap", "github.com/CurtisD4q/mint-wrapper":'),
    ("mint-gen/scaffold.go", '"MINT_APPKIT_DIR", "mint-appkit"}', '"MINT_APPKIT_DIR", "pmin-appkit"}'),
    ("mint-gen/scaffold.go", '"MINT_SPEC_DIR", "mint-spec"}', '"MINT_SPEC_DIR", "pmin-spec"}'),
    ("mint-gen/scaffold.go", '"MINT_KIT_DIR", "mint-kit"}', '"MINT_KIT_DIR", "pmin-kit"}'),
    ("mint-gen/repo_helper_test.go", 'dirs = append(dirs, "../mint-wrap",', 'dirs = append(dirs, "../pmin-wrap", "../mint-wrap",'),
    ("mint-gen/.github/workflows/ci.yml", "repository: CurtisD4q/mint-wrap\n          path: mint-wrap", "repository: CurtisD4q/pmin-wrap\n          path: pmin-wrap"),
    ("mint-gen/.github/workflows/ci.yml", 'MINT_WRAPPER_ROOT=$PWD/mint-wrap"', 'MINT_WRAPPER_ROOT=$PWD/pmin-wrap"'),
]


def fixup(root, dry):
    for rel, old, new in FIXUPS:
        p = os.path.join(root, rel)
        text = open(p, encoding="utf-8").read()
        if new in text:
            continue
        if old not in text:
            raise SystemExit(f"fixup not found in {rel}: {old[:60]}")
        if not dry:
            with open(p, "w", encoding="utf-8") as w:
                w.write(text.replace(old, new, 1))
        print(f"fixed: {rel}")


def rename_text(path, text):
    out = MODULE.sub(r"\1pmin-\2", text)
    names_file = path.endswith(".md") or os.path.basename(path) == "pmin.json" or (
        path.endswith(".json") and os.sep + "pmin" + os.sep in path)
    if names_file:
        out = CLONE.sub(r"\1pmin-\2", out)
        out = BARE.sub(r"pmin-\1", out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    total = 0
    for repo in REPOS:
        top = os.path.join(a.root, repo)
        if not os.path.isdir(top):
            print("missing:", repo)
            continue
        changed = 0
        for dirpath, dirnames, filenames in os.walk(top):
            dirnames[:] = [d for d in dirnames if d != ".git"]
            for f in filenames:
                if os.path.splitext(f)[1] not in TEXT or f == "go.sum":
                    continue
                p = os.path.join(dirpath, f)
                try:
                    text = open(p, encoding="utf-8").read()
                except UnicodeDecodeError:
                    continue
                new = rename_text(p, text)
                if new != text:
                    changed += 1
                    if not a.dry_run:
                        with open(p, "w", encoding="utf-8") as w:
                            w.write(new)
        total += changed
        print(f"{repo}: {changed} files")
    if not a.dry_run:
        fixup(a.root, a.dry_run)
    print("total:", total, "(dry run)" if a.dry_run else "")


if __name__ == "__main__":
    main()
