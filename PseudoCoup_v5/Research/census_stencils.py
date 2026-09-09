#!/usr/bin/env python3
"""The stencil/variant census — the automation, saved as an artifact.

    python3 PseudoCoup_v5/Research/census_stencils.py <src_dir>...

Ran ephemerally in chat 2026-08-07 (produced the 95/58, 91/14, and
120/33 numbers); saved at the owner's push that the pipeline must be
automation, not an anecdote plus a planned human review.

Inputs: the PINNED grammar (tree-sitter 0.26.0 / tree-sitter-rust
0.24.2 — the manifest of record) and a source corpus. Outputs, per
named kind, a mechanical three-way classification with NO judgment
step:

  STENCIL   one anonymous-token pattern ever -> the pack rebuilds it;
            nothing stored per instance.
  DERIVED   pattern varies, but the named sub-node structure fully
            determines it (arity) -> nothing stored; the structure
            already says it.
  VARIANT   one structure maps to SEVERAL token sets -> a genuine
            token fact; the mapper stores it on TsOrigin.variant,
            read from the tree at mint.

Sufficiency is not argued, it is verified: the reconstruction oracle
(log_015 §2 — unparse, re-ingest, converge) run over the corpus is
the check that the classification missed nothing. A convergence
failure names the kind that needs a variant; a human rules on
refusals only.

Trailing-separator variance (arguments `(,)` vs `()`) lands in
VARIANT by this test but may be NORMALIZED away instead of stored —
faithful convergence permits canonical formatting. That is a policy
line in the pack, not a per-row judgment.
"""
import collections
import pathlib
import sys

from tree_sitter import Language, Parser
import tree_sitter_rust as tsr  # per-language: swap the grammar module


def census(src_dirs):
    lang = Language(tsr.language())
    parser = Parser(lang)
    files = [f for d in src_dirs for f in pathlib.Path(d).rglob("*.rs")]
    groups = collections.defaultdict(lambda: collections.defaultdict(set))
    patterns = collections.defaultdict(set)
    counts = collections.Counter()
    for f in files:
        tree = parser.parse(f.read_bytes())
        stack = [tree.root_node]
        while stack:
            n = stack.pop()
            if n.is_named:
                counts[n.type] += 1
                skey = tuple(c.type for c in n.children if c.is_named)
                akey = tuple(c.type for c in n.children if not c.is_named)
                groups[n.type][skey].add(akey)
                patterns[n.type].add(akey)
            stack.extend(n.children)

    rows = []
    for kind in sorted(groups, key=lambda k: -counts[k]):
        if len(patterns[kind]) == 1:
            cls = "STENCIL"
        elif all(len(a) == 1 for a in groups[kind].values()):
            cls = "DERIVED"
        else:
            cls = "VARIANT"
        rows.append((kind, counts[kind], cls))
    return files, rows


def main():
    src = sys.argv[1:] or ["Sources/rust/compiler/rustc_codegen_ssa",
                           "Sources/rust/compiler/rustc_codegen_llvm"]
    src = [pathlib.Path(s).expanduser() for s in src]
    files, rows = census(src)
    tally = collections.Counter(cls for _, _, cls in rows)
    print(f"files: {len(files)}   kinds: {len(rows)}   {dict(tally)}")
    print(f"| kind | instances | class |")
    print(f"| --- | --- | --- |")
    for kind, n, cls in rows:
        print(f"| {kind} | {n} | {cls} |")


if __name__ == "__main__":
    main()
