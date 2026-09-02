"""Phase 0, step 3 of kind_fuzz_clustering: the probe space and its size.

THE COUNTING RULE, stated before the number it produces:

    R1 (the base rule).  One probe is one (host kind, slot, dominant)
    triple, where the slot is a declared slot of the host kind and the
    dominant is one of the six verified data structures — boolean,
    float, integer, string, list, dict — that `node-types.json` declares
    may legally stand in that slot, as a literal of that dominant.

    A slot that no dominant can fill contributes no probe.  A host kind
    with no such slot contributes no probe at all; it is UNPROBEABLE
    under R1 and is counted separately rather than silently dropped.

    R2 (the operator extension, offered beside R1, not folded into it).
    A slot whose declared fillers are all anonymous tokens and number
    two or more is a TOKEN-CHOICE slot: the grammar is saying the host
    holds one operator out of a fixed menu.  `binary_expression` with
    thirteen operators is one host under R1 but thirteen distinct
    measurements — `1 + 2` and `1 * 2` are not the same probe.  Under
    R2 a host's R1 probes are multiplied by the size of its token menu.

The dominant-to-kind map below is the one judgment call phase 0 could
not avoid: which kind of each grammar IS a literal of each dominant.
Every entry is checked against the grammar's own kind list, and any
entry naming a kind the grammar does not have is reported as a miss.

Depth is measured on the containment graph: an edge runs from a host
kind to a kind that may legally fill one of its slots, supertypes
resolved.  Depth 1 means the kind is legal directly at the grammar's
root, so a probe needs no enclosing kind.  Depth 2 means one enclosing
kind is needed — the owner's `break` inside `for`.  Depth 3+ is the tail the
CORE anticipates having to hand-write.
"""

import json
import os
from collections import deque

from extract_kinds import (
    BONUS, HERE, TARGETS, classify, load_entries, slots_of,
)
from legal_pairs import build_closure, declared_triples, resolved_triples

DOMINANTS = ["boolean", "float", "integer", "string", "list", "dict"]

# dominant -> the kinds of that grammar that ARE a literal of it.
# An empty list means the grammar has no literal for that dominant; the
# dominant is then unreachable by R1 in that language, which is a
# measured fact about the grammar, not a gap in the method.
DOMINANT_KINDS = {
    "python": {
        "boolean": ["true", "false"], "integer": ["integer"],
        "float": ["float"], "string": ["string"], "list": ["list"],
        "dict": ["dictionary"],
    },
    "typescript": {
        "boolean": ["true", "false"], "integer": ["number"],
        "float": ["number"], "string": ["string", "template_string"],
        "list": ["array"], "dict": ["object"],
    },
    "java": {
        "boolean": ["true", "false"], "integer": ["decimal_integer_literal"],
        "float": ["decimal_floating_point_literal"],
        "string": ["string_literal"], "list": ["array_initializer"],
        "dict": [],
    },
    "csharp": {
        "boolean": ["boolean_literal"], "integer": ["integer_literal"],
        "float": ["real_literal"],
        "string": ["string_literal", "verbatim_string_literal"],
        "list": ["collection_expression", "initializer_expression"],
        "dict": [],
    },
    "go": {
        "boolean": ["true", "false"], "integer": ["int_literal"],
        "float": ["float_literal"],
        "string": ["interpreted_string_literal", "raw_string_literal"],
        "list": ["composite_literal"], "dict": ["composite_literal"],
    },
    "rust": {
        "boolean": ["boolean_literal"], "integer": ["integer_literal"],
        "float": ["float_literal"], "string": ["string_literal"],
        "list": ["array_expression"], "dict": [],
    },
    "ruby": {
        "boolean": ["true", "false"], "integer": ["integer"],
        "float": ["float"], "string": ["string"], "list": ["array"],
        "dict": ["hash"],
    },
    "php": {
        "boolean": ["boolean"], "integer": ["integer"], "float": ["float"],
        "string": ["string", "encapsed_string"],
        "list": ["array_creation_expression"],
        "dict": ["array_creation_expression"],
    },
    "kotlin": {
        "boolean": [], "integer": ["number_literal"],
        "float": ["float_literal"],
        "string": ["string_literal", "multiline_string_literal"],
        "list": ["collection_literal"], "dict": [],
    },
    "cpp": {
        "boolean": ["true", "false"], "integer": ["number_literal"],
        "float": ["number_literal"],
        "string": ["string_literal", "concatenated_string"],
        "list": ["initializer_list"], "dict": [],
    },
    "dart": {
        "boolean": ["true", "false"], "integer": ["decimal_integer_literal"],
        "float": ["decimal_floating_point_literal"],
        "string": ["string_literal"], "list": ["list_literal"],
        "dict": ["set_or_map_literal"],
    },
    "swift": {
        "boolean": ["boolean_literal", "boolean"], "integer": ["number"],
        "float": ["number"], "string": ["string", "static_string_literal"],
        "list": [], "dict": [],
    },
}


def slot_fillers(entries, closure):
    """(host, role) -> the concrete kinds that may legally stand there."""
    table = {}
    for host, role, filler in resolved_triples(
        declared_triples(entries), closure
    ):
        table.setdefault((host, role), set()).add(filler)
    return table


def dominants_in(fillers, literal_map):
    return [d for d in DOMINANTS
            if literal_map[d] and set(literal_map[d]) & fillers]


def token_choice_menus(entries):
    """host -> [menu size], one entry per all-anonymous slot of 2 or more."""
    menus = {}
    for entry in entries:
        if not entry.get("named"):
            continue
        for role, types in slots_of(entry):
            if len(types) >= 2 and all(not t["named"] for t in types):
                menus.setdefault(entry["type"], []).append(len(types))
    return menus


def containment_edges(slots):
    """host -> the set of kinds that may stand in any of its slots.

    No kind is treated as transparent.  An earlier draft contracted
    "wrapper" kinds so that a body container such as java's `block` did
    not count as a level; the rule could not be written without also
    swallowing `break_statement`, whose only sub-node is an optional
    label, so it was dropped.  Depth is therefore the raw count of
    enclosing named kinds, and the two distortions that leaves are
    stated in the phase-0 log rather than corrected here.
    """
    direct = {}
    for (host, _role), fillers in slots.items():
        direct.setdefault(host, set()).update(fillers)
    return direct


def infer_root(entries, slots):
    """Fallback for a grammar file too old to carry the `root` key.

    swift's file predates it.  The root is then the one kind that has
    slots of its own and never stands in anybody else's slot.
    """
    hosts = {host for host, _role in slots}
    fillers = set()
    for names in slots.values():
        fillers |= names
    loose = sorted(hosts - fillers)
    return loose[0] if len(loose) == 1 else None


def depths(edges, root):
    """Shortest number of enclosing kinds needed to reach each kind."""
    if root is None:
        return {}
    seen = {root: 0}
    queue = deque([root])
    while queue:
        host = queue.popleft()
        for filler in sorted(edges.get(host, ())):
            if filler not in seen:
                seen[filler] = seen[host] + 1
                queue.append(filler)
    return seen


def measure(language):
    entries = load_entries(language)
    parts = classify(entries)
    closure = build_closure(entries)
    literal_map = DOMINANT_KINDS[language]
    named = set(parts["named_concrete"])

    misses = sorted(
        k for kinds in literal_map.values() for k in kinds if k not in named
    )

    slots = slot_fillers(entries, closure)
    root = parts["root"] or infer_root(entries, slots)

    probes = {}
    for (host, role), fillers in slots.items():
        found = dominants_in(fillers, literal_map)
        if found:
            probes[(host, role)] = found
    base = sum(len(v) for v in probes.values())
    probe_hosts = sorted({host for host, _role in probes})

    menus = token_choice_menus(entries)
    expanded = 0
    for host in probe_hosts:
        host_probes = sum(len(v) for (h, _r), v in probes.items() if h == host)
        multiplier = 1
        for size in menus.get(host, []):
            multiplier *= size
        expanded += host_probes * multiplier

    depth = depths(containment_edges(slots), root)

    probeable = set(probe_hosts)
    unprobeable = sorted(named - probeable)

    def bucket(names, table):
        out = {"1": [], "2": [], "3+": [], "unreached": []}
        for name in sorted(names):
            level = table.get(name)
            if level is None:
                out["unreached"].append(name)
            elif level <= 1:
                out["1"].append(name)
            elif level == 2:
                out["2"].append(name)
            else:
                out["3+"].append(name)
        return out

    host_buckets = bucket(probe_hosts, depth)
    kind_buckets = bucket(named, depth)

    probes_by_depth = {"1": 0, "2": 0, "3+": 0, "unreached": 0}
    for (host, _role), found in probes.items():
        level = depth.get(host)
        key = ("unreached" if level is None
               else "1" if level <= 1 else "2" if level == 2 else "3+")
        probes_by_depth[key] += len(found)

    return {
        "language": language,
        "root": root,
        "root_declared": parts["root"] is not None,
        "dominant_kind_misses": misses,
        "dominants_available": [d for d in DOMINANTS if literal_map[d]],
        "counts": {
            "named_kinds": len(named),
            "anonymous_tokens": len(parts["anonymous"]),
            "legal_triples_declared": len(declared_triples(entries)),
            "legal_triples_resolved": len(
                resolved_triples(declared_triples(entries), closure)
            ),
            "slots": len(slots),
            "dominant_typed_slots": len(probes),
            "probe_hosts": len(probe_hosts),
            "probes_R1": base,
            "probes_R2": expanded,
            "unprobeable_kinds": len(unprobeable),
        },
        "probes_by_depth": probes_by_depth,
        "hosts_by_depth": {k: len(v) for k, v in host_buckets.items()},
        "kinds_by_depth": {k: len(v) for k, v in kind_buckets.items()},
        "depth_3_plus_hosts": host_buckets["3+"],
        "unreached_hosts": host_buckets["unreached"],
        "kinds_depth_1": kind_buckets["1"],
        "kinds_unreached": kind_buckets["unreached"],
        "unprobeable_kinds": unprobeable,
        "token_menus": {h: v for h, v in sorted(menus.items())},
    }


def main():
    report = {}
    for language in TARGETS + BONUS:
        report[language] = measure(language)
        counts = report[language]["counts"]
        print(
            "%-11s named=%4d anon=%4d legal=%5d probes_R1=%5d probes_R2=%6d "
            "unprobeable=%4d misses=%s"
            % (
                language, counts["named_kinds"], counts["anonymous_tokens"],
                counts["legal_triples_resolved"], counts["probes_R1"],
                counts["probes_R2"], counts["unprobeable_kinds"],
                report[language]["dominant_kind_misses"] or "-",
            )
        )
    total_r1 = sum(report[l]["counts"]["probes_R1"] for l in TARGETS)
    total_r2 = sum(report[l]["counts"]["probes_R2"] for l in TARGETS)
    print("11 targets: probes_R1=%d probes_R2=%d" % (total_r1, total_r2))
    report["_totals"] = {
        "targets": TARGETS, "bonus": BONUS,
        "probes_R1": total_r1, "probes_R2": total_r2,
    }
    with open(os.path.join(HERE, "probe_space.json"), "w") as handle:
        json.dump(report, handle, indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
