#!/usr/bin/env python3
"""Survey of tree-sitter node-types.json across six grammars for kind clustering.
Vocabulary note: tree-sitter's JSON key "children" denotes the unnamed-slot spec;
in prose we call it the "sub-node spec".
"""
import json, os, collections, sys

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
LANGS = ["rust", "python", "kotlin", "dart", "c", "cpp"]

def slot_iter(entry):
    for name, spec in (entry.get("fields") or {}).items():
        yield name, spec
    if "children" in entry:  # tree-sitter's key name for the sub-node spec
        yield None, entry["children"]

def survey(lang):
    d = json.load(open(os.path.join(RAW, lang + ".node-types.json")))
    named = [e for e in d if e["named"]]
    supertypes = [e for e in named if "subtypes" in e]
    with_fields = [e for e in named if e.get("fields")]
    with_subnode_spec = [e for e in named if "children" in e]
    leaves = [e for e in named if not e.get("fields") and "children" not in e and "subtypes" not in e]
    slots = mr_ok = with_types = 0
    roles = collections.Counter()
    for e in named:
        for name, spec in slot_iter(e):
            slots += 1
            if "multiple" in spec and "required" in spec: mr_ok += 1
            if spec.get("types"): with_types += 1
            if name: roles[name] += 1
    return {
        "total": len(d), "named": len(named),
        "supertype_count": len(supertypes),
        "supertype_names": sorted(e["type"] for e in supertypes),
        "with_fields": len(with_fields),
        "with_subnode_spec": len(with_subnode_spec),
        "leaves": len(leaves),
        "slots": slots, "slots_with_multiple_required": mr_ok,
        "slots_with_type_lists": with_types,
        "distinct_roles": len(roles),
        "top_roles": roles.most_common(10),
        "roles": set(roles),
        "raw": d,
    }

def super_membership(d):
    m = collections.defaultdict(list)
    for e in d:
        for s in e.get("subtypes", []):
            m[s["type"]].append(e["type"])
    return m

def collapse(types, super_map):
    """Collapse a slot's allowed-kind set to supertype names where the set matches."""
    kinds = sorted(t["type"] for t in types)
    out = []
    for k in kinds:
        sups = super_map.get(k, [])
        out.append((k, sups))
    return kinds, out

def demo_vector(lang, kind_names):
    s = survey(lang)
    d = {e["type"]: e for e in s["raw"]}
    sup = super_membership(s["raw"])
    print(f"\n--- demo feature vectors: {lang} ---")
    for k in kind_names:
        e = d.get(k)
        if not e:
            print(f"{k}: NOT PRESENT"); continue
        rows = []
        for name, spec in slot_iter(e):
            kinds = sorted(t["type"] for t in spec.get("types", []))
            # collapse: if every allowed kind shares a common supertype, name it
            common = None
            sets = [set(sup.get(x, [])) for x in kinds]
            if sets and all(sets):
                inter = set.intersection(*sets)
                if inter: common = sorted(inter)[0]
            rows.append((name or "<sub-node spec>", spec.get("multiple"), spec.get("required"), common or kinds))
        print(f"{k}: slots={len(rows)} out_supertypes={sup.get(k, [])}")
        for r in rows:
            print(f"   slot={r[0]!r} multiple={r[1]} required={r[2]} input={r[3]}")

if __name__ == "__main__":
    results = {}
    for lang in LANGS:
        r = survey(lang); results[lang] = r
        print(f"== {lang}: total={r['total']} named={r['named']} supertypes={r['supertype_count']} {r['supertype_names']}")
        print(f"   with_fields={r['with_fields']} with_subnode_spec={r['with_subnode_spec']} leaves={r['leaves']}")
        print(f"   slots={r['slots']} multiple_required_present={r['slots_with_multiple_required']} type_lists={r['slots_with_type_lists']}")
        print(f"   distinct_roles={r['distinct_roles']} top10={r['top_roles']}")
    common_roles = set.intersection(*[results[l]["roles"] for l in LANGS])
    print("\nroles common to all 6:", sorted(common_roles))
    for n in range(5, 2, -1):
        cnt = collections.Counter()
        for l in LANGS: cnt.update(results[l]["roles"])
        pass
    cnt = collections.Counter()
    for l in LANGS: cnt.update({r: 1 for r in results[l]["roles"]})
    print("roles in >=5 languages:", sorted(r for r, c in cnt.items() if c >= 5))
    scnt = collections.Counter()
    for l in LANGS: scnt.update({s: 1 for s in results[l]["supertype_names"]})
    print("supertype name overlap:", {s: c for s, c in scnt.most_common() if c > 1})
    demo_vector("rust", ["binary_expression", "if_expression", "function_item", "call_expression", "identifier"])
    demo_vector("python", ["binary_operator", "if_statement", "function_definition", "call", "identifier"])
