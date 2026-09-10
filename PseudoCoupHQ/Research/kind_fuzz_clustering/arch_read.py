#!/usr/bin/env python3
"""arch_read.py -- fold an ARCH lane's output back onto its manifest.

Reads
    PUBLIC/Airlock/agent/out/arch_<lang>.txt
    arch_manifest_<lang>.json
Writes
    arch_units_<lang>.json
    arch_cross_scalar.json          (with --cross)
    arch_cross_scalar_sem.json      (with --cross --sem)

Each arch-unit keeps THREE columns, unmerged, as ruled, and a FOURTH
that arrived later:

    bytes   the raw hex machine encoding, exactly as the compiler
            emitted it
    mnem    the mnemonic sequence exactly as objdump printed it
    canon   a DERIVED column, computed here and only here

`bytes` and `mnem` are never edited.  `canon` is what is left after
three normalizations are applied to a COPY of them.  Every one of the
three is a fixed mechanical pattern with a stated rule, not a
judgement, and each lives in its own function below whose docstring is
that rule:

    strip_entry_endbr64      the CET landing pad at position 0
    strip_go_stack_growth    go's stack-growth check, tail block, frame
    normalize_addresses      branch targets, call targets, %rip

    sem     a DERIVED column too, computed by arch_sem.py and requested
            with --sem.  A lifted, register-blind and
            selection-blind reading of the same bytes.

`canon` carries both a byte list and a mnemonic list, because both
questions get asked of it.  A canonical byte is the literal byte unless
its instruction's operand was a LINK-TIME fact -- a `call` displacement
or a `%rip` displacement -- in which case every byte of that
instruction reads `??`.  Relative branches are NOT masked: x86 encodes
a near jump as a displacement from the following instruction already,
so two identical operations at two link addresses have identical branch
bytes without any help.

`sem` is the fourth column and is described in full in arch_sem.py,
which computes it.  Where `canon` asks what the compiler WROTE once the
layout facts are off it, `sem` asks what what it wrote COMPUTES: the
bytes are lifted into VEX, the lifted form is normalized until neither
instruction selection nor the choice of physical register can show
through, and what is left is compared.  It is a fourth column and not a
replacement for the third -- the difference between the answers `canon`
and `sem` give is itself a measurement, and collapsing them would throw
it away.

usage:
  arch_read.py <lang> [<lang> ...] [--out-name NAME] [--outdir DIR]
  arch_read.py --cross                    cross-language scalar table
  arch_read.py <lang> ... --sem --cross   with the lifted column too
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
AIRLOCK_OUT = "PUBLIC/Airlock/agent/out"

LANGS = ["cpp", "rust", "go", "swift"]
SCALAR_FORMS = {"whole", "fractional", "truth"}

# `sem` is a FOURTH column and lives in its own module, arch_sem.py,
# because it needs a machine-code lifter (pyvex) that this file must not
# be made to require: a fold has to keep working on a machine where that
# lifter is not installed.  Where it IS importable, `--sem` computes the
# column during the fold; where it is not, `--sem` says so and stops.
try:
    import arch_sem as SEM
except Exception as _sem_exc:                                # noqa: BLE001
    SEM = None
    SEM_WHY = "%s: %s" % (type(_sem_exc).__name__, _sem_exc)


# ------------------------------------------------------------ lane input

def read_lane(path):
    """one record per line; the pipe is the separator.  Field 4 (the
    per-instruction address and byte count) is absent from lane output
    generated before it existed, and its absence is recorded rather
    than filled in."""
    recs = {}
    for raw in open(path):
        raw = raw.rstrip("\n")
        if not raw:
            continue
        parts = raw.split("|")
        if len(parts) < 2:
            continue
        name, state = parts[0], parts[1]
        if not name.startswith("af_"):
            continue
        n = name[3:]
        if state == "OK":
            by = parts[2].split() if len(parts) > 2 else []
            mn = [m for m in (parts[3].split(";") if len(parts) > 3 else [])
                  if m]
            lay = []
            if len(parts) > 4 and parts[4].strip():
                for piece in parts[4].split(";"):
                    if not piece:
                        continue
                    a, _, c = piece.partition(":")
                    lay.append((int(a, 16), int(c)))
            recs[n] = dict(state="OK", bytes=by, mnem=mn, layout=lay)
        else:
            recs[n] = dict(state=state, note="|".join(parts[2:]))
    return recs


def instructions(rec):
    """zip the three raw columns into one instruction list.  Returns
    None when the layout column is absent, because without it nothing
    below can say which bytes belong to which instruction."""
    lay = rec.get("layout") or []
    mn = rec["mnem"]
    by = rec["bytes"]
    if len(lay) != len(mn) or sum(c for _a, c in lay) != len(by):
        return None
    out, k = [], 0
    for (addr, cnt), text in zip(lay, mn):
        out.append(dict(addr=addr, text=text, bytes=by[k:k + cnt]))
        k += cnt
    return out


# ------------------------------------------------------- normalization 1

ENDBR64 = "endbr64"


def strip_entry_endbr64(insns):
    """RULE.  clang can open a function with the CET landing pad
    `endbr64` (f3 0f 1e fa); rustc does not.  It is a four-byte marker
    for the branch-target-identification hardware, it is not part of the
    operation, and by definition it can only be the ENTRY instruction.
    Drop it when, and only when, it stands at position 0.  An `endbr64`
    anywhere else is a real branch target inside the function and is
    left alone."""
    if insns and insns[0]["text"] == ENDBR64:
        return insns[1:], True
    return insns, False


# ------------------------------------------------------- normalization 2

GO_STACK_CHECK = "cmp 0x10(%r14),%rsp"
JUMP = re.compile(r"^(j[a-z]+|loop[a-z]*)\s+([0-9a-f]+)\b")
CALL = re.compile(r"^call(?:q)?\s+([0-9a-f]+)\b")
ANNOT = re.compile(r"<([^<>]*)>\s*$")
SUB_RSP = re.compile(r"^sub\s+\$(0x[0-9a-f]+),%rsp$")


def _annot(text):
    m = ANNOT.search(text)
    return m.group(1) if m else None


def strip_go_stack_growth(insns):
    """RULE.  A non-leaf go function opens with a stack-growth check --
    `cmp 0x10(%r14),%rsp` against the goroutine's stack bound held in
    %r14, followed by a conditional jump to a block at the END of the
    function.  That block spills the arguments, calls
    `runtime.morestack` (or `runtime.morestack_noctxt`), reloads them
    and jumps back to the entry.  The `push %rbp; mov %rsp,%rbp;
    sub $N,%rsp` prologue and the matching `add $N,%rsp; pop %rbp`
    epilogue exist to give that machinery a frame.  None of it is the
    operation; every go function that can grow its stack carries the
    same shape.

    Drop: the two entry instructions, the whole tail block, the
    prologue, and each matching epilogue.

    This is deliberately brittle.  Every element above is CHECKED, not
    assumed -- the conditional jump must land on a real instruction
    address, the tail block must end by jumping back to the entry
    address, it must contain a call whose target symbol is named
    runtime.morestack*, nothing in the body may branch into it, and each
    `pop %rbp` must sit immediately before a `ret` or a `jmp` with its
    `add $N,%rsp` immediately before it.  If any check fails the
    instructions are returned untouched and the unit is flagged
    `canon_unmatched`, so a shape this code does not understand shows up
    as an unanswered question rather than as a quiet mangling.

    Returns (insns, matched, unmatched)."""
    if not insns or insns[0]["text"] != GO_STACK_CHECK:
        return insns, False, False
    bad = (insns, False, True)
    if len(insns) < 4:
        return bad
    j = JUMP.match(insns[1]["text"])
    if not j:
        return bad
    tail_addr = int(j.group(2), 16)
    at = {ins["addr"]: k for k, ins in enumerate(insns)}
    t = at.get(tail_addr)
    if t is None or t < 3 or t >= len(insns):
        return bad

    tail = insns[t:]
    # the tail block must end by jumping back to the entry
    jb = JUMP.match(tail[-1]["text"])
    if not jb or not tail[-1]["text"].startswith("jmp") \
            or int(jb.group(2), 16) != insns[0]["addr"]:
        return bad
    # and it must be the block that calls morestack
    if not any(CALL.match(x["text"])
               and (_annot(x["text"]) or "").startswith("runtime.morestack")
               for x in tail):
        return bad

    body = insns[2:t]
    # nothing in the body may branch into the tail block
    for x in body:
        m = JUMP.match(x["text"])
        if m and int(m.group(2), 16) >= tail_addr:
            return bad

    drop = {0, 1} | set(range(t, len(insns)))

    # prologue
    if insns[2]["text"] != "push %rbp" or insns[3]["text"] != "mov %rsp,%rbp":
        return bad
    drop |= {2, 3}
    size = None
    k = 4
    s = SUB_RSP.match(insns[4]["text"]) if len(insns) > 4 else None
    if s:
        size = s.group(1)
        drop.add(4)
        k = 5

    # epilogue -- one per return path
    pops = 0
    for i in range(k, t):
        if insns[i]["text"] != "pop %rbp":
            continue
        if i + 1 >= t or not (insns[i + 1]["text"] == "ret"
                              or insns[i + 1]["text"].startswith("jmp")):
            return bad
        drop.add(i)
        pops += 1
        if size is not None:
            if i - 1 < k or insns[i - 1]["text"] != "add $%s,%%rsp" % size:
                return bad
            drop.add(i - 1)
    if pops == 0:
        return bad

    return [x for k2, x in enumerate(insns) if k2 not in drop], True, False


# ------------------------------------------------------- normalization 3

RIP = re.compile(r"-?0x[0-9a-f]+\(%rip\)")
RELOC = re.compile(r"\s*!!reloc=(\S+?):(.+?)\s*$")
ADDEND = re.compile(r"[-+]0x[0-9a-f]+$")


def _reloc(text):
    """(text without the relocation note, relocation symbol or None).
    The addend -- `_Znwm-0x4` -- is the four bytes the call displacement
    is measured from, which is an encoding detail of the relocation and
    not part of the name."""
    m = RELOC.search(text)
    if not m:
        return text, None
    return text[:m.start()], ADDEND.sub("", m.group(2))


def normalize_addresses(insns):
    """RULE.  A go unit is disassembled out of a LINKED binary, so
    objdump prints branch and call targets as absolute addresses
    (`je 49df6b`, `call 412aa0`) and `%rip` displacements as whatever
    the linker happened to choose (`lea 0x36b9e(%rip),%rsi`).  A
    cpp/rust/swift unit is disassembled out of an object file and shows
    within-function offsets instead.  Both are facts about where the
    code was PUT, not about what it does, and the same operation linked
    at a different address must canonicalize identically.

      - a branch target becomes a signed offset from the address of the
        branch instruction itself: `je .+0x2b`
      - a `%rip` displacement becomes the token `RIP`, since it names a
        link-time layout slot and nothing about the operation
      - a `call` (or a tail `jmp`) to a NAMED symbol keeps the name --
        `call runtime.concatstring2` IS the operation being performed --
        while a call to a bare address, or to this unit's own body,
        becomes the token `ADDR`
      - objdump's `<symbol+offset>` annotation on a branch within this
        same unit is removed once its information has been used

    Whether a target is INSIDE this unit is decided by the ADDRESS, not
    by the symbol name: a target landing within the span of the unit's
    own instructions is a branch, anything else is a departure.  Name
    matching would be useless here -- a branch inside swift's af_77 is
    annotated `<$s4unit5af_77ySbSi_S2it_Si_S2ittF+0xd>` -- and the span
    settles it without this file having to understand any language's
    mangling scheme.

    Returns (texts, masked) where masked[k] is True when the
    instruction's operand was a link-time fact, so its BYTES are not
    comparable across links and must not be presented as if they
    were."""
    if not insns:
        return [], []
    lo = insns[0]["addr"]
    hi = insns[-1]["addr"] + len(insns[-1]["bytes"])
    texts, masked = [], []
    for ins in insns:
        body, relsym = _reloc(ins["text"])
        base = _annot(body)
        body = ANNOT.sub("", body).strip()
        mask = False
        if RIP.search(body):
            # an INDIRECT call or jump through the GOT --
            # `call *0x0(%rip)` with a GOTPCREL relocation -- is still a
            # named call, and the name is the whole point of recording
            # it: `panic_const_div_by_zero` is what `/` does when the
            # divisor is zero.  Everywhere else the displacement is
            # layout and becomes the placeholder.
            slot = ("%s(%%rip)" % relsym
                    if relsym and re.match(r"^(call|jmp)", body)
                    else "RIP(%rip)")
            body = RIP.sub(slot.replace("\\", "\\\\"), body)
            mask = True
        c = CALL.match(body)
        j = JUMP.match(body)
        if c or j:
            head = "call" if c else j.group(1)
            target = int(c.group(1) if c else j.group(2), 16)
            inside = lo <= target < hi
            # a relocation names the real callee in an object file; the
            # annotation names it in a linked one.  Where the target is
            # inside this unit and no relocation says otherwise, the
            # annotation is only this unit's own name and is discarded.
            named = relsym if relsym else (None if inside else base)
            if c:
                body = "call %s" % (named or "ADDR")
                mask = True
            elif named:
                body = "%s %s" % (head, named)
                mask = True
            else:
                d = target - ins["addr"]
                body = "%s .%s0x%x" % (head, "+" if d >= 0 else "-", abs(d))
        texts.append(" ".join(body.split()))
        masked.append(mask)
    return texts, masked


# ------------------------------------------------------------- the column

def canonicalize(rec):
    """the derived `canon` column.  Returns a dict, or None when the
    raw record cannot support one."""
    insns = instructions(rec)
    if insns is None:
        return None
    insns, had_endbr = strip_entry_endbr64(insns)
    insns, go_stripped, unmatched = strip_go_stack_growth(insns)
    texts, masked = normalize_addresses(insns)
    by = []
    for ins, mk in zip(insns, masked):
        by.extend(["??"] * len(ins["bytes"]) if mk else ins["bytes"])
    return dict(mnem=texts, bytes=by,
                endbr64_stripped=had_endbr,
                go_stack_growth_stripped=go_stripped,
                canon_unmatched=unmatched,
                masked_instructions=sum(1 for m in masked if m))


# ------------------------------------------------------------------ fold

def fold(lang, out_name, outdir, with_sem=False):
    mpath = os.path.join(HERE, "arch_manifest_%s.json" % lang)
    if not os.path.exists(mpath):
        print("!! no manifest %s" % mpath)
        return None
    man = json.load(open(mpath))
    lpath = os.path.join(outdir, "%s.txt" % (out_name or "arch_%s" % lang))
    if not os.path.exists(lpath):
        print("!! no lane output %s" % lpath)
        return None
    recs = read_lane(lpath)

    units, tally = {}, Counter()
    opcodes, whole = Counter(), Counter()
    cop, cwhole = Counter(), Counter()
    semkeys, semterms = Counter(), Counter()
    flags = Counter()
    for n, meta in man["units"].items():
        rec = recs.get(n)
        if rec is None:
            if meta.get("emitted"):
                tally["ABSENT"] += 1
            continue
        u = dict(meta)
        u.update(rec)
        tally[rec["state"]] += 1
        if rec["state"] == "OK":
            for m in rec["mnem"]:
                whole[m] += 1
                opcodes[m.split()[0]] += 1
            can = canonicalize(rec)
            if can is None:
                flags["no_layout_column"] += 1
            else:
                u["canon"] = can
                for m in can["mnem"]:
                    cwhole[m] += 1
                    cop[m.split()[0]] += 1
                for k in ("endbr64_stripped", "go_stack_growth_stripped",
                          "canon_unmatched"):
                    if can[k]:
                        flags[k] += 1
            if with_sem:
                try:
                    sem = SEM.semantics(rec)
                except Exception as exc:                     # noqa: BLE001
                    sem = None
                    u["sem_error"] = "%s: %s" % (type(exc).__name__, exc)
                    flags["sem_error"] += 1
                if sem is not None:
                    u["sem"] = sem
                    semkeys[sem["key"]] += 1
                    for t in sem["values"] + sem["stores"] + sem["events"]:
                        semterms[t] += 1
        units[n] = u

    doc = dict(language=lang,
               lane_output=lpath,
               manifest=mpath,
               unit_count=len(units),
               ok=tally["OK"], buildfail=tally["BUILDFAIL"],
               nosym=tally["NOSYM"], absent=tally["ABSENT"],
               skipped=man.get("skipped", 0),
               distinct_mnemonics=len(opcodes),
               distinct_instruction_texts=len(whole),
               distinct_canonical_mnemonics=len(cop),
               distinct_canonical_instruction_texts=len(cwhole),
               canon_flags=dict(flags),
               mnemonic_census=dict(sorted(opcodes.items(),
                                           key=lambda kv: (-kv[1], kv[0]))),
               canonical_mnemonic_census=dict(
                   sorted(cop.items(), key=lambda kv: (-kv[1], kv[0]))),
               canonical_text_census=dict(
                   sorted(cwhole.items(), key=lambda kv: (-kv[1], kv[0]))),
               units=units)
    if with_sem:
        doc["sem_lifter"] = SEM.LIFTER_ID
        doc["distinct_sem_keys"] = len(semkeys)
        doc["distinct_sem_terms"] = len(semterms)
        doc["sem_term_census"] = dict(
            sorted(semterms.items(), key=lambda kv: (-kv[1], kv[0])))
    dst = os.path.join(HERE, "arch_units_%s.json" % lang)
    json.dump(doc, open(dst, "w"), indent=1)

    print("== %s  (%s)" % (lang, lpath))
    print("   units in lane output : %d" % len(units))
    print("   OK                   : %d" % tally["OK"])
    print("   BUILDFAIL            : %d" % tally["BUILDFAIL"])
    print("   NOSYM                : %d" % tally["NOSYM"])
    print("   still skipped        : %d" % man.get("skipped", 0))
    if tally["ABSENT"]:
        print("   emitted but no line  : %d" % tally["ABSENT"])
    print("   raw   distinct opcodes %5d   distinct instruction texts %5d"
          % (len(opcodes), len(whole)))
    print("   CANON distinct opcodes %5d   distinct instruction texts %5d"
          % (len(cop), len(cwhole)))
    print("   canon flags: %s" % (dict(flags) or "none"))
    if with_sem:
        print("   SEM   distinct terms   %5d   distinct whole-unit forms %5d"
              % (len(semterms), len(semkeys)))
    top = sorted(cop.items(), key=lambda kv: (-kv[1], kv[0]))[:20]
    print("   most frequent canonical opcode: %s"
          % ", ".join("%s x%d" % (k, v) for k, v in top))
    print("   wrote %s" % dst)
    return doc


# --------------------------------------------- cross-language scalar table
#
# The scalar core is the only place where a cross-language comparison
# means anything at the byte level: `whole`, `fractional` and `truth`
# holders exist in all four languages with the same machine width, so
# the same operator on the same width is the SAME question asked four
# times.  The table below is keyed on that width, never on the holder
# index, which is per-language.

SCALAR_KEY = {
    "bool": "b", "Bool": "b",
    "int32_t": "i32", "i32": "i32", "int32": "i32", "Int32": "i32",
    "int64_t": "i64", "i64": "i64", "int64": "i64", "Int64": "i64",
    "int": "i64", "Int": "i64",
    "uint64_t": "u64", "u64": "u64", "uint64": "u64", "UInt64": "u64",
    "__int128": "i128", "i128": "i128",
    "double": "f64", "f64": "f64", "float64": "f64", "Double": "f64",
    "float": "f32", "f32": "f32", "float32": "f32", "Float": "f32",
}


def cross_scalar(basis="canon"):
    """`basis` names the column the comparison is made on.

      canon   the byte and mnemonic form after the three layout
              normalizations.  Two languages agree here only if their
              compilers picked the same instructions AND the same
              registers.
      sem     the lifted form.  Two languages agree here if their
              compilers computed the same thing, whichever instructions
              and whichever registers they used to do it.

    Neither replaces the other, and both are written to their own file,
    because the difference between the two answers is itself the
    finding."""
    docs = {}
    for lang in LANGS:
        p = os.path.join(HERE, "arch_units_%s.json" % lang)
        if os.path.exists(p):
            docs[lang] = json.load(open(p))
    if not docs:
        print("!! no arch_units_*.json to compare")
        return None

    # (op, lhs width, rhs width) -> lang -> canonical signature
    cells = defaultdict(dict)
    column = "canon" if basis == "canon" else "sem"
    for lang, d in docs.items():
        for n, u in d["units"].items():
            if u.get("state") != "OK" or column not in u:
                continue
            if u.get("lhs_form") not in SCALAR_FORMS:
                continue
            if u.get("rhs_form") not in SCALAR_FORMS:
                continue
            lk = SCALAR_KEY.get(u.get("lhs_type"))
            rk = SCALAR_KEY.get(u.get("rhs_type"))
            if not lk or not rk:
                continue
            if basis == "canon":
                sig = (" ".join(u["canon"]["bytes"]),
                       ";".join(u["canon"]["mnem"]))
            else:
                sig = u["sem"]["key"]
            cells[(u["op"], lk, rk)][lang] = sig

    ops = sorted(set(k[0] for k in cells))
    per_op = {}
    for op in ops:
        mine = {k: v for k, v in cells.items() if k[0] == op}
        pair_tot, pair_hit = Counter(), Counter()
        cellrows = []
        for key in sorted(mine):
            byl = mine[key]
            groups = defaultdict(list)
            for lang, sig in byl.items():
                groups[sig].append(lang)
            cellrows.append(dict(cell="%s %s" % (key[1], key[2]),
                                 groups=[sorted(v) for v in groups.values()]))
            langs = sorted(byl)
            for a in range(len(langs)):
                for b in range(a + 1, len(langs)):
                    p = (langs[a], langs[b])
                    pair_tot[p] += 1
                    if byl[langs[a]] == byl[langs[b]]:
                        pair_hit[p] += 1
        # a pair of languages AGREES on an operator when it produced the
        # same canonical form in every cell both of them answered.  A
        # pair that shares no cell at all is absence of evidence, not
        # agreement, and never reaches this list.
        per_op[op] = dict(
            cells=cellrows,
            comparable=dict(("+".join(k), v) for k, v in pair_tot.items()),
            identical=dict(("+".join(k), v) for k, v in pair_hit.items()),
            full_agreement=["+".join(p) for p in sorted(pair_tot)
                            if pair_tot[p] > 0
                            and pair_hit[p] == pair_tot[p]],
            partial=dict(("+".join(p), "%d/%d" % (pair_hit[p], pair_tot[p]))
                         for p in sorted(pair_tot)
                         if 0 < pair_hit[p] < pair_tot[p]))

    dst = os.path.join(HERE, "arch_cross_scalar%s.json"
                       % ("" if basis == "canon" else "_" + basis))
    json.dump(dict(languages=sorted(docs), basis=basis, operators=per_op),
              open(dst, "w"), indent=1)

    print("\n== cross-language scalar core, basis %s "
          "(forms whole/fractional/truth)" % basis)
    head = ("byte-identical after canon" if basis == "canon"
            else "identical after semantic lifting")
    print("   %-6s %-46s %-24s %s"
          % ("op", head, "go pairs", "comparable cells"))
    for op in ops:
        r = per_op[op]
        ok = ", ".join(r["full_agreement"]) or "(none)"
        tot = sum(r["comparable"].values())
        gp = ", ".join("%s %d/%d" % (p, r["identical"].get(p, 0),
                                     r["comparable"][p])
                       for p in sorted(r["comparable"]) if "go" in p)
        print("   %-6s %-46s %-24s %d" % (op, ok, gp or "-", tot))
    print("   wrote %s" % dst)
    return per_op


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("langs", nargs="*")
    ap.add_argument("--out-name", default=None,
                    help="lane output basename, without .txt "
                         "(default arch_<lang>)")
    ap.add_argument("--outdir", default=AIRLOCK_OUT)
    ap.add_argument("--cross", action="store_true",
                    help="also print the cross-language scalar table")
    ap.add_argument("--sem", action="store_true",
                    help="compute the lifted `sem` column during the fold, "
                         "and run --cross on it as well as on canon")
    args = ap.parse_args()
    if args.sem and SEM is None:
        print("!! --sem asked for but arch_sem is not importable -- %s"
              % SEM_WHY)
        return 2
    docs = [fold(l, args.out_name, args.outdir, args.sem)
            for l in args.langs]
    good = [d for d in docs if d]
    if len(good) > 1:
        allop, alltxt = Counter(), Counter()
        for d in good:
            allop.update(d["canonical_mnemonic_census"])
            alltxt.update(d["canonical_text_census"])
        print("\n== across %d languages" % len(good))
        print("   DISTINCT CANONICAL MNEMONICS (opcode word)      : %d"
              % len(allop))
        print("   distinct canonical instruction texts            : %d"
              % len(alltxt))
        if args.sem:
            allsem, allkeys = Counter(), Counter()
            for d in good:
                allsem.update(d["sem_term_census"])
                for u in d["units"].values():
                    if "sem" in u:
                        allkeys[u["sem"]["key"]] += 1
            print("   DISTINCT SEM TERMS                              : %d"
                  % len(allsem))
            print("   distinct whole-unit sem forms                   : %d"
                  % len(allkeys))
        top = sorted(alltxt.items(), key=lambda kv: (-kv[1], kv[0]))[:20]
        for k, v in top:
            print("      %-40s x%d" % (k, v))
    if args.cross:
        cross_scalar("canon")
        if args.sem:
            cross_scalar("sem")
    return 0 if (good or args.cross) else 1


if __name__ == "__main__":
    sys.exit(main())
