#!/usr/bin/env python3
"""sem_anchored.py -- step 4+5 of the ratified pipeline: the lifted
`sem` form with ANCHORED operand identity.

What this file changes, and nothing else
----------------------------------------
`kind_fuzz_clustering/arch_sem.py` already lifts machine bytes into a
normalized semantic form.  Every normalization rule in that file is
reused here verbatim, by import.  This file rewrites exactly ONE step
of it: the naming of the input registers.

arch_sem names a register by WHEN IT IS FIRST MET in a traversal of the
lifted form.  That is name-blind, which was the point there, and it is
also a defect: `in0` means "the register the traversal reached first",
not "the first argument".  Two units that compare their two arguments
in opposite orders then mirror the condition -- `a < b` and `a > b` --
both traverse to a first and a second register, and both get called
in0 and in1, so they collapse onto one key.  That false merge was
observed in the arch campaign and is what step 4 exists to close.

Here `in0` means the FIRST SOURCE OPERAND of the probe's own source
expression, and `in1` the SECOND, because the name is taken from the
language's ARGUMENT REGISTERS, not from the shape of the code.  A
register that is not an argument register cannot become `in0` by
accident: it is named `uN` instead, in a separate namespace.

The three grounds the anchor rests on
-------------------------------------
1. the ABI's own rule, applied to the probe's own parameter types
   (SysV for c/cpp/rust/swift, go's register ABI for go);
2. the ANCHOR build's DWARF parameter table, read per probe, checked
   against the anchor build's own spill of each argument register into
   the home DWARF names -- this is the tool's own testimony, per
   artifact, and it is CHECKED here rather than assumed;
3. the forced probe: a non-commutative operator (`-`) can only be
   written one way round, so `a - b` pins which register carried `a`
   without any reference to the debug table at all.

Each is reported separately by `--anchor-report`, so a language whose
anchor rests on fewer than three grounds says so.

usage:
  sem_anchored.py                     annotate every language, write
                                      sem_anchored_<lang>.json
  sem_anchored.py --anchor-report     the three grounds, per language
  sem_anchored.py --selfcheck         the `<` vs `>` anti-false-merge
                                      test, and arch_sem's own guards
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KFC = os.path.join(os.path.dirname(HERE), "kind_fuzz_clustering")
sys.path.insert(0, KFC)

import arch_read as AR                                       # noqa: E402
import arch_sem as AS                                        # noqa: E402

import capstone                                              # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift", "java", "cpython", "javascript", "csharp", "dart"]

MD = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
MD.detail = False


# ============================================================ the ABI map
#
# Only the scalar case is needed: every probe in this campaign takes one
# or two scalar parameters and returns a scalar.  An aggregate would
# need the full classification algorithm and there is not one here, so a
# probe whose parameter is not a scalar is refused an anchor rather than
# given a guessed one.

FLOAT_REPS = {"f32", "f64"}

SYSV_INT = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]
SYSV_SSE = ["ymm0", "ymm1", "ymm2", "ymm3", "ymm4", "ymm5", "ymm6", "ymm7"]

# go's register ABI (internal ABI0->ABIInternal, amd64): integer
# arguments in RAX, RBX, RCX, RDI, RSI, R8-R11; floating point in
# X0-X14, which archinfo addresses as the ymm base of each.
GO_INT = ["rax", "rbx", "rcx", "rdi", "rsi", "r8", "r9", "r10", "r11"]
GO_SSE = ["ymm%d" % k for k in range(15)]

# java JIT ABI (HotSpot C2 on amd64 linux):
JAVA_INT = ["rsi", "rdx", "rcx", "r8", "r9"]

ABI = {
    "c": ("sysv", SYSV_INT, SYSV_SSE),
    "cpp": ("sysv", SYSV_INT, SYSV_SSE),
    "rust": ("sysv", SYSV_INT, SYSV_SSE),
    "swift": ("sysv", SYSV_INT, SYSV_SSE),
    "go": ("goabi", GO_INT, GO_SSE),
    "java": ("javaabi", JAVA_INT, SYSV_SSE),
    "cpython": ("sysv", SYSV_INT, SYSV_SSE),
    "javascript": ("sysv", SYSV_INT, SYSV_SSE),
    "csharp": ("sysv", SYSV_INT, SYSV_SSE),
    "dart": ("sysv", SYSV_INT, SYSV_SSE),
}


def parameter_reps(meta):
    """the probe's parameters, in source order.  `a` first, then `b`."""
    reps = [meta.get("lhs_rep")]
    if meta.get("arity") == "binary":
        reps.append(meta.get("rhs_rep"))
    return reps


def argument_registers(lang, reps):
    """the physical register each parameter arrives in, by the ABI's own
    rule applied to the parameter's own type.  Returns None when a
    parameter's type is not one this file classifies."""
    if lang not in ABI:
        return None
    _family, ints, sses = ABI[lang]
    ni = 0
    ns = 0
    out = []
    for rep in reps:
        if rep is None:
            return None
        if rep in FLOAT_REPS:
            if ns >= len(sses):
                return None
            out.append(sses[ns])
            ns += 1
        else:
            if ni >= len(ints):
                return None
            out.append(ints[ni])
            ni += 1
    return out


def anchor_names(lang, meta):
    """the naming map handed to the serializer.  `in0` is the first
    source operand, `in1` the second, and nothing else can take those
    tokens."""
    regs = argument_registers(lang, parameter_reps(meta))
    if regs is None:
        return None
    names = dict(AS.FIXED_LEAF)
    for k, reg in enumerate(regs):
        names[reg] = "in%d" % k
    return names


# ================================================== the layout column
#
# arch_units carried a `layout` column -- the address and byte count of
# each instruction -- and arch_read refuses to build an instruction list
# without it.  op_units does not carry one: it has the byte string and
# the mnemonic list side by side and nothing joining them.  The join is
# recovered by DISASSEMBLING the bytes again and requiring the recovered
# instruction count to equal the mnemonic count.  A unit where the two
# disagree is not repaired and not guessed at; it is returned with a
# reason and lands in the UNDECIDED bin.

ANNOT_OFF = re.compile(r"^(?:call|j[a-z]+)\s+([0-9a-f]+)\s+<[^<>]*\+0x([0-9a-f]+)>")
ANNOT_ZERO = re.compile(r"^(?:call|j[a-z]+)\s+([0-9a-f]+)\s+<[^<>+]*>")


def base_address(mnem):
    """the address the unit's first byte was disassembled at.

    A go unit comes out of a LINKED binary, so its branch targets are
    absolute (`je 47a658 <main.op_96+0x18>`).  objdump's own annotation
    states the offset of that target inside the function, so the base is
    the difference.  A cpp/rust/swift/c unit comes out of an object file
    and its targets are already offsets, which the same subtraction
    returns 0 for.  A unit with no branch at all has no base to recover
    and none is needed."""
    for text in mnem:
        m = ANNOT_OFF.match(text)
        if m:
            return int(m.group(1), 16) - int(m.group(2), 16)
        m = ANNOT_ZERO.match(text)
        if m:
            return int(m.group(1), 16)
    return 0


def layout(unit):
    """(layout column, reason).  The reason is None on success."""
    raw = unit.get("bytes") or []
    mnem = unit.get("mnem") or []
    try:
        blob = bytes(int(x, 16) for x in raw)
    except ValueError as exc:
        return None, "byte column is not hex: %s" % exc
    base = base_address(mnem)
    lay = []
    off = 0
    while off < len(blob):
        got = None
        for ins in MD.disasm(blob[off:off + 16], base + off, count=1):
            got = ins.size
        if got is None:
            # capstone declines undecodable bytes.  `ud2` is two bytes
            # and objdump printed it, so the pair is taken as one
            # instruction; anything else stops the recovery.
            if blob[off:off + 2] == b"\x0f\x0b":
                got = 2
            else:
                return None, ("capstone could not decode at offset %d "
                              "(bytes %s)" % (off, blob[off:off + 4].hex()))
        lay.append((base + off, got))
        off += got
    if len(lay) != len(mnem):
        return None, ("recovered %d instructions but the mnemonic column "
                      "has %d" % (len(lay), len(mnem)))
    return lay, None


# ================================ commutative order, under anchored names
#
# arch_sem orders the operands of a commutative operation by its own
# NAME-BLIND key, which cannot tell one register from another and so
# leaves them in whatever order the compiler emitted.  Under anchored
# names the two operands are distinguishable, so the order has to be
# canonicalized again or `add %esi,%edi` and `add %edi,%esi` -- the same
# addition, emitted two ways -- would be given two keys.  This is the
# only rule this file adds, and it adds nothing that arch_sem's own
# COMMUTATIVE table does not already declare commutative.

def canon_commute(e, names):
    kids = AS._kids(e)
    if kids:
        rebuilt = []
        for k in kids:
            rebuilt.append(canon_commute(k, names))
        e = _rebuild(e, rebuilt)
    if e[0] == "b" and AS.COMMUTATIVE.match(e[2]):
        a = AS._ser(e[3], names)
        b = AS._ser(e[4], names)
        if b < a:
            e = ("b", e[1], e[2], e[4], e[3])
    return e


def _rebuild(e, kids):
    k = e[0]
    if k == "ex":
        return ("ex", e[1], e[2], kids[0])
    if k in ("zx", "sx"):
        return (k, e[1], kids[0])
    if k == "ins":
        return ("ins", e[1], kids[0], kids[1], e[4])
    if k == "b":
        return ("b", e[1], e[2], kids[0], kids[1])
    if k == "u":
        return ("u", e[1], e[2], kids[0])
    if k in ("t", "q"):
        return (k, e[1], e[2]) + tuple(kids)
    if k == "ite":
        return ("ite", e[1], kids[0], kids[1], kids[2])
    if k == "ld":
        return ("ld", e[1], e[2], kids[0])
    if k == "cc":
        return ("cc", e[1], e[2], tuple(kids))
    return e


# ======================================================= the anchored sem

def raw_summaries(unit, lang, meta):
    """(summaries, names, reason).  The summaries are arch_sem's own --
    lifted, swept and normalized by arch_sem's rules, untouched here."""
    names = anchor_names(lang, meta)
    if names is None:
        return None, None, "no ABI classification for the parameter types"
    lay, reason = layout(unit)
    if lay is None:
        return None, names, reason
    rec = dict(state="OK", bytes=unit["bytes"], mnem=unit["mnem"],
               layout=lay)
    insns = AR.instructions(rec)
    if insns is None:
        return None, names, "arch_read refused the recovered layout"
    insns, _endbr = AR.strip_entry_endbr64(insns)
    insns, _go, unmatched = AR.strip_go_stack_growth(insns)
    texts, _masked = AR.normalize_addresses(insns)
    index = dict((ins["addr"], k) for k, ins in enumerate(insns))
    spans, block_index = AS.blocks_of(insns, texts, index)
    summaries = []
    for lo, hi in spans:
        st = AS._sweep(insns, texts, index, block_index, lo, hi)
        summaries.append(AS.summarize(st))
    return summaries, names, None


def render_anchored(summaries, anchor):
    """arch_sem's `render`, with the naming step replaced.

    Everything else is the same: the values of each block sorted, the
    stores sorted, the events kept in address order.  The one change is
    that the name map starts already carrying the argument registers,
    and every register that is NOT an argument register is named `uN`
    -- a separate namespace, so nothing that is not an operand can be
    read as one."""
    ordered = []
    for vals, stores, events in summaries:
        vals = sorted(vals, key=AS._key)
        stores = sorted(stores, key=lambda s: (AS._key(s[0]), s[1],
                                               AS._key(s[2])))
        ordered.append((vals, stores, events))

    names = dict(anchor)
    order = []
    for vals, stores, events in ordered:
        for v in vals:
            AS._leaves(v, order)
        for a, _w, v in stores:
            AS._leaves(a, order)
            AS._leaves(v, order)
        for ev in events:
            if ev[0] == "branch" and ev[3] is not None:
                AS._leaves(ev[3], order)
    n = 0
    for r in order:
        if r in names:
            continue
        names[r] = "u%d" % n
        n += 1

    out = []
    for b, (vals, stores, events) in enumerate(ordered):
        vals = [canon_commute(x, names) for x in vals]
        vals = sorted(vals, key=lambda x: AS._ser(x, names))
        v = [AS._ser(x, names) for x in vals]
        s = []
        for a, w, x in stores:
            s.append("st%d(%s)=%s" % (w, AS._ser(a, names),
                                      AS._ser(x, names)))
        e = []
        for ev in events:
            if ev[0] == "branch":
                cond = AS._ser(ev[3], names) if ev[3] else "?"
                e.append("branch %s %s [%s]" % (ev[1], ev[2], cond))
            else:
                e.append(" ".join(str(x) for x in ev))
        out.append(dict(block=b, values=v, stores=s, events=e,
                        text="B%d V[%s] S[%s] E[%s]"
                             % (b, " ".join(v), " ".join(s), " | ".join(e))))
    return out, names


def semantics_anchored(unit, lang, meta):
    """the anchored `sem` column for one ship (or anchor) unit."""
    summaries, names, reason = raw_summaries(unit, lang, meta)
    if summaries is None:
        return dict(ok=False, reason=reason)
    parts, names = render_anchored(summaries, names)
    key = "  ".join(p["text"] for p in parts)
    values = [x for p in parts for x in p["values"]]
    stores = [x for p in parts for x in p["stores"]]
    events = [x for p in parts for x in p["events"]]
    return dict(ok=True, blocks=parts, values=values, stores=stores,
                events=events, key=key,
                anchor_registers=dict((v, k) for k, v in names.items()
                                      if v.startswith("in")),
                block_count=len(parts))


# ============================================ ground 2: the DWARF check
#
# The anchor build gives every parameter a memory home and states the
# home in the debug table.  The check below is a JOIN of two independent
# statements about the same artifact: the debug table says `a` lives at
# frame offset X, and the anchor's own instruction stream says register
# R was written to frame offset X on entry.  Together they say `a`
# arrived in R.  Neither is assumed; where the shape is not recognized
# the probe is reported UNVERIFIED and is never given a guessed answer.

FBREG = re.compile(r"DW_OP_fbreg:\s*(-?\d+)")
SPILL = re.compile(r"^(?:mov|movl|movq|movss|movsd|movb|movw)\s+"
                   r"%([a-z0-9]+),(-?0x[0-9a-f]+)\(%(rbp|rsp)\)$")

# the anchor's stores name a sub-register; this maps it back to the
# 64-bit register the ABI talks about.
SUBREG = {}
for _full, _parts in [
        ("rax", ["eax", "ax", "al"]), ("rbx", ["ebx", "bx", "bl"]),
        ("rcx", ["ecx", "cx", "cl"]), ("rdx", ["edx", "dx", "dl"]),
        ("rsi", ["esi", "si", "sil"]), ("rdi", ["edi", "di", "dil"]),
        ("r8", ["r8d", "r8w", "r8b"]), ("r9", ["r9d", "r9w", "r9b"]),
        ("r10", ["r10d", "r10w", "r10b"]),
        ("r11", ["r11d", "r11w", "r11b"])]:
    SUBREG[_full] = _full
    for _p in _parts:
        SUBREG[_p] = _full
for _k in range(16):
    SUBREG["xmm%d" % _k] = "ymm%d" % _k
    SUBREG["ymm%d" % _k] = "ymm%d" % _k


def dwarf_check(probe, lang):
    """(verdict, detail).  verdict is one of CONFIRMED, CONTRADICTED,
    UNVERIFIED."""
    meta = probe["meta"]
    anchor = probe.get("anchor") or {}
    dwarf = anchor.get("dwarf")
    if not dwarf:
        return "UNVERIFIED", "the anchor build carries no DWARF table"
    predicted = argument_registers(lang, parameter_reps(meta))
    if predicted is None:
        return "UNVERIFIED", "no ABI classification for the parameter types"

    homes = {}
    for row in dwarf:
        m = FBREG.search(row.get("location") or "")
        if m:
            homes[row.get("name")] = int(m.group(1))
    wanted = ["a", "b"][:len(predicted)]
    if any(w not in homes for w in wanted):
        return "UNVERIFIED", ("the DWARF table does not give a frame home "
                              "for every parameter: %s" % sorted(homes))

    spills = {}
    for text in anchor.get("mnem") or []:
        m = SPILL.match(text.strip())
        if not m:
            continue
        reg = SUBREG.get(m.group(1))
        disp = int(m.group(2), 16)
        if disp >= 0x80000000:
            disp -= 0x100000000
        if disp not in spills:
            spills[disp] = reg
    if not spills:
        return "UNVERIFIED", ("the anchor build stores no register into a "
                             "frame slot -- nothing to join the table to")

    detail = []
    verdict = "CONFIRMED"
    for k, name in enumerate(wanted):
        off = homes[name]
        got = spills.get(off)
        if got is None:
            return "UNVERIFIED", ("no store into the frame slot DWARF gives "
                                  "for `%s` (fbreg %d)" % (name, off))
        detail.append("%s@fbreg%d<-%%%s (ABI says %%%s)"
                      % (name, off, got, predicted[k]))
        if got == predicted[k]:
            continue
        if got in predicted:
            # the slot DWARF names for `a` was filled from the register
            # the ABI assigns to `b`, or the other way round.  That is a
            # real contradiction and it must be reported as one.
            verdict = "CONTRADICTED"
            continue
        # the value reached its home through some register the ABI
        # assigns to no parameter at all -- a `bool` parameter is
        # narrowed through %al before it is stored, for instance.  This
        # join does not follow moves, so it cannot speak; it says so
        # rather than calling a move a contradiction.
        if verdict != "CONTRADICTED":
            verdict = "UNVERIFIED"
    return verdict, "; ".join(detail)


# =============================== ground 3: the forced non-commutative probe
#
# `-` cannot be written the other way round and mean the same thing, so
# the ship unit for `a - b` states which register carried `a` without
# any reference to a debug table.  The test asks the ANCHORED sem form
# whether the minuend is `in0`.  If the anchor were the wrong way round
# the form would read Sub(in1,in0) and the test would fail loudly.

SUBOP = re.compile(r"Sub\d+\(")


def minuend_first(key):
    """True when the first anchored operand named inside the first
    subtraction of the key is `in0`.  The subtraction's minuend is its
    left operand and the serializer writes the left operand first, so
    whichever of `in0`/`in1` appears first is the minuend."""
    m = SUBOP.search(key)
    if not m:
        return None
    tail = key[m.end():]
    i0 = tail.find("in0")
    i1 = tail.find("in1")
    if i0 < 0 or i1 < 0:
        return None
    return i0 < i1


def forced_probe(doc, lang, rep="i32"):
    """(verdict, probe number, sem key)."""
    for n, probe in sorted(doc["probes"].items(), key=lambda kv: int(kv[0])):
        meta = probe["meta"]
        if meta.get("operator") != "-" or meta.get("arity") != "binary":
            continue
        if meta.get("lhs_rep") != rep or meta.get("rhs_rep") != rep:
            continue
        if not probe.get("ship"):
            continue
        sem = semantics_anchored(probe["ship"], lang, meta)
        if not sem["ok"]:
            return "UNVERIFIED", n, sem["reason"]
        first = minuend_first(sem["key"])
        if first is True:
            return "CONFIRMED", n, sem["key"]
        if first is False:
            return "CONTRADICTED", n, sem["key"]
        return "UNVERIFIED", n, sem["key"]
    return "UNVERIFIED", None, "no `a - b` probe on %s/%s" % (rep, rep)


# ================================================================== drive

def load(lang):
    path = os.path.join(HERE, "op_units_%s.json" % lang)
    return json.load(open(path))


def annotate(lang, verbose=True):
    doc = load(lang)
    out = {}
    ok = 0
    failed = {}
    for n, probe in doc["probes"].items():
        ship = probe.get("ship")
        if not ship:
            continue
        meta = probe["meta"]
        try:
            sem = semantics_anchored(ship, lang, meta)
        except Exception as exc:                            # noqa: BLE001
            sem = dict(ok=False,
                       reason="%s: %s" % (type(exc).__name__, exc))
        if sem["ok"]:
            ok += 1
        else:
            failed[sem["reason"]] = failed.get(sem["reason"], 0) + 1
        out[n] = dict(meta=meta, sem=sem,
                      bytes=" ".join(ship["bytes"]),
                      mnem=ship["mnem"])
    doc_out = dict(language=lang, lifter=AS.LIFTER_ID,
                   capstone=capstone.__version__,
                   units=out, ok=ok, failed=len(out) - ok,
                   failure_reasons=failed)
    path = os.path.join(HERE, "sem_anchored_%s.json" % lang)
    json.dump(doc_out, open(path, "w"), indent=1)
    if verbose:
        print("== %-6s %d ship units, %d anchored sem, %d refused"
              % (lang, len(out), ok, len(out) - ok))
        for reason, count in sorted(failed.items(), key=lambda kv: -kv[1]):
            print("     %4d  %s" % (count, reason[:110]))
    return doc_out


def anchor_report():
    print("== step 4: the ground each language's operand anchor rests on")
    for lang in LANGS:
        doc = load(lang)
        family = ABI[lang][0]
        counts = {}
        examples = {}
        for n, probe in doc["probes"].items():
            if not probe.get("ship"):
                continue
            verdict, detail = dwarf_check(probe, lang)
            counts[verdict] = counts.get(verdict, 0) + 1
            if verdict not in examples:
                examples[verdict] = (n, detail)
        fverdict, fn, fkey = forced_probe(doc, lang)
        print()
        print("-- %s" % lang)
        print("   ground 1  ABI rule           %s: a->%%%s, b->%%%s "
              "(int path)" % (family, ABI[lang][1][0], ABI[lang][1][1]))
        print("   ground 2  DWARF at anchor    %s"
              % ", ".join("%s %d" % (k, v)
                          for k, v in sorted(counts.items())))
        if "CONFIRMED" in examples:
            print("             example probe %s   %s"
                  % (examples["CONFIRMED"][0], examples["CONFIRMED"][1]))
        if "CONTRADICTED" in examples:
            print("             CONTRADICTED probe %s   %s"
                  % (examples["CONTRADICTED"][0],
                     examples["CONTRADICTED"][1]))
        if "UNVERIFIED" in examples:
            print("             unverified example probe %s   %s"
                  % (examples["UNVERIFIED"][0], examples["UNVERIFIED"][1]))
        print("   ground 3  forced `a - b`     %s (probe %s)"
              % (fverdict, fn))
        print("             %s" % fkey)


# ------------------------------------------------- the anti-false-merge

def _find(doc, lang, operator, lhs, rhs):
    for n, probe in sorted(doc["probes"].items(), key=lambda kv: int(kv[0])):
        meta = probe["meta"]
        if meta.get("operator") != operator:
            continue
        if meta.get("lhs_rep") != lhs or meta.get("rhs_rep") != rhs:
            continue
        if not probe.get("ship"):
            continue
        return n, probe
    return None, None


def selfcheck():
    print("== sem_anchored selfcheck")
    print("   lifter %s" % AS.LIFTER_ID)
    print()
    print("-- the `<` vs `>` anti-false-merge test")
    print("   arch_sem names a register by traversal order, so `a < b`")
    print("   and `a > b` -- the same two registers compared in opposite")
    print("   orders with a mirrored condition -- were given one key.")
    print("   Anchored, they must be given two.")
    bad = 0
    for lang in LANGS:
        doc = load(lang)
        for rep in ("i32", "f64"):
            nl, pl = _find(doc, lang, "<", rep, rep)
            ng, pg = _find(doc, lang, ">", rep, rep)
            if not pl or not pg:
                continue
            al = semantics_anchored(pl["ship"], lang, pl["meta"])
            ag = semantics_anchored(pg["ship"], lang, pg["meta"])
            bl = AS.semantics(dict(state="OK", bytes=pl["ship"]["bytes"],
                                   mnem=pl["ship"]["mnem"],
                                   layout=layout(pl["ship"])[0]))
            bg = AS.semantics(dict(state="OK", bytes=pg["ship"]["bytes"],
                                   mnem=pg["ship"]["mnem"],
                                   layout=layout(pg["ship"])[0]))
            if not (al["ok"] and ag["ok"]):
                print("   [skip] %-6s %-4s a lift was refused" % (lang, rep))
                continue
            same_blind = bl["key"] == bg["key"]
            same_anch = al["key"] == ag["key"]
            ok = "ok " if not same_anch else "FAIL"
            if same_anch:
                bad += 1
            print()
            print("   [%s] %-6s %-4s  name-blind keys equal: %s   "
                  "anchored keys equal: %s"
                  % (ok, lang, rep, same_blind, same_anch))
            print("        probe %-4s a < b   %s" % (nl, al["key"]))
            print("        probe %-4s a > b   %s" % (ng, ag["key"]))
    print()
    print("   %d false merges remaining" % bad)
    return bad


def main():
    if "--anchor-report" in sys.argv:
        anchor_report()
        return 0
    if "--selfcheck" in sys.argv:
        return 1 if selfcheck() else 0
    for lang in LANGS:
        annotate(lang)
    return 0


if __name__ == "__main__":
    sys.exit(main())
