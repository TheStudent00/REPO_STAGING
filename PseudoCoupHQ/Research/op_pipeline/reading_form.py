#!/usr/bin/env python3
"""reading_form.py -- renders the reading-form second column for every
instruction of every unit, per SPEC_reading_form.md.

Consumes, for every language in ("c", "cpp", "go", "rust", "swift"):
  - op_units_{lang}.json      -- every unit that has a `ship` block
  - canon2_units_{lang}.json  -- every unit whose `derived_text` field
                                  is present AND is a non-empty list of
                                  instruction strings (a pipeline note
                                  string like "not derived this slice: ..."
                                  is NOT instruction text and does not
                                  qualify)

Reuses canon.py's exact instruction parser (parse/registers_in/
is_plain_register) and its register family/width tables, imported
directly rather than re-implemented.

Writes reading_units_{lang}.json for each language, plus
reading_sample.txt.  Never touches an existing pipeline artifact.
"""

import datetime
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon  # noqa: E402  (reused per task instructions)

LANGS = ["c", "cpp", "go", "rust", "swift"]

REG = canon.REG
GP_NAMES = canon.GP_NAMES
FAMILY_OF = canon.FAMILY_OF
WIDTH_OF = canon.WIDTH_OF


# --------------------------------------------------------------- errors

class Unsupported(Exception):
    """raised with the offending mnemonic when no template applies."""

    def __init__(self, mnem):
        Exception.__init__(self, mnem)
        self.mnem = mnem


# ---------------------------------------------------------- flag names

FLAG_NAME = {
    "e": "equal", "ne": "not_equal",
    "l": "signed_less", "le": "signed_less_equal",
    "g": "signed_greater", "ge": "signed_greater_equal",
    "b": "below", "be": "below_equal",
    "a": "above", "ae": "above_equal",
    "s": "sign", "ns": "not_sign",
    "p": "nan", "np": "not_nan",
    "o": "overflow",
}

SETCC_MNEM = set("set" + k for k in FLAG_NAME)
JCC_MNEM = set("j" + k for k in FLAG_NAME)
CMOVCC_MNEM = set("cmov" + k for k in FLAG_NAME)

# exact widening-move mnemonics the spec's movzbl/movslq rows generalize
# to -- mechanical width analogs of the same instruction shape, not new
# semantics.
ZERO_EXTEND_MNEM = set(["movzbl", "movzwl", "movzbq", "movzwq"])
SIGN_EXTEND_MNEM = set(["movsbl", "movsbq", "movswl", "movswq",
                         "movslq", "movsxd"])

PLAIN_MOVE_MNEM = set(["mov", "movq", "movd", "movb", "movw",
                        "movss", "movsd", "movaps", "movapd"])

NOP_MNEM = set(["nop", "nopl", "nopw"])

# templateless per spec -- the trio note (punpckldq/unpckhpd/subpd) is
# documentary prose, not a reading-line formula; see final report.
NO_TEMPLATE_NOTE_ONLY = set(["punpckldq", "unpckhpd", "subpd"])


# --------------------------------------------------------- lea parsing

LEA_ADDR = re.compile(
    r"^(?P<disp>-?0x[0-9a-fA-F]+)?\((?P<base>%[a-z0-9]+)"
    r"(?:,(?P<index>%[a-z0-9]+),(?P<scale>\d+))?\)$"
)


def render_lea(src, dst):
    if "%rip" in src:
        raise Unsupported("lea(rip-relative)")
    m = LEA_ADDR.match(src)
    if m is None:
        raise Unsupported("lea(unparsed-address:%s)" % src)
    disp = m.group("disp")
    base = m.group("base")
    index = m.group("index")
    scale = m.group("scale")
    terms = [base]
    if index is not None:
        if scale == "1":
            terms.append(index)
        else:
            terms.append("%s*%s" % (index, scale))
    if disp is not None:
        if disp.startswith("-"):
            terms.append("- " + disp[1:])
        else:
            terms.append("+ " + disp)
        # first two terms joined with "+", trailing disp term already
        # carries its own sign
        head = " + ".join(terms[:-1])
        return "%s = %s %s" % (dst, head, terms[-1])
    return "%s = %s" % (dst, " + ".join(terms))


# ------------------------------------------------------- register width

def family_of_operand(op):
    if not op.startswith("%"):
        return None
    name = op[1:]
    return FAMILY_OF.get(name)


def width_index_of(op):
    if not op.startswith("%"):
        return None
    name = op[1:]
    return WIDTH_OF.get(name)


def widen(family, width_index):
    """spell `family` (e.g. 'rax') at `width_index` (0=64bit .. 3=8bit),
    default to full width if unknown."""
    if family not in GP_NAMES:
        return "%" + family  # vector register, no width variants
    if width_index is None:
        width_index = 0
    names = GP_NAMES[family]
    if width_index >= len(names):
        width_index = 0
    return "%" + names[width_index]


# --------------------------------------------------------- instruction

def render_instruction(mnem, operands, ret_register, refuse_ret_bare_ok):
    """-> reading line string, or raises Unsupported(mnem)."""

    # ---- hidden-operand family ------------------------------------
    if mnem == "cltd":
        return "%edx = sign_bits(%eax)"
    if mnem == "cqto":
        return "%rdx = sign_bits(%rax)"

    if mnem in ("idiv", "div"):
        s = operands[0]
        w = width_index_of(s)
        if w is None:
            w = 1  # default 32-bit, documented assumption
        acc = widen("rax", w)
        dx = widen("rdx", w)
        fn = "sdiv" if mnem == "idiv" else "udiv"
        return "%s, %s = %s(join(%s, %s), %s)" % (acc, dx, fn, dx, acc, s)

    if mnem in ("imul", "mul") and len(operands) == 1:
        s = operands[0]
        w = width_index_of(s)
        if w is None:
            w = 1
        acc = widen("rax", w)
        dx = widen("rdx", w)
        fn = "smul" if mnem == "imul" else "umul"
        return "%s, %s = %s(%s, %s)" % (acc, dx, fn, acc, s)

    if mnem == "imul" and len(operands) == 2:
        s, d = operands[0], operands[1]
        return "%s = %s * %s" % (d, d, s)

    if mnem == "imul" and len(operands) == 3:
        raise Unsupported("imul(3-operand)")

    if mnem == "sbb":
        s, d = operands[0], operands[1]
        return "%s = %s - %s - flags.carry" % (d, d, s)

    if mnem in ("shl", "shr", "sar"):
        s, d = operands[0], operands[1]
        fn = {"shl": "shift_left", "shr": "shift_right_zeros",
              "sar": "shift_right_sign"}[mnem]
        return "%s = %s(%s, %s)" % (d, fn, d, s)

    if mnem in ("ret", "retq"):
        if ret_register is None:
            return "return"
        return "return %s" % ret_register

    if mnem in ("call", "callq"):
        f = operands[0]
        return "call %s()" % f

    # ---- moves and widening ----------------------------------------
    if mnem == "movabs":
        s, d = operands[0], operands[1]
        return "%s = %s" % (d, s)

    if mnem in ZERO_EXTEND_MNEM:
        s, d = operands[0], operands[1]
        return "%s = zero_extend(%s)" % (d, s)

    if mnem in SIGN_EXTEND_MNEM:
        s, d = operands[0], operands[1]
        return "%s = sign_extend(%s)" % (d, s)

    if mnem in PLAIN_MOVE_MNEM:
        s, d = operands[0], operands[1]
        return "%s = %s" % (d, s)

    if mnem in ("lea", "leaq", "leal"):
        s, d = operands[0], operands[1]
        return render_lea(s, d)

    if mnem in ("push", "pushq"):
        s = operands[0]
        return "push(%s)" % s

    if mnem in ("pop", "popq"):
        d = operands[0]
        return "%s = pop()" % d

    if mnem in NOP_MNEM:
        return "# nothing"

    # ---- integer arithmetic / bit work ------------------------------
    if mnem in ("add", "sub"):
        s, d = operands[0], operands[1]
        op = "+" if mnem == "add" else "-"
        return "%s = %s %s %s" % (d, d, op, s)

    if mnem == "neg":
        d = operands[0]
        return "%s = -%s" % (d, d)

    if mnem in ("and", "or", "xor"):
        s, d = operands[0], operands[1]
        op = {"and": "&", "or": "|", "xor": "^"}[mnem]
        return "%s = %s %s %s" % (d, d, op, s)

    if mnem == "not":
        d = operands[0]
        return "%s = ~%s" % (d, d)

    # ---- flags: writers ----------------------------------------------
    if mnem == "cmp":
        s, d = operands[0], operands[1]
        return "flags = compare(%s, %s)" % (d, s)

    if mnem == "test":
        s, d = operands[0], operands[1]
        return "flags = bit_compare(%s, %s)" % (d, s)

    if mnem == "ucomiss":
        s, d = operands[0], operands[1]
        return "flags = fcompare_f32(%s, %s)" % (d, s)

    if mnem == "ucomisd":
        s, d = operands[0], operands[1]
        return "flags = fcompare_f64(%s, %s)" % (d, s)

    # ---- flags: readers ------------------------------------------------
    if mnem in SETCC_MNEM:
        suffix = mnem[3:]
        d = operands[0]
        return "%s = flags.%s" % (d, FLAG_NAME[suffix])

    if mnem in JCC_MNEM:
        suffix = mnem[1:]
        target = operands[0]
        return "if flags.%s: goto %s" % (FLAG_NAME[suffix], target)

    if mnem in ("jmp", "jmpq"):
        target = operands[0]
        return "goto %s" % target

    if mnem in CMOVCC_MNEM:
        suffix = mnem[4:]
        s, d = operands[0], operands[1]
        return "%s = %s if flags.%s else %s" % (d, s, FLAG_NAME[suffix], d)

    # ---- floats --------------------------------------------------------
    if mnem in ("addss", "addsd", "subss", "subsd", "mulss", "mulsd",
                "divss", "divsd"):
        s, d = operands[0], operands[1]
        op = {"add": "+", "sub": "-", "mul": "*", "div": "/"}[mnem[:3]]
        return "%s = %s %s %s" % (d, d, op, s)

    if mnem in ("cvtsi2ss", "cvtsi2sd"):
        s, d = operands[0], operands[1]
        fn = "int_to_f32" if mnem == "cvtsi2ss" else "int_to_f64"
        return "%s = %s(%s)" % (d, fn, s)

    if mnem == "cvtss2sd":
        s, d = operands[0], operands[1]
        return "%s = f32_to_f64(%s)" % (d, s)

    if mnem in ("xorps", "xorpd"):
        s, d = operands[0], operands[1]
        if s == d:
            return "zero %s" % d
        return "%s = %s ^ %s" % (d, d, s)

    if mnem in ("andps", "andpd"):
        s, d = operands[0], operands[1]
        return "%s = %s & %s" % (d, d, s)

    if mnem in ("orps", "orpd"):
        s, d = operands[0], operands[1]
        return "%s = %s | %s" % (d, d, s)

    if mnem == "pxor":
        s, d = operands[0], operands[1]
        return "%s = %s ^ %s" % (d, d, s)

    if mnem in ("cmpeqss", "cmpeqsd", "cmpneqss", "cmpneqsd"):
        s, d = operands[0], operands[1]
        eq = "eq" in mnem
        width = "f32" if mnem.endswith("ss") else "f64"
        fn = ("mask_equal_" if eq else "mask_unequal_") + width
        return "%s = %s(%s, %s)" % (d, fn, d, s)

    if mnem in NO_TEMPLATE_NOTE_ONLY:
        # SPEC_reading_form.md names this trio only in a descriptive
        # note ("rendered individually, with a note that this trio is
        # the standard unsigned-64-to-float conversion") and gives no
        # actual reading-line formula for punpckldq/unpckhpd/subpd.
        # Per "no guessing", refused rather than invented.
        raise Unsupported(mnem)

    # ---- ending --------------------------------------------------------
    if mnem == "ud2":
        return "trap()"

    raise Unsupported(mnem)


def render_unit_instructions(instr_texts, ret_register):
    """-> (reading_lines or None, refusal or None)."""
    lines = []
    for text in instr_texts:
        mnem, operands = canon.parse(text)
        try:
            line = render_instruction(mnem, operands, ret_register, True)
        except Unsupported as e:
            return None, e.mnem
        lines.append(line)
    assert len(lines) == len(instr_texts), (
        "1:1 length invariant violated: %d instructions, %d reading "
        "lines" % (len(instr_texts), len(lines)))
    return lines, None


# ------------------------------------------------ result-register lookup

def find_ret_spelling(family, instr_texts, ret_index):
    """search backward from `ret_index` (exclusive) for the last mention
    of a register in `family`'s width family; fall back to full width."""
    if family.startswith("xmm") or family.startswith("ymm"):
        wanted = set([family])
        for i in range(ret_index - 1, -1, -1):
            for name in REG.findall(instr_texts[i]):
                if name == family:
                    return "%" + family
        return "%" + family
    names = set(canon.GP_NAMES.get(family, [family]))
    for i in range(ret_index - 1, -1, -1):
        for name in REG.findall(instr_texts[i]):
            if name in names:
                return "%" + name
    return "%" + canon.GP_NAMES.get(family, [family])[0]


def resolve_result_register(lang, n, instr_texts, canon_units, canon2_units):
    """priority: (1) unit's own result_register field -- not present
    anywhere in op_units/canon2_units per inspection of the actual JSON,
    so this step is a no-op by data shape, kept for documentation;
    (2) canon_units_{lang}.json result_register by unit id;
    (3) canon2_units_{lang}.json entry_contract.result by unit id;
    (4) sem_anchored data -- inspected, carries no result-register field,
    so unreachable in practice, kept as a defined-but-empty step.
    -> (spelling_or_None, source_string, reason_if_none)"""
    family = None
    source = None

    cu = canon_units.get(n) if canon_units else None
    if cu is not None and cu.get("result_register"):
        family = cu["result_register"]
        source = "canon_units_%s.json result_register" % lang

    if family is None:
        c2 = canon2_units.get(n) if canon2_units else None
        if c2 is not None:
            ec = c2.get("entry_contract") or {}
            if ec.get("result"):
                family = ec["result"]
                source = "canon2_units_%s.json entry_contract.result" % lang

    if family is None:
        return None, None, ("no result_register found in canon_units, "
                             "canon2_units entry_contract, or "
                             "sem_anchored data for this unit id")

    ret_indices = [i for i, t in enumerate(instr_texts)
                   if t.strip().split(None, 1)[0] in ("ret", "retq")]
    if not ret_indices:
        return None, source, "unit has no ret instruction"
    spelling = find_ret_spelling(family, instr_texts, ret_indices[0])
    return spelling, source, None


# --------------------------------------------------------------- loading

def load_json(name):
    path = os.path.join(HERE, name)
    with open(path) as f:
        return json.load(f)


def load_lang_sources(lang):
    op_units = load_json("op_units_%s.json" % lang)
    canon_units = load_json("canon_units_%s.json" % lang)["units"]
    canon2_units = load_json("canon2_units_%s.json" % lang)["units"]
    return op_units, canon_units, canon2_units


# ------------------------------------------------------------- rendering

def build_unit_record(lang, n, unit_id, instr_texts, source_kind,
                       canon_units, canon2_units, all_refused_mnem,
                       refusal_counter):
    instr_texts = [t for t in instr_texts if t.strip()]

    ret_register, ret_source, ret_reason = resolve_result_register(
        lang, n, instr_texts, canon_units, canon2_units)

    reading_lines, bad_mnem = render_unit_instructions(
        instr_texts, ret_register)

    rec = {
        "lang": lang,
        "unit": unit_id,
        "source": source_kind,
        "instructions": instr_texts,
        "reading": reading_lines,
        "result_register": ret_register,
        "result_register_source": ret_source,
        "result_register_reason": ret_reason,
        "refusal": None,
    }

    if reading_lines is None:
        refusal_counter[0] += 1
        all_refused_mnem.add(bad_mnem)
        rec["refusal"] = {
            "mnemonic": bad_mnem,
            "reason": "no reading-form template defined in "
                      "SPEC_reading_form.md for mnemonic %r" % bad_mnem,
        }
    else:
        assert len(rec["instructions"]) == len(rec["reading"])

    return rec


def process_language(lang, all_refused_mnem, refusal_counter, per_lang_stats):
    op_units, canon_units, canon2_units = load_lang_sources(lang)
    probes = op_units["probes"]

    units = []

    # source 1: op_units ship builds -- every unit with a ship block
    for n, v in probes.items():
        if "ship" not in v:
            continue
        symbol = v["meta"]["symbol"]  # e.g. "op_246"
        unit_id = "%s/%s" % (lang, symbol)
        instr_texts = v["ship"]["mnem"]
        rec = build_unit_record(lang, n, unit_id, instr_texts, "op_units",
                                 canon_units, canon2_units,
                                 all_refused_mnem, refusal_counter)
        units.append(rec)

    # source 2: canon2_units derived_text -- only where it is a real,
    # non-empty list of instruction strings (a pipeline note string
    # such as "not derived this slice: ..." is not instruction text)
    for n, v in canon2_units.items():
        dt = v.get("derived_text")
        if not isinstance(dt, list) or not dt:
            continue
        symbol = "op_%s" % n
        unit_id = "%s/%s/canon2_derived" % (lang, symbol)
        rec = build_unit_record(lang, n, unit_id, dt, "canon2_derived_text",
                                 canon_units, canon2_units,
                                 all_refused_mnem, refusal_counter)
        units.append(rec)

    ok = sum(1 for u in units if u["reading"] is not None)
    refused = sum(1 for u in units if u["reading"] is None)
    per_lang_stats[lang] = {
        "total": len(units),
        "rendered_ok": ok,
        "refused": refused,
        "refused_mnemonics": sorted(set(
            u["refusal"]["mnemonic"] for u in units if u["refusal"])),
    }
    return units


def write_lang_output(lang, units, stats):
    out = {
        "meta": {
            "role": "generator provenance",
            "generator": "reading_form.py",
            "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
            "source_files": [
                "op_units_%s.json" % lang,
                "canon_units_%s.json" % lang,
                "canon2_units_%s.json" % lang,
            ],
            "spec": "SPEC_reading_form.md",
            "language": lang,
            "counts": stats,
        },
        "units": units,
    }
    path = os.path.join(HERE, "reading_units_%s.json" % lang)
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    return path


# --------------------------------------------------------------- sample

def find_unit(units, unit_id_suffix):
    for u in units:
        if u["unit"] == unit_id_suffix:
            return u
    return None


def find_by_predicate(units, pred):
    for u in units:
        if u["reading"] is None:
            continue
        joined = " ".join(u["instructions"])
        if pred(joined):
            return u
    return None


def make_sample(all_units_by_lang):
    entries = []
    notes = []

    c_units = all_units_by_lang["c"]
    swift_units = all_units_by_lang["swift"]
    go_units = all_units_by_lang["go"]

    # 1. c/op_246
    u = find_unit(c_units, "c/op_246")
    if u is None:
        notes.append("c/op_246 not found; substitute needed")
    entries.append(("c/op_246 (idiv, GLOSSARY's own example)", u))

    # 2. swift/op_150
    u = find_unit(swift_units, "swift/op_150")
    entries.append(("swift/op_150 (division)", u))

    # 3. swift/op_186
    u = find_unit(swift_units, "swift/op_186")
    entries.append(("swift/op_186 (modulo)", u))

    # 4. cmp + setl
    u = find_by_predicate(c_units, lambda j: "cmp " in j and "setl " in j)
    entries.append(("comparison: cmp + setl", u))

    # 5. ucomisd + setp + setne + or
    u = find_by_predicate(
        c_units,
        lambda j: "ucomisd " in j and "setp " in j and "setne " in j
        and "or " in j)
    entries.append(("float unordered-compare: ucomisd + setp + setne + or",
                     u))

    # 6. lea as addition (index,scale form, matches GLOSSARY example)
    u = find_unit(c_units, "c/op_102")
    entries.append(("lea as addition: c/op_102", u))

    # 7. go unit with a panic call
    u = find_by_predicate(go_units, lambda j: "call " in j and "panic" in j)
    entries.append(("go panic call", u))

    # 8. cmov
    u = find_by_predicate(c_units, lambda j: "cmov" in j)
    entries.append(("cmov", u))

    # 9. shifts
    u = find_by_predicate(
        c_units,
        lambda j: any(t.split()[0] in ("shl", "shr", "sar")
                      for t in j.split("  ")) or
        (" shl " in (" " + j) or " shr " in (" " + j) or " sar " in
         (" " + j)))
    entries.append(("shifts (shl/shr/sar)", u))

    # 10. call / stack push+pop
    # go/main.op_30 is a REFUSED unit (rip-relative lea has no reading-form
    # template) and does not actually contain push/pop/call, so it cannot
    # demonstrate this. Use go/main.op_110 instead: a short, successfully
    # rendered unit with push, pop, and call all present.
    u = find_unit(go_units, "go/main.op_110")
    if u is None:
        u = find_by_predicate(go_units, lambda j: "push " in j and "pop " in j)
    entries.append(("stack push/pop + call", u))

    # 11. movzx/movsx
    u = find_by_predicate(
        c_units, lambda j: "movzbl " in j or "movslq " in j)
    entries.append(("zero/sign extension: movzbl / movslq", u))

    # 12. sse moves
    u = find_by_predicate(
        c_units, lambda j: "movss " in j or "movsd " in j)
    entries.append(("sse scalar move", u))

    return entries, notes


def render_sample_text(entries, notes):
    lines = []
    lines.append("reading_sample.txt -- 12 hand-picked units, instruction "
                  "text | reading line, space-aligned.")
    lines.append("=" * 100)
    if notes:
        lines.append("")
        lines.append("NOTES:")
        for n in notes:
            lines.append("  - " + n)
    for i, (label, u) in enumerate(entries, 1):
        lines.append("")
        lines.append("-" * 100)
        lines.append("%d. %s" % (i, label))
        if u is None:
            lines.append("    (no matching unit found)")
            continue
        lines.append("    unit: %s   source: %s" % (u["unit"], u["source"]))
        if u["reading"] is None:
            lines.append("    REFUSED: %s" % u["refusal"])
            continue
        left_w = max(len(t) for t in u["instructions"])
        left_w = max(left_w, 10)
        for text, reading in zip(u["instructions"], u["reading"]):
            lines.append("    %-*s   %s" % (left_w, text, reading))
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- main

def main():
    all_refused_mnem = set()
    refusal_counter = [0]
    per_lang_stats = {}
    all_units_by_lang = {}
    written_files = []

    for lang in LANGS:
        units = process_language(lang, all_refused_mnem, refusal_counter,
                                  per_lang_stats)
        all_units_by_lang[lang] = units
        path = write_lang_output(lang, units, per_lang_stats[lang])
        written_files.append(path)

    entries, notes = make_sample(all_units_by_lang)
    sample_text = render_sample_text(entries, notes)
    sample_path = os.path.join(HERE, "reading_sample.txt")
    with open(sample_path, "w") as f:
        f.write(sample_text)
    written_files.append(sample_path)

    print("=== per-language stats ===")
    for lang in LANGS:
        s = per_lang_stats[lang]
        print("%s: total=%d ok=%d refused=%d refused_mnemonics=%s" % (
            lang, s["total"], s["rendered_ok"], s["refused"],
            s["refused_mnemonics"]))
    print()
    print("global refusal count: %d" % refusal_counter[0])
    print("global un-templated mnemonics: %s" % sorted(all_refused_mnem))
    print()
    print("files written:")
    for p in written_files:
        print("  " + p)

    if notes:
        print()
        print("substitution notes:")
        for n in notes:
            print("  " + n)


if __name__ == "__main__":
    main()
