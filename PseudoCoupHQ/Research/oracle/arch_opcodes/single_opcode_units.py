#!/usr/bin/env python3
"""single_opcode_units.py -- task o2 deliverable 1.

Per language, per chaff rule (narrow / wide), the units whose body
with chaff removed is exactly ONE instruction, grouped by
(mnemonic, distinct machine body bytes) -- never keyed by the
operator token (THE SPELLING BAN). Also the per-language, per-rule
histogram of instructions-remaining -> unit count, and the
zero-opcode units listed separately with three literal examples.

Population (all nine languages, every canonical unit):
  - canon40_wrapped_{c,cpp,go,rust,swift}.json  (units dict; ORIGINAL)
  - canon40_regen_store/*.json                  (units dict per shard; REGEN)
  - canon40_interp.json                         (units dict; interpreters:
                                                  java, cpython, php, ruby)

Streams shards; never holds the whole 110 MB store at once beyond one
shard plus the running per-language tallies (which are small summaries,
not raw bodies repeated).

Run:
    /usr/bin/time -v python3 single_opcode_units.py
"""
import json
import glob
import os
import sys
import resource
import re

LABEL_LINE_RE = re.compile(r'^[A-Za-z_.$][\w.$]*:$')

OP_PIPELINE = "/projects/PseudoCoupHQ/Research/op_pipeline"
OUT_DIR = "/projects/PseudoCoupHQ/Research/oracle/arch_opcodes"

NARROW_PURE_MOVE = {"mov", "movabs", "movq", "movd", "movaps", "movapd", "movss", "movsd"}
NARROW_BARE = {"ret", "nop", "push", "pop"}
WIDTH_CHANGE = {"movzbl", "movzwl", "movzbq", "movzwq", "movslq", "movsbl", "movsbq", "movswl",
                "cltq", "cwtl", "cltd", "cqto"}


def is_reg_or_slot_operand(op):
    op = op.strip()
    if op.startswith("%"):
        return True
    # a ledger/stack slot: has a parenthesis addressing form, or a bare
    # symbol reference (e.g. "ledger+0x10(%rip)"), or a resolved
    # placeholder like "IN-0" / "OUT-0" / "TEMP-2".
    if "(" in op and ")" in op:
        return True
    if op.replace("-", "").replace("_", "").isalnum() and any(c.isupper() for c in op):
        return True
    return False


def parse_insn(insn):
    insn = insn.strip()
    if not insn:
        return None, []
    parts = insn.split(None, 1)
    mnem = parts[0]
    operands = []
    if len(parts) > 1:
        operands = [o.strip() for o in parts[1].split(",")]
    return mnem, operands


def is_chaff(insn, rule):
    mnem, operands = parse_insn(insn)
    if mnem is None:
        return False
    if mnem in NARROW_BARE:
        return True
    if mnem in NARROW_PURE_MOVE:
        if len(operands) == 2 and all(is_reg_or_slot_operand(o) for o in operands):
            return True
        return False
    if rule == "wide" and mnem in WIDTH_CHANGE:
        return True
    return False


def is_label_line(insn):
    """a branch-target label definition (e.g. 'L0:') -- not an
    instruction, so not an arch opcode and not counted at all (not
    even as chaff)."""
    return bool(LABEL_LINE_RE.match(insn.strip()))


def strip_chaff(body_verbatim, rule):
    return [insn for insn in body_verbatim
            if not is_label_line(insn) and not is_chaff(insn, rule)]


def iter_all_units():
    """Yields (lang, unit_id, record, source) for every unit in the
    population, source in {"wrapped", "regen", "interp"}."""
    for lang in ("c", "cpp", "go", "rust", "swift"):
        path = os.path.join(OP_PIPELINE, f"canon40_wrapped_{lang}.json")
        with open(path) as f:
            d = json.load(f)
        for uid, rec in d["units"].items():
            yield lang, uid, rec, "wrapped"

    shard_paths = sorted(glob.glob(os.path.join(OP_PIPELINE, "canon40_regen_store", "*.json")))
    for i, path in enumerate(shard_paths):
        with open(path) as f:
            d = json.load(f)
        for uid, rec in d["units"].items():
            lang = rec.get("lang")
            if lang is None:
                base = os.path.basename(path)
                lang = base.split("op_units2_")[1].split("_")[0]
            yield lang, uid, rec, "regen"
        del d

    path = os.path.join(OP_PIPELINE, "canon40_interp.json")
    with open(path) as f:
        d = json.load(f)
    for uid, rec in d["units"].items():
        lang = rec.get("lang")
        yield lang, uid, rec, "interp"


def main():
    population = {}  # lang -> {"read":N, "with_body":N, "without_body":N, "without_ids":[...]}
    # per lang, per rule -> {(mnem, body_text): {"members":[], "operators":set()}}
    grouped = {}
    # per lang, per rule -> histogram {n_remaining: count}
    histogram = {}
    zero_opcode_examples = {}  # lang -> rule -> [ (uid, operator, body_text) ]
    langs_seen = set()

    for lang, uid, rec, source in iter_all_units():
        langs_seen.add(lang)
        pop = population.setdefault(lang, {"read": 0, "with_body": 0, "without_body": 0, "without_ids": []})
        pop["read"] += 1
        bv = rec.get("body_verbatim")
        if not bv:
            pop["without_body"] += 1
            pop["without_ids"].append(uid)
            continue
        pop["with_body"] += 1
        operator = rec.get("operator", "?")
        body_text = rec.get("body_text") or "; ".join(bv)

        for rule in ("narrow", "wide"):
            stripped = strip_chaff(bv, rule)
            n = len(stripped)
            hist = histogram.setdefault(lang, {}).setdefault(rule, {})
            hist[n] = hist.get(n, 0) + 1
            if n == 0:
                ex = zero_opcode_examples.setdefault(lang, {}).setdefault(rule, [])
                if len(ex) < 3:
                    # `lang` is here for the spelling guard, added
                    # 2026-09-08 by task m1b (log_235 cause D). The
                    # guard allows an operator token in an `operator`
                    # field only on a record that identifies ONE unit,
                    # which its `is_unit_object()` reads as carrying
                    # BOTH a language field and a unit id. This record
                    # carried the id and not the language, so its
                    # display label was walked as an ordinary
                    # structure field and failed.
                    ex.append({"lang": lang, "unit": uid,
                               "operator": operator,
                               "body_text": body_text})
            if n == 1:
                mnem, _ = parse_insn(stripped[0])
                g = grouped.setdefault(lang, {}).setdefault(rule, {})
                key = (mnem, body_text)
                entry = g.setdefault(key, {"mnem": mnem, "body_text": body_text,
                                            "members": [], "operators": set()})
                entry["members"].append({"lang": lang, "unit": uid, "operator": operator})
                entry["operators"].add(operator)

    # Assemble JSON-serializable output.
    out = {
        "population": population,
        "histogram": histogram,
        "zero_opcode_examples": zero_opcode_examples,
        "single_opcode_groups": {},
        "note_chaff_rules": {
            "narrow": "ret, nop, push, pop, mov/movabs/movq/movd/movaps/movapd/movss/movsd "
                      "when both operands are registers or one is a ledger/stack slot (pure copy)",
            "wide": "narrow chaff PLUS width-changing moves and sign/zero extensions "
                    "(movzbl, movslq, movsbl, cltq, cwtl, cltd, cqto)",
        },
    }
    for lang, rules in grouped.items():
        out["single_opcode_groups"][lang] = {}
        for rule, groups in rules.items():
            rows = []
            for (mnem, body_text), entry in sorted(groups.items(), key=lambda kv: kv[0][0]):
                # members: each a UNIT OBJECT (lang + unit id), the
                # operator token carried once per unit as its own
                # display-label field -- never as a bare-token list on
                # this grouping row (THE SPELLING BAN).
                rows.append({
                    "mnem": entry["mnem"],
                    "body_text": entry["body_text"],
                    "member_count": len(entry["members"]),
                    "example_unit_id": entry["members"][0]["unit"],
                    "members": entry["members"],
                })
            out["single_opcode_groups"][lang][rule] = rows

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "single_opcode_units.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)

    # Markdown rendering.
    lines = []
    lines.append("# single_opcode_units -- task o2 deliverable 1")
    lines.append("")
    lines.append("## Population")
    lines.append("")
    lines.append("| language | units read | units with body | units without body |")
    lines.append("|---|---|---|---|")
    for lang in sorted(population):
        p = population[lang]
        lines.append(f"| {lang} | {p['read']} | {p['with_body']} | {p['without_body']} |")
    lines.append("")

    for lang in sorted(out["single_opcode_groups"]):
        lines.append(f"## {lang}")
        for rule in ("narrow", "wide"):
            rows = out["single_opcode_groups"][lang].get(rule, [])
            lines.append("")
            lines.append(f"### {rule} chaff -- {len(rows)} distinct single-opcode bodies")
            lines.append("")
            lines.append("| mnemonic | body (LITERAL) | members | operator labels seen | example unit id |")
            lines.append("|---|---|---|---|---|")
            for r in rows:
                ops_seen = sorted(set(m["operator"] for m in r["members"]))
                lines.append(f"| {r['mnem']} | `{r['body_text']}` | {r['member_count']} | "
                              f"{', '.join(ops_seen)} | {r['example_unit_id']} |")
        lines.append("")
        lines.append("#### zero-opcode units (pure move, chaff-stripped body is empty)")
        for rule in ("narrow", "wide"):
            exs = out["zero_opcode_examples"].get(lang, {}).get(rule, [])
            lines.append(f"- {rule}: {len(exs)} example(s) shown of the histogram's n=0 count")
            for e in exs:
                lines.append(f"  - `{e['unit']}` operator `{e['operator']}`: `{e['body_text']}`")
        lines.append("")

    with open(os.path.join(OUT_DIR, "single_opcode_units.md"), "w") as f:
        f.write("\n".join(lines) + "\n")

    print("languages seen:", sorted(langs_seen))
    for lang in sorted(population):
        p = population[lang]
        print(f"[{lang}] read={p['read']} with_body={p['with_body']} without_body={p['without_body']}")
    for lang in sorted(out["single_opcode_groups"]):
        for rule in ("narrow", "wide"):
            n = len(out["single_opcode_groups"][lang].get(rule, []))
            print(f"[{lang}] {rule}: {n} distinct single-opcode bodies")
    print("wrote", os.path.join(OUT_DIR, "single_opcode_units.json"))
    print("wrote", os.path.join(OUT_DIR, "single_opcode_units.md"))


if __name__ == "__main__":
    main()
    peak_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(f"PEAK_RSS_KB={peak_kb} PEAK_RSS_MB={peak_kb/1024:.1f}")

