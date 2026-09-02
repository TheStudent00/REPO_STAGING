#!/usr/bin/env python3
"""verdicts4.py -- the relations as COMPUTED COLUMNS over core+modes.

What changes from verdicts3
---------------------------
verdicts3 decided each pair by a cascade: bytes, then the anchored
lifted form, then a one-sided-guard reading, then z3.  The answer was a
verdict word, and the interesting part of `DIFFERS-BY-DESIGN` -- WHICH
mode one side has and the other has not -- lived inside a detail string.

Here every unit already carries a core and a list of modes
(`core_modes.py`), so the relation between two units is not decided at
all.  It is READ OFF the two records as a column:

  total equality            the cores are equal and the mode sets are
                            equal
  core equality, modes      the cores are equal and the mode sets are
  differ                    not.  The difference is carried AS DATA --
                            the list of modes one side has and the
                            other has not, each with its condition and
                            its response.  This is the fence.
  core difference           the cores are not equal

Rows are the SAME machine-form groups verdicts3 built, imported from
verdicts3 unchanged: a cluster of identical bytes or identical anchored
lifted forms, or a shared maximal sub-term over the anchored variables,
on one operand type pair.  No operator token takes part in choosing,
grouping or naming a row; each member carries its token as a display
label and nothing else does.  `check_no_spelling_keys.py` is run on the
output and a FAIL means the output is refused.

How two modes are compared, stated because it is a choice
---------------------------------------------------------
A mode is compared on (RESPONSE KIND, CONDITION).  The response kind is
the head of the response: `trap`, `panic-call`, `wrap-continue`,
`clamp-continue`, `continue-with-a-different-answer`.  The panic
callee's NAME is deliberately not part of the comparison: rust calls
`panic_const_div_by_zero` and swift traps, and those are two
languages' spellings for one behaviour -- the unit stops rather than
answering.  The callee name is carried on the mode and printed, so a
reader sees it; it just does not make two modes different by itself.

usage:
  verdicts4.py        write verdicts4.json and verdicts4.md
"""

import json
import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import verdicts as V                                          # noqa: E402
import verdicts3 as V3                                        # noqa: E402
import arch_sem as AS                                         # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]

TOTAL = "total equality"
FENCED = "core equality, modes differ"
CORE_DIFF = "core difference"


def load_core_modes():
    out = {}
    meta = {}
    for lang in LANGS:
        path = os.path.join(HERE, "core_modes_%s.json" % lang)
        doc = json.load(open(path))
        meta[lang] = dict(solver_run=doc.get("solver_run"),
                          lifter=doc.get("lifter"), z3=doc.get("z3"))
        for n, rec in doc["units"].items():
            out[(lang, n)] = rec
    return out, meta


def mode_key(mode):
    """what makes two modes the same mode."""
    kind = str(mode.get("response", "")).split(":")[0]
    return (kind, str(mode.get("condition", "")))


def mode_row(mode):
    """one mode, as it is printed in a fence list."""
    keep = dict(
        condition=mode.get("condition"),
        response=mode.get("response"),
        detection=mode.get("detection"),
    )
    if mode.get("mode_name"):
        keep["mode_name"] = mode["mode_name"]
    if mode.get("lands_in"):
        keep["lands_in"] = mode["lands_in"]
    if mode.get("read_from"):
        keep["read_from"] = mode["read_from"]
    if mode.get("contrast"):
        keep["contrast"] = mode["contrast"]
    return keep


def relate(ra, rb):
    """the column for one pair, and the fence where there is one."""
    same_core = ra["core"] == rb["core"]
    ka = {}
    for m in ra["modes"]:
        ka[mode_key(m)] = m
    kb = {}
    for m in rb["modes"]:
        kb[mode_key(m)] = m
    only_a = []
    for key in sorted(ka):
        if key not in kb:
            only_a.append(mode_row(ka[key]))
    only_b = []
    for key in sorted(kb):
        if key not in ka:
            only_b.append(mode_row(kb[key]))
    shared = []
    for key in sorted(ka):
        if key in kb:
            shared.append(mode_row(ka[key]))
    if same_core and not only_a and not only_b:
        column = TOTAL
    elif same_core:
        column = FENCED
    else:
        column = CORE_DIFF
    return dict(column=column, shared_modes=shared,
                modes_only_left=only_a, modes_only_right=only_b)


def label(rec):
    return "%s/op_%s" % (rec["lang"], rec["n"])


def main():
    units, excluded, excluded_rows = V.load_units()
    for u in units:
        u["subterms"] = V3.unit_subterms(u)
    by_id = {}
    for u in units:
        by_id[(u["lang"], u["n"])] = u

    records, cm_meta = load_core_modes()

    rows = []
    rows.extend(V3.cluster_groups(by_id))
    rows.extend(V3.connection_groups(units, by_id))

    tally = Counter()
    seen = {}
    out_rows = []
    for row in rows:
        by_lang = defaultdict(list)
        for m in row["members"]:
            by_lang[m["lang"]].append(m)
        langs = sorted(by_lang)
        pairs = []
        for i, la in enumerate(langs):
            for lb in langs[i + 1:]:
                for ua in by_lang[la]:
                    for ub in by_lang[lb]:
                        ra = records[(ua["lang"], ua["n"])]
                        rb = records[(ub["lang"], ub["n"])]
                        got = relate(ra, rb)
                        got["left"] = label(ra)
                        got["right"] = label(rb)
                        pairs.append(got)
                        key = (got["left"], got["right"])
                        seen[key] = got["column"]
        if not pairs:
            continue
        members = []
        for m in row["members"]:
            rec = records[(m["lang"], m["n"])]
            members.append(dict(
                lang=m["lang"], n=m["n"],
                operator=rec["operator"],
                type_pair=rec["type_pair"],
                mode_count=len(rec["modes"]),
            ))
        keep = dict(
            ground=row["ground"],
            name=V3.row_name(row),
            type_pair=row["type_pair"],
            languages=langs,
            members=members,
            pairs=pairs,
        )
        if row["ground"] == "cluster":
            keep["cluster_kind"] = row["cluster_kind"]
            keep["cluster_key"] = row["cluster_key"]
        else:
            keep["core"] = row["core"]
        out_rows.append(keep)

    for column in seen.values():
        tally[column] += 1

    mode_tally = Counter()
    unit_tally = Counter()
    for rec in records.values():
        if rec["modes"]:
            unit_tally["units with 1+ modes"] += 1
        else:
            unit_tally["units with 0 modes"] += 1
        for m in rec["modes"]:
            mode_tally[str(m.get("response", "")).split(":")[0]] += 1

    doc = dict(
        languages=LANGS,
        shape="relations as computed columns over core+modes",
        columns=[TOTAL, FENCED, CORE_DIFF],
        candidate_set="verdicts3's own machine-form groups, imported: "
                      "cluster identity or shared maximal sub-term, on "
                      "one operand type pair.  No operator token takes "
                      "part.",
        mode_comparison="two modes are the same when their response KIND "
                        "and their condition are the same; the panic "
                        "callee's name is carried and printed but does "
                        "not make two modes different by itself",
        units_considered=len(units),
        excluded=dict(excluded),
        excluded_rows=excluded_rows,
        rows=out_rows,
        distinct_pairs=len(seen),
        column_tally=dict(tally),
        mode_response_tally=dict(mode_tally),
        unit_tally=dict(unit_tally),
        core_modes=cm_meta,
        lifter=AS.LIFTER_ID,
    )
    json.dump(doc, open(os.path.join(HERE, "verdicts4.json"), "w"),
              indent=1)
    write_md(doc)

    print("== verdicts4: relations as columns over core+modes")
    print("   units considered   %d" % len(units))
    print("   rows               %d" % len(out_rows))
    print("   distinct pairs     %d" % len(seen))
    for column in (TOTAL, FENCED, CORE_DIFF):
        print("   %-26s %d" % (column, tally.get(column, 0)))
    print("   mode responses     %s" % dict(mode_tally))
    print("   units              %s" % dict(unit_tally))
    return 0


def write_md(doc):
    out = []
    out.append("# verdicts4 -- the relations as columns over core+modes")
    out.append("")
    out.append("Every unit is a CORE (the normal-path lifted form) and a "
               "list of MODES (condition, response, detection).  The "
               "relation between two units is not decided by a cascade; "
               "it is read off the two records.")
    out.append("")
    out.append("- `%s` -- the cores are equal and the mode sets are equal."
               % TOTAL)
    out.append("- `%s` -- the cores are equal and the mode sets are not.  "
               "The modes one side has and the other has not are printed "
               "as data.  That list is the fence." % FENCED)
    out.append("- `%s` -- the cores are not equal." % CORE_DIFF)
    out.append("")
    out.append("Rows are verdicts3's machine-form groups, imported.  A "
               "row is never named by an operator token; each member "
               "carries its token as a display label.")
    out.append("")
    out.append("- units considered: %d" % doc["units_considered"])
    out.append("- distinct unit pairs: %d" % doc["distinct_pairs"])
    out.append("- column tally: %s" % doc["column_tally"])
    out.append("- mode responses: %s" % doc["mode_response_tally"])
    out.append("- units: %s" % doc["unit_tally"])
    out.append("- lifter: %s" % doc["lifter"])
    out.append("")
    out.append("## the fences, gathered")
    out.append("")
    out.append("| left | right | mode | condition | response | detection |")
    out.append("| --- | --- | --- | --- | --- | --- |")
    seen = set()
    for row in doc["rows"]:
        for p in row["pairs"]:
            if p["column"] != FENCED:
                continue
            for side, modes in (("left", p["modes_only_left"]),
                                ("right", p["modes_only_right"])):
                for m in modes:
                    key = (p["left"], p["right"], side,
                           str(m.get("condition")), str(m.get("response")))
                    if key in seen:
                        continue
                    seen.add(key)
                    out.append("| %s | %s | on the %s | %s | %s | %s |"
                               % (p["left"], p["right"], side,
                                  str(m.get("condition")).replace("|", "/"),
                                  m.get("response"), m.get("detection")))
    out.append("")
    out.append("## rows")
    out.append("")
    for row in doc["rows"]:
        out.append("### %s" % row["name"])
        out.append("")
        out.append("- ground: %s" % row["ground"])
        out.append("- languages: %s" % ", ".join(row["languages"]))
        labels = []
        for m in row["members"]:
            labels.append("%s `%s` (%s, %d modes)"
                          % (m["lang"], m["operator"], m["type_pair"],
                             m["mode_count"]))
        out.append("- members: %s" % "; ".join(labels))
        out.append("")
        for p in row["pairs"]:
            out.append("  - %s / %s -- **%s**"
                       % (p["left"], p["right"], p["column"]))
            for side, modes in (("only on the left", p["modes_only_left"]),
                                ("only on the right",
                                 p["modes_only_right"])):
                for m in modes:
                    out.append("    - %s: `%s` -> `%s` (%s)"
                               % (side, m.get("condition"),
                                  m.get("response"), m.get("detection")))
        out.append("")
    path = os.path.join(HERE, "verdicts4.md")
    open(path, "w").write("\n".join(out))


if __name__ == "__main__":
    sys.exit(main())
