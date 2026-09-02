#!/usr/bin/env python3
"""l3_answers.py -- layer 3 phase 4, the ANSWER-GRAIN clustering.

Log 030 clustered on DOMAINS: which ordered form pairs an operation
accepts.  Its own §5 recorded the limit -- the CORE defines
`contradicts' at the ANSWER grain (same input, different answer) and
log 030 could not test it, because acceptance asks only `can this
typecheck'.  Two languages can both accept `1 + true' and answer
differently, and nothing in log 030 would see it.

This pass reads the computed values.  Only python, ruby and php have
executed answers, so this pass covers those three and no others; the
nine statically checked languages enter when route C runs for them.

Decisions 18 through 27 are numbered here and carried in the output so
that overturning any one of them is a one-line instruction.  Decisions
1 through 17 stand where they are not superseded; they are reproduced
from `clusters_final.json` rather than restated, so there is one copy.

Every canonicalization is REVERSIBLE: the pre-canonical raw string is
kept beside the canonical token in `answer_alphabet`, and every merge a
canonicalization performs is counted and exampled in `canon_merges`.
"""

import itertools
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from l3_final import merge_history, count_at, clusters_at, plateaus  # noqa
from l3_cluster import bar, FORMS                                    # noqa

LANGS = ["python", "ruby", "php"]

SHARED = [(a, b) for a in FORMS for b in FORMS]      # the 64 cells

# --------------------------------------------------------------------
# DECISIONS
# --------------------------------------------------------------------

DECISIONS = [
 ("18", "ANSWER GRAIN IS THE PROBE ID, NOT THE FORM PAIR.  The three "
  "route-C manifests use ONE value-class vocabulary -- `base_42', "
  "`i64max', `p53_plus1', `negzero', `nan', `eacute' and the rest are "
  "spelled identically in all three -- so an INPUT CELL is the tuple "
  "(operation, form_a, value_class_a, form_b, value_class_b) and it "
  "means the same input in every language that has it.  This is what "
  "makes `same input, different answer' a measurable statement rather "
  "than an analogy.  Verified rather than assumed: the value-class sets "
  "per form are compared across the three and reported as "
  "`value_class_vocabulary'.  Overturnable: two languages spelling "
  "`base_pi' may still not hold the same bits, and layer 2 is exactly "
  "where that leaks; the load-check discipline of decision 15 has no "
  "counterpart here yet."),
 ("19", "THE RECORDED RESULT IS (RUNTIME TYPE, PRINTED VALUE), AND BOTH "
  "ARE KEPT RAW.  Every ANSWER cell in a route-C behavior table is the "
  "string `TYPE:VALUE', where TYPE is the language's OWN type name and "
  "VALUE is the language's OWN printing of the result.  Neither is "
  "normalised at read time.  The canonical token built below is stored "
  "BESIDE the raw string, never in place of it, so every rule 20 to 24 "
  "can be switched off by re-reading `answer_alphabet' and no re-run is "
  "needed to overturn one."),
 ("20", "BOOLEANS ARE CANONICALISED, AND PHP FORCES IT.  php's harness "
  "printed booleans through echo, so php false is the EMPTY STRING and "
  "php true is `1': the raw cells read `boolean:' and `boolean:1'.  "
  "python reads `bool:True' / `bool:False' and ruby `TrueClass:true' / "
  "`FalseClass:false'.  These are three spellings of two values and "
  "they are merged to `truth:true' and `truth:false'.  This is a "
  "MERGING rule -- it makes three languages agree that would otherwise "
  "differ on every comparison operator in the pass -- and it is the "
  "single most load-bearing canonicalization here.  It is also the one "
  "with the least doubt attached: no other value in php prints as the "
  "empty string with type `boolean'."),
 ("21", "NUMERIC EQUALITY ACROSS INT/FLOAT SPELLINGS IS *NOT* ASSUMED; "
  "EXACTNESS WRAPPERS ARE UNWRAPPED, KIND IS TAKEN FROM THE VALUE.  "
  "`Decimal(42)', `Fraction(42, 1)', `Rational (42/1)', `BigDecimal' "
  "and a plain `42' are unwrapped to the same canonical token "
  "`whole:42', because the wrapper is a HOLDER fact and layer 3 asks "
  "what the operation computed.  But a value that is not an integer "
  "canonicalises to `fractional:...' and NEVER equals a `whole:...' "
  "token -- `whole:42' and `fractional:42.0' are DIFFERENT answers "
  "here.  Rationale: an operation that answers 42 and an operation "
  "that answers 42.0 have made different decisions, and this pass "
  "exists to see decisions.  Overturnable in the loose direction "
  "(merge whole and fractional on numeric value) by one comparison; "
  "the pre-canonical forms make it a re-read."),
 ("22", "FLOATS ARE COMPARED AT 14 SIGNIFICANT DIGITS, BECAUSE PHP'S "
  "PRINT IS LOSSY AND THE HARNESS DID NOT PRESERVE BITS.  php echoed "
  "`9.2233720368548E+18' where python's repr gives "
  "`9.223372036854776e+18' -- php's default `precision' ini is 14 and "
  "the harness printed through echo, so php's float answers carry 14 "
  "significant digits and no more.  Comparing at 17 would report a "
  "disagreement that is the INSTRUMENT, exactly the class of fault log "
  "030 decision 12 found in dart.  So floats are re-parsed and "
  "re-formatted `%.14g'.  THE COST IS RECORDED AND IT IS REAL: any "
  "genuine php-versus-python float difference below the 15th digit is "
  "INVISIBLE to this pass, including the whole 2^53 neighbourhood once "
  "a value has passed through a php float.  This is a limit on the "
  "measurement, not a finding about php."),
 ("23", "SIGNED ZERO, NAN AND INFINITY ARE PRESERVED, AND NAN EQUALS "
  "NAN *AS AN ANSWER*.  `-0.0' canonicalises to `fractional:-0.0' and "
  "`0.0' to `fractional:0.0' and they are DIFFERENT answers -- php's "
  "echo prints `-0', which is parsed back to negative zero by its sign "
  "character rather than by float arithmetic, since `float(\"-0\") == "
  "0.0' would destroy the distinction the fracture is about.  `nan', "
  "`NaN' and `NAN' all canonicalise to `fractional:nan', and two "
  "`fractional:nan' tokens COMPARE EQUAL in this pass.  That is a "
  "statement about answer identity, not about the languages: every one "
  "of the three answers false to `nan == nan', and the pass records "
  "that as agreement on the answer `truth:false' while also recording "
  "that both computed the same NaN.  Infinities keep their sign: "
  "`inf', `Infinity', `INF' -> `fractional:inf'."),
 ("24", "TEXT IS CANONICALISED TO ITS BYTES; A NUMBER-SHAPED STRING IS "
  "NEVER A NUMBER.  python prints text four ways (`'e'', `b'\\xc3\\xa9'', "
  "`bytearray(b'...')'), ruby two (`\"e\"', `\"\\xC3\\xA9\"'), php one "
  "(bare).  Quoting, the `b' prefix and the `bytearray(...)' wrapper "
  "are stripped, hex escapes are decoded, and literal characters are "
  "utf-8 encoded, so the canonical token is `text:' plus a lowercase "
  "hex byte string.  This MERGES python's `str' answer with its own "
  "`bytes' answer and with ruby's byte-string answer wherever the "
  "bytes coincide -- which is precisely the e-acute question, so the "
  "merge is the measurement and the raws are kept beside it.  Separately "
  "and firmly: `text:3834' (the string \"84\") never equals `whole:84'.  "
  "The kind is part of the answer."),
 ("25", "CONTAINERS ARE COMPARED ON THEIR PRINTED BODY, WHITESPACE AND "
  "QUOTE STYLE NORMALISED, AND NOTHING ELSE.  `list', `tuple', "
  "`deque([...])', `Array', `Set: #<Set: {...}>', php `array' and the "
  "rest are reduced to a kind (`sequence' when the body opens `[', "
  "`keyed' when it opens `{') plus the body with spaces removed and "
  "double quotes rewritten to single.  That merges python `[1, 2, 3, "
  "'a', 'b']' with ruby `[1, 2, 3, \"a\", \"b\"]'.  It does NOT "
  "reorder, deduplicate, or reconcile key spelling, so php's "
  "`{\"a\":1,...}' stays distinct from python's `{'a': 1,...}' only by "
  "separator, and any element-level difference counts as a "
  "disagreement.  This is deliberately the CONSERVATIVE end: a "
  "container canonicalization that reordered would smooth away real "
  "answers.  Anything the rules cannot parse becomes "
  "`opaque:<raw>', which equals only an identical raw."),
 ("26", "HOLDER-TO-FORM ANSWER PROJECTION IS EXISTENTIAL WITH A SPLIT "
  "MARKER.  Decision 1 projects holders onto forms and decision 2 makes "
  "acceptance existential over holders.  Answers need the same rule and "
  "the same escape hatch: an input cell's answer is the SET of "
  "canonical tokens over every holder pair carrying those two forms, "
  "and the cell is marked `uniform' when the set has one element and "
  "`split' when it has more.  Two languages AGREE on a cell when their "
  "answer sets INTERSECT.  Rationale: existential matches the two "
  "rulings above and the alternative -- majority -- would silently pick "
  "a winner among python's four whole-number holders, which is the "
  "distinction log 024 §5 was created to keep.  PROPOSED, FLAGGED FOR "
  "DEE: the split-marker rate is reported per language and per "
  "operation so he can see what the rule is hiding before he keeps it, "
  "and the universal reading (agree only if the sets are EQUAL) is "
  "computed alongside as `agreement_universal'."),
 ("28", "THE HARNESS TRUNCATES EVERY PRINTED ANSWER AT 120 "
  "CHARACTERS, AND THAT IS AN INSTRUMENT FACT, NOT A LANGUAGE ONE.  "
  "`l3_routec.py' writes `repr(r)[:120]' in python, `r.inspect[0,120]' "
  "in ruby and `substr((string)$s, 0, 120)' in php.  Any answer at the "
  "cap is flagged `#trunc' on its canonical token and NEVER compares "
  "equal to an untruncated one.  Two truncated answers still compare, "
  "because all three harnesses cut at the same 120, so `2**large' "
  "digits line up -- but a wrapper that eats characters before the "
  "digits start (python's `Fraction(') shifts the window and the "
  "comparison then fails for a reason that is the printer.  Every "
  "truncated cell is counted and reported; nothing is silently "
  "dropped.  The fix, for whoever runs route C next, is to print "
  "without a cap or to hash the tail."),
 ("29", "THREE LANGUAGES, THREE SERIALISERS, AND THE PASS DOES NOT "
  "PRETEND OTHERWISE.  python answers come through `repr', ruby "
  "through `inspect', php through `(string)' for scalars and "
  "`json_encode' for everything else.  Ruby also prints an OBJECT "
  "ADDRESS in the type name of an anonymous Struct or Data class "
  "(`#<Class:0x00007ee82bbaa6e8>'), which is a different string on "
  "every run and would make ruby disagree with ITSELF between runs; "
  "addresses are rewritten to `0xADDR'.  Hash rockets are rewritten to "
  "colons so ruby's `{\"a\"=>1}' meets php's `{\"a\":1}' and python's "
  "`{'a': 1}'.  What is NOT reconciled: python's `OrderedDict([('a', "
  "1)])' is a list-of-pairs where the other two print a mapping, and "
  "such a cell counts as a disagreement at that holder.  Decision 26's "
  "existential projection is what keeps it from becoming a false "
  "cross-language contradiction, since the plain `dict' holder answers "
  "in the shared shape.  Overturnable, and the honest fix is a "
  "harness that prints one agreed serialisation."),
 ("30", "PHP'S `and', `or' AND `xor' ROWS ARE VOID, AND THE ANSWER "
  "GRAIN IS WHAT CAUGHT IT.  `l3_routec.py' emits `$__r = ($a) $op "
  "($b);' for every php operation.  For `&&', `||' and every operator "
  "in the table that is correct, but php's `and', `or' and `xor' bind "
  "LOOSER THAN ASSIGNMENT, so the statement parses as `($__r = ($a)) "
  "and ($b)' and the recorded answer is the LEFT OPERAND, every time.  "
  "MEASURED, not argued: php's `and' returns `integer:42' for "
  "`42 and null', `42 and false', `42 and true', `42 and 42' and "
  "`42 and 0' -- 6,241 answer cells and the answer is the left operand "
  "in all of them.  The acceptance-grain passes could not see this "
  "because a wrong answer is still an ACCEPT, which is exactly the "
  "argument log 030 §6 made for running this pass.  The three "
  "signatures are marked VOID, excluded from the clustering and kept "
  "in the artifact with the diagnosis, following the standing rule "
  "that a wrong measurement stays on the record.  php's `&&' and `||' "
  "are UNAFFECTED -- they bind tighter than `=' -- and their "
  "disagreement with ruby is a real one."),
 ("27", "THE COMBINED DISTANCE: JACCARD ON DOMAINS TIMES AGREEMENT RATE "
  "ON THE SHARED INPUT CELLS.  similarity(a, b) = J x A, where J is "
  "decision 4's Jaccard over the 64 form-pair cells and A is the "
  "fraction of INPUT CELLS accepted by BOTH signatures on which their "
  "answer sets intersect (decision 26).  The product is chosen so that "
  "neither factor can be ignored: two operations that accept the same "
  "forms but compute different values are far apart, and two that "
  "always agree where they overlap are still far apart if they overlap "
  "on little.  A is defined only where a shared input cell exists; "
  "where the domains intersect but no input cell is shared, A is "
  "recorded as null and similarity falls back to J alone, flagged "
  "`domain_only' on the edge.  An empty domain is excluded from the "
  "clustering entirely, as in decision 4.  PROPOSED, FLAGGED FOR DEE: "
  "the sum form (wJ + (1-w)A) and the min form are the obvious rivals "
  "and both are computable from the stored J and A without a re-run."),
]

# --------------------------------------------------------------------
# canonicalization
# --------------------------------------------------------------------

TRUTH_TYPES = {"bool", "TrueClass", "FalseClass", "boolean"}
NULL_TYPES = {"NoneType", "NilClass", "NULL"}
TEXT_TYPES = {"str", "bytes", "bytearray", "String", "Symbol", "string"}
NUM_TYPES = {"int", "Integer", "integer", "float", "Float", "double",
             "Decimal", "Fraction", "Rational", "BigDecimal", "complex"}
SEQ_TYPES = {"list", "tuple", "deque", "array", "frozenset", "Array",
             "Set", "SplFixedArray", "SplDoublyLinkedList"}
KEY_TYPES = {"dict", "namespace", "OrderedDict", "SimpleNamespace", "Hash", "Struct",
             "Data", "object", "stdClass", "ArrayObject"}

TRUE_RAW = {"True", "true", "1"}
FALSE_RAW = {"False", "false", ""}

RE_DEC = re.compile(r"^Decimal\('(.*)'\)$")
RE_FRAC = re.compile(r"^Fraction\((-?\d+), (\d+)\)$")
RE_RAT = re.compile(r"^\((-?\d+)/(\d+)\)$")
RE_BA = re.compile(r"^bytearray\((.*)\)$")
RE_WRAP = re.compile(r"^(?:deque|array|frozenset|Set|OrderedDict"
                     r"|SimpleNamespace)\((.*)\)$")
RE_SETRB = re.compile(r"^#<Set: \{(.*)\}>$")
RE_CALL = re.compile(r"^[A-Za-z_][\w.]*\((.*)\)$")
RE_STRUCT = re.compile(r"^#<(?:struct|data)\s*(.*)>$")
RE_ADDR = re.compile(r"0x[0-9a-fA-F]{4,}")
TRUNC_AT = 120                                       # DECISION 28
RE_INT = re.compile(r"^[+-]?\d+$")
RE_HEX = re.compile(r"\\x([0-9a-fA-F]{2})")
ESCAPES = {"n": b"\n", "t": b"\t", "r": b"\r", "0": b"\0", "e": b"\x1b",
           "\\": b"\\", '"': b'"', "'": b"'"}

# DECISION 30: the php harness's own precedence fault.
# DECISION 44 (log 035): LIFTED, because the fault is repaired and the
# run retaken.  Decision 30 voided php's `and', `or' and `xor' because
# `$__r = ($a) and ($b);' binds as `($__r = $a) and $b' and recorded the
# LEFT OPERAND.  `l3_wordops.repair_routec' parenthesises the whole
# expression, `rc_php2' re-ran php WHOLE under the repaired driver, and
# `l3_refold.refold_routec' folded that run into behavior_php_C.json.
# The three rows are measurements again, so they are no longer voided.
#
# The voiding is KEPT here rather than deleted, because decision 30
# produced published numbers in logs 031 and 033 and those logs must
# stay readable against the reason they excluded three leaves.
VOID_LIFTED = {"php.and": "decision 30, lifted by decision 44",
               "php.or": "decision 30, lifted by decision 44",
               "php.xor": "decision 30, lifted by decision 44"}
VOID = {}

NAN_RAW = {"nan", "NaN", "NAN", "-nan"}
INF_RAW = {"inf": "inf", "Infinity": "inf", "INF": "inf",
           "-inf": "-inf", "-Infinity": "-inf", "-INF": "-inf"}


FLOAT_TYPES = {"float", "Float", "double"}


def canon_number(v, force_float=False):
    """DECISION 21/22/23.  -> (kind, token) or None if unparsable.

    `force_float' is set when the RUNTIME TYPE is already a float type.
    Without it php's `double:-0' would parse as the integer 0 and the
    signed-zero fracture decision 23 exists to keep would be destroyed
    by the reader rather than by the language.
    """
    s = v.strip()
    if force_float:
        if s in NAN_RAW:
            return "fractional", "nan"
        if s in INF_RAW:
            return "fractional", INF_RAW[s]
        neg = s.startswith("-")
        try:
            f = float(s)
        except ValueError:
            return None
        if f != f:
            return "fractional", "nan"
        if f in (float("inf"), float("-inf")):
            return "fractional", "-inf" if f < 0 else "inf"
        if f == 0.0:
            return "fractional", "-0.0" if neg else "0.0"
        return "fractional", "%.14g" % f
    m = RE_DEC.match(s)
    if m:
        s = m.group(1)
    m = RE_FRAC.match(s) or RE_RAT.match(s)
    if m:
        num, den = int(m.group(1)), int(m.group(2))
        if den and num % den == 0:
            return "whole", str(num // den)
        s = "%d/%d" % (num, den)
        return "fractional", s
    if s in NAN_RAW:
        return "fractional", "nan"
    if s in INF_RAW:
        return "fractional", INF_RAW[s]
    if RE_INT.match(s):
        return "whole", str(int(s))
    # DECISION 23: signed zero read off the sign CHARACTER
    neg = s.startswith("-")
    try:
        f = float(s)
    except ValueError:
        return None
    if f != f:
        return "fractional", "nan"
    if f in (float("inf"), float("-inf")):
        return "fractional", "-inf" if f < 0 else "inf"
    if f == 0.0:
        return "fractional", "-0.0" if neg else "0.0"
    return "fractional", "%.14g" % f          # DECISION 22


def canon_text(v):
    """DECISION 24.  -> hex byte string."""
    s = v
    m = RE_BA.match(s)
    if m:
        s = m.group(1)
    if s[:2] in ("b'", 'b"'):
        s = s[2:-1] if len(s) >= 3 else ""
    elif len(s) >= 2 and s[0] == s[-1] and s[0] in "'\"":
        s = s[1:-1]
    elif s.startswith(":"):                    # ruby Symbol inspect
        s = s[1:]
    # decode hex and the standard one-character escapes, utf-8 encode
    # everything else.  python's repr and ruby's inspect choose their
    # quote character differently, so ruby escapes a double quote that
    # python leaves bare -- decoding both is what makes the two
    # printers comparable at all (DECISION 24).
    out = bytearray()
    i = 0
    while i < len(s):
        m = RE_HEX.match(s, i)
        if m:
            out.append(int(m.group(1), 16))
            i = m.end()
        elif s[i] == "\\" and i + 1 < len(s) and s[i + 1] in ESCAPES:
            out += ESCAPES[s[i + 1]]
            i += 2
        else:
            out += s[i].encode("utf-8")
            i += 1
    return out.hex()


def canon_container(v):
    """DECISION 25.  -> (kind, normalised body) or None."""
    s = v.strip()
    m = RE_SETRB.match(s)
    if m:
        s = "{%s}" % m.group(1)
    m = RE_STRUCT.match(s)                     # DECISION 29
    if m:
        s = "{%s}" % m.group(1)
    m = RE_WRAP.match(s)
    if m:
        nm = s.split("(", 1)[0]
        s = m.group(1).strip()
        if s == "":
            s = "{}" if nm in KEY_TYPES else "[]"
    m = RE_CALL.match(s)                       # OrderedDict(), R3(a=1, ...)
    if m:
        inner = m.group(1).strip()
        name = m.group(0).split("(", 1)[0]
        if inner[:1] in "[{(":
            s = inner
        elif "=" in inner or name in KEY_TYPES or name.startswith("R"):
            s = "{%s}" % inner.replace("=", ":")
        else:
            s = "[%s]" % inner
    if s.startswith("(") and s.endswith(")"):
        s = "[%s]" % s[1:-1]
    body = s.replace(" ", "").replace('"', "'").replace("=>", ":")
    if body.startswith("["):
        return "sequence", body
    if body.startswith("{"):
        return "keyed", body
    return None


def canonicalise(raw):
    """DECISIONS 19-25, 28, 29.  raw `TYPE:VALUE' -> canonical token."""
    raw = RE_ADDR.sub("0xADDR", raw)           # DECISION 29
    if raw.startswith("#<Class") and ">:" in raw:
        typ, val = "Struct", raw.split(">:", 1)[1]
    else:
        typ, _, val = raw.partition(":")
    trunc = "#trunc" if len(val) >= TRUNC_AT else ""   # DECISION 28
    if trunc:
        # strip a known numeric wrapper PREFIX even without its close
        for pre in ("Decimal('", "Fraction(", "Rational("):
            if val.startswith(pre):
                val = val[len(pre):]
        if RE_INT.match(val.split(",")[0].split("/")[0] or "x"):
            return "whole:%s%s" % (val.split(",")[0].split("/")[0], trunc)
        return "opaque:%s:%s%s" % (typ, val, trunc)
    if typ in NULL_TYPES:
        return "nothing:null"
    if typ in TRUTH_TYPES:
        if val in TRUE_RAW:
            return "truth:true"
        if val in FALSE_RAW:
            return "truth:false"
        return "opaque:" + raw
    if typ in NUM_TYPES or typ.startswith("c_"):
        r = canon_number(val, force_float=(typ in FLOAT_TYPES))
        if r:
            return "%s:%s" % r
    if typ in TEXT_TYPES:
        return "text:" + canon_text(val)
    r = canon_container(val)
    if r:
        return "%s:%s" % r
    r = canon_number(val)
    if r:
        return "%s:%s" % r
    return "opaque:" + raw


# --------------------------------------------------------------------
# load
# --------------------------------------------------------------------

def load(lang):
    man = json.load(open(os.path.join(HERE, "manifest_%s.json" % lang)))
    beh = json.load(open(os.path.join(HERE, "behavior_%s_C.json" % lang)))
    assert beh.get("complete"), "%s route-C table not complete" % lang
    hs = man["holders"]
    cells = beh["cells"]
    # per operation: input cell -> {token: [raw, ...]}, plus holder accepts
    per = {}
    alphabet = {}
    t0 = time.time()
    done = 0
    for i, ha in enumerate(hs):
        for j, hb in enumerate(hs):
            for vca, _ in ha["value_classes"]:
                for vcb, _ in hb["value_classes"]:
                    for op in man["operations"]:
                        pid = "P%d_%d_%s_%s_%s" % (i, j, vca, vcb, op)
                        c = cells.get(pid)
                        if c is None:
                            continue
                        rec = per.setdefault(op, dict(
                            accept=set(), total=set(), inputs={},
                            holder_answers={}))
                        rec["total"].add((i, j))
                        if c[0] != "ANSWER":
                            continue
                        rec["accept"].add((i, j))
                        tok = canonicalise(c[1])
                        alphabet.setdefault(tok, {}).setdefault(c[1], 0)
                        alphabet[tok][c[1]] += 1
                        key = (ha["form"], vca, hb["form"], vcb)
                        rec["inputs"].setdefault(key, {}).setdefault(
                            tok, []).append((i, j))
        done += 1
        bar(done, len(hs), t0, "%s answers" % lang)
    print()
    return dict(language=lang, holders=hs, ops=man["operations"], per=per,
                alphabet=alphabet, probes=beh["probes"], kinds=beh["kinds"])


# --------------------------------------------------------------------
# signatures
# --------------------------------------------------------------------

def signatures(L):
    out = {}
    form = [h["form"] for h in L["holders"]]
    for op, rec in L["per"].items():
        if not rec["total"]:
            continue
        cells = {}
        for (i, j) in rec["total"]:
            k = (form[i], form[j])
            c = cells.setdefault(k, [0, 0])
            c[1] += 1
            if (i, j) in rec["accept"]:
                c[0] += 1
        dom = sorted(k for k, c in cells.items() if c[0] > 0)
        # DECISION 26: per form-pair answer class, existential + split
        per_cell = {}
        for (fa, vca, fb, vcb), toks in rec["inputs"].items():
            per_cell.setdefault((fa, fb), {})
            for t in toks:
                per_cell[(fa, fb)][t] = per_cell[(fa, fb)].get(t, 0) + 1
        answer_classes = {}
        for k in dom:
            d = per_cell.get(k, {})
            kinds = {}
            for t, n in d.items():
                kinds[t.split(":", 1)[0]] = kinds.get(t.split(":", 1)[0], 0) + n
            answer_classes["%s|%s" % k] = dict(
                tokens=len(d),
                shape="uniform" if len(d) == 1 else "split",
                kinds=sorted(kinds, key=lambda x: -kinds[x]),
                top=sorted(d, key=lambda t: -d[t])[:4])
        n_split = sum(1 for v in rec["inputs"].values() if len(v) > 1)
        out["%s.%s" % (L["language"], op)] = dict(
            language=L["language"], operation=op, route="C answers",
            holder_accepts=len(rec["accept"]), holder_probes=len(rec["total"]),
            domain=["%s|%s" % k for k in dom],
            input_cells=len(rec["inputs"]),
            input_cells_split=n_split,
            split_rate=round(n_split / len(rec["inputs"]), 4)
            if rec["inputs"] else None,
            answer_classes=answer_classes)
    return out


def sim_pair(ia, ib, da, db):
    """DECISION 27.  -> (similarity, jaccard, agreement, shared)"""
    A, B = set(da), set(db)
    u = A | B
    j = (len(A & B) / len(u)) if u else 0.0
    shared = set(ia) & set(ib)
    if not shared:
        return j, j, None, 0
    agree = sum(1 for k in shared if set(ia[k]) & set(ib[k]))
    a = agree / len(shared)
    return j * a, j, a, len(shared)


def main():
    print("layer 3 phase 4 -- ANSWER GRAIN, three route-C languages")
    Ls = {}
    for lang in LANGS:
        Ls[lang] = load(lang)

    # value class vocabulary check (DECISION 18)
    vocab = {}
    for lang, L in Ls.items():
        v = {}
        for h in L["holders"]:
            v.setdefault(h["form"], set()).update(
                x[0] for x in h["value_classes"])
        vocab[lang] = {f: sorted(s) for f, s in sorted(v.items())}
    identical = all(vocab[l] == vocab[LANGS[0]] for l in LANGS)

    sigs = {}
    inputs = {}
    for lang, L in Ls.items():
        s = signatures(L)
        sigs.update(s)
        for op, rec in L["per"].items():
            key = "%s.%s" % (lang, op)
            inputs[key] = {"%s|%s|%s|%s" % k: sorted(v)
                           for k, v in rec["inputs"].items()}

    for k, why in VOID.items():                     # DECISION 30
        if k in sigs:
            sigs[k]["void"] = why
    keys = sorted(k for k in sigs
                  if sigs[k]["domain"] and k not in VOID)
    empty = sorted(k for k in sigs if not sigs[k]["domain"])
    print("  %d signatures, %d with a non-empty domain, %d empty"
          % (len(sigs), len(keys), len(empty)))

    sim = {}
    edge = {}
    t0 = time.time()
    n = 0
    for a, b in itertools.combinations(keys, 2):
        s, j, ag, sh = sim_pair(inputs[a], inputs[b], sigs[a]["domain"],
                                sigs[b]["domain"])
        sim[(a, b)] = sim[(b, a)] = s
        edge[(a, b)] = dict(similarity=round(s, 6), jaccard=round(j, 6),
                            agreement=(round(ag, 6) if ag is not None
                                       else None), shared_inputs=sh)
        n += 1
        if n % 200 == 0:
            bar(n, len(keys) * (len(keys) - 1) // 2, t0, "pairs")
    bar(len(keys) * (len(keys) - 1) // 2,
        len(keys) * (len(keys) - 1) // 2, t0, "pairs")
    print()

    merges, members = merge_history(keys, sim)
    curve = [dict(threshold=round(t / 100.0, 2),
                  clusters=count_at(merges, len(keys), t / 100.0))
             for t in range(0, 101)]
    plat = plateaus(merges, len(keys))
    snaps = {}
    for p in plat[:8]:
        t = (p["low"] + p["high"]) / 2.0
        snaps["%.3f-%.3f" % (p["low"], p["high"])] = dict(
            clusters=clusters_at(keys, merges, members, t),
            count=p["clusters"], width=p["width"])

    # ---- the CONTROL: the same 69 leaves clustered on domain alone.
    # Without it, nothing in this pass would show what the ANSWER grain
    # contributed as against what the domains were already saying.
    simJ = {k: edge.get(k, edge.get((k[1], k[0])))["jaccard"]
            for k in list(sim)}
    cmerges, cmembers = merge_history(keys, simJ)
    ccurve = [dict(threshold=round(t / 100.0, 2),
                   clusters=count_at(cmerges, len(keys), t / 100.0))
              for t in range(0, 101)]
    cplat = plateaus(cmerges, len(keys))
    ags = [e["agreement"] for e in edge.values() if e["agreement"] is not None]
    ags.sort()
    control = dict(
        cluster_count_curve=ccurve,
        stability_plateaus=cplat[:12],
        widest_plateau_clusters=clusters_at(
            keys, cmerges, cmembers,
            (cplat[0]["low"] + cplat[0]["high"]) / 2.0),
        widest_plateau="[%.3f, %.3f)" % (cplat[0]["low"], cplat[0]["high"]),
        edges_with_agreement=len(ags),
        edges_domain_only=sum(1 for e in edge.values()
                              if e["agreement"] is None),
        agreement_median=round(ags[len(ags) // 2], 4) if ags else None,
        agreement_is_1=sum(1 for a in ags if a == 1.0),
        agreement_is_0=sum(1 for a in ags if a == 0.0),
    )

    # coarse readings: the widest plateau inside each low band
    coarse = {}
    for lo, hi in ((0.0, 0.2), (0.2, 0.4), (0.4, 0.6)):
        cand = [p for p in plat if lo <= p["low"] < hi]
        if not cand:
            continue
        p = cand[0]
        t = (p["low"] + p["high"]) / 2.0
        gs = clusters_at(keys, merges, members, t)
        coarse["%.3f-%.3f" % (p["low"], p["high"])] = dict(
            count=p["clusters"], width=p["width"],
            clusters=[dict(size=len(g), members=g,
                           languages=sorted({m.split(".")[0] for m in g}),
                           spellings=sorted({m.split(".", 1)[1] for m in g}))
                      for g in gs])

    # ------------------------------- same-spelling agreement, per cell
    spell = {}
    for a, b in itertools.combinations(keys, 2):
        la, oa = sigs[a]["language"], sigs[a]["operation"]
        lb, ob = sigs[b]["language"], sigs[b]["operation"]
        if la == lb or oa != ob:
            continue
        sh = sorted(set(inputs[a]) & set(inputs[b]))
        if not sh:
            continue
        by = {}
        for k in sh:
            fa, _, fb, _ = k.split("|")
            r = by.setdefault("%s|%s" % (fa, fb), [0, 0])
            r[1] += 1
            if set(inputs[a][k]) & set(inputs[b][k]):
                r[0] += 1
        spell.setdefault(oa, {})["%s vs %s" % (la, lb)] = dict(
            shared_inputs=len(sh),
            agree=sum(v[0] for v in by.values()),
            rate=round(sum(v[0] for v in by.values()) / len(sh), 4),
            by_form_pair={k: dict(agree=v[0], shared=v[1],
                                  rate=round(v[0] / v[1], 3))
                          for k, v in sorted(by.items())})

    # ---------------------------------------------- contradicts
    contra = []
    partial = []
    for a, b in itertools.combinations(keys, 2):
        la, oa = sigs[a]["language"], sigs[a]["operation"]
        lb, ob = sigs[b]["language"], sigs[b]["operation"]
        if la == lb or oa != ob:
            continue
        sh = set(inputs[a]) & set(inputs[b])
        dis = [k for k in sh if not set(inputs[a][k]) & set(inputs[b][k])]
        if not sh:
            continue
        rec = dict(a=a, b=b, shared_inputs=len(sh), disagreeing=len(dis),
                   rate=round(len(dis) / len(sh), 4),
                   examples=sorted(dis)[:6])
        if dis and len(dis) == len(sh):
            rec["kind"] = "contradicts_total"
            contra.append(rec)
        elif dis:
            rec["kind"] = "contradicts_partial"
            partial.append(rec)
    contra.sort(key=lambda r: -r["shared_inputs"])
    partial.sort(key=lambda r: -r["disagreeing"])

    # worked examples: pull the raw answers for named fractures
    def raws(lang, op, key):
        L = Ls[lang]
        rec = L["per"].get(op)
        if not rec:
            return None
        fa, vca, fb, vcb = key.split("|")
        d = rec["inputs"].get((fa, vca, fb, vcb))
        if not d:
            return None
        form = [h["form"] for h in L["holders"]]
        out = []
        for tok, hp in sorted(d.items()):
            i, j = hp[0]
            out.append(dict(token=tok, holders="%s %s %s"
                            % (L["holders"][i]["holder"], op,
                               L["holders"][j]["holder"]),
                            holder_pairs=len(hp)))
        return out

    NAMED = [
        ("+", "whole|i64max|whole|base_42", "int overflow at 2^63-1"),
        ("+", "whole|u64max|whole|base_42", "int overflow at 2^64-1"),
        ("+", "whole|p53_plus1|whole|base_42", "2^53+1"),
        ("+", "fractional|negzero|fractional|negzero", "-0.0 + -0.0"),
        ("==", "fractional|negzero|fractional|base_1_5", "-0.0 == 1.5"),
        ("+", "fractional|nan|fractional|nan", "nan + nan"),
        ("==", "fractional|nan|fractional|nan", "nan == nan"),
        ("+", "text|eacute|text|base_hello", "e-acute concatenation"),
        ("==", "text|eacute|text|eacute", "e-acute equality"),
        ("+", "sequence|base|sequence|strs", "sequence + sequence"),
        ("==", "truth|true|whole|base_42", "true == 42"),
        ("&", "truth|true|whole|base_42", "true & 42"),
        ("+", "truth|true|whole|base_42", "true + 42"),
        ("<", "fractional|inf|fractional|nan", "inf < nan"),
    ]
    worked = []
    for op, key, label in NAMED:
        row = dict(label=label, operation=op, input_cell=key, per_language={})
        for lang in LANGS:
            r = raws(lang, op, key)
            if r is not None:
                row["per_language"][lang] = r
        toks = {l: sorted(set(x["token"] for x in v))
                for l, v in row["per_language"].items()}
        row["tokens"] = toks
        ls = [l for l in toks if toks[l]]
        row["all_agree"] = (len(ls) > 1 and
                            bool(set.intersection(*[set(toks[l])
                                                    for l in ls])))
        worked.append(row)

    # canonical merges: tokens with more than one pre-canonical raw
    merges_tab = []
    allraw = {}
    for lang, L in Ls.items():
        for tok, d in L["alphabet"].items():
            for raw, n in d.items():
                allraw.setdefault(tok, {}).setdefault(lang, {})
                allraw[tok][lang][raw] = allraw[tok][lang].get(raw, 0) + n
    for tok, per_l in allraw.items():
        forms_ = set()
        for lang, d in per_l.items():
            forms_ |= set(d)
        if len(forms_) > 1:
            merges_tab.append(dict(token=tok, pre_canonical=sorted(forms_)[:8],
                                   n_pre=len(forms_),
                                   languages=sorted(per_l),
                                   probes=sum(sum(d.values())
                                              for d in per_l.values())))
    merges_tab.sort(key=lambda r: -r["probes"])

    prior = json.load(open(os.path.join(HERE, "clusters_final.json")))
    out = dict(
        status="ANSWER-GRAIN",
        extends="clusters_final.json",
        built=time.strftime("%Y-%m-%d %H:%M:%S"),
        scope="the FIRST answer-grain pass: python, ruby and php, the "
              "three languages with executed answers.  Distance counts "
              "answer agreement on shared accepted input cells, not "
              "domain overlap alone (decision 27).",
        languages={l: dict(probes=Ls[l]["probes"], kinds=Ls[l]["kinds"])
                   for l in LANGS},
        value_class_vocabulary=vocab,
        value_class_vocabulary_identical=identical,
        forms=FORMS, shared_space_cells=len(SHARED),
        prior_decisions=[d["n"] for d in prior["decisions"]],
        decisions=[dict(n=n_, text=t)
                   for n_, t in sorted(DECISIONS, key=lambda x: int(x[0]))],
        answer_alphabet={l: {t: d for t, d in sorted(
            Ls[l]["alphabet"].items())} for l in LANGS},
        canon_merges=merges_tab[:120],
        canon_merges_total=len(merges_tab),
        signatures=sigs,
        empty_domain=empty,
        void_signatures=VOID,
        n_leaves=len(keys),
        edges={"%s :: %s" % k: v for k, v in sorted(edge.items())},
        merge_history=merges,
        cluster_count_curve=curve,
        stability_plateaus=plat,
        cluster_snapshots=snaps,
        coarse_readings=coarse,
        control_domain_only=control,
        spelling_agreement=spell,
        contradicts=contra,
        contradicts_partial=partial,
        contradicts_counts=dict(total=len(contra), partial=len(partial)),
        worked_examples=worked,
    )
    p = os.path.join(HERE, "clusters_answers.json")
    json.dump(out, open(p, "w"), indent=1, default=str)
    print("  wrote %s (%.1f MB)" % (p, os.path.getsize(p) / 1e6))
    print("  leaves %d | contradicts total %d | partial %d"
          % (len(keys), len(contra), len(partial)))
    print("  widest plateau %s -> %d clusters"
          % ([p2 for p2 in plat[:3]], plat[0]["clusters"]))


# ====================================================================
# THE BRIDGE -- decisions 31 to 42, added for the TWELVE-language pass
# ====================================================================
#
# Log 031 read three languages whose answers arrive as PRINTED TOKENS
# (`TYPE:VALUE', the language's own repr).  Log 032 recorded nine more
# whose answers arrive as BITS (`INT:64:<hex>', `FLOAT:64:<hex>',
# `STR:<len>:<bytes>:<hex>', containers recursive).  Two encodings, one
# question.  Everything below maps the BIT form into the SAME canonical
# token space decisions 20 to 25 built, so that an `INT:64' carrying 84
# and python's `whole:84' can meet.
#
# The rule the whole section obeys: a merge is only ever performed on
# the CANONICAL side.  The pre-bridge form -- the raw
# `TYPE|ENCODING:PAYLOAD' triple for the nine, the raw `TYPE:VALUE'
# string for the three -- is kept beside the token in `answer_alphabet',
# so every decision here is overturned by a re-read.
#
# `l3_answers.py' run as a script is UNCHANGED and still reproduces
# log 031's `clusters_answers.json' from the three languages alone.
# The twelve-language driver is `l3_answers12.py'.

NINE = ["go", "rust", "cpp", "java", "csharp", "typescript", "swift",
        "kotlin", "dart"]
THREE = ["python", "ruby", "php"]
LANGS12 = THREE + NINE

BRIDGE_DECISIONS = [
 ("31", "A NON-ANSWER OUTCOME IS AN ANSWER CLASS.  Route C returns four "
  "things and only one of them is a value.  A RAISE is recorded as the "
  "token `raise:<name>', a DEATH as `death:<rc>'.  Both compare like any "
  "other token: two languages agree on an input cell when their token "
  "sets intersect, so go's `raise:integer divide by zero' and rust's "
  "`raise:panic' AGREE with each other only if the names match, and "
  "dart's `fractional:inf' on the same cell agrees with neither.  This "
  "is what lets `42 / 0' be measured as the six-way split log 032 §5 "
  "described rather than as six blanks.  The three print-grain "
  "languages get the same treatment: their route-C tables carry RAISE "
  "cells with the exception class name and those cells now carry "
  "`raise:<name>' tokens where log 031 discarded them.  CONSEQUENCE, "
  "STATED: this pass's input-cell counts for python, ruby and php are "
  "LARGER than log 031's, and the two passes' A factors are therefore "
  "not the same number.  Overturnable by dropping the two token "
  "families from `answer_set'."),
 ("32", "THE DOMAIN STAYS WHAT IT WAS; ONLY THE ANSWER SET GREW.  The "
  "64-cell form-pair domain of decision 1 and 4 -- and therefore the "
  "Jaccard factor J of decision 27 -- counts a form pair as IN only if "
  "some holder pair produced a VALUE answer.  A form pair on which the "
  "language only ever raises or dies is OUT.  Rationale: J is the one "
  "quantity comparable straight back to log 030 and log 031, and "
  "letting raises into it would silently change the meaning of every "
  "curve those logs published.  So decision 31's new tokens enter the "
  "AGREEMENT factor A and nothing else."),
 ("33", "INTEGERS BRIDGE BY VALUE, NOT BY WIDTH.  `INT:<bits>:<hex>' is "
  "decoded two's complement, `UINT:<bits>:<hex>' unsigned, "
  "`BIGINT:<hex>' by its sign-and-magnitude form, and each becomes "
  "`whole:<decimal>' -- the exact token decision 21 gives python's "
  "`42'.  The WIDTH IS DROPPED on purpose: `INT:32:0000002a' and "
  "`INT:64:000000000000002a' and python's `whole:42' are one answer "
  "here, because the width is a HOLDER fact and layer 3 asks what the "
  "operation computed.  The consequence is the one worth having: "
  "go's wrapped `INT:64:8000000000000029' becomes "
  "`whole:-9223372036854775767' and python's unwrapped "
  "`whole:9223372036854775849' does not, and the overflow story is "
  "measurable across the divide.  c#'s `DEC128' is decoded to its exact "
  "decimal and takes `whole:' when integral, `fractional:' otherwise."),
 ("34", "FLOATS KEEP THEIR BITS AND ALSO CARRY A 14-DIGIT SHADOW, AND "
  "WHICH ONE IS COMPARED DEPENDS ON WHO IS IN THE COMPARISON.  The nine "
  "recorded `FLOAT:<bits>:<hex>', which is exact.  The three recorded a "
  "printed decimal, and decision 22 already reduced those to 14 "
  "significant digits because php's echo carries no more.  Rather than "
  "throw the nine's precision away globally, every float answer is "
  "given TWO tokens: `fractional:<repr>' from the bits, and "
  "`fractional:<%.14g>' as its shadow.  A comparison between two of the "
  "NINE uses the exact tokens.  A comparison with python, ruby or php "
  "on either side uses the shadows, for both sides.  WHERE PRECISION IS "
  "LOST IS COUNTED, NOT ASSUMED: `float_precision' reports how many "
  "edges fell back to the shadow and how many token pairs are equal at "
  "14 digits and unequal at full width.  NaN and the infinities keep "
  "decision 23's spellings on both sides; a signed zero decodes off its "
  "SIGN BIT here, which is stronger than decision 23's sign character "
  "and agrees with it.  `FLOAT:32' is decoded as the float32 it is and "
  "then rendered in the same way, so a float32 answer and a float64 "
  "answer meet only where the decimal rendering coincides."),
 ("35", "BOOLEANS, NULL AND THE VOIDS.  `BOOL:true'/`BOOL:false' become "
  "`truth:true'/`truth:false', which is the token decision 20 built for "
  "php's empty string.  That is the largest merge in the pass by count "
  "and it is the one with the least doubt in it.  `NULL' becomes "
  "`nothing:null', joining python's `None' and ruby's `nil' and php's "
  "`NULL'.  `UNDEFINED' and `UNIT' are NOT merged into it: javascript's "
  "undefined and rust's `()' are answers those languages distinguish "
  "from null themselves, so they become `nothing:undefined' and "
  "`nothing:unit'.  Overturnable in the loose direction by one line."),
 ("36", "TEXT BRIDGES STRAIGHT, BECAUSE DECISION 24 ALREADY CHOSE BYTES. "
  " `STR:<own len>:<utf8 bytes>:<hex>' drops both lengths and becomes "
  "`text:<hex>' -- the same lowercase hex byte token decision 24 built "
  "from python's repr and ruby's inspect.  This is the one bridge that "
  "needed no design: the nine were recorded in the target form already. "
  " The two length notions are NOT part of the token, and that is a "
  "loss with a name: a java `String` of one astral character reports "
  "length 2 and a swift `String` reports 1, and this pass cannot see "
  "the difference.  `CHAR:<hex>' is utf-8 encoded and becomes `text:' "
  "too, so java's `char' answer meets a one-character string; that IS a "
  "merge and it is counted."),
 ("37", "CONTAINERS ARE RENDERED INTO DECISION 25'S PRINTED GRAMMAR, "
  "AND MOSTLY WILL NOT MEET.  `LIST:<n>[...]' and `TUP:<n>[...]' become "
  "`sequence:[...]', `MAP:<n>[k=>v,...]' and `STRUCT:<n>[f=e,...]' "
  "become `keyed:{...}', with each element rendered from its own "
  "bridged token by the same rules the three's printers happened to "
  "use: a whole number bare, text single-quoted, `true'/`false'/`null' "
  "lowercase, spaces removed.  THIS IS THE WEAKEST BRIDGE IN THE PASS "
  "and it is labelled so rather than trusted.  python prints `True' "
  "where this renders `true' and `None' where this renders `null', so a "
  "python container answer holding a boolean or a null will NOT meet a "
  "go one that holds the same thing.  Every container token carries the "
  "flag `bridged_container' and the count of cells where a container "
  "token from the nine met a container token from the three is reported "
  "as `container_meets'.  The honest fix is a re-print, not a "
  "re-canonicalisation."),
 ("38", "OPTIONALS AND REFERENCES ARE UNWRAPPED; AN OPAQUE POINTER IS "
  "NOT.  `SOME(<enc>)' and `REF(<enc>)' unwrap to the inner token, on "
  "decision 21's reasoning -- an optional or a go interface is a HOLDER "
  "fact and the operation computed the thing inside.  `PTR' becomes "
  "`opaque:ptr', which equals only another `opaque:ptr' and carries no "
  "address, since an address is the heap and not the answer (log 032 §6 "
  "found kotlin recording one and called it a fault)."),
 ("39", "WHAT HAS NO COUNTERPART KEEPS ITS OWN KIND.  `ORD:LT|EQ|GT|UN' "
  "becomes `ord:lt' and so on and does NOT become `whole:-1', even "
  "though php's `<=>' answers `whole:-1' on the same question; c++'s "
  "`std::strong_ordering' is not an integer and saying so is the "
  "finding.  `RANGE[a,b,incl]' becomes `range:[a,b,incl]' over the "
  "bridged endpoint tokens.  `ENUM:<n>' becomes `enum:<n>'.  `OPAQUE:"
  "<hex>' is utf-8 decoded and becomes `opaque:<text>', matching "
  "decision 25's last resort."),
 ("40", "SWIFT'S CODEGEN_REFUSE ROWS ARE NOT ANSWERS AND ARE EXCLUDED "
  "WITH THEIR COUNT.  1,066 of swift's 2,618 accepted probes are "
  "refused by `swiftc' after `swiftc -typecheck' accepted them (log 032 "
  "§5).  A refused probe never reached the operation, so it has no "
  "answer, no raise and no death -- there is nothing to put in a token. "
  " They are excluded from the domain, from the input cells and from "
  "the agreement factor, and the count is carried per operation as "
  "`codegen_refuse' on the signature.  The alternative -- a "
  "`refused:' token class -- would make swift DISAGREE with every other "
  "language on 1,066 cells on the strength of an instrument fault, "
  "which is exactly the mistake log 030 decision 12 and log 031 "
  "decision 30 were written to avoid.  Excluded-with-count is the "
  "honest default and the count is what makes it overturnable."),
 ("41", "THE VALUE-CLASS VOCABULARY CHECK OF DECISION 18 IS RE-RUN OVER "
  "ALL TWELVE AND IT PASSES AS A CONTAINMENT, NOT AS AN EQUALITY.  Each "
  "of the nine uses a SUBSET of the three's per-form value classes "
  "-- go has no `sequence|bigint' holder and no `nesting' form at all "
  "-- and no language invents a class name the others do not have.  "
  "That is the condition decision 18 actually needs: an input cell "
  "means the same input wherever it exists.  The check is reported as "
  "`value_class_vocabulary_contained' with the per-language difference, "
  "and a FAILURE would mean the cross-language shared-cell counts are "
  "meaningless rather than merely small."),
 ("42", "THE PRE-BRIDGE FORM IS KEPT FOR EVERY TOKEN AND THE BRIDGE IS "
  "COUNTED AS A MERGE TABLE OF ITS OWN.  `answer_alphabet' holds, per "
  "language, canonical token -> pre-canonical raw -> count, exactly as "
  "log 031 built it; for the nine the raw is the string "
  "`<TYPE>|<ENCODING>:<PAYLOAD>' so no bit is discarded on the way in.  "
  "`bridge_merges' lists every canonical token reached from BOTH a "
  "printed pre-form and a bit pre-form, with both spellings and both "
  "counts, so the exact set of places the two encodings were made to "
  "meet is a table and not a claim."),
]

RE_RANGE = re.compile(r"^RANGE\[(.*),(incl|excl)\]$")


def _split_top(s):
    """split on commas not inside brackets/parens."""
    out, depth, cur = [], 0, []
    for ch in s:
        if ch in "[(":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == "," and depth == 0:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if cur or out:
        out.append("".join(cur))
    return out


def _float_tokens(bits, width):
    """DECISION 34.  -> (exact token, 14-digit shadow token)."""
    import struct
    if width == 32:
        f = struct.unpack(">f", bytes.fromhex(bits))[0]
    else:
        f = struct.unpack(">d", bytes.fromhex(bits))[0]
    if f != f:
        return "fractional:nan", "fractional:nan"
    if f in (float("inf"), float("-inf")):
        t = "fractional:-inf" if f < 0 else "fractional:inf"
        return t, t
    if f == 0.0:
        neg = int(bits[0], 16) >= 8            # the SIGN BIT, decision 34
        t = "fractional:-0.0" if neg else "fractional:0.0"
        return t, t
    return "fractional:%r" % f, "fractional:%.14g" % f


def _dec128(hexs):
    """c# decimal: lo, mid, hi, flags -- each little-endian 4 bytes."""
    b = bytes.fromhex(hexs)
    if len(b) != 16:
        return None
    lo = int.from_bytes(b[0:4], "big")
    mid = int.from_bytes(b[4:8], "big")
    hi = int.from_bytes(b[8:12], "big")
    fl = int.from_bytes(b[12:16], "big")
    mag = lo | (mid << 32) | (hi << 64)
    scale = (fl >> 16) & 0xFF
    neg = bool(fl >> 31)
    if scale == 0:
        v = -mag if neg else mag
        return "whole", str(v)
    from decimal import Decimal
    d = Decimal(mag).scaleb(-scale)
    if neg:
        d = -d
    if d == d.to_integral_value():
        return "whole", str(int(d))
    return "fractional", "%.14g" % float(d)


def bridge(enc):
    """DECISIONS 33 to 39.  bit encoding string -> (exact, shadow).

    Both returns are canonical tokens in the SAME space decisions 20 to
    25 built.  They differ only for floats (decision 34).
    """
    t = _bridge1(enc)
    return t


def _render(tok):
    """DECISION 37.  a bridged token -> its element rendering."""
    kind, _, val = tok.partition(":")
    if kind == "whole" or kind == "fractional":
        return val
    if kind == "truth":
        return val
    if kind == "nothing":
        return "null" if val == "null" else val
    if kind == "text":
        try:
            return "'%s'" % bytes.fromhex(val).decode("utf-8")
        except Exception:
            return "'%s'" % val
    if kind in ("sequence", "keyed"):
        return val
    return tok


def _bridge1(enc, shadow=False):
    """-> (exact token, shadow token)."""
    if enc == "NULL":
        return "nothing:null", "nothing:null"
    if enc == "UNDEFINED":
        return "nothing:undefined", "nothing:undefined"
    if enc == "UNIT":
        return "nothing:unit", "nothing:unit"
    if enc == "PTR":
        return "opaque:ptr", "opaque:ptr"
    if enc.startswith("BOOL:"):
        v = enc[5:]
        t = "truth:true" if v == "true" else "truth:false"
        return t, t
    if enc.startswith("INT:") or enc.startswith("UINT:"):
        u = enc.startswith("UINT:")
        _, w, h = enc.split(":", 2)
        n = int.from_bytes(bytes.fromhex(h), "big", signed=not u)
        t = "whole:%d" % n
        return t, t
    if enc.startswith("BIGINT:"):
        h = enc[7:]
        try:
            if h[:1] == "-":
                n = -int(h[1:], 16)
            else:
                n = int.from_bytes(bytes.fromhex(h), "big", signed=True)
        except Exception:
            return "opaque:" + enc, "opaque:" + enc
        t = "whole:%d" % n
        return t, t
    if enc.startswith("FLOAT:"):
        _, w, h = enc.split(":", 2)
        return _float_tokens(h, int(w))
    if enc.startswith("DEC128:"):
        r = _dec128(enc[7:])
        if r:
            t = "%s:%s" % r
            return t, t
        return "opaque:" + enc, "opaque:" + enc
    if enc.startswith("CHAR:"):                      # DECISION 36
        try:
            cp = int(enc[5:], 16)
            t = "text:" + chr(cp).encode("utf-8").hex()
        except Exception:
            t = "opaque:" + enc
        return t, t
    if enc.startswith("STR:"):                       # DECISION 36
        parts = enc.split(":", 3)
        t = "text:" + (parts[3] if len(parts) > 3 else "")
        return t, t
    if enc.startswith("ORD:"):                       # DECISION 39
        t = "ord:" + enc[4:].lower()
        return t, t
    if enc.startswith("ENUM:"):
        t = "enum:" + enc[5:]
        return t, t
    if enc.startswith("OPAQUE:"):                    # DECISION 39
        try:
            s = bytes.fromhex(enc[7:]).decode("utf-8", "replace")
        except Exception:
            s = enc[7:]
        t = "opaque:" + s
        return t, t
    if enc.startswith("SOME(") and enc.endswith(")"):    # DECISION 38
        return _bridge1(enc[5:-1])
    if enc.startswith("REF(") and enc.endswith(")"):
        return _bridge1(enc[4:-1])
    m = RE_RANGE.match(enc)                          # DECISION 39
    if m:
        parts = _split_top(m.group(1))
        if len(parts) == 2:
            a = _bridge1(parts[0])
            b = _bridge1(parts[1])
            return ("range:[%s,%s,%s]" % (a[0], b[0], m.group(2)),
                    "range:[%s,%s,%s]" % (a[1], b[1], m.group(2)))
        return "opaque:" + enc, "opaque:" + enc
    for head, kind, op, cl in (("LIST:", "sequence", "[", "]"),
                               ("TUP:", "sequence", "[", "]"),
                               ("MAP:", "keyed", "{", "}"),
                               ("STRUCT:", "keyed", "{", "}")):
        if enc.startswith(head):                     # DECISION 37
            body = enc[len(head):]
            i = body.find("[")
            if i < 0 or not body.endswith("]"):
                return "opaque:" + enc, "opaque:" + enc
            inner = body[i + 1:-1]
            outs = [[], []]
            for part in (_split_top(inner) if inner else []):
                if kind == "keyed":
                    sep = "=>" if "=>" in part else "="
                    k, _, v = part.partition(sep)
                    ka, ks = _bridge1(k)
                    va, vs = _bridge1(v)
                    outs[0].append("%s:%s" % (_render(ka), _render(va)))
                    outs[1].append("%s:%s" % (_render(ks), _render(vs)))
                else:
                    ea, es = _bridge1(part)
                    outs[0].append(_render(ea))
                    outs[1].append(_render(es))
            return tuple("%s:%s%s%s" % (kind, op, ",".join(o), cl)
                         for o in outs)
    return "opaque:" + enc, "opaque:" + enc


def bridge_row(r):
    """DECISIONS 31, 33-40.  an answers_<lang>.json row -> (exact,
    shadow, raw pre-bridge string) or None where the row is not an
    answer class at all."""
    o = r["outcome"]
    if o == "answer":
        res = r["result"]
        enc = res["encoding"]
        if res.get("payload", "") != "":
            enc = enc + ":" + res["payload"]
        a, s = _bridge1(enc)
        return a, s, "%s|%s" % (res["type"], enc)
    if o == "raise":                                 # DECISION 31
        t = "raise:" + r["raise"].strip()
        return t, t, "RAISE:" + r["raise"].strip()
    if o == "death":                                 # DECISION 31
        t = "death:" + r["death"].strip()
        return t, t, "DEATH:" + r["death"].strip()
    return None                                      # DECISION 40


def canon_pair(raw):
    """the THREE's printed answer -> (exact, shadow).

    Both are the same token: decision 22 already reduced these to 14
    significant digits, so a print-grain language has no exact form to
    offer.  Returning the pair keeps one comparison path for all twelve.
    """
    t = canonicalise(raw)
    return t, t


if __name__ == "__main__":
    main()
