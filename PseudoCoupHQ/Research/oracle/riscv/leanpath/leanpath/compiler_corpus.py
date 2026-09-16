"""compiler_corpus -- Language.compiler_corpus (plan node
hq.research.lean_proof_path_resistant_to_churn.language.compiler_corpus):
EVERY compiler-operator of a language, function-wrapped and lowered.

The probes come from the operator pipeline's manifest for the language
(`Research/op_pipeline/probe_manifest_<lang>.json`: one probe per
(operator, lhs holder, rhs holder), generated from the language's own
grammar and holders; its `source` is the function-wrapped operator).
This file writes each probe's source to a file and lists them as units
for the walk, which compiles each at the corpus's own ship flags for
riscv64 (`Language.compile`), cuts the body out at its symbol and reads
its meaning through Sail's decoder and definitions.

  python3 -m leanpath probes <probe_manifest.json> <lang> <out_dir> [n_limit] [stride]

`stride k` takes every k-th probe of the manifest (the gate before a
long run: a dozen units spread over the operators, not the first dozen).

Nothing here names an operator: every probe in the manifest is taken,
in manifest order. A probe the compiler refuses is a refusal row of the
walk, with the compiler's line.
"""
import json
import os
import re

EXT = {"c": "c", "cpp": "cpp", "rust": "rs", "go": "go"}

# the one invocation line per language: the corpus's own ship flags for riscv64 (plumbing, written once).
# c and go are the lines task rv2 attested the corpus with (Research/oracle/riscv/attest_rv.json meta);
# cpp and rust are the same route through the walk's compile_unit.
SHIP_FLAGS = {
    "c": "clang -std=c17 -O1 --target=riscv64-unknown-linux-gnu -nostdlibinc",
    # cpp: the corpus's own `-O1`; for riscv64 the C++ headers come from the gcc toolchain (the line that lowered
    # the cpp probes on the tower on 2026-09-14; `-nostdlibinc` has no <cstdint>)
    "cpp": "clang++ -std=c++20 -O1 --target=riscv64-linux-gnu --gcc-toolchain=/usr",
    "rust": "rustc --target riscv64gc-unknown-linux-gnu --crate-type lib --emit obj -C opt-level=1",
    "go": "GOARCH=riscv64 GOOS=linux go build",
}


def holder_width(rep):
    """the width of a holder from the manifest's rep: i32 -> 32, u64 -> 64, f32 -> 32, bool -> 1; None when unknown"""
    if not rep:
        return None
    m = re.search(r"(\d+)$", rep)
    if m:
        return int(m.group(1))
    return 1 if rep == "bool" else None


def units_of_manifest(manifest_path, lang, out_dir, limit=None, stride=1):
    m = json.load(open(manifest_path))
    probes = m["probes"]
    items = list(probes.values()) if isinstance(probes, dict) else list(probes)
    items.sort(key=lambda p: p["n"])
    if stride and stride > 1:
        items = items[::stride]
    if limit:
        items = items[:limit]
    src_dir = os.path.join(out_dir, "corpus")
    os.makedirs(src_dir, exist_ok=True)
    units = []
    for p in items:
        name = "%s__op_%d" % (lang, p["n"])
        path = os.path.join(src_dir, "%s.%s" % (name, EXT[lang]))
        open(path, "w").write(p["source"])
        symbol = p["symbol"]
        if lang == "go" and symbol.startswith("main."):
            symbol = symbol[len("main."):]          # the walk spells go's symbol main.<symbol> itself
        units.append({"name": name, "lang": lang, "source": path, "symbol": symbol, "flags": SHIP_FLAGS[lang],
                      "cell_display": "%s %s %s %s" % (lang, p["operator"], p.get("lhs_type"), p.get("rhs_type") or ""),
                      # the probe's own label, on an object that identifies the one unit (the spelling guard's rule:
                      # an operator token is a per-unit display label, never a key or a grouping)
                      "probe": {"unit": name, "lang": lang, "n": p["n"], "operator": p["operator"], "arity": p["arity"],
                                "lhs_type": p.get("lhs_type"), "rhs_type": p.get("rhs_type"),
                                "lhs_rep": p.get("lhs_rep"), "rhs_rep": p.get("rhs_rep"), "expression": p["expression"]},
                      # the holder widths of the unit's parameters, read off the manifest's reps (i32 -> 32, u64 -> 64,
                      # bool -> 1): the width rule of log 283 §3, so a unit on a narrow holder is never called at 64
                      "holders": [holder_width(p.get("lhs_rep"))] + ([holder_width(p.get("rhs_rep"))] if p.get("rhs_rep") else [])})
    return units, m.get("meta", {})


def cmd_probes(argv, say, write_json):
    manifest, lang, out_dir = argv[0], argv[1], argv[2]
    limit = int(argv[3]) if len(argv) > 3 and argv[3] not in ("", "0") else None
    stride = int(argv[4]) if len(argv) > 4 else 1
    units, meta = units_of_manifest(manifest, lang, out_dir, limit, stride)
    write_json(os.path.join(out_dir, "units.json"), units)
    write_json(os.path.join(out_dir, "manifest_meta.json"), {"manifest": manifest, "meta": meta, "units": len(units)})
    say("  compiler_corpus %s: %d probes written as units under %s" % (lang, len(units), out_dir))
    return 0
