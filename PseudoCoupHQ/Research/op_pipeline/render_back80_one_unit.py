#!/usr/bin/env python3
"""render_back80_one_unit.py -- LITERAL: one conditional unit's own
ship body, its term, its rendered text, its assembled bytes, and the
gate's verdict, printed end to end so the claim "the return path now
covers conditionals" can be read off the page.

Two units are printed, one of each shape the corpus writes:

  * a `set<cc>` unit -- the arms are the literals 1 and 0;
  * a `cmov<cc>` unit -- the arms are two values.

Every line below is produced by the same objects the run uses:
`term.Term.transcribe` for the term, `term.RenderBack` for the text,
`canonical_form.CanonicalForm.assemble` / `.disassemble` for the real
`as` and `objdump -d` round trip, `gate.Gate.prove_wrapped` for the
verdict against the unit's OWN ship body.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

No operator token appears in this file.

Coding discipline: no compound one-liner statements.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import z3                                                        # noqa: E402
import canonical_form as CF                                      # noqa: E402
import gate as G                                                 # noqa: E402
import reference as R                                            # noqa: E402
import term as T                                                 # noqa: E402
import term61_run as D                                           # noqa: E402

SHARD = os.path.join(HERE, "canon39_wrapped_c.json")
PRINTED = os.path.join(HERE, "render_back80_one_unit_printed.txt")
WORK = "/tmp/render_back80_one_unit_work"
WANTED = ["c/op_0", "c/op_179"]


def assemble_one(form, text):
    """the real `as` and the real `objdump -d`, over the same batch
    file `CanonicalForm.write_batch` writes for the run."""
    if not os.path.isdir(WORK):
        os.makedirs(WORK)
    symbol = "rb80_one"
    lines, count, notes, stubs = form.render_for_assembler(symbol,
                                                           text)
    source = os.path.join(WORK, "one.s")
    obj = os.path.join(WORK, "one.o")
    form.write_batch(source, [(symbol, lines, count, stubs, notes)])
    code, message = form.assemble(source, obj)
    if code != 0:
        return None, None, message
    dump = form.disassemble(obj)
    counts = form.counts_from_dump(dump)
    return count, counts.get(symbol), dump


def show(out, unit, maker, renderer, gate, form):
    name = unit["unit"]
    out.append("=" * 68)
    out.append("UNIT %s   language %s   population %s"
               % (name, unit.get("lang"), unit.get("population")))
    out.append("=" * 68)
    out.append("")
    out.append("ITS OWN SHIP BODY, as the compiler wrote it:")
    for line in unit.get("body_verbatim") or []:
        out.append("    %s" % line)
    out.append("")
    out.append("its arrival contract: families %s, answer home %s at "
               "%s bits"
               % (unit.get("arrival_families"),
                  unit.get("result_family"), unit.get("result_width")))
    out.append("")
    out.append("LAYER 3, the same body wrapped:")
    out.append("    %s" % unit.get("wrapped_text"))
    out.append("")
    walked = maker.transcribe(unit)
    term = walked.out_term
    out.append("ITS TERM, as the reference walk left it:")
    out.append("    %s" % one_line(term))
    simplified = z3.simplify(term)
    out.append("")
    out.append("the same term simplified once, which is what the "
               "return path renders:")
    out.append("    %s" % one_line(simplified))
    out.append("")
    rendering = renderer.render_and_wrap(term, unit)
    if rendering.wrapped_text is None:
        out.append("REFUSED: %s" % rendering.refused)
        return
    out.append("THE RENDERED BODY, by the one fixed rule:")
    for line in rendering.body:
        out.append("    %s" % line)
    out.append("")
    out.append("THE RENDERED TEXT, wrapped by the same "
               "CanonicalForm.wrap layer 3 goes through:")
    out.append("    %s" % rendering.wrapped_text)
    out.append("")
    written, read_back, dump = assemble_one(form,
                                            rendering.wrapped_text)
    if written is None:
        out.append("`as` REFUSED: %s" % dump)
        return
    out.append("ASSEMBLED by the real `as` and read back by the real "
               "`objdump -d`:")
    out.append("    instructions written %d, read back %s"
               % (written, read_back))
    out.append("    the disassembler's own lines:")
    for line in dump.splitlines():
        out.append("        %s" % line)
    out.append("")
    verdict = renderer.verify(gate, unit, rendering.fields)
    out.append("THE GATE'S VERDICT, the rendered text against this "
               "unit's OWN ship body:")
    out.append("    outcome: %s" % verdict.outcome)
    out.append("    reason:  %s" % verdict.reason)
    out.append("")


def one_line(term):
    text = "%s" % term
    return " ".join(text.split())


def main():
    reference = R.Reference()
    maker = T.Term(reference=reference,
                   runtime_routines=CF.runtime_routine_names(),
                   runtime_units=D.runtime_units())
    renderer = T.RenderBack(reference)
    gate = G.Gate(reference=reference)
    form = CF.CanonicalForm()
    document = json.load(open(SHARD))
    out = []
    out.append("render_back80 -- LITERAL, one conditional unit of each "
               "shape the corpus writes")
    out.append("")
    for name in WANTED:
        unit = document["units"].get(name)
        if unit is None:
            out.append("%s is not in %s" % (name, SHARD))
            continue
        show(out, unit, maker, renderer, gate, form)
    text = "\n".join(out)
    handle = open(PRINTED, "w")
    handle.write(text)
    handle.write("\n")
    handle.close()
    sys.stdout.write(text)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
