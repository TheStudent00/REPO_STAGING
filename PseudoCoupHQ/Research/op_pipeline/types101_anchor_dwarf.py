#!/usr/bin/env python3
"""types101_anchor_dwarf.py -- TASK t101b, step 1 of the dominant-types
join done the way log_213 §8 said it had to be done: the parameter and
return types of every accepted probe are READ FROM THE COMPILER, by
recompiling the probe at its ANCHOR flags and following DW_AT_type in
the binary's own DWARF.

WHY THIS EXISTS.  Task t101 (log_213) found that every stored DWARF
parameter table on disk carries two fields, `name` and `location`; the
probe lane that captured them took DW_AT_name and DW_AT_location off
each DW_TAG_formal_parameter and never followed DW_AT_type, so no byte
size (DW_AT_byte_size) and no encoding (DW_AT_encoding) exists in any
store, and the anchor objects themselves were built in a container
scratch that did not survive.  The coordinator's ruling: the types are
re-read from the compiler.  That is this program.

METHOD, exactly.
  1. The population is every ACCEPTED probe of the two compiled
     populations the pool draws from:
       regenerated -- trickle_store/op_units2_<lang>_c<NNNN>.json
                      (29,288 accepted over 326 chunks, log_131)
       original    -- op_units_<lang>.json (1,779 accepted, logs 125-130)
     A probe is accepted when its store record carries an `anchor`
     side and no `refused` field.
  2. Each probe's source is REGENERATED FROM ITS `meta` by the same
     template functions that wrote it -- probe_gen.emit_c / emit_cpp /
     emit_go / emit_rust / emit_swift, imported, not copied -- from
     the meta fields (n, operator, arity, position, lhs_type, rhs_type,
     result_type).  The rendering is cross-checked byte for byte
     against the manifest's own stored `source` (probe_manifest2_<lang>
     .json / probe_manifest_<lang>.json); a probe whose re-rendering
     differs is REFUSED by name and not compiled.
  3. The probe is compiled at its ANCHOR flags only -- no ship build,
     no objdump.  The flags are the ones the probe lanes pinned
     (type_inventory3.json `pins_verified_in_container.flags`):
       c      clang   -std=c17   -O0 -g -c
       cpp    clang++ -std=c++20 -O0 -g -c
       rust   rustc --crate-type=lib --emit=obj -C opt-level=0 -g
       go     go build -gcflags=all=-N -l        (DWARF on, the default)
       swift  swiftc -Onone -g -c
     The go flag is the brief's `all=-N -l` form; the trickle lane
     wrote `-gcflags=-N -l`, which is the same two flags applied to the
     main package only.  The difference cannot reach the probe
     function's DWARF, which lives in the main package either way.
  4. pyelftools opens the object (go: the linked binary).  The
     DW_TAG_subprogram carrying the probe's symbol is found (DW_AT_name
     or DW_AT_linkage_name; exact, or -- for a swift probe whose result
     is not C-representable and so has no @_cdecl thunk -- the symbol
     as a whole token inside the mangled name).  For each
     DW_TAG_formal_parameter under it, DW_AT_type is followed through
     typedef / const / volatile / pointer to the type that carries
     DW_AT_byte_size and DW_AT_encoding, and the chain is written down
     as pyelftools read it.  The walk is dwarf_typed_key.py's
     `render_type` (task 24), copied here with two changes: it also
     records DW_AT_encoding, and it dereferences DW_AT_type through
     pyelftools' `get_DIE_from_attribute`, which honours the reference
     FORM -- go writes DW_FORM_ref_addr (an absolute .debug_info offset),
     clang and rustc write DW_FORM_ref4 (CU-relative), and the task-24
     walk handled only the second.
     The RETURN type is the subprogram's own DW_AT_type; for go, whose
     subprogram DIEs carry no DW_AT_type, it is the formal parameter
     the compiler flags DW_AT_variable_parameter (go's result slot,
     named `~r0`).
  5. One row per parameter and one row per result goes to a shard
     named after the store file it came from, under
     types101_dwarf_rows/, and an index types101_dwarf_rows.json is
     written at the end.  The build directory is deleted the moment
     its DWARF has been read.  Nothing on disk is edited: the stores,
     the manifests, fold.py and dwarf_typed_key.py are read only.

WHAT A ROW SAYS.  Every fact on it is either the compiler's (the
`dwarf_*` fields, read off DIEs) or the manifest's (`declared_spelling`,
the type the probe's source declared).  No class and no width is
assigned from a spelling anywhere here: a base type that carries no
DW_AT_encoding is recorded with `dwarf_encoding: null` and
`dwarf_encoding_absent_on_the_type: true`, and the first such DIE per
language is kept LITERAL in the index so the report can quote it.

MEMORY.  Bound ABORT_MEMORY_T101B = 4 GB on the PARENT, checked with
resource.getrusage(RUSAGE_SELF) after every store file; the parent
holds one store file, one language's manifest narrowed to the accepted
probes' sources, and one store file's rows at a time.  The workers are
separate processes (a compiler and a small pyelftools read each).

SPELLING BAN.  Nothing is keyed, grouped, paired or selected by an
operator token.  The probe's `operator` is read only to hand it to
probe_gen's template so the source can be re-rendered; it is not
written to any row.  Rows are keyed by store file and probe number.

USAGE (inside the t101b instance, cwd this folder):
  python3 types101_anchor_dwarf.py --sample 12        60 probes, 12 per language
  python3 types101_anchor_dwarf.py                    the whole population
  options: --langs c,cpp,go,rust,swift  --workers 6  --force  --work DIR
"""

import argparse
import collections
import concurrent.futures
import json
import os
import re
import resource
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import probe_gen  # noqa: E402  -- the templates that wrote every probe

LANGS = ["c", "cpp", "go", "rust", "swift"]
ABORT_MEMORY_T101B_BYTES = 4 * 1024 * 1024 * 1024

CLANG = "/usr/bin/clang"
CLANGXX = "/usr/bin/clang++"
SWIFTC = "/persist/swift/usr/bin/swiftc"
GOMOD = "module opprobe\n\ngo 1.26\n"

# The anchor flags, literal, so the index can carry them.
ANCHOR_FLAGS = {
    "c": "/usr/bin/clang -std=c17 -O0 -g -c unit.c -o unit_anchor.o",
    "cpp": "/usr/bin/clang++ -std=c++20 -O0 -g -c unit.cpp -o unit_anchor.o",
    "rust": "rustc --crate-type=lib --emit=obj -C opt-level=0 -g -o unit_anchor.o unit.rs",
    "go": "go build -gcflags=all=-N -l -o bin_anchor .",
    "swift": "/persist/swift/usr/bin/swiftc -Onone -g -c unit.swift -o unit_anchor.o",
}


# ------------------------------------------------------------------ util

def peak_rss_bytes():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024


def memory_guard(where):
    rss = peak_rss_bytes()
    if rss > ABORT_MEMORY_T101B_BYTES:
        sys.stderr.write("ABORT_MEMORY_T101B: parent peak RSS %d bytes "
                         "exceeded the stated 4 GB bound after %s\n"
                         % (rss, where))
        sys.exit(3)
    return rss


def sh(cmd, cwd=None, timeout=180, env=None):
    try:
        p = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=timeout, env=env)
        return (p.returncode, p.stdout.decode("utf-8", "replace"),
                p.stderr.decode("utf-8", "replace"))
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT after %ds" % timeout
    except OSError as e:
        return 125, "", "OSError %s" % e


DIAG = re.compile(r"^[^\s:]+:\d+(:\d+)?:")


def firstline(txt):
    """The compiler's own words for why it refused.  The rule is the
    probe lane's (lane_gen.py `firstline`): a line saying `error`, else a
    line in the file:line:col: shape, else the first non-banner line."""
    lines = [ln.strip() for ln in txt.splitlines() if ln.strip()]
    for ln in lines:
        if re.search(r"\berror\b", ln, re.I):
            return ln[:200]
    for ln in lines:
        if DIAG.match(ln):
            return ln[:200]
    for ln in lines:
        if not ln.startswith("#"):
            return ln[:200]
    return lines[0][:200] if lines else "(no diagnostic)"


def strip_paths(line):
    """A refusal line begins with the build directory, which carries the
    probe number; drop it so identical refusals fold together."""
    return re.sub(r"^/\S*?/(unit\.\w+|main\.go)", r"\1", line)


# ------------------------------------------------------- the population

def store_files(langs):
    """(language, population, path) for every store the pool draws on."""
    got = []
    trickle = os.path.join(HERE, "trickle_store")
    for lang in langs:
        for name in sorted(os.listdir(trickle)):
            if name.startswith("op_units2_%s_c" % lang) and name.endswith(".json"):
                got.append((lang, "regenerated", os.path.join(trickle, name)))
        p = os.path.join(HERE, "op_units_%s.json" % lang)
        if os.path.isfile(p):
            got.append((lang, "original", p))
    return got


def accepted_probes(doc):
    """[(n, meta)] for every accepted probe in one store document."""
    out = []
    for key, probe in doc["probes"].items():
        if not isinstance(probe, dict) or "refused" in probe:
            continue
        if not isinstance(probe.get("anchor"), dict):
            continue
        meta = probe["meta"]
        out.append((int(meta["n"]), meta))
    out.sort()
    return out


def render_source(lang, meta):
    """The probe's source, regenerated from its meta by the template that
    wrote it.  Returns (source, cdecl_or_None)."""
    n = meta["n"]
    op, ar, pos = meta["operator"], meta["arity"], meta["position"]
    lt, rt, res = meta["lhs_type"], meta["rhs_type"], meta.get("result_type")
    if lang == "c":
        return probe_gen.emit_c(n, op, ar, pos, lt, rt), None
    if lang == "cpp":
        return probe_gen.emit_cpp(n, op, ar, pos, lt, rt), None
    if lang == "go":
        return probe_gen.emit_go(n, op, ar, pos, lt, rt, res), None
    if lang == "rust":
        return probe_gen.emit_rust(n, op, ar, pos, lt, rt, res), None
    if lang == "swift":
        return probe_gen.emit_swift(n, op, ar, pos, lt, rt, res)
    raise KeyError(lang)


class Manifests:
    """One language's manifest at a time, narrowed to {n: source}."""

    def __init__(self):
        self.key = None
        self.sources = {}

    def sources_for(self, lang, population, wanted):
        key = (lang, population)
        if self.key != key:
            name = ("probe_manifest2_%s.json" if population == "regenerated"
                    else "probe_manifest_%s.json") % lang
            doc = json.load(open(os.path.join(HERE, name)))
            self.sources = {int(k): p["source"] for k, p in doc["probes"].items()}
            del doc
            self.key = key
        return {n: self.sources.get(n) for n in wanted}


# --------------------------------------------------------- the compile

def compile_anchor(lang, d, source):
    """(rc, artifact, diagnostic) at the ANCHOR flags only."""
    env = dict(os.environ)
    if lang == "c":
        src = os.path.join(d, "unit.c")
        obj = os.path.join(d, "unit_anchor.o")
        open(src, "w").write(source)
        rc, so, se = sh([CLANG, "-std=c17", "-O0", "-g", "-c", src, "-o", obj])
        return rc, obj, (se or so)
    if lang == "cpp":
        src = os.path.join(d, "unit.cpp")
        obj = os.path.join(d, "unit_anchor.o")
        open(src, "w").write(source)
        rc, so, se = sh([CLANGXX, "-std=c++20", "-O0", "-g", "-c", src, "-o", obj])
        return rc, obj, (se or so)
    if lang == "rust":
        src = os.path.join(d, "unit.rs")
        obj = os.path.join(d, "unit_anchor.o")
        open(src, "w").write(source)
        rc, so, se = sh(["rustc", "--crate-type=lib", "--emit=obj",
                         "-C", "opt-level=0", "-g", "-o", obj, src])
        return rc, obj, (se or so)
    if lang == "go":
        open(os.path.join(d, "go.mod"), "w").write(GOMOD)
        open(os.path.join(d, "main.go"), "w").write(source)
        obj = os.path.join(d, "bin_anchor")
        rc, so, se = sh(["go", "build", "-gcflags=all=-N -l", "-o", obj, "."],
                        cwd=d, timeout=300, env=env)
        return rc, obj, (se or so)
    if lang == "swift":
        src = os.path.join(d, "unit.swift")
        obj = os.path.join(d, "unit_anchor.o")
        open(src, "w").write(source)
        rc, so, se = sh([SWIFTC, "-Onone", "-g", "-c", src, "-o", obj],
                        timeout=300)
        return rc, obj, (se or so)
    raise KeyError(lang)


# ------------------------------------------------------- the DWARF read

def _elftools():
    from elftools.elf.elffile import ELFFile
    from elftools.dwarf.enums import ENUM_DW_ATE
    ate = {v: k for k, v in ENUM_DW_ATE.items()}
    return ELFFile, ate


def attr(die, name):
    a = die.attributes.get(name)
    return a.value if a is not None else None


def sname(die):
    v = attr(die, "DW_AT_name")
    if v is None:
        return None
    return v.decode("utf-8", "replace") if isinstance(v, bytes) else str(v)


def linkage(die):
    v = attr(die, "DW_AT_linkage_name")
    if v is None:
        v = attr(die, "DW_AT_MIPS_linkage_name")
    if v is None:
        return None
    return v.decode("utf-8", "replace") if isinstance(v, bytes) else str(v)


def deref(die):
    """The DIE DW_AT_type points at, whatever reference FORM carries it."""
    if "DW_AT_type" not in die.attributes:
        return None
    try:
        return die.get_DIE_from_attribute("DW_AT_type")
    except Exception:
        return None


def literal_die(die, ate):
    """The DIE as pyelftools read it: tag, offset, every attribute with
    its form and value.  Kept so the report can quote a DIE verbatim."""
    out = {"tag": die.tag, "offset": hex(die.offset), "attributes": {}}
    for name, a in die.attributes.items():
        v = a.value
        if isinstance(v, bytes):
            v = v.decode("utf-8", "replace")
        elif isinstance(v, list):
            v = [int(x) for x in v]
        if name == "DW_AT_encoding" and isinstance(v, int):
            v = "%d (%s)" % (v, ate.get(v, "DW_ATE_?"))
        out["attributes"][name] = {"form": a.form, "value": v}
    return out


def type_chain(die, ate, depth=0):
    """Follow DW_AT_type through the modifiers and typedefs, writing each
    DIE down as read, until the DIE that carries the size and encoding."""
    chain = []
    while die is not None and depth < 24:
        enc = attr(die, "DW_AT_encoding")
        node = {
            "tag": die.tag,
            "name": sname(die),
            "byte_size": attr(die, "DW_AT_byte_size"),
            "encoding": ate.get(enc, "DW_ATE_%d" % enc) if enc is not None else None,
        }
        chain.append(node)
        if die.tag in ("DW_TAG_typedef", "DW_TAG_const_type",
                       "DW_TAG_volatile_type", "DW_TAG_pointer_type",
                       "DW_TAG_reference_type", "DW_TAG_rvalue_reference_type",
                       "DW_TAG_restrict_type", "DW_TAG_atomic_type"):
            die = deref(die)
            depth += 1
            continue
        break
    return chain


def render_spelling(chain):
    """The C-style spelling of a chain, the way dwarf_typed_key.py renders
    it: modifiers prefixed, pointer suffixed, typedef by its own name."""
    if not chain:
        return None
    last = chain[-1]
    base = last["name"] or last["tag"]
    if last["tag"] in ("DW_TAG_structure_type", "DW_TAG_class_type",
                       "DW_TAG_union_type", "DW_TAG_enumeration_type"):
        kw = {"DW_TAG_structure_type": "struct ", "DW_TAG_class_type": "class ",
              "DW_TAG_union_type": "union ", "DW_TAG_enumeration_type": "enum "}
        base = kw[last["tag"]] + (last["name"] or "<anon>")
    out = base
    for node in reversed(chain[:-1]):
        t = node["tag"]
        if t == "DW_TAG_typedef":
            out = node["name"] or out
        elif t == "DW_TAG_const_type":
            out = "const " + out
        elif t == "DW_TAG_volatile_type":
            out = "volatile " + out
        elif t == "DW_TAG_pointer_type":
            out = out + "*"
        elif t == "DW_TAG_reference_type":
            out = out + "&"
        elif t == "DW_TAG_rvalue_reference_type":
            out = out + "&&"
    return out


def structure_members(die, ate, limit=4):
    """For a type DIE that is a structure (swift's Int32 is one), the
    stored members and their own chains, one hop deep."""
    if die is None or die.tag != "DW_TAG_structure_type":
        return None
    got = []
    for ch in die.iter_children():
        if ch.tag != "DW_TAG_member":
            continue
        got.append({"name": sname(ch), "chain": type_chain(deref(ch), ate)})
        if len(got) >= limit:
            break
    return got


def terminal_die(die):
    """The DIE the chain stops on (same walk as type_chain)."""
    depth = 0
    while die is not None and depth < 24:
        if die.tag in ("DW_TAG_typedef", "DW_TAG_const_type",
                       "DW_TAG_volatile_type", "DW_TAG_pointer_type",
                       "DW_TAG_reference_type", "DW_TAG_rvalue_reference_type",
                       "DW_TAG_restrict_type", "DW_TAG_atomic_type"):
            die = deref(die)
            depth += 1
            continue
        break
    return die


def symbol_matches(sym, exact, names):
    if exact:
        return any(n == sym for n in names if n)
    pat = re.compile(r"(?<![0-9A-Za-z_])" + re.escape(sym) + r"(?![0-9])")
    return any(pat.search(n) for n in names if n)


def read_types(path, lang, sym, exact):
    """({rows-in-the-making}, error) for the subprogram carrying `sym`."""
    ELFFile, ate = _elftools()
    with open(path, "rb") as fh:
        elf = ELFFile(fh)
        if not elf.has_dwarf_info():
            return None, "no DWARF in the anchor object"
        dw = elf.get_dwarf_info()
        hits = []
        for cu in dw.iter_CUs():
            top = cu.get_top_DIE()
            if lang == "go" and sname(top) != "main":
                continue
            for die in cu.iter_DIEs():
                if die.tag != "DW_TAG_subprogram":
                    continue
                if not symbol_matches(sym, exact, [sname(die), linkage(die)]):
                    continue
                params = [ch for ch in die.iter_children()
                          if ch.tag == "DW_TAG_formal_parameter"]
                hits.append((die, params, cu))
            if lang == "go":
                break
        if not hits:
            return None, "no DW_TAG_subprogram named %s" % sym
        chosen = None
        for die, params, cu in hits:
            if params:
                chosen = (die, params, cu)
                break
        if chosen is None:
            return None, ("%d subprogram DIE(s) match %s and none carries a "
                          "DW_TAG_formal_parameter" % (len(hits), sym))
        die, params, cu = chosen
        out = {"subprogram_name": sname(die),
               "subprogram_linkage_name": linkage(die),
               "subprograms_matching": len(hits),
               "parameters": [], "result": None}
        for ch in params:
            tdie = deref(ch)
            chain = type_chain(tdie, ate)
            term = terminal_die(tdie)
            rec = {
                "param_name": sname(ch),
                "variable_parameter": attr(ch, "DW_AT_variable_parameter"),
                "chain": chain,
                "spelling": render_spelling(chain),
                "members": structure_members(term, ate),
                "terminal_literal": literal_die(term, ate) if term is not None else None,
            }
            out["parameters"].append(rec)
        if "DW_AT_type" in die.attributes:
            tdie = deref(die)
            chain = type_chain(tdie, ate)
            term = terminal_die(tdie)
            out["result"] = {
                "param_name": None,
                "chain": chain,
                "spelling": render_spelling(chain),
                "members": structure_members(term, ate),
                "terminal_literal": literal_die(term, ate) if term is not None else None,
            }
        return out, None


# ------------------------------------------------------------ one probe

def one_probe(task):
    """Runs in a worker process: compile at anchor, read, delete."""
    lang = task["lang"]
    d = os.path.join(task["work"], "%s_%s_n%d" % (lang, task["population"][:4], task["n"]))
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    t0 = time.time()
    try:
        rc, obj, err = compile_anchor(lang, d, task["source"])
        if rc != 0 or not os.path.exists(obj):
            return {"n": task["n"], "outcome": "refused",
                    "refusal": strip_paths(firstline(err)),
                    "seconds": round(time.time() - t0, 3)}
        try:
            got, why = read_types(obj, lang, task["symbol"], task["symbol_exact"])
        except Exception as e:  # pyelftools raised: recorded, never hidden
            got, why = None, "pyelftools raised %s: %s" % (type(e).__name__, e)
        if got is None:
            return {"n": task["n"], "outcome": "no_dwarf_read", "why": why,
                    "seconds": round(time.time() - t0, 3)}
        got["n"] = task["n"]
        got["outcome"] = "typed"
        got["seconds"] = round(time.time() - t0, 3)
        return got
    finally:
        shutil.rmtree(d, ignore_errors=True)


def rows_of(lang, population, store_name, meta, got):
    """The rows one typed probe contributes."""
    n = meta["n"]
    unit = "%s/%s_%d" % (lang, "regen" if population == "regenerated" else "op", n)
    declared = [meta.get("lhs_type"), meta.get("rhs_type")]
    common = {
        "language": lang, "population": population, "store_file": store_name,
        "probe_n": n, "unit": unit, "symbol": meta["symbol"],
        "subprogram_name": got["subprogram_name"],
        "subprogram_linkage_name": got["subprogram_linkage_name"],
    }
    rows = []
    pos = 0
    for p in got["parameters"]:
        role = "result" if p.get("variable_parameter") else "parameter"
        chain = p["chain"]
        term = chain[-1] if chain else {}
        row = dict(common)
        row.update({
            "role": role,
            "position": pos if role == "parameter" else None,
            "param_name": p["param_name"],
            "declared_spelling": (declared[pos] if role == "parameter" and pos < 2
                                  else (meta.get("result_type") if role == "result" else None)),
            "dwarf_spelling": p["spelling"],
            "dwarf_byte_size": term.get("byte_size"),
            "dwarf_encoding": term.get("encoding"),
            "dwarf_encoding_absent_on_the_type": bool(chain) and term.get("encoding") is None,
            "dwarf_terminal_tag": term.get("tag"),
            "dwarf_type_chain": chain,
        })
        if p.get("members"):
            row["dwarf_structure_members"] = p["members"]
        rows.append(row)
        if role == "parameter":
            pos += 1
    if got.get("result") is not None:
        p = got["result"]
        chain = p["chain"]
        term = chain[-1] if chain else {}
        row = dict(common)
        row.update({
            "role": "result", "position": None, "param_name": None,
            "declared_spelling": meta.get("result_type"),
            "dwarf_spelling": p["spelling"],
            "dwarf_byte_size": term.get("byte_size"),
            "dwarf_encoding": term.get("encoding"),
            "dwarf_encoding_absent_on_the_type": bool(chain) and term.get("encoding") is None,
            "dwarf_terminal_tag": term.get("tag"),
            "dwarf_type_chain": chain,
        })
        if p.get("members"):
            row["dwarf_structure_members"] = p["members"]
        rows.append(row)
    elif lang != "go" and not any(p.get("variable_parameter") for p in got["parameters"]):
        row = dict(common)
        row.update({"role": "result", "position": None, "param_name": None,
                    "declared_spelling": meta.get("result_type"),
                    "dwarf_spelling": None, "dwarf_byte_size": None,
                    "dwarf_encoding": None,
                    "dwarf_encoding_absent_on_the_type": False,
                    "dwarf_terminal_tag": None, "dwarf_type_chain": [],
                    "return_type_absent_in_dwarf": True})
        rows.append(row)
    return rows


# ------------------------------------------------------------- banners

def banners():
    out = {}
    for lang, cmd in [("c", [CLANG, "--version"]), ("cpp", [CLANGXX, "--version"]),
                      ("go", ["go", "version"]), ("rust", ["rustc", "--version"]),
                      ("swift", [SWIFTC, "--version"])]:
        rc, so, se = sh(cmd, timeout=60)
        text = (so or se).strip().splitlines()
        out[lang] = text[0] if text else "(rc %d: %s)" % (rc, (se or so).strip()[:120])
    try:
        import elftools
        out["pyelftools"] = elftools.__version__
    except Exception as e:
        out["pyelftools"] = "absent: %s" % e
    return out


# ----------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=0,
                    help="probes per language, spread over the population")
    ap.add_argument("--langs", default=",".join(LANGS))
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--force", action="store_true", help="rewrite existing shards")
    ap.add_argument("--work", default=os.environ.get("T101B_WORK", "/work/t101b"))
    args = ap.parse_args()
    langs = [l for l in args.langs.split(",") if l]

    sample = args.sample > 0
    shard_dir = os.path.join(HERE, "types101_dwarf_rows_sample" if sample
                             else "types101_dwarf_rows")
    index_path = shard_dir + ".json"
    os.makedirs(shard_dir, exist_ok=True)
    os.makedirs(args.work, exist_ok=True)
    os.environ.setdefault("HOME", args.work)
    os.environ["GOCACHE"] = os.path.join(args.work, "gocache")
    os.environ["GOPATH"] = os.path.join(args.work, "gopath")
    os.environ["GOTOOLCHAIN"] = "local"
    os.environ["GOPROXY"] = "off"
    os.environ["GOFLAGS"] = "-mod=mod"
    os.environ["PATH"] = "/persist/swift/usr/bin:" + os.environ.get("PATH", "")

    print("types101_anchor_dwarf.py -- %s" % ("SAMPLE %d per language" % args.sample
                                              if sample else "the whole population"))
    print("bound: ABORT_MEMORY_T101B at %d bytes on the parent" % ABORT_MEMORY_T101B_BYTES)
    ban = banners()
    for k, v in ban.items():
        print("  toolchain %-10s %s" % (k, v))
    sys.stdout.flush()

    files = store_files(langs)
    # In sample mode, pick `--sample` accepted probes per language spread
    # evenly over that language's whole accepted list (both populations).
    picks = None
    if sample:
        picks = {}
        for lang in langs:
            acc = []
            for l, pop, path in files:
                if l != lang:
                    continue
                doc = json.load(open(path))
                for n, meta in accepted_probes(doc):
                    acc.append((path, n))
                del doc
            k = min(args.sample, len(acc))
            chosen = set()
            for i in range(k):
                chosen.add(acc[(i * len(acc)) // k])
            picks[lang] = chosen
            print("  sample %-6s %d of %d accepted" % (lang, len(chosen), len(acc)))
        memory_guard("sampling")

    manifests = Manifests()
    tally = {l: collections.Counter() for l in langs}
    refusals = {l: collections.Counter() for l in langs}
    no_read = {l: collections.Counter() for l in langs}
    render_mismatch = {l: 0 for l in langs}
    encoding_absent = {l: collections.Counter() for l in langs}
    first_absent_die = {}
    shards = []
    peak = 0
    t_start = time.time()

    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
        for fi, (lang, population, path) in enumerate(files, 1):
            store_name = os.path.basename(path)
            shard_path = os.path.join(shard_dir, store_name)
            if os.path.exists(shard_path) and not args.force:
                sh_doc = json.load(open(shard_path))
                for k, v in sh_doc["tally"].items():
                    tally[lang][k] += v
                for r in sh_doc["refused"]:
                    refusals[lang][r["first_line"]] += 1
                for r in sh_doc["no_dwarf_read"]:
                    no_read[lang][r["why"]] += 1
                render_mismatch[lang] += sh_doc["tally"].get("render_differs_from_manifest", 0)
                for row in sh_doc["rows"]:
                    if row.get("dwarf_encoding_absent_on_the_type"):
                        encoding_absent[lang][row["dwarf_spelling"]] += 1
                if sh_doc.get("first_encoding_absent_die") and lang not in first_absent_die:
                    first_absent_die[lang] = sh_doc["first_encoding_absent_die"]
                shards.append({"store_file": store_name, "shard": os.path.relpath(shard_path, HERE),
                               "language": lang, "population": population,
                               "tally": sh_doc["tally"], "reused": True})
                print("[%d/%d] %s  (shard exists, reused)" % (fi, len(files), store_name))
                sys.stdout.flush()
                continue

            doc = json.load(open(path))
            acc = accepted_probes(doc)
            del doc
            if picks is not None:
                acc = [(n, m) for n, m in acc if (path, n) in picks[lang]]
            if not acc:
                continue
            sources = manifests.sources_for(lang, population, [n for n, _ in acc])

            tasks = []
            shard = {"generated_by": "types101_anchor_dwarf.py",
                     "store_file": store_name, "language": lang,
                     "population": population,
                     "anchor_flags": ANCHOR_FLAGS[lang],
                     "tally": collections.Counter(), "refused": [],
                     "no_dwarf_read": [], "rows": [],
                     "first_encoding_absent_die": None}
            metas = {}
            for n, meta in acc:
                shard["tally"]["accepted_in_store"] += 1
                src, cdecl = render_source(lang, meta)
                if sources.get(n) != src:
                    shard["tally"]["render_differs_from_manifest"] += 1
                    shard["refused"].append({"n": n, "first_line":
                                             "render_differs_from_manifest: the meta re-rendered "
                                             "by probe_gen is not the manifest's stored source"})
                    continue
                metas[n] = meta
                tasks.append({"lang": lang, "population": population, "n": n,
                              "symbol": meta["symbol"],
                              "symbol_exact": bool(meta["symbol_exact"]),
                              "source": src, "work": args.work})
            shard["tally"]["attempted"] = len(tasks)

            t0 = time.time()
            for got in pool.map(one_probe, tasks, chunksize=4):
                n = got["n"]
                if got["outcome"] == "refused":
                    shard["tally"]["refused_by_the_compiler"] += 1
                    shard["refused"].append({"n": n, "first_line": got["refusal"]})
                    continue
                shard["tally"]["compiled_at_anchor"] += 1
                if got["outcome"] != "typed":
                    shard["tally"]["no_dwarf_read"] += 1
                    shard["no_dwarf_read"].append({"n": n, "why": got["why"]})
                    continue
                shard["tally"]["typed"] += 1
                rows = rows_of(lang, population, store_name, metas[n], got)
                for row in rows:
                    if row["role"] == "parameter":
                        shard["tally"]["parameter_rows"] += 1
                        if row["dwarf_byte_size"] is not None:
                            shard["tally"]["parameters_with_a_byte_size"] += 1
                        if row["dwarf_encoding"] is not None:
                            shard["tally"]["parameters_with_an_encoding"] += 1
                    else:
                        shard["tally"]["result_rows"] += 1
                    if row["dwarf_encoding_absent_on_the_type"]:
                        encoding_absent[lang][row["dwarf_spelling"]] += 1
                        if shard["first_encoding_absent_die"] is None:
                            # the literal DIE, from the worker's read
                            src_p = None
                            for p in got["parameters"] + ([got["result"]] if got.get("result") else []):
                                if p["spelling"] == row["dwarf_spelling"]:
                                    src_p = p
                                    break
                            shard["first_encoding_absent_die"] = {
                                "probe_n": n, "unit": row["unit"],
                                "dwarf_spelling": row["dwarf_spelling"],
                                "die": src_p["terminal_literal"] if src_p else None,
                            }
                shard["rows"].extend(rows)
                shard["tally"]["seconds"] += got["seconds"]

            shard["tally"] = dict(shard["tally"])
            shard["tally"]["wall_seconds"] = round(time.time() - t0, 1)
            shard["rows"].sort(key=lambda r: (r["probe_n"], r["role"] == "result",
                                              r["position"] if r["position"] is not None else 99))
            tmp = shard_path + ".tmp"
            with open(tmp, "w") as fh:
                json.dump(shard, fh, indent=1, sort_keys=True)
                fh.write("\n")
            os.replace(tmp, shard_path)

            for k, v in shard["tally"].items():
                tally[lang][k] += v
            for r in shard["refused"]:
                refusals[lang][r["first_line"]] += 1
            for r in shard["no_dwarf_read"]:
                no_read[lang][r["why"]] += 1
            render_mismatch[lang] += shard["tally"].get("render_differs_from_manifest", 0)
            if shard["first_encoding_absent_die"] and lang not in first_absent_die:
                first_absent_die[lang] = shard["first_encoding_absent_die"]
            shards.append({"store_file": store_name, "shard": os.path.relpath(shard_path, HERE),
                           "language": lang, "population": population,
                           "tally": shard["tally"], "reused": False})
            print("[%d/%d] %-28s accepted %4d attempted %4d anchor %4d typed %4d "
                  "refused %3d  %.1fs" % (
                      fi, len(files), store_name, shard["tally"].get("accepted_in_store", 0),
                      shard["tally"].get("attempted", 0),
                      shard["tally"].get("compiled_at_anchor", 0),
                      shard["tally"].get("typed", 0),
                      shard["tally"].get("refused_by_the_compiler", 0),
                      shard["tally"]["wall_seconds"]))
            sys.stdout.flush()
            del shard, tasks, metas, sources
            peak = max(peak, memory_guard(store_name))

    per_language = {}
    for lang in langs:
        t = tally[lang]
        per_language[lang] = {
            "probes_accepted_in_the_stores": t.get("accepted_in_store", 0),
            "probes_attempted": t.get("attempted", 0),
            "render_differs_from_manifest": render_mismatch[lang],
            "compiled_at_anchor": t.get("compiled_at_anchor", 0),
            "refused_by_the_compiler": t.get("refused_by_the_compiler", 0),
            "no_dwarf_read": t.get("no_dwarf_read", 0),
            "probes_typed": t.get("typed", 0),
            "parameter_rows": t.get("parameter_rows", 0),
            "parameters_with_a_byte_size": t.get("parameters_with_a_byte_size", 0),
            "parameters_with_an_encoding": t.get("parameters_with_an_encoding", 0),
            "result_rows": t.get("result_rows", 0),
            "compile_and_read_seconds": round(t.get("seconds", 0.0), 1),
            "refused_by_compiler_message_first_line": [
                {"first_line": k, "probes": v}
                for k, v in refusals[lang].most_common()],
            "no_dwarf_read_by_cause": [
                {"why": k, "probes": v} for k, v in no_read[lang].most_common()],
            "types_carrying_no_DW_AT_encoding": [
                {"dwarf_spelling": k, "rows": v}
                for k, v in encoding_absent[lang].most_common()],
            "first_type_carrying_no_DW_AT_encoding_LITERAL": first_absent_die.get(lang),
        }

    index = {
        "generated_by": "types101_anchor_dwarf.py",
        "task": "t101b -- the parameter and return types of every accepted probe, "
                "re-read from the compiler at the ANCHOR flags (CORE_0_3_research "
                "§4.2 step 3, second leg after log_213's flag)",
        "mode": ("SAMPLE, %d probes per language spread over the population"
                 % args.sample) if sample else "the whole population",
        "population": {
            "regenerated": "trickle_store/op_units2_<lang>_c<NNNN>.json, accepted probes",
            "original": "op_units_<lang>.json, accepted probes",
            "a_probe_is_accepted_when": "its store record carries an `anchor` side and no `refused` field",
        },
        "source_regeneration": (
            "each probe's source is re-rendered from its store `meta` by probe_gen.emit_<lang>, "
            "and compared byte for byte with the manifest's stored `source`; a mismatch is "
            "refused by name (render_differs_from_manifest) and never compiled"),
        "anchor_flags": ANCHOR_FLAGS,
        "toolchain_banners_printed_in_lane": ban,
        "dwarf_read": (
            "pyelftools; DW_TAG_subprogram matched on DW_AT_name / DW_AT_linkage_name; "
            "each DW_TAG_formal_parameter's DW_AT_type followed through typedef / const / "
            "volatile / pointer to the DIE carrying DW_AT_byte_size and DW_AT_encoding; "
            "the return type from the subprogram's DW_AT_type, or for go from the formal "
            "parameter flagged DW_AT_variable_parameter"),
        "row_fields": {
            "declared_spelling": "the manifest's own declaration (meta lhs_type / rhs_type / result_type)",
            "dwarf_spelling": "the chain rendered C-style (typedef by its own name, modifiers prefixed)",
            "dwarf_byte_size": "DW_AT_byte_size on the terminal DIE of the chain",
            "dwarf_encoding": "DW_AT_encoding on the terminal DIE, by its DW_ATE_ name; null when absent",
            "dwarf_encoding_absent_on_the_type": "true when the terminal DIE carries no DW_AT_encoding",
            "dwarf_type_chain": "every DIE the walk passed, as read",
            "dwarf_structure_members": "when the terminal DIE is a structure: its members' own chains, one hop",
        },
        "per_language": per_language,
        "totals": {
            "store_files": len(shards),
            "probes_attempted": sum(v["probes_attempted"] for v in per_language.values()),
            "compiled_at_anchor": sum(v["compiled_at_anchor"] for v in per_language.values()),
            "probes_typed": sum(v["probes_typed"] for v in per_language.values()),
            "parameter_rows": sum(v["parameter_rows"] for v in per_language.values()),
            "result_rows": sum(v["result_rows"] for v in per_language.values()),
            "wall_seconds": round(time.time() - t_start, 1),
        },
        "shards": shards,
        "memory": {
            "bound": "ABORT_MEMORY_T101B at 4 GB on the parent, resource.getrusage(RUSAGE_SELF) after every store file",
            "parent_peak_rss_bytes": max(peak, peak_rss_bytes()),
            "parent_peak_rss_mb": round(max(peak, peak_rss_bytes()) / (1024.0 * 1024.0), 1),
            "workers": args.workers,
        },
        "spelling_ban": (
            "no operator token appears in any key, grouping, pairing or row structure; rows are "
            "keyed by store file and probe number, and the probe operator is read only to hand "
            "it to probe_gen's template"),
    }
    tmp = index_path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(index, fh, indent=1, sort_keys=True)
        fh.write("\n")
    os.replace(tmp, index_path)

    print("")
    print("wrote %s and %d shard(s) under %s" % (index_path, len(shards), shard_dir))
    print("%-6s %9s %9s %9s %9s %9s %9s %9s" % (
        "lang", "accepted", "attempt", "anchor", "typed", "refused", "params", "enc"))
    for lang in langs:
        v = per_language[lang]
        print("%-6s %9d %9d %9d %9d %9d %9d %9d" % (
            lang, v["probes_accepted_in_the_stores"], v["probes_attempted"],
            v["compiled_at_anchor"], v["probes_typed"], v["refused_by_the_compiler"],
            v["parameter_rows"], v["parameters_with_an_encoding"]))
    print("parent peak RSS: %.1f MB (bound 4096.0 MB); wall %.1fs" % (
        index["memory"]["parent_peak_rss_mb"], index["totals"]["wall_seconds"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
