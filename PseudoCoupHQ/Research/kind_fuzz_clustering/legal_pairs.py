"""Phase 0, step 2 of kind_fuzz_clustering: the legal-triple table.

The CORE names this table as what replaces blind n^2 enumeration: for
each language, every (host kind, slot role, filler kind) triple that
`node-types.json` declares to be legal.  A slot role is a key of the
entry's `fields` map; the entry's `children` key is one further slot
with no role name, reported under the role label "*".

Two readings of the same table are produced:

- DECLARED — the filler exactly as the grammar writes it.  A declared
  filler may be a supertype (`expression`), which is not a kind that can
  ever be written into a script.
- RESOLVED — every supertype replaced by the concrete kinds it stands
  for, transitively.  This is the population a probe generator can
  actually emit.

Only the declared triples are stored in full; the resolved reading is
recovered from them with `supertype_closure`, which is stored beside
them.  Both counts are reported.
"""

import json
import os

from extract_kinds import (
    BONUS, HERE, LANGUAGES, TARGETS, UNNAMED_SLOT,
    classify, load_entries, slots_of,
)


def entry_index(entries):
    return {entry["type"]: entry for entry in entries}


def build_closure(entries):
    """supertype name -> the concrete kinds it stands for, transitively.

    A supertype is an entry carrying `subtypes`.  Hidden kinds (leading
    underscore) are supertypes in all twelve grammars measured here, so
    no separate inlining rule is needed.
    """
    index = entry_index(entries)
    closure = {}

    def resolve(name, seen):
        entry = index.get(name)
        if entry is None or "subtypes" not in entry:
            return {name}
        if name in seen:
            return set()
        seen = seen | {name}
        out = set()
        for sub in entry["subtypes"]:
            out |= resolve(sub["type"], seen)
        return out

    for entry in entries:
        if "subtypes" in entry:
            closure[entry["type"]] = sorted(resolve(entry["type"], set()))
    return closure


def declared_triples(entries):
    """Every (host, role, filler, filler_named) the grammar declares."""
    triples = []
    for entry in entries:
        if not entry.get("named"):
            continue
        host = entry["type"]
        for role, types in slots_of(entry):
            for filler in types:
                triples.append(
                    [host, role, filler["type"],
                     "named" if filler["named"] else "anon"]
                )
    return triples


def resolved_triples(triples, closure):
    """Declared triples with supertype fillers replaced by concrete kinds."""
    out = set()
    for host, role, filler, flag in triples:
        if flag == "named" and filler in closure:
            for concrete in closure[filler]:
                out.add((host, role, concrete))
        else:
            out.add((host, role, filler))
    return sorted(out)


def build(language):
    entries = load_entries(language)
    parts = classify(entries)
    closure = build_closure(entries)
    declared = declared_triples(entries)
    resolved = resolved_triples(declared, closure)
    hosts = sorted({t[0] for t in declared})
    slots = sorted({(t[0], t[1]) for t in declared})
    return {
        "language": language,
        "root": parts["root"],
        "counts": {
            "hosts_with_slots": len(hosts),
            "slots": len(slots),
            "declared_triples": len(declared),
            "resolved_triples": len(resolved),
        },
        "supertype_closure": closure,
        "declared_triples": declared,
    }


def main():
    for language in TARGETS + BONUS:
        table = build(language)
        out = os.path.join(HERE, "legal_pairs_%s.json" % language)
        with open(out, "w") as handle:
            json.dump(table, handle, indent=1, sort_keys=True)
        counts = table["counts"]
        print(
            "%-11s hosts_with_slots=%4d slots=%5d declared=%6d resolved=%7d"
            % (
                language, counts["hosts_with_slots"], counts["slots"],
                counts["declared_triples"], counts["resolved_triples"],
            )
        )
    print("(role label %r marks tree-sitter's unnamed `children` slot)"
          % UNNAMED_SLOT)
    print("grammar files read from %s" % os.path.join(HERE, os.pardir,
                                                      "kind_signature_clustering",
                                                      "raw_all"))
    print("languages: %s" % ", ".join(sorted(LANGUAGES)))


if __name__ == "__main__":
    main()
