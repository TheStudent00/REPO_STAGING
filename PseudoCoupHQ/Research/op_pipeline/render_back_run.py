#!/usr/bin/env python3
"""render_back_run.py -- the driver that runs the sub-node
`render_back` (node 0_3_5_6_5, the class `term.RenderBack`) over the
proved terms, ASSEMBLES each rendered text with `as`, and GATES it
with `gate.Gate.prove_wrapped` against the unit's OWN ship code.

CORE:
`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_6_term/node_0_3_5_6_5_render_back/CORE_0_3_5_6_5_render_back.md`

WHAT THE RENDERED TEXT IS, relative to layer 3 and layer 5.  Layer 3 is
the unit's own machine code wrapped: the compiler's body verbatim
between a standardized prelude and epilogue.  Layer 5 is that body's
computation as a z3 term, simplified and printed by one fixed rule --
a comparison key, not something that runs.  The rendered text is the
LAYER-5 TERM MADE RUNNABLE: the same computation, emitted as
instructions by one fixed rule, wrapped by the same
`CanonicalForm.wrap` into the same form layer 3 has.  It is therefore a
SECOND canonical rendering of the same unit, beside the first.  It
replaces nothing -- the accumulate ruling -- and whether it is
character-identical to the layer-3 text is measured per unit, never
assumed.

POPULATIONS, in the order the brief names them:

  1. every proved term of the pool entry `E00029` -- 158 members over
     seven languages, whose one normalized text is `v0 + v1`;
  2. every proved term of the whole population -- 26,040 of the 30,432
     units canon39 proved.

ONE PROCESS.  Everything below runs in this single process.  The run is
resumable: `render_back_state.json` names the shards already written.

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

No operator token appears in this file.  The `operator` field of a unit
record is a display label this file copies onto the member and never
reads, never groups on and never pairs on.

Coding discipline: no compound one-liner statements.
"""

import glob
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canonical_form as CF                                      # noqa: E402
import gate as G                                                 # noqa: E402
import reference as R                                            # noqa: E402
import term as T                                                 # noqa: E402
import term61_run as D                                           # noqa: E402

STORE = os.path.join(HERE, "render_back_store")
STATE = os.path.join(HERE, "render_back_state.json")
TERM_STORE = os.path.join(HERE, "term61_store")
WORK = "/tmp/render_back_assemble_work"

PROVED = "WRAPPED_TEXT_PROVED"
PROVED_ON_SHIP = "PROVED_ON_SHIP"
BATCH = 60


# ------------------------------------------------------------------
# the population: the canon39 shards, and which of their units the
# term store records as PROVED
# ------------------------------------------------------------------

def shards():
    """the same 332 shards `term61_run` walked, in the same order."""
    return D.shards()


def term_record_path(path):
    key = os.path.relpath(path, HERE)
    return os.path.join(TERM_STORE, key.replace("/", "__"))


def proved_terms_of(path):
    """unit name -> its term-store record, for the units whose LAYER-4
    TERM was proved.  A unit with no proved term has no layer-5 key and
    therefore nothing to render back; it is counted, never rendered."""
    written = term_record_path(path)
    if not os.path.exists(written):
        return {}
    document = json.load(open(written))
    out = {}
    for name, record in document.get("units", {}).items():
        if record.get("proved"):
            out[name] = record
    return out


# ------------------------------------------------------------------
# assembling a batch of rendered texts with the real assembler
# ------------------------------------------------------------------

class Assembler(object):
    """`as --64` over the rendered texts of one shard, then
    `objdump -d` back.  The same two commands
    `canonical_form.CanonicalForm.assemble` / `.disassemble` run, over
    the same batch file `CanonicalForm.write_batch` writes, so no
    second assembly rule is written here."""

    def __init__(self, form):
        self.form = form
        if not os.path.isdir(WORK):
            os.makedirs(WORK)

    def symbol_for(self, index):
        return "rb_%06d" % index

    def run(self, rendered):
        """[(unit name, wrapped text)] -> unit name -> what the
        assembler and the disassembler said about it."""
        out = {}
        position = 0
        while position < len(rendered):
            chunk = rendered[position:position + BATCH]
            position = position + BATCH
            self.one_batch(chunk, out)
        return out

    def one_at_a_time(self, chunk, out):
        """each unit of a failed batch, assembled alone, so the
        assembler's refusal is charged to the text that earned it."""
        for name, text in chunk:
            symbol = "rb_alone"
            lines, count, notes, stubs = \
                self.form.render_for_assembler(symbol, text)
            items = [(symbol, lines, count, stubs, notes)]
            source = os.path.join(WORK, "alone.s")
            obj = os.path.join(WORK, "alone.o")
            self.form.write_batch(source, items)
            code, message = self.form.assemble(source, obj)
            if code != 0:
                out[name] = {
                    "assembled": False,
                    "why": "`as` refused this rendered text: %s"
                           % last_error(message),
                }
                continue
            dump = self.form.disassemble(obj)
            counts = self.form.counts_from_dump(dump)
            got = counts.get(symbol)
            out[name] = {
                "assembled": True,
                "instructions_written": count,
                "instructions_disassembled": got,
                "round_trips": got == count,
                "assembler_notes": notes,
            }

    def one_batch(self, chunk, out):
        items = []
        names = {}
        for index, pair in enumerate(chunk):
            name, text = pair
            symbol = self.symbol_for(len(names))
            names[symbol] = name
            lines, count, notes, stubs = \
                self.form.render_for_assembler(symbol, text)
            items.append((symbol, lines, count, stubs, notes))
        source = os.path.join(WORK, "batch.s")
        obj = os.path.join(WORK, "batch.o")
        self.form.write_batch(source, items)
        code, message = self.form.assemble(source, obj)
        if code != 0:
            # A BATCH IS NOT A CAUSE.  One rejected instruction fails
            # the whole batch file, which would charge the refusal to
            # every unit in it -- reporting by sighting, and a false
            # count.  So a failed batch is re-run ONE UNIT AT A TIME
            # and each unit gets the assembler's own words about its
            # own text.
            self.one_at_a_time(chunk, out)
            return
        dump = self.form.disassemble(obj)
        counts = self.form.counts_from_dump(dump)
        for item in items:
            symbol = item[0]
            wanted = item[2]
            got = counts.get(symbol)
            record = {
                "assembled": True,
                "instructions_written": wanted,
                "instructions_disassembled": got,
                "round_trips": got == wanted,
                "assembler_notes": item[4],
            }
            if got != wanted:
                record["why"] = (
                    "`as` wrote %s instructions and `objdump -d` read "
                    "back %s" % (wanted, got))
            out[names[symbol]] = record


# ------------------------------------------------------------------
# one unit
# ------------------------------------------------------------------

def one_unit(maker, renderer, gate, name, unit, term_record):
    """one proved-term unit -> its return-path record."""
    out = {
        "unit": name,
        "lang": unit.get("lang"),
        "population": unit.get("population"),
        "operator": unit.get("operator"),
        "arrival_families": list(unit.get("arrival_families") or []),
        "result_family": unit.get("result_family"),
        "result_width": unit.get("result_width"),
        "layer5_normalized_text":
            term_record.get("layer5_normalized_text"),
        "layer3_wrapped_text": unit.get("wrapped_text"),
    }
    walked = maker.transcribe(unit)
    if walked.out_term is None:
        out["rendered"] = False
        out["refusal_cause"] = "the term did not rebuild"
        out["why"] = ("the transcription that the term store records "
                      "as proved did not rebuild a term in this run")
        return out
    rendering = renderer.render_and_wrap(walked.out_term, unit)
    if rendering.wrapped_text is None:
        out["rendered"] = False
        out["refusal_cause"] = rendering.refusal_cause
        out["why"] = rendering.refused
        return out
    out["rendered"] = True
    out["rendered_body"] = rendering.body
    out["rendered_wrapped_text"] = rendering.wrapped_text
    out["character_identical_to_layer_3"] = (
        rendering.wrapped_text == unit.get("wrapped_text"))
    verdict = renderer.verify(gate, unit, rendering.fields)
    out["verdict"] = verdict.as_dict()
    out["outcome"] = verdict.outcome
    out["proved"] = verdict.outcome == PROVED_ON_SHIP
    if not out["proved"]:
        out["not_proved_cause"] = cause_of_verdict(verdict)
    return out


def last_error(message):
    """the assembler's own error line, quoted rather than
    paraphrased."""
    for line in message.splitlines():
        if "Error:" in line:
            return line.split("Error:", 1)[-1].strip()
    return message.strip()[:200]


def cause_of_verdict(verdict):
    """the verdict's own reason, cut to the CAUSE it names, so the
    report groups by cause and not by sighting."""
    text = "%s" % verdict.reason
    if verdict.outcome == "DISPROVED":
        return "z3 found a starting state under which the two differ"
    if "did not answer inside its" in text:
        return "the solver did not answer inside its limit"
    if "has no model for something this body spells" in text:
        head = text.split("(", 1)[-1]
        head = head.split(")", 1)[0]
        return "the reference has no model for: %s" % head[:160]
    return text[:200]


# ------------------------------------------------------------------
# the run
# ------------------------------------------------------------------

def load_state():
    if not os.path.exists(STATE):
        return {"done": [], "started": time.time()}
    return json.load(open(STATE))


def save_state(state):
    handle = open(STATE, "w")
    json.dump(state, handle, indent=1, sort_keys=True)
    handle.close()


def new_tools():
    reference = R.Reference()
    maker = T.Term(reference=reference,
                   runtime_routines=CF.runtime_routine_names(),
                   runtime_units=D.runtime_units())
    renderer = T.RenderBack(reference)
    gate = G.Gate(reference=reference)
    form = CF.CanonicalForm()
    return maker, renderer, gate, form


def run(budget_seconds):
    if not os.path.isdir(STORE):
        os.makedirs(STORE)
    state = load_state()
    done = set(state["done"])
    maker, renderer, gate, form = new_tools()
    assembler = Assembler(form)
    started = time.time()
    every = shards()
    for path in every:
        key = os.path.relpath(path, HERE)
        if key in done:
            continue
        if time.time() - started > budget_seconds:
            print("budget spent; %d shards still to walk"
                  % (len(every) - len(done)))
            sys.stdout.flush()
            return False
        document = json.load(open(path))
        wanted = proved_terms_of(path)
        out = {}
        skipped_no_proved_term = 0
        for name, unit in sorted(document.get("units", {}).items()):
            if unit.get("outcome") != PROVED:
                continue
            record = wanted.get(name)
            if record is None:
                skipped_no_proved_term = skipped_no_proved_term + 1
                continue
            out[name] = one_unit(maker, renderer, gate, name, unit,
                                 record)
        rendered = []
        for name in sorted(out):
            if out[name].get("rendered_wrapped_text") is None:
                continue
            rendered.append((name, out[name]["rendered_wrapped_text"]))
        said = assembler.run(rendered)
        for name in said:
            out[name]["assembly"] = said[name]
        written = os.path.join(STORE, key.replace("/", "__"))
        handle = open(written, "w")
        json.dump({"shard": key,
                   "skipped_no_proved_term": skipped_no_proved_term,
                   "units": out}, handle, sort_keys=True)
        handle.close()
        done.add(key)
        state["done"] = sorted(done)
        save_state(state)
        print("%s: %d with proved terms, %d rendered, %d skipped"
              % (key, len(out), len(rendered), skipped_no_proved_term))
        sys.stdout.flush()
    print("all %d shards walked" % len(done))
    return True


if __name__ == "__main__":
    budget = 3600
    if len(sys.argv) > 1:
        budget = int(sys.argv[1])
    finished = run(budget)
    if not finished:
        sys.exit(3)
