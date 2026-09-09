#!/usr/bin/env python3
"""t98_settle.py -- the three places where task 98's recount DISAGREED
with the figures the brief carried, counted under every candidate
definition so the disagreement is explained rather than argued.

THE THREE DISAGREEMENTS, from lane 2's log
(agent/logs/20260905T134435Z__t98_l2_shapes.sh.log):

  1. DISTINCT MACHINE CODE.  The brief: "31,067 compiled units hold
     3,547 distinct body_bytes -- 8.8 units per distinct".  The recount:
     2,744 distinct over the whole corpus, 11.3 units per distinct.  The
     per-language distinct counts SUM to 1282+1393+192+169+511 = 3,547,
     so the two numbers are two different measurements: one counts a
     body once per language it appears in, the other counts it once.
     This program prints both, and how many bodies appear in more than
     one language, which is the whole of the difference.

  2. EMPTY BODIES.  The brief: "624 regenerated and 16 original units
     have no instructions at all".  The recount: 628 regenerated, 16
     original, and 2 interpreter units the brief does not mention.  Four
     candidate spellings of "no instructions" are counted here, per
     arrival population, so the 4-unit gap is either explained by a
     different field or stands as a real disagreement.

  3. THE OPCODE-COUNT DISTRIBUTION.  The brief's distribution (original
     peaks at 3, 543 units, 30.5%, median 4, max 23) matches the count of
     INSTRUCTION LINES in the body, not the count of DISTINCT opcode
     mnemonics.  Its "93 distinct opcodes / 162 distinct opcodes" is the
     vocabulary over the population, which is a different measurement
     again.  This program counts a fourth definition -- lines whose head
     word actually reads as an opcode mnemonic -- to check that "lines"
     and "opcode instructions" are the same number here.

It also prints the shapes of the further computed stats the pane will
carry, so nothing goes on the page unmeasured.

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

Every grouping here is by LANGUAGE, by ARRIVAL POPULATION or by MACHINE
CODE -- three machine-form facts carried on the record.  The operator
field is never read.

usage:
    t98_settle.py bodies      the two body-repetition measurements
    t98_settle.py empty       four spellings of "no instructions"
    t98_settle.py opcodes     the four count definitions
    t98_settle.py extras      the shapes of the further computed stats
    t98_settle.py all
"""

import glob
import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

LANGS = ["c", "cpp", "go", "rust", "swift"]


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def peak_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def units_in(document):
    held = document.get("units")
    if isinstance(held, dict):
        return list(held.values())
    if isinstance(held, list):
        return held
    return []


def bump(counter, key):
    counter[key] = counter.get(key, 0) + 1


def corpus_inputs():
    inputs = []
    for lang in LANGS:
        inputs.append("canon39_wrapped_%s.json" % lang)
    inputs.append("canon39_interp.json")
    shards = sorted(os.path.basename(p) for p in
                    glob.glob(os.path.join(HERE, "canon39_regen_store",
                                           "*.json")))
    for shard in shards:
        inputs.append(os.path.join("canon39_regen_store", shard))
    return inputs


def each_unit():
    for rel in corpus_inputs():
        path = os.path.join(HERE, rel)
        if not os.path.exists(path):
            continue
        document = json.load(open(path))
        for unit in units_in(document):
            yield unit
        del document


def head_word(line):
    return str(line).strip().split(" ")[0].strip()


def reads_as_opcode(line):
    word = head_word(line)
    if not word:
        return False
    if not word[0].isalpha():
        return False
    return word.isalnum()


def bodies():
    started = time.time()
    langs_of_body = {}
    times_seen = {}
    per_lang = {}
    compiled = 0
    for unit in each_unit():
        raw = unit.get("body_bytes")
        if not raw:
            continue
        compiled = compiled + 1
        lang = unit.get("lang") or "?"
        bump(times_seen, raw)
        if raw not in langs_of_body:
            langs_of_body[raw] = set()
        langs_of_body[raw].add(lang)
        if lang not in per_lang:
            per_lang[lang] = set()
        per_lang[lang].add(raw)

    corpus_distinct = len(times_seen)
    summed = sum(len(per_lang[lang]) for lang in per_lang)
    shared = len([b for b in langs_of_body if len(langs_of_body[b]) > 1])
    worst = max(times_seen, key=lambda b: times_seen[b])

    say("== distinct machine code, the two measurements")
    say("compiled units (carrying body_bytes)          %d" % compiled)
    say("distinct bodies, COUNTED ONCE for the corpus  %d" % corpus_distinct)
    say("distinct bodies, SUMMED per language          %d" % summed)
    say("bodies appearing in more than one language    %d" % shared)
    say("units per distinct body, corpus-wide          %.1f"
        % (float(compiled) / corpus_distinct))
    say("units per distinct body, summed per language  %.1f"
        % (float(compiled) / summed))
    say("the most repeated body appears                %d times"
        % times_seen[worst])
    say("  its bytes                                   %s"
        % (worst if len(worst) < 60 else worst[:57] + "..."))
    say("  the languages it appears in                 %s"
        % ", ".join(sorted(langs_of_body[worst])))
    say("-- per language: distinct bodies and the most repeated one")
    for lang in sorted(per_lang):
        held = per_lang[lang]
        best = 0
        for body in held:
            here = 0
            if len(langs_of_body[body]) == 1:
                here = times_seen[body]
            if here > best:
                best = here
        say("  %-10s %d distinct" % (lang, len(held)))
    say("")
    say("bodies walk: %.1f s, peak resident %.1f MB"
        % (time.time() - started, peak_mb()))


def empty():
    started = time.time()
    shapes = {}
    for name in ("body_as_read empty", "body_verbatim empty",
                 "body_text empty", "body_bytes empty"):
        shapes[name] = {}
    both = {}
    for unit in each_unit():
        population = unit.get("population") or "original"
        if not (unit.get("body_as_read") or []):
            bump(shapes["body_as_read empty"], population)
        if not (unit.get("body_verbatim") or []):
            bump(shapes["body_verbatim empty"], population)
        if not (unit.get("body_text") or "").strip():
            bump(shapes["body_text empty"], population)
        if not (unit.get("body_bytes") or "").strip():
            bump(shapes["body_bytes empty"], population)
        lines = unit.get("body_as_read") or []
        opcodes = len([one for one in lines if reads_as_opcode(one)])
        if opcodes == 0:
            bump(both, population)

    say("== four spellings of 'no instructions at all', per arrival "
        "population")
    for name in sorted(shapes):
        parts = []
        for population in sorted(shapes[name]):
            parts.append("%s %d" % (population, shapes[name][population]))
        say("  %-24s %s   (total %d)"
            % (name, ", ".join(parts) or "none",
               sum(shapes[name].values())))
    parts = []
    for population in sorted(both):
        parts.append("%s %d" % (population, both[population]))
    say("  %-24s %s   (total %d)"
        % ("no line reads as opcode", ", ".join(parts) or "none",
           sum(both.values())))
    say("")
    say("empty walk: %.1f s, peak resident %.1f MB"
        % (time.time() - started, peak_mb()))


def spread(counter):
    keys = sorted(counter)
    if not keys:
        return "(empty)"
    population = sum(counter[key] for key in keys)
    top = max(keys, key=lambda k: (counter[k], -k))
    seen = 0
    median = keys[0]
    for key in keys:
        seen = seen + counter[key]
        if seen >= (population + 1) // 2:
            median = key
            break
    return ("population %d, peak at %d (%d, %.1f%%), median %d, min %d, "
            "max %d, zero %d"
            % (population, top, counter[top],
               100.0 * counter[top] / population, median, keys[0],
               keys[-1], counter.get(0, 0)))


def opcodes():
    started = time.time()
    lines_dist = {}
    opline_dist = {}
    distinct_dist = {}
    disagreed = 0
    for unit in each_unit():
        population = unit.get("population") or "original"
        if population not in lines_dist:
            lines_dist[population] = {}
            opline_dist[population] = {}
            distinct_dist[population] = {}
        lines = unit.get("body_as_read") or []
        count_lines = len(lines)
        count_ops = len([one for one in lines if reads_as_opcode(one)])
        if count_lines != count_ops:
            disagreed = disagreed + 1
        words = set()
        for one in lines:
            if reads_as_opcode(one):
                words.add(head_word(one).lower())
        bump(lines_dist[population], count_lines)
        bump(opline_dist[population], count_ops)
        bump(distinct_dist[population], len(words))

    say("== how many arch opcodes a body holds -- the definitions, per "
        "arrival population")
    for population in sorted(lines_dist):
        say("-- %s" % population)
        say("   body lines               %s" % spread(lines_dist[population]))
        say("   lines reading as opcode  %s" % spread(opline_dist[population]))
        say("   distinct mnemonics       %s"
            % spread(distinct_dist[population]))
    say("")
    say("units where the two line counts differ: %d" % disagreed)
    say("opcodes walk: %.1f s, peak resident %.1f MB"
        % (time.time() - started, peak_mb()))


def extras():
    started = time.time()
    byte_len = {}
    ledger_rows = {}
    branch = {}
    outcome39 = {}
    result_width = {}
    for unit in each_unit():
        raw = unit.get("body_bytes") or ""
        if raw:
            bump(byte_len, len(raw) // 2)
        bump(ledger_rows, len(unit.get("ledger") or []))
        bump(branch, unit.get("branch_kind"))
        bump(outcome39, unit.get("outcome"))
        bump(result_width, unit.get("result_width"))

    say("== further computed stats, their shapes")
    say("body length in bytes      %s" % spread(byte_len))
    say("ledger rows per unit      %s" % spread(ledger_rows))
    say("-- branch_kind, every value seen")
    for value in sorted(branch, key=lambda v: -branch[v]):
        say("   %-24s %d" % (value, branch[value]))
    say("-- canon39 outcome, every value seen")
    for value in sorted(outcome39, key=lambda v: -outcome39[v]):
        say("   %-30s %d" % (value, outcome39[value]))
    say("-- result_width, every value seen")
    for value in sorted(result_width, key=lambda v: -result_width[v]):
        say("   %-12s %d" % (value, result_width[value]))

    say("")
    say("-- term66_store: what a record carries beyond its state")
    callee_units = {}
    hole_units = {}
    cascade_units = {}
    relink = {}
    records = 0
    for path in sorted(glob.glob(os.path.join(HERE, "term66_store",
                                              "*.json"))):
        document = json.load(open(path))
        for unit in units_in(document):
            records = records + 1
            lang = unit.get("lang") or "?"
            if (unit.get("runtime_callee_rows") or 0) > 0:
                bump(callee_units, lang)
            if unit.get("holes"):
                bump(hole_units, lang)
            if unit.get("cascades"):
                bump(cascade_units, lang)
            if unit.get("relink_refusal"):
                bump(relink, lang)
        del document
    say("   records                        %d" % records)
    say("   units carrying a runtime-callee row, per language:")
    for lang in sorted(callee_units):
        say("     %-10s %d" % (lang, callee_units[lang]))
    say("   total with a runtime-callee row  %d" % sum(callee_units.values()))
    say("   total with a hole                %d" % sum(hole_units.values()))
    say("   total with a cascade             %d" % sum(cascade_units.values()))
    say("   total with a relink refusal      %d" % sum(relink.values()))
    say("")
    say("extras walk: %.1f s, peak resident %.1f MB"
        % (time.time() - started, peak_mb()))


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    for name, run in (("bodies", bodies), ("empty", empty),
                      ("opcodes", opcodes), ("extras", extras)):
        if which in (name, "all"):
            run()
            say("")
    say("whole process peak resident %.1f MB" % peak_mb())


if __name__ == "__main__":
    main()
