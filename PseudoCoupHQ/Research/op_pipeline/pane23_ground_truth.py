#!/usr/bin/env python3
"""pane23_ground_truth.py -- task 70's OFF-PAGE ARITHMETIC.

Node: hq.research.compiler_graph.dashboard, methods `selector` and
`opcode_index`.

This script is NOT part of the dashboard and the dashboard does not know
it exists.  It computes, in python and over the same files on disk, the
numbers the live page must show for panes 2 and 3 over the FULL
population: the signature index, the selector's menus, and the arch
opcode index.  The browser's own numbers are then compared to these.
Where they differ, the page is wrong.

THE SPELLING BAN.  Nothing here is keyed, grouped, paired or selected by
an operator token.  The grouping key is `lang + '#' + opGroup + '#' +
sig`, where opGroup is the opaque per-language id the page mints
(`c#g07`).  The token is carried once per unit, as `label`, and the
emitted json is walked by the unmodified check_no_spelling_keys.py.
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["c", "cpp", "go", "rust", "swift"]


def load(name):
    with open(os.path.join(HERE, name)) as fh:
        return json.load(fh)


def units_of(doc):
    u = doc.get("units", doc)
    if isinstance(u, dict):
        out = []
        for k, row in u.items():
            if isinstance(row, dict) and not row.get("unit"):
                row["unit"] = k
            out.append(row)
        return out
    return list(u)


LEADING_MNEM = __import__("re").compile(r"^\s*([a-z][a-z0-9]*)")


def mnems_of(unit):
    out = set()
    for row in unit.get("ledger") or []:
        p = row.get("produced_by") or {}
        if p.get("kind") == "arch_opcode":
            out.add(p.get("mnem"))
        elif p.get("kind") == "flag_pair":
            for m in p.get("mnem") or []:
                out.add(m)
        elif p.get("kind") == "runtime_callee":
            out.add("call")
    for line in unit.get("body_as_read") or []:
        m = LEADING_MNEM.match(line)
        if m:
            out.add(m.group(1))
    return sorted(x for x in out if x)


class OperatorGroups(object):
    """the page's opaque id, minted per language in first-appearance
    order.  Generator provenance, read once; never a comparison key."""

    def __init__(self):
        self.by_lang = {}

    def mint(self, lang, token):
        if token is None or token == "":
            return None
        seen = self.by_lang.setdefault(lang, {})
        if token not in seen:
            seen[token] = "%s#g%02d" % (lang, len(seen))
        return seen[token]


def signature_of(probe, out_size):
    """DashboardJoin.signatureOf, in python.  The probe's declared types,
    with the result read off the OUT row's own width when the compiler
    did not state it."""
    if probe is None:
        return None
    lhs = probe[0]
    rhs = probe[1]
    res = probe[2]
    if not res:
        if out_size is not None:
            res = "%d-bit" % (out_size * 8)
        else:
            res = "compiler-stated"
    if rhs:
        return "(a: %s, b: %s) -> %s" % (lhs, rhs, res)
    return "(a: %s) -> %s" % (lhs, res)


def read_manifest(name):
    """only the three declared type fields, keyed by probe number."""
    path = os.path.join(HERE, name)
    if not os.path.exists(path):
        return None
    doc = load(name)
    probes = doc.get("probes") or {}
    if isinstance(probes, list):
        probes = {str(p.get("n")): p for p in probes}
    out = {}
    for k, p in probes.items():
        out[str(k)] = (p.get("lhs_type"), p.get("rhs_type"),
                       p.get("result_type"))
    return out


def main():
    manifests = {}
    manifest_files = 0
    for lang in LANGS:
        for pop, stem in (("original", "probe_manifest_"),
                          ("regenerated", "probe_manifest2_")):
            m = read_manifest(stem + lang + ".json")
            if m is not None:
                manifests[(lang, pop)] = m
                manifest_files += 1
    print("manifests: %d files, %s"
          % (manifest_files,
             ", ".join("%s/%s=%d probes" % (k[0], k[1], len(v))
                       for k, v in sorted(manifests.items()))))

    jobs = [("canon39_wrapped_%s.json" % lang) for lang in LANGS]
    jobs.append("canon39_interp.json")
    regen = sorted(os.path.basename(p) for p in
                   glob.glob(os.path.join(HERE, "canon39_regen_store",
                                          "*.json")))
    jobs += [os.path.join("canon39_regen_store", n) for n in regen]

    groups = OperatorGroups()
    rows = []
    opcode_rows = {}
    for job in jobs:
        doc = load(job)
        for u in units_of(doc):
            uid = u.get("unit")
            if not uid:
                continue
            lang = u.get("lang") or uid.split("/")[0]
            pop = u.get("population")
            outs = [r for r in (u.get("ledger") or [])
                    if str(r.get("row", "")).startswith("OUT")]
            out_size = outs[0].get("size") if outs else None
            probe = None
            man = manifests.get((lang, pop))
            if man is not None and u.get("n") is not None:
                probe = man.get(str(u.get("n")))
            rows.append({
                "id": uid,
                "lang": lang,
                "opGroup": groups.mint(lang, u.get("operator")),
                "label": u.get("operator"),
                "sig": signature_of(probe, out_size),
                "pop": pop,
                "outcome": u.get("outcome"),
                "has_ledger": bool(u.get("ledger")),
            })
            for m in mnems_of(u):
                opcode_rows.setdefault(m, []).append(uid)

    n = len(rows)
    with_sig = [r for r in rows if r["sig"]]
    without = [r for r in rows if not r["sig"]]
    by_lang = {}
    for r in rows:
        b = by_lang.setdefault(r["lang"], {"units": 0, "sig": 0, "groups": set(),
                                           "sigs": set()})
        b["units"] += 1
        if r["sig"]:
            b["sig"] += 1
            b["sigs"].add(r["sig"])
        if r["opGroup"]:
            b["groups"].add(r["opGroup"])

    cause = {}
    for r in without:
        key = "%s / population %s" % (r["lang"], r["pop"])
        cause[key] = cause.get(key, 0) + 1

    # the opcode index, grouped the way the pane groups it
    pane_groups = {}
    by_id = {r["id"]: r for r in rows}
    for mnem, ids in opcode_rows.items():
        ks = set()
        for uid in ids:
            r = by_id.get(uid)
            if not r:
                continue
            ks.add("%s#%s#%s" % (r["lang"], r["opGroup"] or "no-group",
                                 r["sig"] or "no-signature-recorded"))
        pane_groups[mnem] = len(ks)

    print("")
    print("POPULATION: %d arch-units, from %d files" % (n, len(jobs)))
    print("  units with a signature      %d of %d" % (len(with_sig), n))
    print("  units with no signature     %d of %d" % (len(without), n))
    for k in sorted(cause):
        print("      %-34s %d" % (k, cause[k]))
    print("  distinct signatures         %d over %d units"
          % (len({r["sig"] for r in with_sig}), len(with_sig)))
    print("  distinct operator groups    %d over %d units"
          % (len({r["opGroup"] for r in rows if r["opGroup"]}), n))
    print("  languages in the selector   %d" % len(by_lang))
    print("  units with no ledger        %d of %d"
          % (len([r for r in rows if not r["has_ledger"]]), n))
    print("")
    print("  %-10s %8s %8s %8s %8s" % ("language", "units", "with sig",
                                       "groups", "sigs"))
    for lang in sorted(by_lang, key=lambda k: -by_lang[k]["units"]):
        b = by_lang[lang]
        print("  %-10s %8d %8d %8d %8d"
              % (lang, b["units"], b["sig"], len(b["groups"]), len(b["sigs"])))
    print("")
    print("OPCODE INDEX: %d distinct arch opcodes over %d units"
          % (len(opcode_rows), n))
    top = sorted(opcode_rows, key=lambda k: -len(opcode_rows[k]))[:12]
    print("  %-10s %10s %10s" % ("opcode", "units", "groups"))
    for m in top:
        print("  %-10s %10d %10d" % (m, len(opcode_rows[m]), pane_groups[m]))
    print("  total (lang, operator-group, signature) groups over all "
          "opcodes: %d" % sum(pane_groups.values()))

    out = {
        "meta": {
            "role": "task 70 ground truth for panes 2 and 3",
            "population": "every arch-unit on disk: %d units from %d files"
                          % (n, len(jobs)),
        },
        "counts": {
            "units": n,
            "units_with_a_signature": len(with_sig),
            "units_with_no_signature": len(without),
            "distinct_signatures": len({r["sig"] for r in with_sig}),
            "distinct_operator_groups":
                len({r["opGroup"] for r in rows if r["opGroup"]}),
            "languages": len(by_lang),
            "arch_opcode_count": len(opcode_rows),
            "files_read": len(jobs) + manifest_files,
        },
        "by_language": {
            k: {"units": v["units"], "units_with_a_signature": v["sig"],
                "operator_groups": len(v["groups"]),
                "signatures": len(v["sigs"])}
            for k, v in by_lang.items()
        },
        "no_signature_by_cause": cause,
        # THE ARCH OPCODE INDEX, AS A LIST OF ROWS AND NOT A KEYED MAP.
        # Four x86 mnemonics -- `and`, `or`, `xor`, `not` -- are
        # HOMOGRAPHS of C++'s alternative operator tokens, which are in
        # the 91-token inventory.  A mnemonic is machine-form evidence
        # read out of objdump and is exactly what the ban says a
        # candidate set may come from, but a json DICT KEY cannot carry
        # that distinction and the unmodified guard is right to refuse
        # it.  So the mnemonic rides as `mnem`, a value on a row, and
        # the row is keyed by an opaque arch id.
        "arch_opcodes": [
            {"arch_id": "arch#%03d" % i, "mnem": m,
             "units": len(opcode_rows[m]), "groups": pane_groups[m]}
            for i, m in enumerate(sorted(opcode_rows))
        ],
        "index": rows,
    }
    with open(os.path.join(HERE, "pane23_ground_truth.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("")
    print("wrote pane23_ground_truth.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
