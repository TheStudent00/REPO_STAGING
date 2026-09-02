#!/usr/bin/env python3
"""sem_anchored_spill.py -- wrapper around sem_anchored.py that fixes the
SPILL/RELOAD gap tree_match.py's report identified: a unit that computes
its answer in one straight-line block and carries it into the block that
actually returns it (either through a register that block never itself
writes, or through a stack slot spilled in one block and reloaded in
another) showed the RET block's bare, unresolved reference instead of the
real computation, because `sem_anchored.py` (by way of arch_sem.py's
`_sweep`) resets ALL machine state -- registers AND the store list -- at
every block boundary.  That reset is deliberate upstream (arch_sem.py's
`blocks_of` docstring: a trailing panic path must not be swept as part of
the straight line and clobber the real answer), so this file does not
edit arch_sem.py or sem_anchored.py.  It reruns their same sweep,
unit by unit, and adds exactly one thing on top: a CARRY map, built by
walking the unit's blocks in address order and recording, for every
register a block writes and every address a block stores to, the
(already-substituted) expression it holds -- so that a later block's read
of that register, or a load from that address, is not left as a bare
`uN`/`ld(...)` leaf; it is replaced by the expression the machine actually
put there.

THE LIMITATION, STATED HONESTLY.  The carry is ADDRESS-ORDER, LAST-WRITE-
WINS, not a real dominance/reaching-definitions analysis over the arch
unit's actual control-flow graph.  For every unit this file was built
against (go/op_132, rust/op_678, and the wider sweep below), the pattern
is a special-case shortcut block, emitted FIRST at a lower address,
merging into the general-path answer, emitted SECOND at a higher address,
at the return block -- so "last write in address order" already picks the
general path, which is the normal-path answer tree_match.py wants.  It is
NOT a sound fixed point over an arbitrary CFG with back edges; a unit
whose true dataflow disagrees with address order would be given the wrong
carried value silently, which is why this file is a SEPARATE, NAMED
wrapper rather than a silent change to sem_anchored.py's own output.

THE SPELLING BAN: nothing here keys, groups, or selects candidates by
`operator`.  The carry map is keyed by register name / address
expression -- machine evidence -- and `operator` is read only as a
display label when a unit is emitted to the meta record.
"""

import copy
import json
import os
import re
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
KFC = os.path.join(os.path.dirname(HERE), "kind_fuzz_clustering")
sys.path.insert(0, KFC)
sys.path.insert(0, HERE)

import arch_read as AR                                        # noqa: E402
import arch_sem as AS                                         # noqa: E402
import sem_anchored as SA                                      # noqa: E402

LANGS = SA.LANGS


# --------------------------------------------------------------------
# the carry substitution -- walks the same tuple shapes arch_sem.py's
# own `_map`/`_rebuild` walk (raw, pre-anchoring: 'r' leaves still name
# a physical register).
# --------------------------------------------------------------------

def subst(e, regmap, storelist):
    k = e[0]
    if k == "r":
        name = e[2]
        if name in regmap:
            return regmap[name]
        return e
    if k in ("c", "op"):
        return e
    if k == "ld":
        addr = subst(e[3], regmap, storelist)
        w = e[1]
        for a, sw, v in reversed(storelist):
            if sw == w and a == addr:
                return v
        if addr is e[3]:
            return e
        return ("ld", e[1], e[2], addr)
    if k == "ex":
        return ("ex", e[1], e[2], subst(e[3], regmap, storelist))
    if k in ("zx", "sx"):
        return (k, e[1], subst(e[2], regmap, storelist))
    if k == "ins":
        return ("ins", e[1], subst(e[2], regmap, storelist),
                subst(e[3], regmap, storelist), e[4])
    if k == "b":
        return ("b", e[1], e[2], subst(e[3], regmap, storelist),
                subst(e[4], regmap, storelist))
    if k == "u":
        return ("u", e[1], e[2], subst(e[3], regmap, storelist))
    if k in ("t", "q"):
        return (k, e[1], e[2]) + tuple(subst(x, regmap, storelist)
                                        for x in e[3:])
    if k == "ite":
        return ("ite", e[1], subst(e[2], regmap, storelist),
                subst(e[3], regmap, storelist),
                subst(e[4], regmap, storelist))
    if k == "cc":
        return ("cc", e[1], e[2], tuple(subst(x, regmap, storelist)
                                         for x in e[3]))
    return e


BTGT = re.compile(r"^B(\d+)$")


def block_edges(sweeps, n):
    """successor edges, read off each block's own recorded events -- the
    same machine evidence `blocks_of` itself is built from (jmp/branch
    targets, a `ret`), plus the FALLTHROUGH edge to the next block when
    nothing in a block's events claims it ends the straight line (a
    branch's not-taken side, or a block that simply runs out because the
    next block starts there for some OTHER block's jump).  A block that
    ends unconditionally (`jmp`, `ret`) gets no fallthrough edge."""
    edges = {i: [] for i in range(n)}
    for i, st in enumerate(sweeps):
        has_jmp = False
        has_ret = False
        for ev in st.events:
            if ev[0] == "jmp":
                has_jmp = True
                m = BTGT.match(ev[1])
                if m:
                    edges[i].append(int(m.group(1)))
            elif ev[0] == "branch":
                m = BTGT.match(ev[2])
                if m:
                    edges[i].append(int(m.group(1)))
            elif ev[0] == "ret":
                has_ret = True
        if not has_jmp and not has_ret and i + 1 < n:
            edges[i].append(i + 1)
    return edges


def predecessors(edges, n):
    pred = {i: [] for i in range(n)}
    for src, dsts in edges.items():
        for d in dsts:
            pred[d].append(src)
    return pred


def tree_size_raw(e):
    kids = {"ex": (3,), "zx": (2,), "sx": (2,), "ins": (2, 3), "b": (3, 4),
            "u": (3,), "ite": (2, 3, 4), "ld": (3,)}.get(e[0])
    if kids:
        return 1 + sum(tree_size_raw(e[i]) for i in kids)
    if e[0] in ("t", "q"):
        return 1 + sum(tree_size_raw(x) for x in e[3:])
    if e[0] == "cc":
        return 1 + sum(tree_size_raw(x) for x in e[3])
    return 1


def carrying_summaries(insns, texts, index, block_index, spans):
    """path-sensitive carry: a block with exactly one predecessor inherits
    that predecessor's exit state exactly (no ambiguity -- this is the
    spill/reload case: a value written in the one block that can reach
    here is read back here).  A block with SEVERAL predecessors (a real
    merge -- e.g. a special-cased shortcut path rejoining the general
    path right before the return) is evaluated ONCE PER predecessor
    variant, and the variant whose own filtered values are the largest
    tree is kept -- the same "largest tree is the real computation, a
    guard's shortcut is smaller" evidence tree_match.py's own fallback
    rule already rests on, just applied per predecessor instead of per
    block.  A block with NO predecessor (block 0, or an unreachable one)
    starts from a clean state, exactly as arch_sem.py itself does."""
    n = len(spans)
    sweeps = [AS._sweep(insns, texts, index, block_index, lo, hi)
              for lo, hi in spans]
    edges = block_edges(sweeps, n)
    pred = predecessors(edges, n)

    # incoming[i]: list of (regmap, storelist) variants reaching block i.
    incoming = {0: [({}, [])]}
    outgoing = {}          # i -> list of (regmap, storelist) after block i
    summaries = [None] * n
    carry_notes = [False] * n

    order = list(range(n))     # address order; no back edges expected
    for i in order:
        st = sweeps[i]
        variants_in = incoming.get(i)
        if not variants_in:
            variants_in = [({}, [])]
        results = []
        for regmap0, storelist0 in variants_in:
            resolved_reg = {}
            changed = False
            for name in st.written:
                v = st.reg.get(name)
                if v is None:
                    continue
                rv = subst(v, regmap0, storelist0)
                resolved_reg[name] = rv
                if rv != v:
                    changed = True
            resolved_stores = []
            for a, w, v in st.stores:
                ra = subst(a, regmap0, storelist0)
                rv = subst(v, regmap0, storelist0)
                resolved_stores.append((ra, w, rv))
            fake = types.SimpleNamespace(written=st.written,
                                          reg=resolved_reg,
                                          stores=resolved_stores,
                                          events=st.events)
            vals, stores_out, events = AS.summarize(fake)
            new_regmap = dict(regmap0)
            new_regmap.update(resolved_reg)
            new_storelist = list(storelist0) + resolved_stores
            size = sum(tree_size_raw(v) for v in
                       [x for x in fake.reg.values()]) if fake.reg else 0
            results.append(dict(vals=vals, stores=stores_out, events=events,
                                 regmap=new_regmap, storelist=new_storelist,
                                 changed=changed, size=size))
        best = max(results, key=lambda r: r["size"])
        summaries[i] = (best["vals"], best["stores"], best["events"])
        carry_notes[i] = best["changed"]
        outgoing[i] = [(r["regmap"], r["storelist"]) for r in results]
        for dst in edges[i]:
            incoming.setdefault(dst, [])
            incoming[dst].extend(outgoing[i])
    return summaries, carry_notes


def raw_summaries_spill(unit, lang, meta):
    names = SA.anchor_names(lang, meta)
    if names is None:
        return None, None, "no ABI classification for the parameter types"
    lay, reason = SA.layout(unit)
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
    summaries, carry_notes = carrying_summaries(insns, texts, index,
                                                 block_index, spans)
    return summaries, names, None, carry_notes


def semantics_spill(unit, lang, meta):
    summaries, names, reason, carry_notes = (None, None, None, None)
    result = raw_summaries_spill(unit, lang, meta)
    summaries, names, reason = result[0], result[1], result[2]
    carry_notes = result[3] if len(result) > 3 else None
    if summaries is None:
        return dict(ok=False, reason=reason)
    parts, names_out = SA.render_anchored(summaries, names)
    key = "  ".join(p["text"] for p in parts)
    values = [x for p in parts for x in p["values"]]
    stores = [x for p in parts for x in p["stores"]]
    events = [x for p in parts for x in p["events"]]
    any_carry = any(carry_notes) if carry_notes else False
    return dict(ok=True, blocks=parts, values=values, stores=stores,
                events=events, key=key, carried=any_carry,
                anchor_registers=dict((v, k) for k, v in names_out.items()
                                      if v.startswith("in")),
                block_count=len(parts))


# ================================================================== drive

def annotate(lang, verbose=True):
    doc = SA.load(lang)
    out = {}
    ok = 0
    carried_count = 0
    failed = {}
    for n, probe in doc["probes"].items():
        ship = probe.get("ship")
        if not ship:
            continue
        meta = probe["meta"]
        try:
            sem = semantics_spill(ship, lang, meta)
        except Exception as exc:                              # noqa: BLE001
            sem = dict(ok=False,
                       reason="%s: %s" % (type(exc).__name__, exc))
        if sem["ok"]:
            ok += 1
            if sem.get("carried"):
                carried_count += 1
        else:
            failed[sem["reason"]] = failed.get(sem["reason"], 0) + 1
        out[n] = dict(meta=meta, sem=sem,
                      bytes=" ".join(ship["bytes"]),
                      mnem=ship["mnem"])
    doc_out = dict(language=lang, lifter=AS.LIFTER_ID,
                   wrapper="sem_anchored_spill (carry-forward substitution)",
                   units=out, ok=ok, failed=len(out) - ok,
                   carried_units=carried_count,
                   failure_reasons=failed)
    path = os.path.join(HERE, "sem_anchored_spill_%s.json" % lang)
    json.dump(doc_out, open(path, "w"), indent=1)
    if verbose:
        print("== %-6s %d ship units, %d anchored sem, %d refused, "
              "%d carried a cross-block substitution"
              % (lang, len(out), ok, len(out) - ok, carried_count))
    return doc_out


def main():
    for lang in LANGS:
        annotate(lang)
    return 0


if __name__ == "__main__":
    sys.exit(main())
