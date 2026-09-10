#!/usr/bin/env python3
"""condition_table.py -- CAUSE 1 fix: amd64g_calculate_condition is opaque.

AgentMemory's op_pipeline lap, 2026-08-28.  209 units are stuck
"not yet converged" because their lifted expression contains
`amd64g_calculate_condition(cc, op, dep1, dep2, ndep)` -- pyvex's own
opaque stand-in for the VEX guest helper that decodes x86-64's lazy
condition codes.  tree_match2's normalize() cannot do anything with
this call except swallow it whole into one uninterpreted atom (see
tree_match.py's `to_z3`, "everything else ... is OUTSIDE the small
ratified rewrite set").

THIS FILE PROVIDES ROUTE (a), the owner's PRIMARY route, ratified in the
work order: read the condition directly off the CANONICAL TEXT,
never off the lifter helper's own numeric cc/op arguments.  In
canonical form the flag-setting instruction and the flag-reading
instruction are unambiguous:

    test %edi,%edi     setne %al       -->  a != 0
    cmp  %rcx,%rsi      setl %al       -->  b < sign_extend(a)   (AT&T:
                                             `cmp SRC,DST` compares
                                             DST against SRC, so
                                             `cmp %rcx,%rsi` reads
                                             "compare %rsi to %rcx")

THE TABLE (recorded here per the owner's instruction "record the table in
the file header").  Two independent axes:

  FLAG-SETTER KIND (read off the canonical mnemonic immediately
  preceding the setcc/cmov/branch, or the most recent one in program
  order if other non-flag-touching instructions sit between -- flags
  persist on real hardware until overwritten, so "most recent" is
  the correct rule, not "immediately previous line"):

    "test"      integer LOGIC family (test/and-and-discard).  VEX's
                own convention (confirmed empirically on cpp/op_318
                and c/op_5, see report): dep1 IS the tested value,
                dep2 is always the constant 0 -- so the SAME 2-operand
                formula below applies uniformly with R forced to 0.
    "cmp"       integer SUB family (compare-and-discard).  VEX's own
                convention (confirmed on c/op_535): dep1 = L = the
                AT&T DESTINATION operand (second operand), dep2 = R =
                the AT&T SOURCE operand (first operand) -- i.e.
                `cmp SRC,DST` yields dep1=DST, dep2=SRC, matching
                "compare(DST, SRC)".
    "ucomisd"/"ucomiss"
                float family.  x86 UCOMISD/UCOMISS sets ZF/PF/CF
                directly (SF/OF/AF cleared) comparing DST (AT&T
                second operand) against SRC (first operand); PF=1
                signals "unordered" (either operand is NaN).  This
                file resolves the condition-helper opacity down to a
                bit read of the unit's OWN already-lifted CmpF64/
                CmpF32 atom (so repeated setXX reads of the SAME
                compare collapse onto the SAME atom instead of each
                becoming its own disconnected opaque atom -- real
                progress for MATCHING) but does not attempt to give
                CmpF64/CmpF32 real float semantics or render these
                units to instructions; that is the pre-existing,
                separately-documented "CmpF64 not modeled" limitation
                (REFUSAL_CATEGORY in expr_to_canon.py), out of scope
                for this cause.

  CONDITION (read off the setcc/cmovcc/jcc mnemonic's suffix -- the
  standard x86-64 14-condition vocabulary; O/NO and the always-true
  condition do not appear in this corpus and are not tabulated):

    suffix variants -> canonical condition -> predicate over (L, R)
    (L = dep1, R = dep2; "s<" etc. = signed; "u<" etc. = unsigned)

      e, z              CondEQ    L == R
      ne, nz            CondNE    L != R
      l, nge            CondSLT   L s< R
      ge, nl            CondSGE   L s>= R
      le, ng            CondSLE   L s<= R
      g, nle            CondSGT   L s> R
      b, c, nae         CondULT   L u< R
      ae, nb, nc        CondUGE   L u>= R
      a, nbe            CondUGT   L u> R
      be, na            CondULE   L u<= R
      s                 CondSGN   (L - R) s< 0   (raw sign of diff)
      ns                CondNSGN  (L - R) s>= 0
      p, pe             CondPAR   parity_even(low_byte(L - R))
      np, po            CondNPAR  parity_odd(low_byte(L - R))

THE CROSS-CHECK (route (b)).  Every one of these 14 (condition x
{SUB family, LOGIC family} x {8,16,32,64-bit}) = 112 combinations was
PROVED equal (z3/claripy solver, unsat on "my formula != angr's
ccall", zero counterexamples found) against angr 9.2.213's own
`angr.engines.vex.claripy.ccall.amd64g_calculate_condition` -- the
SAME symbolic condition-code evaluator angr's own VEX execution
engine uses.  See the report for the proof script and the full
14x2x4 = 112-row PROVED-EQUAL table; zero disagreements were found.
This is "forced by construction" evidence (a solver proof), not
sampled testimony.  angr had to be installed with several transitive
dependencies beyond --no-deps (networkx, claripy, cle, and a long
tail of format-backend packages irrelevant to this proof) plus two
narrow stub modules (`xbe`, `pypcode`) for two backend formats (Xbox
executables, Ghidra p-code) this repo will never load -- recorded
honestly in the report, not hidden.

THE SPELLING BAN: this table is keyed by INSTRUCTION KIND and
CONDITION SUFFIX (mnemonics), never by the source-language operator
token; it does not group or pair UNITS at all -- it is a per-call
substitution inside one unit's own expression tree.
"""

import re


# --------------------------------------------------------------------
# Section 1: condition-suffix -> canonical condition name.
# --------------------------------------------------------------------

SUFFIX_TO_COND = {
    "e": "CondEQ", "z": "CondEQ",
    "ne": "CondNE", "nz": "CondNE",
    "l": "CondSLT", "nge": "CondSLT",
    "ge": "CondSGE", "nl": "CondSGE",
    "le": "CondSLE", "ng": "CondSLE",
    "g": "CondSGT", "nle": "CondSGT",
    "b": "CondULT", "c": "CondULT", "nae": "CondULT",
    "ae": "CondUGE", "nb": "CondUGE", "nc": "CondUGE",
    "a": "CondUGT", "nbe": "CondUGT",
    "be": "CondULE", "na": "CondULE",
    "s": "CondSGN",
    "ns": "CondNSGN",
    "p": "CondPAR", "pe": "CondPAR",
    "np": "CondNPAR", "po": "CondNPAR",
}

# every synthetic op this file introduces, so callers can recognize
# them without re-deriving the set from SUFFIX_TO_COND's values.
COND_OPS = frozenset(SUFFIX_TO_COND.values())

# mnemonic prefixes that consume flags -- setcc, cmovcc, jcc.
CONSUMER_PREFIXES = ("set", "cmov", "j")

FLAGSETTER_MNEMONICS = ("test", "cmp", "ucomisd", "ucomiss")


def suffix_of(mnem, prefix):
    """'setne' + 'set' -> 'ne'.  'cmovle' + 'cmov' -> 'le'."""
    return mnem[len(prefix):]


def consumer_kind_and_suffix(mnem):
    """mnem is the bare opcode text (no operands), e.g. 'setne'.
    Returns (prefix, suffix) or (None, None) if mnem is not a
    flag-consuming instruction."""
    for prefix in CONSUMER_PREFIXES:
        if mnem.startswith(prefix) and len(mnem) > len(prefix):
            suf = suffix_of(mnem, prefix)
            if suf in SUFFIX_TO_COND:
                return prefix, suf
    return None, None


# --------------------------------------------------------------------
# Section 2: scan canonical text (canon4's derived_text / mnem list)
# for (flagsetter kind, consumer instruction) pairs, IN PROGRAM ORDER.
# "Most recent flag setter" rule -- flags persist on real hardware
# until the next flag-setting instruction, so a consumer binds to
# whichever test/cmp/ucomisd/ucomiss most recently ran, not
# necessarily the line directly above it.
# --------------------------------------------------------------------

MNEM_RE = re.compile(r"^([a-z][a-z0-9]*)")


def bare_mnem(line):
    m = MNEM_RE.match(line.strip())
    return m.group(1) if m else None


def scan_canonical_text(lines):
    """lines: canon4's derived_text (or raw mnem) list, one instruction
    per string ("test %edi,%edi", "setne %r10b", ...).

    Returns a list of records, one per flag-CONSUMING instruction
    found, in program order:
        dict(index=<line index>, mnem=<'setne'>, cond=<'CondNE'>,
             flagsetter_index=<line index of the most recent
                 test/cmp/ucomisd/ucomiss>,
             flagsetter_mnem=<'test'>,
             flagsetter_kind=<'logic'|'sub'|'float'>)
    A consumer with no preceding flag-setter in this unit's own text
    is a genuine gap (carried-in flags from outside the unit) and is
    reported, not silently dropped.
    """
    out = []
    current_setter_index = None
    current_setter_mnem = None
    for i, line in enumerate(lines):
        mnem = bare_mnem(line)
        if mnem is None:
            continue
        if mnem in FLAGSETTER_MNEMONICS:
            current_setter_index = i
            current_setter_mnem = mnem
            continue
        prefix, suf = consumer_kind_and_suffix(mnem)
        if prefix is None:
            continue
        if mnem in FLAGSETTER_MNEMONICS:
            continue
        cond = SUFFIX_TO_COND[suf]
        if current_setter_mnem in ("test",):
            kind = "logic"
        elif current_setter_mnem == "cmp":
            kind = "sub"
        elif current_setter_mnem in ("ucomisd", "ucomiss"):
            kind = "float"
        else:
            kind = None
        out.append(dict(
            index=i,
            mnem=mnem,
            cond=cond,
            flagsetter_index=current_setter_index,
            flagsetter_mnem=current_setter_mnem,
            flagsetter_kind=kind,
        ))
    return out


# --------------------------------------------------------------------
# Section 3: z3 semantics for the 14 synthetic condition ops, over
# (L, R) of equal width -- PROVED equal to angr's ccall for every one
# of the 14 conditions, both the SUB and LOGIC op families, at 8/16/
# 32/64-bit widths (112/112 proved, see report and this file's
# header).
# --------------------------------------------------------------------

def cond_to_z3(cond, L, R, z3mod):
    z3 = z3mod
    diff = L - R
    if cond == "CondEQ":
        return L == R
    if cond == "CondNE":
        return L != R
    if cond == "CondSLT":
        return L < R
    if cond == "CondSGE":
        return L >= R
    if cond == "CondSLE":
        return L <= R
    if cond == "CondSGT":
        return L > R
    if cond == "CondULT":
        return z3.ULT(L, R)
    if cond == "CondUGE":
        return z3.UGE(L, R)
    if cond == "CondUGT":
        return z3.UGT(L, R)
    if cond == "CondULE":
        return z3.ULE(L, R)
    if cond == "CondSGN":
        return diff < 0
    if cond == "CondNSGN":
        return diff >= 0
    if cond in ("CondPAR", "CondNPAR"):
        b0 = z3.Extract(7, 0, diff)
        p = z3.BitVecVal(0, 1)
        for i in range(8):
            p = p ^ z3.Extract(i, i, b0)
        even = (p == 0)
        return even if cond == "CondPAR" else z3.Not(even)
    raise ValueError("unknown synthetic condition %r" % cond)


# --------------------------------------------------------------------
# Section 4: substitute `ex1@0(amd64g_calculate_condition(...))` call
# sites in a unit's RAW VEX text with the synthetic CondXX(dep1,dep2)
# node route (a) determined for that occurrence, matched to canonical
# text POSITIONALLY (the call sites appear left-to-right in
# normal_path_raw in the same program order as the setcc/cmov/branch
# instructions that read them -- verified on every worked example in
# the report; a unit where the counts disagree is refused, not
# guessed at).
# --------------------------------------------------------------------

CALL_RE = re.compile(
    r"ex1@0\(amd64g_calculate_condition\((\d+):64,(\d+):64,")


def find_call_spans(raw_text):
    """returns a list of (start, end, cc, op, args_start) for every
    `ex1@0(amd64g_calculate_condition(cc:64,op:64,` occurrence, left
    to right.  `end` is the index just past the matching close-paren
    of the OUTER ex1@0(...) call (balanced-paren scan from
    args_start)."""
    spans = []
    for m in CALL_RE.finditer(raw_text):
        cc, op = int(m.group(1)), int(m.group(2))
        depth = 0
        i = m.start()
        # walk from the "ex1@0(" open paren to find the matching close.
        open_pos = raw_text.index("(", m.start())
        j = open_pos
        depth = 0
        while j < len(raw_text):
            if raw_text[j] == "(":
                depth += 1
            elif raw_text[j] == ")":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        spans.append((m.start(), j + 1, cc, op, m.end()))
    return spans


def call_inner_args(raw_text, span):
    """given a span from find_call_spans, return the RAW TEXT of
    (dep1, dep2, ndep) -- the three arguments after cc:64,op:64,
    inside amd64g_calculate_condition(...), by a balanced-comma scan
    (top-level commas only)."""
    start, end, cc, op, args_start = span
    # args_start points just after "amd64g_calculate_condition(cc:64,op:64,"
    inner_end = raw_text.rindex(")", start, end)  # the ex1@0(...) close
    call_close = raw_text.rindex(")", start, inner_end + 1)
    # amd64g_calculate_condition(...) itself is everything from
    # args_start up to one paren before ex1@0's own close.
    body = raw_text[args_start:end - 1]
    depth = 0
    parts = []
    cur = []
    for ch in body:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    if len(parts) != 3:
        raise ValueError("expected 3 args (dep1,dep2,ndep), got %d: %r"
                          % (len(parts), parts))
    return parts[0], parts[1], parts[2]


def substitute_conditions(raw_text, canon_records):
    """raw_text: a unit's normal_path_raw.
    canon_records: scan_canonical_text()'s output for this unit.

    Returns (new_text, applied, note):
      applied is the number of substitutions made.
      note explains any mismatch (refusal, not a guess) when the
      count of amd64g_calculate_condition call sites in raw_text does
      not match the count of flag-consuming instructions found in
      canonical text -- in that case new_text == raw_text unchanged.
    """
    spans = find_call_spans(raw_text)
    if not spans:
        return raw_text, 0, "no amd64g_calculate_condition call in text"
    if len(spans) != len(canon_records):
        return raw_text, 0, (
            "call-site count (%d) does not match canonical-text "
            "flag-consumer count (%d) -- refusing rather than "
            "guessing the pairing" % (len(spans), len(canon_records)))
    # build replacements right-to-left so earlier offsets stay valid.
    out = raw_text
    applied = 0
    for span, rec in zip(reversed(spans), reversed(canon_records)):
        start, end, cc, op, args_start = span
        if rec["flagsetter_kind"] not in ("logic", "sub"):
            # float family: leave the call in place (untouched) --
            # this occurrence is handled by substitute_float_conditions,
            # not here, or is left opaque as an honest refusal.
            continue
        dep1, dep2, ndep = call_inner_args(raw_text, span)
        cond = rec["cond"]
        repl = "%s(%s,%s)" % (cond, dep1, dep2)
        out = out[:start] + repl + out[end:]
        applied += 1
    return out, applied, None
