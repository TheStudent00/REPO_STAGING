"""Phase 0, step 1 of kind_fuzz_clustering: per-language kind extraction.

Reads each target language's `node-types.json` (already on disk, fetched
2026-08-12 by the co-node kind_signature_clustering) and emits
`kinds_<language>.json`: the named kinds, the supertypes and their
sub-kind lists, the hidden kinds, and the anonymous tokens.

Vocabulary note: tree-sitter's own JSON key `children` is quoted here as
its key name only.  In our own prose a slot holding sub-nodes is the
UNNAMED SLOT, written with the role label "*".

Nothing here executes a probe or decides a probe's shape.  Measurement
only.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(HERE, os.pardir, "kind_signature_clustering", "raw_all")
OUT_DIR = HERE

# language -> file stem in RAW_DIR.  typescript and php ship dialects;
# the stem chosen is recorded in the phase-0 log as a numbered decision.
LANGUAGES = {
    "python": "python",
    "typescript": "typescript__typescript",
    "java": "java",
    "csharp": "c-sharp",
    "go": "go",
    "rust": "rust",
    "ruby": "ruby",
    "php": "php__php",
    "kotlin": "kotlin",
    "cpp": "cpp",
    "dart": "dart",
    "swift": "swift",
}

TARGETS = [
    "python", "typescript", "java", "csharp", "go", "rust",
    "ruby", "php", "kotlin", "cpp", "dart",
]
BONUS = ["swift"]

UNNAMED_SLOT = "*"


def grammar_path(language):
    return os.path.join(RAW_DIR, LANGUAGES[language] + ".node-types.json")


def load_entries(language):
    with open(grammar_path(language)) as handle:
        return json.load(handle)


def is_hidden(type_name):
    """tree-sitter hides kinds whose name starts with an underscore."""
    return type_name.startswith("_")


def slots_of(entry):
    """Every declared slot of one entry, as (role, [declared filler types]).

    A role comes from a key of the entry's `fields` map.  The entry's
    `children` key is one further slot that carries no role name; it is
    reported under the role label "*".
    """
    slots = []
    for role in sorted(entry.get("fields", {})):
        slots.append((role, entry["fields"][role].get("types", [])))
    if "children" in entry:
        slots.append((UNNAMED_SLOT, entry["children"].get("types", [])))
    return slots


def anonymous_tokens_in_slots(entries):
    """Anonymous tokens that node-types.json places in some slot.

    An anonymous token absent from this set still exists in the grammar
    (it is listed as a top-level entry) but the file does not say which
    host kind it attaches to.
    """
    seen = set()
    for entry in entries:
        for _role, types in slots_of(entry):
            for filler in types:
                if not filler["named"]:
                    seen.add(filler["type"])
    return seen


def classify(entries):
    """Split one grammar's entries into the populations phase 0 counts."""
    named_concrete = []
    supertypes = {}
    hidden = []
    anonymous = []
    root = None
    for entry in entries:
        name = entry["type"]
        if entry.get("root"):
            root = name
        if not entry.get("named"):
            anonymous.append(name)
            continue
        if "subtypes" in entry:
            supertypes[name] = [s["type"] for s in entry["subtypes"]]
            if is_hidden(name):
                hidden.append(name)
            continue
        if is_hidden(name):
            hidden.append(name)
            continue
        named_concrete.append(name)
    return {
        "root": root,
        "named_concrete": sorted(set(named_concrete)),
        "supertypes": {k: sorted(set(v)) for k, v in supertypes.items()},
        "hidden": sorted(set(hidden)),
        "anonymous": sorted(set(anonymous)),
    }


def extract(language):
    entries = load_entries(language)
    parts = classify(entries)
    positioned = anonymous_tokens_in_slots(entries)
    parts["anonymous_positioned"] = sorted(positioned)
    parts["anonymous_unpositioned"] = sorted(
        set(parts["anonymous"]) - positioned
    )
    parts["counts"] = {
        "entries": len(entries),
        "named_concrete": len(parts["named_concrete"]),
        "supertypes": len(parts["supertypes"]),
        "hidden": len(parts["hidden"]),
        "anonymous": len(parts["anonymous"]),
        "anonymous_positioned": len(parts["anonymous_positioned"]),
        "anonymous_unpositioned": len(parts["anonymous_unpositioned"]),
    }
    parts["language"] = language
    parts["source"] = os.path.relpath(grammar_path(language), HERE)
    return parts


def main():
    rows = []
    for language in TARGETS + BONUS:
        parts = extract(language)
        out = os.path.join(OUT_DIR, "kinds_%s.json" % language)
        with open(out, "w") as handle:
            json.dump(parts, handle, indent=1, sort_keys=True)
        counts = parts["counts"]
        rows.append((language, counts, parts["root"]))
        print(
            "%-11s root=%-17s named=%4d supertypes=%3d hidden=%3d "
            "anon=%4d (positioned %3d / unpositioned %3d)"
            % (
                language, parts["root"], counts["named_concrete"],
                counts["supertypes"], counts["hidden"], counts["anonymous"],
                counts["anonymous_positioned"],
                counts["anonymous_unpositioned"],
            )
        )
    total_named = sum(c["named_concrete"] for _l, c, _r in rows
                      if _l in TARGETS)
    total_anon = sum(c["anonymous"] for _l, c, _r in rows if _l in TARGETS)
    print("11 targets: named %d, anonymous %d" % (total_named, total_anon))


if __name__ == "__main__":
    main()
