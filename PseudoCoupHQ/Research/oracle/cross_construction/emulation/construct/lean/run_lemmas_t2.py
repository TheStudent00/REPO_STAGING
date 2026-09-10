#!/usr/bin/env python3
"""run_lemmas_t2.py -- THE SCHEMAS' LEMMAS, in Lean, instantiated per
width.

Node: hq.research.compiler_graph.gate.lean (the proof system) and
hq.research.arch_unit_oracle.cross_construction.autopoly (the tier).
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_t2_brief.md`.

WHAT A LEMMA HERE SAYS, in one sentence: at this width and this word,
the term the schema builds out of limbs of the word computes the same
mapping as the operation it replaces.

WHY IT IS INSTANTIATED AND NOT STATED ONCE FOR EVERY WIDTH.  The general
statement is a theorem about `BitVec w` for every `w` and its proof is an
induction over the limb count; `bv_decide` -- Lean's bit-blasting tactic,
the one this project's proof system already uses -- decides a goal at a
FIXED width and cannot be handed a variable one.  So the general lemma is
STATED in `OWED.md`, in words and in Lean syntax, and what is machine
checked here is its instance at each width the tier actually uses.  That
is what the brief asks for ("instantiated per width") and the difference
between the two is written down rather than glossed.

WHAT IS GENERATED RATHER THAN TRANSCRIBED, and it matters: the two sides
of every theorem are printed FROM `schemas.py` ITSELF -- the left is the
z3 operation, the right is `schemas.lower`'s own output on it -- and
`term_to_lean.py` translates both, with its own round-trip check.  A
lemma transcribed by hand could state something the tier does not do;
one generated from the tier cannot.

MEMORY: one `lean` process per theorem file, its wall clock and peak read
from `os.wait4`; this process holds only the rows.  Bound 6 GB, named
abort ABORT_MEMORY_T2.

usage:
  run_lemmas_t2.py instances          the (schema, width, word) rows the
                                      refused population needs, off the
                                      bank -- and nothing run
  run_lemmas_t2.py prove [<seconds>]  the theorems generated and run
  run_lemmas_t2.py table              what `lemmas_t2.json` holds

Coding discipline: no compound one-liner statements.
"""

import json
import os
import resource
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CONSTRUCT = os.path.normpath(os.path.join(HERE, ".."))
EMULATION = os.path.normpath(os.path.join(CONSTRUCT, ".."))
OP = os.path.normpath(os.path.join(EMULATION, "..", "..", "..",
                                   "op_pipeline"))
LEAN = os.path.join(OP, "lean")
sys.path.insert(0, CONSTRUCT)
sys.path.insert(0, LEAN)
sys.path.insert(0, OP)

import z3                                                        # noqa: E402
import schemas as S                                              # noqa: E402
import term_to_lean                                              # noqa: E402

OUT = os.path.join(HERE, "lemmas_t2.json")
ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_T2"
PER_THEOREM_SECONDS = 600

STATEMENT_CEILING = 200000
"""how large a term may be to be STATED as a theorem, counted written
out.  It is the tier's own ceiling (`construct.UNFOLDED_CEILING`) and
for the same reason: a printed term names no intermediate."""


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_memory(where):
    peak = peak_kb()
    if peak > ABORT_KB:
        raise SystemExit("%s: %d kB at %s" % (ABORT_NAME, peak, where))
    return peak


# ==================================================================
# section 1: the obligations, generated from `schemas.py` itself
# ==================================================================

def limbed_symbol(start, width, word):
    """one operand of `width` bits built out of free symbols no wider
    than the word, named `v<start>`, `v<start+1>`, ... in the order the
    printed text meets them -- which for a concatenation is the MOST
    significant first, because that is z3's own argument order."""
    count = S.limb_count(width, word)
    top = S.top_bits(width, word)
    pieces = []
    widths = {}
    index = start
    for which in range(count - 1, -1, -1):
        bits = word
        if which == count - 1:
            bits = top
        name = "v%d" % index
        pieces.append(z3.BitVec(name, bits))
        widths[name] = bits
        index = index + 1
        continue
    if count == 1:
        return pieces[0], widths, index
    return z3.Concat(*pieces), widths, index


def build_shape(shape, word):
    """one SHAPE as the z3 operation it names, over free symbols no wider
    than the word, plus those symbols' widths.

    The shape is the rewrite the lowering performed -- the operation and
    the widths and offsets that make it that rewrite -- so the theorem
    built here is about the node the tier actually replaced and not
    about a nearby one."""
    operation = shape["operation"]
    width = shape["width"]
    if operation == "concat":
        pieces = []
        widths = {}
        index = 0
        for inner in shape["widths"]:
            piece, more, index = limbed_symbol(index, inner, word)
            pieces.append(piece)
            widths.update(more)
            continue
        return z3.Concat(*pieces), widths
    left, widths, index = limbed_symbol(0, width, word)
    right, more, index = limbed_symbol(index, width, word)
    widths.update(more)
    picked = z3.BitVec("v%d" % index, word)
    widths["v%d" % index] = word
    one = z3.BitVecVal(1, 8)
    zero = z3.BitVecVal(0, 8)
    table = {
        "add": lambda: left + right,
        "sub": lambda: left - right,
        "negate": lambda: -left,
        "product": lambda: left * right,
        "shift_up": lambda: left << right,
        "shift_down_logical": lambda: z3.LShR(left, right),
        "shift_down_arithmetic": lambda: left >> right,
        "rotate_left": lambda: rotate_of(left, right, shape, True),
        "rotate_right": lambda: rotate_of(left, right, shape, False),
        "quotient_unsigned": lambda: z3.UDiv(left, right),
        "remainder_unsigned": lambda: z3.URem(left, right),
        "quotient_signed": lambda: left / right,
        "remainder_signed": lambda: z3.SRem(left, right),
        "below_unsigned": lambda: z3.If(z3.ULT(left, right), one, zero),
        "below_or_equal_unsigned":
            lambda: z3.If(z3.ULE(left, right), one, zero),
        "below_signed": lambda: z3.If(left < right, one, zero),
        "below_or_equal_signed": lambda: z3.If(left <= right, one, zero),
        "equal": lambda: z3.If(left == right, one, zero),
        "meet": lambda: left & right,
        "join_bits": lambda: left | right,
        "differ": lambda: left ^ right,
        "complement": lambda: ~left,
        "select": lambda: z3.If(picked == z3.BitVecVal(0, word), left,
                                right),
        "extract": lambda: z3.Extract(shape["high"], shape["low"], left),
        "extend_zero": lambda: z3.ZeroExt(shape["to"] - width, left),
        "extend_sign": lambda: z3.SignExt(shape["to"] - width, left),
    }
    if operation not in table:
        return None, widths
    return table[operation](), widths


def rotate_of(left, right, shape, leftward):
    if shape.get("amount") is not None:
        if leftward:
            return z3.RotateLeft(left, shape["amount"])
        return z3.RotateRight(left, shape["amount"])
    if leftward:
        return z3.RotateLeft(left, right)
    return z3.RotateRight(left, right)


LADDER_SHAPES = {
    S.ADD_SUB: ["add", "sub", "negate"],
    S.SHIFT_ROTATE: ["shift_up", "shift_down_logical",
                     "shift_down_arithmetic"],
    S.MULTIPLY: ["product"],
    S.DIVIDE: ["quotient_unsigned", "remainder_unsigned",
               "quotient_signed", "remainder_signed"],
    S.COMPARE: ["below_unsigned", "below_or_equal_unsigned",
                "below_signed", "below_or_equal_signed", "equal"],
    S.BITWISE: ["meet", "join_bits", "differ", "complement", "select"],
}
"""the shapes stated at every width of the ladder, so the schemas'
behaviour AS THE WIDTH DOUBLES is on the record.  `widening / narrowing
/ sign spread` is not here: its shapes are an extract at a pair of
OFFSETS and a concatenation of a list of WIDTHS, so a ladder of them
would be a list somebody chose -- what is stated for it is what the
population uses."""


def limb_pieces(term, word):
    """the obligations one operation carries: ONE PER LIMB.

    THIS IS THE HOLE THE FIRST DRAFT LEFT.  A theorem about the LOW WORD
    of a wide operation says nothing about the second limb, and every
    real use of a wide value reads it through an extract that may name
    any limb.  So a wide operation is stated once per limb, and the
    schema's row is proved only where every limb of every shape is."""
    if not z3.is_bv(term):
        return [(0, term)]
    width = term.size()
    if width <= word:
        return [(0, term)]
    out = []
    for index in range(S.limb_count(width, word)):
        low = word * index
        high = min(width - 1, low + word - 1)
        out.append((index, z3.Extract(high, low, term)))
        continue
    return out


PRINT_FORMS = ["simplified", "as built"]
"""THE TWO FORMS A THEOREM MAY BE STATED IN, tried in this order.

"as built" is the term exactly as `schemas.py` constructed it.
"simplified" is `z3.simplify` alone -- `term.Term.normalize`'s middle
step, WITHOUT its two ordering steps and without its positional
renaming, because the two sides of a theorem must keep one set of names
between them and z3's own printed order is the one the translator's
rebuild reproduces.

WHY THE ORDER IS THIS WAY ROUND, measured in lane `t2_l11`.  The
translator confirms its parse by REBUILDING the term in z3 and demanding
the input text back character for character, and two of the pipeline's
own print steps break that demand on these terms:
  * `order_commutative` puts a numeral LAST in an equality (`x == 0`)
    and z3's own constructor prints it FIRST (`0 == x`), so the reprint
    differs and the statement is refused -- the same commutative-order
    seam log_251 is about, met from the other side.  So the ordering
    step is not applied here, and `z3.simplify` alone is;
  * `z3.simplify` rewrites a logical shift by a constant into
    `Concat(0, Extract(...))`, whose leading numeral has no width the
    translator's unification can pin, and the statement is refused as
    WIDTH_UNRESOLVED.
Neither is a defect in the translator and neither is this file's to
change, so the term is offered AS BUILT first and the simplified form is
the fallback; the row records which form the theorem was stated in."""


def printed(term, form):
    import term as T
    if form == "as built":
        return T.one_line(term), term
    held = z3.simplify(term)
    return T.one_line(held), held


def theorem_text(name, binders, body):
    lines = ["-- generated by construct/lean/run_lemmas_t2.py from "
             "construct/schemas.py itself",
             "import Std.Tactic.BVDecide", ""]
    lines.append("theorem %s %s :" % (name, " ".join(binders)))
    lines.append("    %s := by" % body)
    lines.append("  bv_decide")
    return "\n".join(lines) + "\n"


def run_lean(path, seconds):
    started = time.time()
    process = subprocess.Popen(["lean", path], stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, cwd=HERE)
    timed_out = False
    out = b""
    try:
        out, _ = process.communicate(timeout=seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        process.terminate()
        try:
            out, _ = process.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            process.terminate()
            out, _ = process.communicate()
    wall = time.time() - started
    peak = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    return (process.returncode, out.decode("utf-8", "replace"), wall,
            peak, timed_out)


def translated(text, widths, result_width):
    """`term_to_lean.translate`, with a raise recorded as a refusal.

    Its round trip REBUILDS the parsed term in z3, and a form whose
    widths its unification does not pin makes that rebuild raise rather
    than answer.  A raise is a statement that could not be made, which
    is a refusal by cause, so it is recorded as one -- never swallowed
    and never allowed to stop the lane."""
    try:
        return term_to_lean.translate(text, widths, result_width)
    except Exception as problem:                              # noqa: BLE001
        return {"refused": ["TRANSLATOR_RAISED",
                            "%s: %s" % (type(problem).__name__, problem)],
                "lean": None}


def one_theorem(schema, shape, word, limb, posed, widths, seconds):
    """one obligation: one limb of one shape at one word, stated and
    run."""
    key = S.shape_key(shape)
    row = {"schema": schema, "width": shape["width"], "word": word,
           "shape": key, "shape_row": dict(shape), "limb": limb,
           "theorem_name": "schema_%s_%d_%d"
                           % (sanitised(key), word, limb)}
    try:
        built, _order, _instances = S.lower(posed, word)
    except S.Refused as refusal:
        row["outcome"] = "REFUSED_BY_THE_SCHEMA"
        row["cause"] = refusal.cause
        row["cause_detail"] = refusal.detail
        return row
    # THE STATEMENT IS THE UNFOLDED TERM, because a printed term names
    # no intermediate -- the same property that stops the renderer
    # writing the divider.  So the size is measured BEFORE anything
    # prints or simplifies it, and a statement beyond the ceiling is
    # recorded as owed with its measured size rather than attempted.
    size = S.unfolded_size(built, STATEMENT_CEILING)
    row["unfolded_nodes"] = size
    row["unfolded_ceiling"] = STATEMENT_CEILING
    if size >= STATEMENT_CEILING:
        row["outcome"] = "TOO_LARGE_TO_STATE"
        row["cause"] = ("the theorem's own statement is the term written "
                        "out, and this one is at or above %d nodes"
                        % STATEMENT_CEILING)
        row["cause_detail"] = ("the same property that stops the "
                               "renderer writing it: a step that reads "
                               "its own previous step more than once is "
                               "written out once per read")
        return row
    left_text = None
    right_text = None
    left = None
    right = None
    refusals = []
    for form in PRINT_FORMS:
        left_text, left_term = printed(posed, form)
        right_text, right_term = printed(built, form)
        result_width = None
        if z3.is_bv(left_term):
            result_width = left_term.size()
        left = translated(left_text, widths, result_width)
        right = translated(right_text, widths, result_width)
        row["stated_in_the_form"] = form
        if not left["refused"] and not right["refused"]:
            break
        refusals.append({"form": form,
                         "refused": left["refused"] or right["refused"]})
        continue
    row["left_text"] = left_text
    row["right_text"] = right_text
    row["forms_refused"] = refusals
    if left["refused"] or right["refused"]:
        row["outcome"] = "REFUSED_BEFORE_LEAN"
        refusal = left["refused"] or right["refused"]
        row["cause"] = refusal[0]
        row["cause_detail"] = refusal[1]
        return row
    used = set()
    import re
    for text in (left_text, right_text):
        for found in re.finditer(r"\bv[0-9]+\b", text):
            used.add(found.group(0))
            continue
        continue
    binders = []
    for symbol in sorted(used, key=lambda s: int(s[1:])):
        binders.append("(%s : BitVec %d)" % (symbol, widths[symbol]))
        continue
    body = "%s = %s" % (left["lean"], right["lean"])
    path = os.path.join(HERE, "%s.lean" % row["theorem_name"])
    handle = open(path, "w")
    handle.write(theorem_text(row["theorem_name"], binders, body))
    handle.close()
    row["lean_file"] = os.path.basename(path)
    row["theorem"] = "theorem %s %s : %s := by bv_decide" % (
        row["theorem_name"], " ".join(binders), body)
    code, output, wall, peak, timed = run_lean(path, seconds)
    row["lean_exit"] = code
    row["wall_seconds"] = round(wall, 3)
    row["children_peak_rss_kb"] = peak
    row["lean_output"] = output.strip()[:2000]
    if timed:
        row["outcome"] = "TIMED_OUT"
        row["timed_out_at_seconds"] = seconds
        return row
    if code == 0:
        row["outcome"] = "PROVED_BY_LEAN"
        return row
    row["outcome"] = "LEAN_REFUSED"
    return row


def sanitised(text):
    out = []
    for letter in text:
        if letter.isalnum():
            out.append(letter)
            continue
        out.append("_")
        continue
    return "".join(out)


# ==================================================================
# section 2: which instances the population needs
# ==================================================================

def instances_the_pass_recorded():
    """every SHAPE the tier's own lowering rewrote, read off THE PASS'S
    OWN RUN STORE.

    WHY NOT OFF THE BANK, and it is a defect this file had for one lane:
    the bank is where the pass's proofs LAND, so once a place is proved
    on the constructed route it is no longer a width-or-kind refusal and
    a plan built by re-reading the bank silently drops the very shapes
    that carried it.  The run store records what the tier lowered,
    whatever the verdict was, so it is the plan's source."""
    store = os.path.join(EMULATION, "autopoly",
                         "t2_construct_runs.jsonl")
    rows = {}
    if not os.path.exists(store):
        return rows
    handle = open(store)
    for line in handle:
        text = line.strip()
        if not text:
            continue
        run = json.loads(text)
        if run.get("route") != "constructed":
            continue
        for place in run.get("places") or []:
            block = place.get("constructed") or {}
            for row in block.get("instances") or []:
                for shape in row.get("shapes") or []:
                    key = (row["schema"], row["word"],
                           S.shape_key(shape))
                    rows[key] = {"schema": row["schema"],
                                 "word": row["word"], "shape": shape}
                    continue
                continue
            continue
        continue
    handle.close()
    return rows


def instances_the_population_needs():
    """every SHAPE the tier's own lowering reaches over the places the
    bank records a width-or-kind refusal for, UNION what the pass's own
    store recorded.

    Read off the BANK, the outer set and the store, so the lemmas proved
    are the lemmas the population needs and not a list somebody chose."""
    sys.path.insert(0, os.path.join(EMULATION, "handful"))
    sys.path.insert(0, os.path.join(EMULATION, "autopoly"))
    import autopoly as AP
    import handful as H
    import construct as CONS
    MARKS = ["has no ", "is not spelled by this renderer",
             "a width c has no holder for",
             "answer home or arrival on the x87 stack",
             "operator not covered by the renderer"]
    bank = os.path.join(EMULATION, "autopoly", "certificates.jsonl")
    want = {}
    handle = open(bank)
    for line in handle:
        text = line.strip()
        if not text:
            continue
        cert = json.loads(text)
        if not cert.get("preferred"):
            continue
        if cert["target"] not in ("c", "cpp", "rust", "go", "swift"):
            continue
        if cert["kind"] != "refused":
            continue
        cause = cert.get("cause") or ""
        held = False
        for mark in MARKS:
            if mark in cause:
                held = True
                break
            continue
        if not held:
            continue
        key = (cert["cell"]["mnem"], cert["cell"]["shape"],
               cert["cell"]["key_width"])
        want.setdefault(key, set()).add(cert["target"])
        continue
    handle.close()
    cells = json.load(open(AP.CELLS))
    rows = {}
    for key in sorted(want):
        held = H.cell_input(cells, key)
        if held.get("refusal_cause") is not None:
            continue
        for target in sorted(want[key]):
            word = CONS.word_of(target)
            for place in held.get("places") or []:
                term = place.get("term")
                if term is None:
                    continue
                try:
                    _built, _order, instances = S.lower(term, word)
                except S.Refused:
                    continue
                for row in instances:
                    for shape in row["shapes"]:
                        key = (row["schema"], row["word"],
                               S.shape_key(shape))
                        rows[key] = {"schema": row["schema"],
                                     "word": row["word"],
                                     "shape": shape}
                        continue
                    continue
                continue
            continue
        continue
    for key, entry in instances_the_pass_recorded().items():
        rows[key] = entry
        continue
    return rows


# ==================================================================
# section 3: the commands
# ==================================================================

def instances_command():
    rows = instances_the_population_needs()
    say("| schema | word | the SHAPE the lowering rewrote |")
    say("|---|---|---|")
    for key in sorted(rows, key=lambda k: (k[0], k[1], k[2])):
        say("| %s | %d | `%s` |" % (key[0], key[1], key[2]))
        continue
    say("")
    say("distinct (schema, word, shape) instances: %d" % len(rows))
    say("peak resident: %d kB" % check_memory("instances"))
    return 0


LADDER = [(16, 8), (32, 16), (64, 32), (65, 64), (128, 64)]
"""the widths this task's lemmas are instantiated at.

THE LADDER IS THE SCHEMAS' OWN SHAPE: each row is a width built from two
of half that width, which is the composition the general lemma is an
induction over, and (65, 64) and (96, 64) are the two widths the outer
set's own places actually carry beside the doubling."""


def prove_command(seconds):
    plan = []
    seen = set()
    for width, word in LADDER:
        for schema in S.SCHEMA_ORDER:
            if schema not in LADDER_SHAPES:
                continue
            for operation in LADDER_SHAPES[schema]:
                shape = {"operation": operation, "width": width}
                key = (schema, word, S.shape_key(shape))
                if key in seen:
                    continue
                seen.add(key)
                plan.append({"schema": schema, "word": word,
                             "shape": shape})
                continue
            continue
        continue
    needed = instances_the_population_needs()
    added = 0
    for key in sorted(needed, key=lambda k: (k[0], k[1], k[2])):
        if key in seen:
            continue
        seen.add(key)
        plan.append(needed[key])
        added = added + 1
        continue
    say("the ladder: %s"
        % ", ".join("%d over %d" % pair for pair in LADDER))
    say("shapes from the ladder: %d; shapes the refused population "
        "needs and the ladder does not carry: %d; obligations to state: "
        "one per LIMB of each" % (len(plan) - added, added))
    say("")
    rows = []
    index = 0
    for entry in plan:
        shape = entry["shape"]
        word = entry["word"]
        left, widths = build_shape(shape, word)
        if left is None:
            rows.append({"schema": entry["schema"],
                         "width": shape["width"], "word": word,
                         "shape": S.shape_key(shape), "limb": 0,
                         "shape_row": dict(shape),
                         "theorem_name": None,
                         "outcome": "NO_BUILDER_FOR_THIS_SHAPE",
                         "cause": "this file states no operation for "
                                  "the shape %s" % S.shape_key(shape)})
            continue
        for limb, posed in limb_pieces(left, word):
            index = index + 1
            say("[%d] %s at %d over %d, limb %d: %s"
                % (index, entry["schema"], shape["width"], word, limb,
                   S.shape_key(shape)))
            row = one_theorem(entry["schema"], shape, word, limb, posed,
                              widths, seconds)
            rows.append(row)
            say("    %s in %s s" % (row["outcome"],
                                    row.get("wall_seconds")))
            check_memory("%s limb %d" % (S.shape_key(shape), limb))
            continue
        continue
    collapsed = collapse(rows)
    document = {
        "meta": {
            "written_by": "construct/lean/run_lemmas_t2.py prove",
            "per_theorem_seconds": seconds,
            "what": "one Lean theorem per LIMB of each SHAPE at each "
                    "word; a shape's row is PROVED_BY_LEAN only where "
                    "every limb of it is",
            "toolchain": toolchain(),
        },
        "theorems": rows,
        "rows": collapsed,
    }
    handle = open(OUT, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    report(rows, collapsed)
    say("")
    say("peak resident: %d kB" % peak_kb())
    return 0


def collapse(rows):
    """one row per (schema, width, word, SHAPE): PROVED_BY_LEAN only
    where every LIMB of that shape proved, so a term that reads any limb
    of it is covered."""
    held = {}
    for row in rows:
        key = (row["schema"], row["width"], row["word"], row["shape"])
        entry = held.get(key)
        if entry is None:
            entry = {"schema": row["schema"], "width": row["width"],
                     "word": row["word"], "shape": row["shape"],
                     "shape_row": row.get("shape_row"),
                     "limbs": [], "outcome": "PROVED_BY_LEAN",
                     "theorem_name": row.get("theorem_name"),
                     "seconds": 0.0}
            held[key] = entry
        entry["limbs"].append({"limb": row["limb"],
                               "outcome": row["outcome"],
                               "theorem": row.get("theorem_name")})
        entry["seconds"] = round(entry["seconds"]
                                 + (row.get("wall_seconds") or 0.0), 3)
        if row["outcome"] != "PROVED_BY_LEAN":
            entry["outcome"] = row["outcome"]
        continue
    out = []
    for key in sorted(held, key=lambda k: (k[0], k[1], k[2], k[3])):
        out.append(held[key])
        continue
    return out


def toolchain():
    try:
        answer = subprocess.run(["lean", "--version"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=60)
        return answer.stdout.decode("utf-8", "replace").strip()
    except Exception as problem:                              # noqa: BLE001
        return "lean --version raised %s" % problem


def report(rows, collapsed):
    say("")
    say("| schema | width | word | the shape | the shape's row | limbs "
        "| s |")
    say("|---|---|---|---|---|---|---|")
    for entry in collapsed:
        pieces = []
        for one in entry["limbs"]:
            pieces.append("%d %s" % (one["limb"], one["outcome"]))
            continue
        say("| %s | %s | %s | `%s` | %s | %s | %s |"
            % (entry["schema"], entry["width"], entry["word"],
               entry["shape"], entry["outcome"], "; ".join(pieces),
               entry["seconds"]))
        continue
    say("")
    tally = {}
    for row in rows:
        tally[row["outcome"]] = tally.get(row["outcome"], 0) + 1
        continue
    say("| outcome | theorems |")
    say("|---|---|")
    for outcome in sorted(tally):
        say("| %s | %d |" % (outcome, tally[outcome]))
        continue
    say("")
    say("the theorems that did not prove, LITERAL:")
    for row in rows:
        if row["outcome"] == "PROVED_BY_LEAN":
            continue
        say("  %s at %s over %s, `%s` limb %s: %s -- %s"
            % (row["schema"], row["width"], row["word"], row["shape"],
               row["limb"], row["outcome"],
               (row.get("cause") or row.get("lean_output")
                or "")[:200].replace("\n", " ")))
        continue
    return


def table_command():
    if not os.path.exists(OUT):
        say("no lemmas_t2.json on disk")
        return 1
    handle = open(OUT)
    document = json.load(handle)
    handle.close()
    report(document["theorems"], document["rows"])
    return 0


def main(argv):
    if len(argv) < 2:
        say(__doc__)
        return 2
    if argv[1] == "instances":
        return instances_command()
    if argv[1] == "prove":
        seconds = PER_THEOREM_SECONDS
        if len(argv) > 2:
            seconds = int(argv[2])
        return prove_command(seconds)
    if argv[1] == "table":
        return table_command()
    say("unknown command %r" % argv[1])
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
