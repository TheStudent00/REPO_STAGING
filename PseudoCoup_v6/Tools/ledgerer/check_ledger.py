"""Check ledger integrity invariants; nonzero exit on any failure.

Provenance: invariant set from
PRIVATE/StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/ledger_unified.py
check() (every id exactly once, entry count == independent recount,
nothing missing/extra), extended per the settled integrity node
(PRIVATE/PseudoCoup_v6/Planning/node_0_0_tools/node_0_0_0_ledgerer/SUPPORT_validation.md):
declaration-kind entries must carry a type or the explicit
"unresolvable" marker; the unresolvable count is a first-class
number.
"""
from build_ledger import DECLARATION_KINDS
from generate_ids import walk_file


def check(ledger, corpus_root):
    """-> report dict; report['ok'] is the verdict."""
    recs = ledger["records"]
    ids = [r["id"] for r in recs]
    report = {"entry_count": len(recs)}

    seen, dupes = set(), []
    for i in ids:
        (dupes if i in seen else seen).__contains__  # no-op guard
        if i in seen:
            dupes.append(i)
        seen.add(i)
    report["distinct_ids"] = len(seen)
    report["duplicate_ids"] = sorted(set(dupes))

    # independent recount from the same pinned corpus
    recount_named, missing, extra = 0, [], []
    fresh = set()
    for i, c in enumerate(ledger["meta"]["corpus"]):
        records, _ = walk_file(f"{corpus_root}/{c['file']}", c["grammar"],
                               f"{i}:source_file")
        recount_named += len(records)
        fresh.update(r.id for r in records)
    report["recount_named"] = recount_named
    report["missing_from_ledger"] = sorted(fresh - seen)[:20]
    report["extra_in_ledger"] = sorted(seen - fresh)[:20]

    unresolved, untyped_decls = 0, []
    for r in recs:
        g = next((c["grammar"] for c in ledger["meta"]["corpus"]
                  if c["file"] == r["file"]), None)
        if r["node_kind"] in DECLARATION_KINDS.get(g, set()):
            t = r["semantic"]["type"]
            if t == "unresolvable":
                unresolved += 1
            elif t is None:
                untyped_decls.append(r["id"])
    report["unresolvable_count"] = unresolved
    report["declarations_missing_type_field"] = untyped_decls[:20]

    report["ok"] = (not report["duplicate_ids"]
                    and len(recs) == recount_named
                    and not report["missing_from_ledger"]
                    and not report["extra_in_ledger"]
                    and not untyped_decls)
    return report
