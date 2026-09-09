#!/usr/bin/env python3
"""Mass updates across every repo using the planning framework.

    python3 ~/Programming/PlanPlan/framework/migrate.py <migration> <repo>...
    python3 ~/Programming/PlanPlan/framework/migrate.py <migration> <repo>... --apply

Dry run is the DEFAULT. Nothing is written until --apply is given.

WHY THIS EXISTS. `generate_nodes.py --rename-field` handles one
frontmatter key. Anything wider — an address scheme, a filename
grammar, a section heading — had no tool, so it meant hand-editing
hundreds of files across five repos, which is how a migration ends up
half-applied. the owner, 2026-08-05: "we should probably have something to
make mass updates to all PlanPlan infrastructure."

WHAT A MIGRATION TOUCHES. Four surfaces, always in this order, so that
a partial run leaves a state the checks can describe:

    1. text inside files   (frontmatter paths, headings, prose)
    2. file names
    3. folder names        (deepest first, so parents stay findable)
    4. nothing else        -- code is REPORTED, never rewritten

Code is reported rather than rewritten BY DEFAULT: a `.py` or `.sh`
matching an address may be a constant needing a human decision, not a
substitution. The dry run names them, and `--include-code` folds them
into the run once you have looked.

The patterns are anchored to the grammar prefixes (`node_`, `CORE_`,
`CHECK_`, `SUPPORT_`, or a `CORE <chain>` heading), so a bare chain in
code — `CHAIN = "1_0"`, `return "1"` — never matches, in either mode.
Those are exactly the constants a person must decide about, and they
stay invisible to this tool on purpose. Grep for them separately when
a migration changes what they mean.

MIGRATIONS

  renumber-root   The leading address segment becomes 0 instead of 1,
                  so the root's own numbering (`CORE_0`, level 0) and
                  its children's addresses agree. `node_0_0_tools`
                  becomes `node_0_0_tools`; chain `1_0_0` becomes
                  `0_0_0`. Level arithmetic is unchanged: it has always
                  been `segments - 1`, and the leading segment has
                  always been a constant.

Standard library only, like every tool here.
"""
import os
import re
import sys

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv"}
TEXT_EXT = {".md", ".txt"}
CODE_EXT = {".py", ".sh", ".json", ".yaml", ".yml"}


# ---------------------------------------------------------------- migrations
class RenumberRoot:
    """Leading address segment 1 -> 0."""

    name = "renumber-root"

    # Anchored so a bare "1_0" in prose is never touched. Every pattern
    # requires a grammar prefix (node_/CORE_/CHECK_/SUPPORT_) or a
    # heading form, and requires a digit to follow.
    TEXT_RULES = [
        (re.compile(r"\b(node|CORE|CHECK|SUPPORT)_1(?=_\d)"), r"\1_0"),
        (re.compile(r"\b(CORE|CHECK)(\s+)1(?=_\d)"), r"\1\g<2>0"),
        (re.compile(r"\b(CORE|CHECK)(\s+—\s+)1(?=_\d)"), r"\1\g<2>0"),
    ]
    NAME_RE = re.compile(r"^(node|CORE|CHECK|SUPPORT)_1(_\d)")

    def rename(self, basename):
        """New basename, or None if this name is not affected."""
        if self.NAME_RE.match(basename):
            return self.NAME_RE.sub(r"\1_0\2", basename, count=1)
        return None

    def rewrite(self, text):
        out = text
        for pat, rep in self.TEXT_RULES:
            out = pat.sub(rep, out)
        return out


MIGRATIONS = {m.name: m for m in [RenumberRoot()]}


# ------------------------------------------------------------------- engine
def walk_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            yield os.path.join(dirpath, fn)


def plan(migration, repos, include_code=False):
    """-> (text_edits, file_renames, dir_renames, code_hits)."""
    text_edits, file_renames, dir_renames, code_hits = [], [], [], []
    editable = TEXT_EXT | CODE_EXT if include_code else TEXT_EXT
    for repo in repos:
        for path in walk_files(repo):
            ext = os.path.splitext(path)[1]
            base = os.path.basename(path)
            if ext in editable:
                try:
                    with open(path, encoding="utf-8") as fh:
                        old = fh.read()
                except (OSError, UnicodeDecodeError):
                    continue
                new = migration.rewrite(old)
                if new != old:
                    n = sum(1 for a, b in zip(old.splitlines(),
                                              new.splitlines()) if a != b)
                    text_edits.append((path, n))
            elif ext in CODE_EXT:   # only reached when include_code is off
                try:
                    with open(path, encoding="utf-8", errors="replace") as fh:
                        body = fh.read()
                except OSError:
                    continue
                if migration.rewrite(body) != body:
                    code_hits.append(path)
            new_base = migration.rename(base)
            if new_base:
                file_renames.append((path, os.path.join(
                    os.path.dirname(path), new_base)))

        # folders, deepest first so a parent rename cannot orphan a child
        dirs = []
        for dirpath, dirnames, _ in os.walk(repo):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for d in dirnames:
                dirs.append(os.path.join(dirpath, d))
        for d in sorted(dirs, key=lambda p: p.count(os.sep), reverse=True):
            nb = migration.rename(os.path.basename(d))
            if nb:
                dir_renames.append((d, os.path.join(os.path.dirname(d), nb)))
    return text_edits, file_renames, dir_renames, code_hits


def apply(migration, text_edits, file_renames, dir_renames):
    for path, _ in text_edits:
        with open(path, encoding="utf-8") as fh:
            old = fh.read()
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(migration.rewrite(old))
    for src, dst in file_renames:
        if os.path.exists(src):
            os.rename(src, dst)
    for src, dst in dir_renames:      # already deepest-first
        if os.path.isdir(src):
            os.rename(src, dst)


def disp(p):
    home = os.path.expanduser("~")
    return "~" + p[len(home):] if p.startswith(home + os.sep) else p


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    apply_mode = "--apply" in sys.argv
    include_code = "--include-code" in sys.argv
    if len(args) < 2 or args[0] not in MIGRATIONS:
        print(__doc__)
        print("migrations:", ", ".join(sorted(MIGRATIONS)))
        sys.exit(2)
    migration = MIGRATIONS[args[0]]
    repos = [os.path.abspath(os.path.expanduser(r)) for r in args[1:]]
    for r in repos:
        if not os.path.isdir(r):
            sys.exit(f"not a directory: {r}")

    text_edits, file_renames, dir_renames, code_hits = plan(
        migration, repos, include_code)

    print(f"migration: {migration.name}")
    print(f"repos: {', '.join(disp(r) for r in repos)}")
    print(f"code:  {'INCLUDED' if include_code else 'reported only'}")
    print()
    print(f"  text files to edit   {len(text_edits)}")
    print(f"  files to rename      {len(file_renames)}")
    print(f"  folders to rename    {len(dir_renames)}")
    print(f"  code files MATCHED   {len(code_hits)}   (reported, not rewritten)")
    print()
    for label, rows in (("text (first 5)", [(f"{disp(p)}  [{n} lines]",)
                                            for p, n in text_edits[:5]]),
                        ("file renames (first 5)",
                         [(f"{disp(a)}\n        -> {os.path.basename(b)}",)
                          for a, b in file_renames[:5]]),
                        ("folder renames (first 5)",
                         [(f"{disp(a)}\n        -> {os.path.basename(b)}",)
                          for a, b in dir_renames[:5]])):
        if rows:
            print(f"  {label}:")
            for (r,) in rows:
                print(f"    {r}")
            print()
    if code_hits:
        print("  code files matching an address — review by hand:")
        for p in code_hits:
            print(f"    {disp(p)}")
        print()

    if not apply_mode:
        print("dry run — nothing written. Re-run with --apply.")
        return 0
    apply(migration, text_edits, file_renames, dir_renames)
    print("applied.")
    print("now run: generate_nodes.py <roots> --projections --apply,")
    print("         generate_dashboards.py <roots>, check_plans.py <roots>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
