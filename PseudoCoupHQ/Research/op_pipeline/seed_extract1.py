#!/usr/bin/env python3
"""seed_extract1.py -- STEP 1/2 of THE JOB (branching-unit seed
extraction + survey), per AgentMemory's SEEDED GROUPING UNDER
CONDITIONS ruling and the standing example (go/op_132).

SEED = the normal-path computation graph. This file's method,
stated so its evidence class is clear (evidence doctrine):

  - GUARD (trap/panic) blocks: read directly from core_modes_*.json
    route-1 output (`modes`, response `trap`/`panic-call:*`,
    detection `branch-to-response`) -- EXISTING, PROVEN machinery,
    just consumed here. FORCED BY CONSTRUCTION (block content
    string-matched against core_modes' own `response_blocks`).
  - DISPATCH blocks (pure compare+branch, no data computation):
    excluded from seed text -- they gate, they do not compute.
  - INLINE-ALTERNATE-PATH guards (the go/op_132 b==-1 case: a
    second, non-trapping, disjoint computation path to its own
    return): detected by grouping computation blocks by the
    terminal (`ret`-bearing) block they each reach. When more than
    one such group exists, EACH group is a *candidate* seed. The
    candidate is RESOLVED, not guessed: every candidate's text is
    looked up against the existing 1,641-unit 0-branch table's own
    canonical texts (character-identical, per THE REPRESENTATIVE
    RULE). Exactly one match => that candidate is the seed, the
    other group(s) become guard rows (response
    `inline-special-case`), condition text pulled with verdicts.py's
    own `divergence_conditions` (same route already used for
    trap guards, just pointed at the extra block). Zero or 2+
    matches => left UNRESOLVED, reason recorded verbatim, unit does
    NOT enter dominant_table22.json this lap. This is honest
    resolution-by-evidence, not a structural heuristic dressed up as
    ground truth -- see the printed report for how many units each
    path covers.

Output: seeds1.json (per-unit seed_text/status/guards),
survey1.json (counts by state).
"""
import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import verdicts as V                                          # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]

JUMP_RE = re.compile(r"^(j\w+)\s+(L\w+)$")
DISPATCH_MNEM = re.compile(
    r"^(test|cmp|je|jne|jl|jle|jg|jge|ja|jae|jb|jbe|js|jns|jo|jno|jp|jnp|jmp)\b")


def label_key(lbl):
    m = re.match(r"^L(\d+)(?:_p(\d+))?$", lbl)
    if not m:
        return (999999, 0, lbl)
    return (int(m.group(1)), int(m.group(2) or 0), lbl)


def is_dispatch_block(steps):
    for s in steps:
        mnem = s.split()[0] if s.split() else s
        if not DISPATCH_MNEM.match(mnem):
            return False
    return True


def block_text(steps):
    return "; ".join(steps)


def edges_of(steps):
    tgts = []
    for s in steps:
        m = JUMP_RE.match(s.strip())
        if m:
            tgts.append(m.group(2))
    return tgts


def load_core_modes():
    out = {}
    for lang in LANGS:
        path = os.path.join(HERE, "core_modes_%s.json" % lang)
        if not os.path.exists(path):
            continue
        d = json.load(open(path))
        for k, u in d["units"].items():
            out[(lang, str(k))] = u
    return out


def build_0branch_index():
    """canonical_text -> class_id, for every member of
    dominant_table21.json (the 1,641-unit 0-branch table), text read
    straight from canon3 (derived_mnem_joined)."""
    table = json.load(open(os.path.join(HERE, "dominant_table21.json")))
    canon = {}
    for lang in LANGS:
        d = json.load(open(os.path.join(HERE, "canon3_units_%s.json" % lang)))
        for k, u in d["units"].items():
            if u.get("erasure") == "ok" and "derived_mnem_joined" in u:
                canon[(lang, str(k))] = u["derived_mnem_joined"]
    text_to_class = {}
    for row in table["rows"]:
        for m in row["members"]:
            unit = m["unit"]
            lang, num = unit.split("/op_")
            text = canon.get((lang, num))
            if text is not None:
                text_to_class.setdefault(text, row["class_id"])
    return text_to_class, canon


def guard_trap_blocks(unit_cm):
    """block label -> mode row, for trap/panic-call guard blocks,
    matched by response_blocks TEXT against this unit's own canon3
    block texts (caller passes canon3 blocks in)."""
    modes = unit_cm.get("modes", [])
    resp_texts = set(unit_cm.get("response_blocks", []))
    return modes, resp_texts


def terminal_groups(blocks_by_label, order, trap_labels):
    """group computation (non-dispatch, non-trap) blocks by the
    ret-bearing block they each forward-reach, stepping only through
    non-trap blocks. Returns {ret_label: [member labels in order]}."""
    adj = {}
    for i, lbl in enumerate(order):
        steps = blocks_by_label[lbl]
        e = edges_of(steps)
        is_ret = any(s.strip() == "ret" or s.strip().startswith("ret")
                     for s in steps)
        if not e and not is_ret and i + 1 < len(order):
            # no explicit jump and no ret -- implicit fallthrough to
            # the next block in (label-order-sorted) sequence.
            e = [order[i + 1]]
        adj[lbl] = e

    def reach_ret(start, seen=None):
        seen = seen or set()
        if start in seen:
            return None
        seen.add(start)
        steps = blocks_by_label[start]
        if any(s.strip() == "ret" or s.strip().startswith("ret") for s in steps):
            return start
        for nxt in adj.get(start, []):
            if nxt in trap_labels or nxt not in blocks_by_label:
                continue
            got = reach_ret(nxt, seen)
            if got:
                return got
        return None

    groups = defaultdict(list)
    for lbl in order:
        if lbl in trap_labels:
            continue
        if is_dispatch_block(blocks_by_label[lbl]) and not any(
                s.strip() == "ret" or s.strip().startswith("ret")
                for s in blocks_by_label[lbl]):
            continue
        ret_lbl = reach_ret(lbl)
        if ret_lbl is None:
            continue
        groups[ret_lbl].append(lbl)
    return groups


def main():
    core_modes = load_core_modes()
    text_to_class, canon0 = build_0branch_index()

    survey = {lang: dict(units_read=0, single_block=0, branching=0,
                          seed_ok=0, seed_unresolved=0,
                          erasure_refused=0) for lang in LANGS}
    seeds = {}
    reasons = defaultdict(int)

    for lang in LANGS:
        d = json.load(open(os.path.join(HERE, "canon3_units_%s.json" % lang)))
        survey[lang]["units_read"] = d["units_read"]
        for k, u in d["units"].items():
            if u.get("erasure") != "ok":
                survey[lang]["erasure_refused"] += 1
                continue
            blocks = u.get("blocks")
            if not blocks or len(blocks) <= 1:
                survey[lang]["single_block"] += 1
                continue
            survey[lang]["branching"] += 1
            unit_id = "%s/op_%s" % (lang, k)

            blocks_by_label = {b["label"]: b["steps"] for b in blocks}
            order = sorted(blocks_by_label, key=label_key)

            cm = core_modes.get((lang, str(k)))
            modes, resp_texts = ([], set())
            if cm is not None:
                modes, resp_texts = guard_trap_blocks(cm)
            trap_labels = {lbl for lbl in blocks_by_label
                           if block_text(blocks_by_label[lbl]) in resp_texts}

            groups = terminal_groups(blocks_by_label, order, trap_labels)

            guards = []
            for m in modes:
                guards.append(dict(
                    kind="trap-or-panic",
                    condition=m.get("condition"),
                    response=m.get("response"),
                    detection=m.get("detection"),
                    branch=m.get("branch"),
                    lands_in=m.get("lands_in")))

            if len(groups) == 0:
                seeds[unit_id] = dict(
                    lang=lang, n=str(k), operator=u["meta"]["operator"],
                    status="unresolved",
                    reason="no computation group reached a ret block "
                           "(dispatch/trap-only structure this pass "
                           "did not model)",
                    guards=guards)
                reasons["no ret-reaching computation group"] += 1
                survey[lang]["seed_unresolved"] += 1
                continue

            if len(groups) == 1:
                (ret_lbl, members), = groups.items()
                mem_sorted = sorted(set(members), key=label_key)
                seed_steps = []
                for lbl in mem_sorted:
                    seed_steps.extend(blocks_by_label[lbl])
                seed_text = block_text(seed_steps)
                seeds[unit_id] = dict(
                    lang=lang, n=str(k), operator=u["meta"]["operator"],
                    status="ok", method="single-group",
                    seed_text=seed_text,
                    seed_blocks=mem_sorted,
                    matched_class=text_to_class.get(seed_text),
                    guards=guards)
                survey[lang]["seed_ok"] += 1
                continue

            # multiple disjoint computation groups -- the go/op_132
            # inline-alternate-path shape. Resolve by table lookup.
            candidates = {}
            for ret_lbl, members in groups.items():
                mem_sorted = sorted(set(members), key=label_key)
                seed_steps = []
                for lbl in mem_sorted:
                    seed_steps.extend(blocks_by_label[lbl])
                text = block_text(seed_steps)
                candidates[ret_lbl] = dict(members=mem_sorted, text=text,
                                            matched_class=text_to_class.get(text))

            matched = [rl for rl, c in candidates.items()
                       if c["matched_class"] is not None]

            if len(matched) == 1:
                seed_rl = matched[0]
                seed_c = candidates[seed_rl]
                extra_guards = []
                for rl, c in candidates.items():
                    if rl == seed_rl:
                        continue
                    gmap_extra = {}
                    # find the block(s) that ARE branch targets among
                    # this group's members, for divergence_conditions
                    for lbl in c["members"]:
                        gmap_extra[int(re.match(r"L(\d+)", lbl).group(1))] = \
                            block_text(blocks_by_label[lbl])
                    try:
                        unit_full = dict(lang=lang, n=str(k),
                                          bytes=u["bytes"], mnem=u["mnem"],
                                          meta=u["meta"])
                        conds = V.divergence_conditions(unit_full, gmap_extra)
                    except Exception as exc:
                        conds = [dict(text="condition lookup failed: %s" % exc)]
                    extra_guards.append(dict(
                        kind="inline-special-case",
                        response="inline-special-case",
                        detection="disjoint-return-group,"
                                   " unmatched-by-seed-table-lookup",
                        text=c["text"],
                        blocks=c["members"],
                        conditions=conds))
                seeds[unit_id] = dict(
                    lang=lang, n=str(k), operator=u["meta"]["operator"],
                    status="ok", method="multi-group-resolved-by-table",
                    seed_text=seed_c["text"],
                    seed_blocks=seed_c["members"],
                    matched_class=seed_c["matched_class"],
                    guards=guards + extra_guards)
                survey[lang]["seed_ok"] += 1
            else:
                seeds[unit_id] = dict(
                    lang=lang, n=str(k), operator=u["meta"]["operator"],
                    status="unresolved",
                    reason=("%d disjoint computation groups, %d matched "
                            "an existing 0-branch canonical text (need "
                            "exactly 1 to resolve which is the seed)"
                            % (len(candidates), len(matched))),
                    candidates=candidates,
                    guards=guards)
                reasons["ambiguous inline-alternate-path (0 or 2+ table matches)"] += 1
                survey[lang]["seed_unresolved"] += 1

    out = dict(
        meta=dict(
            generator="seed_extract1.py",
            method="see module docstring: trap guards from core_modes "
                   "(existing route), inline-alternate-path guards "
                   "resolved by exact-text lookup against the existing "
                   "1,641-unit 0-branch table (dominant_table21.json)",
        ),
        seeds=seeds)
    json.dump(out, open(os.path.join(HERE, "seeds1.json"), "w"), indent=1)

    survey_out = dict(by_lang=survey, unresolved_reasons=dict(reasons))
    json.dump(survey_out, open(os.path.join(HERE, "survey1.json"), "w"), indent=1)

    print(json.dumps(survey_out, indent=2))

    # worked example
    ex = seeds.get("go/op_132")
    print("\n--- worked example go/op_132 ---")
    print(json.dumps(ex, indent=2))


if __name__ == "__main__":
    main()
