#!/usr/bin/env python3
"""types101_join.py -- TASK t101 / t101b, master plan CORE_0_3_research
§4.2 step 3: the join of each language's TYPE SPELLINGS to the MACHINE
HOLDERS.

WHAT A HOLDER IS (research CORE §1, verbatim): "one machine-level holder --
a class (signed integer, unsigned integer, float, truth) at a width -- with
every language's spellings for it hanging off it, so that a language type
resolves to the holder the machine distinguishes and no further."

THE TWO SIDES
  left side  -- type_inventory2_core2.json: per language, per scalar-core
                spelling, an `extracted_marking` and a `normalised_class`.
                A CLASS per spelling and NO WIDTH.
  right side -- the compiler's own DWARF record of each probe parameter:
                DW_AT_byte_size and DW_AT_encoding on the DIE that
                DW_AT_type resolves to.  In task t101 (log_213) this side
                was found ABSENT from every store on disk; task t101b
                re-read it from the compiler by recompiling every
                accepted probe at its anchor flags
                (types101_anchor_dwarf.py), and this program now reads
                THOSE rows: types101_dwarf_rows.json and the shards under
                types101_dwarf_rows/.
  the rule    -- the brief's first stop rule: the DWARF encoding decides
                the class and the width.  Nothing here assigns a class or
                a width from a spelling.  A spelling whose DWARF type
                carries no DW_AT_encoding (swift: every stdlib scalar is
                a DW_TAG_structure_type with a byte size and no encoding)
                hangs off a holder whose class reads
                `DW_AT_encoding_absent`; it is recorded, never resolved.

HISTORY OF THIS FILE.  Its first version (t101, 2026-09-06 morning)
measured the stored tables, found the two-field row shape on all 64,398
rows, and refused at step 1 by name, writing types101_dwarf_flag.json.
That file stays on disk as the record of the flag.  This version is the
join proper, over the re-read rows.

WHAT IT WRITES
  types101_holders.json        the holder table: class x width, each
                               language's spellings hanging off it with
                               attesting counts (rows and probes); the
                               result-type side kept beside it; the rows
                               that sit on no scalar holder (pointers,
                               non-scalar structures, absent return types)
  types101_spellings.json      per language, per scalar-core spelling: the
                               holder(s) DWARF put it on, the DWARF
                               spelling, the inventory's class, and the
                               verdict AGREE / DISAGREE / UNDECIDABLE /
                               UNATTESTED; plus the attested spellings
                               outside the scalar core (the originals'
                               stdint aliases)
  types101_entry_holders.json  per pool entry (the_pool5.json, 1,831
                               entries, 88 type keys): every member's
                               parameter holders and result holder; the
                               coverage over the 88 type keys, with the
                               DWARF result width set against the key's
                               own answer width; the disagreements

THE CLASS WORDS.  A holder's class is the DWARF standard's own name for
its encoding (DWARF 5 §5.1.1, table 5.1): DW_ATE_boolean is a true or
false value, DW_ATE_float a floating-point number, DW_ATE_signed and
DW_ATE_signed_char signed, DW_ATE_unsigned and DW_ATE_unsigned_char
unsigned, DW_ATE_UTF a Unicode character.  The four holder classes the
research CORE names are read off that table -- truth, float, signed
integer, unsigned integer -- and DW_ATE_UTF is none of the four, so a
spelling on it is listed and not placed.

MEMORY.  Bound ABORT_MEMORY_T101B = 4 GB, checked with resource.getrusage
after every shard and after the pool; shards are read one at a time and
only counters and one small record per unit are kept.

SPELLING BAN.  Nothing here is keyed, grouped, paired or selected by an
operator token.  Groupings are by holder (encoding x width), language,
type spelling, pool entry and type key.  The member `operator` display
label is never read.
"""

import collections
import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ABORT_MEMORY_T101B_BYTES = 4 * 1024 * 1024 * 1024
LANGS = ["c", "cpp", "go", "rust", "swift"]

# DWARF 5 table 5.1, the standard's own words, and the research CORE's
# four class names read off them.
DWARF_STANDARD_CLASS = {
    "DW_ATE_boolean": "truth",
    "DW_ATE_float": "float",
    "DW_ATE_signed": "signed integer",
    "DW_ATE_signed_char": "signed integer",
    "DW_ATE_unsigned": "unsigned integer",
    "DW_ATE_unsigned_char": "unsigned integer",
    "DW_ATE_UTF": "unicode character (none of the four holder classes)",
}
# the inventory's vocabulary for the same four classes (core_rule2.py)
INVENTORY_WORD = {
    "truth": "truth_value",
    "float": "float",
    "signed integer": "integer_signed",
    "unsigned integer": "integer_unsigned",
}
CLASS_ORDER = ["truth", "signed integer", "unsigned integer", "float",
               "unicode character (none of the four holder classes)",
               "DW_AT_encoding_absent"]

POINTERISH = ("DW_TAG_pointer_type", "DW_TAG_reference_type",
              "DW_TAG_rvalue_reference_type")


def peak_rss_bytes():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024


def memory_guard(where):
    rss = peak_rss_bytes()
    if rss > ABORT_MEMORY_T101B_BYTES:
        sys.stderr.write("ABORT_MEMORY_T101B: peak RSS %d bytes exceeded the "
                         "stated 4 GB bound while reading %s\n" % (rss, where))
        sys.exit(3)
    return rss


# ------------------------------------------------------------ classify

def classify(row):
    """(kind, holder_id) for one row, from its DWARF chain only.

    kind      scalar     a base type with a byte size (encoding may be absent)
              structure  the chain ends on a structure / class / union / enum
              pointer    a pointer or reference sits anywhere in the chain
              absent     no DWARF type at all (a subprogram with no DW_AT_type)
    holder_id "<encoding>|<byte_size>", with `DW_AT_encoding_absent` when
              the terminal DIE carries no DW_AT_encoding and `no_size` when
              it carries no DW_AT_byte_size."""
    chain = row.get("dwarf_type_chain") or []
    if not chain:
        return "absent", None
    if any(n["tag"] in POINTERISH for n in chain):
        ptr = next(n for n in chain if n["tag"] in POINTERISH)
        return "pointer", "%s|%s" % (ptr["tag"], ptr["byte_size"] if ptr["byte_size"] is not None else "no_size")
    term = chain[-1]
    enc = term["encoding"] or "DW_AT_encoding_absent"
    size = term["byte_size"] if term["byte_size"] is not None else "no_size"
    hid = "%s|%s" % (enc, size)
    if term["tag"] == "DW_TAG_base_type":
        return "scalar", hid
    if term["tag"] in ("DW_TAG_structure_type", "DW_TAG_class_type",
                       "DW_TAG_union_type", "DW_TAG_enumeration_type"):
        return "structure", hid
    return "other:" + term["tag"], hid


def holder_class(holder_id):
    enc = holder_id.split("|")[0]
    if enc == "DW_AT_encoding_absent":
        return "DW_AT_encoding_absent"
    return DWARF_STANDARD_CLASS.get(enc, "encoding %s (not in table 5.1's scalar rows)" % enc)


def holder_width(holder_id):
    size = holder_id.split("|")[1]
    return None if size == "no_size" else int(size)


# ------------------------------------------------------------------ read

def read_rows():
    """One pass over the shards; only counters and one record per unit."""
    index = json.load(open(os.path.join(HERE, "types101_dwarf_rows.json")))
    # attesting counts: holder -> lang -> declared spelling -> Counter(rows) + set(units)
    param_rows = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int)))
    param_units = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(set)))
    result_rows = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int)))
    spelling_holders = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    spelling_dwarf = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    off_holder = collections.defaultdict(collections.Counter)  # (lang, role, kind) -> holder -> rows
    off_holder_examples = {}
    member = {}  # unit -> record
    totals = collections.Counter()
    peak = 0
    shards = index["shards"]
    for i, sh in enumerate(shards, 1):
        doc = json.load(open(os.path.join(HERE, sh["shard"])))
        for row in doc["rows"]:
            lang = row["language"]
            unit = row["unit"]
            kind, hid = classify(row)
            totals["rows"] += 1
            rec = member.setdefault(unit, {"lang": lang, "population": row["population"],
                                           "parameter_holders": [], "parameter_kinds": [],
                                           "result_holder": None, "result_kind": None,
                                           "result_byte_size": None})
            if row["role"] == "parameter":
                totals["parameter_rows"] += 1
                pos = row["position"]
                while len(rec["parameter_holders"]) <= pos:
                    rec["parameter_holders"].append(None)
                    rec["parameter_kinds"].append(None)
                rec["parameter_holders"][pos] = hid
                rec["parameter_kinds"][pos] = kind
                sp = row["declared_spelling"]
                if kind in ("scalar", "structure") and hid is not None:
                    param_rows[hid][lang][sp] += 1
                    param_units[hid][lang][sp].add(unit)
                    spelling_holders[lang][sp][hid] += 1
                    spelling_dwarf[lang][sp][row["dwarf_spelling"]] += 1
                else:
                    off_holder[(lang, "parameter", kind)][hid] += 1
                    off_holder_examples.setdefault((lang, "parameter", kind, hid),
                                                   {"unit": unit, "declared_spelling": sp,
                                                    "dwarf_spelling": row["dwarf_spelling"]})
            else:
                totals["result_rows"] += 1
                rec["result_holder"] = hid
                rec["result_kind"] = kind
                rec["result_byte_size"] = row["dwarf_byte_size"] if kind != "pointer" else holder_width(hid)
                if kind in ("scalar", "structure") and hid is not None:
                    result_rows[hid][lang][row["dwarf_spelling"]] += 1
                else:
                    off_holder[(lang, "result", kind)][hid] += 1
                    off_holder_examples.setdefault((lang, "result", kind, hid),
                                                   {"unit": unit, "declared_spelling": row["declared_spelling"],
                                                    "dwarf_spelling": row["dwarf_spelling"]})
        del doc
        if i % 50 == 0 or i == len(shards):
            print("[%d/%d] shards read, %d rows, %d units" % (i, len(shards), totals["rows"], len(member)))
            sys.stdout.flush()
        peak = max(peak, memory_guard(sh["shard"]))
    return dict(index=index, param_rows=param_rows, param_units=param_units,
                result_rows=result_rows, spelling_holders=spelling_holders,
                spelling_dwarf=spelling_dwarf, off_holder=off_holder,
                off_holder_examples=off_holder_examples, member=member,
                totals=totals, peak=peak)


def core_spellings():
    doc = json.load(open(os.path.join(HERE, "type_inventory2_core2.json")))
    got = {}
    for lang, block in doc["languages"].items():
        got[lang] = [dict(spelling=r["spelling"], extracted_marking=r.get("extracted_marking"),
                          normalised_class=r.get("normalised_class"))
                     for r in block["scalar_core"]]
    return got


# ------------------------------------------------------------- step 2

def holders_table(R):
    hids = set(R["param_rows"]) | set(R["result_rows"])
    holders = []
    for hid in hids:
        cls = holder_class(hid)
        width = holder_width(hid)
        langs = {}
        for lang in LANGS:
            sp = R["param_rows"].get(hid, {}).get(lang, {})
            if not sp:
                continue
            langs[lang] = [
                {"spelling": s, "parameter_rows": n,
                 "probes_attesting": len(R["param_units"][hid][lang][s])}
                for s, n in sorted(sp.items(), key=lambda kv: (-kv[1], kv[0]))]
        results = {}
        for lang in LANGS:
            sp = R["result_rows"].get(hid, {}).get(lang, {})
            if sp:
                results[lang] = [{"dwarf_spelling": s, "result_rows": n}
                                 for s, n in sorted(sp.items(), key=lambda kv: (-kv[1], kv[0]))]
        holders.append({
            "holder_id": hid,
            "dwarf_encoding": hid.split("|")[0],
            "byte_size": width,
            "bits": width * 8 if width is not None else None,
            "dwarf_standard_class": cls,
            "inventory_word_for_the_class": INVENTORY_WORD.get(cls),
            "languages_with_a_spelling_on_this_holder": sorted(langs),
            "spellings_by_language": langs,
            "parameter_rows": sum(x["parameter_rows"] for v in langs.values() for x in v),
            "probes_attesting": sum(x["probes_attesting"] for v in langs.values() for x in v),
            "result_types_by_language": results,
            "result_rows": sum(x["result_rows"] for v in results.values() for x in v),
        })
    order = {c: i for i, c in enumerate(CLASS_ORDER)}
    holders.sort(key=lambda h: (order.get(h["dwarf_standard_class"], 99),
                                h["byte_size"] if h["byte_size"] is not None else 999,
                                h["holder_id"]))
    off = []
    for (lang, role, kind), c in sorted(R["off_holder"].items()):
        for hid, n in c.most_common():
            ex = R["off_holder_examples"][(lang, role, kind, hid)]
            off.append({"language": lang, "role": role, "kind": kind,
                        "chain_head_or_terminal": hid, "rows": n, "example": ex})
    return holders, off


# ------------------------------------------------------------- step 3/5

def spellings_table(R, core):
    out = {}
    disagreements = []
    for lang in LANGS:
        rows = []
        core_set = set()
        for r in core.get(lang, []):
            s = r["spelling"]
            core_set.add(s)
            hs = R["spelling_holders"][lang].get(s, collections.Counter())
            n = sum(hs.values())
            holders = [{"holder_id": h, "parameter_rows": k,
                        "dwarf_standard_class": holder_class(h),
                        "byte_size": holder_width(h)} for h, k in hs.most_common()]
            dw = [{"dwarf_spelling": d, "rows": k}
                  for d, k in R["spelling_dwarf"][lang].get(s, collections.Counter()).most_common()]
            if n == 0:
                verdict = "UNATTESTED: no accepted probe declared an operand with this spelling"
                dclass = None
            else:
                classes = sorted(set(h["dwarf_standard_class"] for h in holders))
                dclass = classes[0] if len(classes) == 1 else classes
                if classes == ["DW_AT_encoding_absent"]:
                    verdict = ("UNDECIDABLE: the anchor DWARF carries no DW_AT_encoding on "
                               "this type; the width is read, the class is not")
                elif len(classes) > 1:
                    verdict = "DISAGREE: DWARF put this spelling on more than one class"
                else:
                    word = INVENTORY_WORD.get(classes[0])
                    if word is None:
                        verdict = ("DISAGREE: DWARF's class is %s, which is none of the "
                                   "inventory's four" % classes[0])
                    elif word == r["normalised_class"]:
                        verdict = "AGREE"
                    else:
                        verdict = ("DISAGREE: DWARF says %s (%s), the inventory says %s"
                                   % (classes[0], word, r["normalised_class"]))
                if verdict.startswith("DISAGREE"):
                    disagreements.append({"language": lang, "spelling": s,
                                          "inventory_normalised_class": r["normalised_class"],
                                          "inventory_extracted_marking": r["extracted_marking"],
                                          "dwarf_holders": holders, "verdict": verdict})
            widths = sorted(set(h["byte_size"] for h in holders if h["byte_size"] is not None))
            rows.append({
                "language": lang, "spelling": s,
                "inventory_extracted_marking": r["extracted_marking"],
                "inventory_normalised_class": r["normalised_class"],
                "parameter_rows_attesting": n,
                "attested": bool(n),
                "dwarf_holders": holders,
                "dwarf_spellings": dw,
                "dwarf_byte_size": widths[0] if len(widths) == 1 else (widths or None),
                "dwarf_standard_class": dclass,
                "verdict": verdict,
            })
        outside = []
        for s, hs in R["spelling_holders"][lang].items():
            if s in core_set:
                continue
            outside.append({
                "language": lang, "spelling": s,
                "parameter_rows_attesting": sum(hs.values()),
                "dwarf_holders": [{"holder_id": h, "parameter_rows": k,
                                   "dwarf_standard_class": holder_class(h),
                                   "byte_size": holder_width(h)} for h, k in hs.most_common()],
                "dwarf_spellings": [{"dwarf_spelling": d, "rows": k}
                                    for d, k in R["spelling_dwarf"][lang][s].most_common()],
                "why_outside": ("the originals' six hand-written holder types are stdint "
                                "aliases, which log_131 §2.1.3 made lookup-only rather "
                                "than core members; DWARF resolves the typedef"),
            })
        outside.sort(key=lambda x: (-x["parameter_rows_attesting"], x["spelling"]))
        out[lang] = {
            "scalar_core": rows,
            "scalar_core_size": len(rows),
            "attested": sum(1 for r in rows if r["attested"]),
            "agree": sum(1 for r in rows if r["verdict"] == "AGREE"),
            "disagree": sum(1 for r in rows if r["verdict"].startswith("DISAGREE")),
            "undecidable": sum(1 for r in rows if r["verdict"].startswith("UNDECIDABLE")),
            "unattested": sum(1 for r in rows if r["verdict"].startswith("UNATTESTED")),
            "attested_spellings_outside_the_scalar_core": outside,
        }
    return out, disagreements


# ------------------------------------------------------------- step 4

def entry_holders(R):
    pool = json.load(open(os.path.join(HERE, "the_pool5.json")))
    member = R["member"]
    entries = []
    by_key = collections.defaultdict(lambda: {
        "entries": 0, "members": 0, "members_with_rows": 0,
        "members_interpreter": 0, "members_compiled_without_rows": 0,
        "parameter_holder_tuples": collections.Counter(),
        "result_holders": collections.Counter(),
        "dwarf_result_bits": collections.Counter(),
        "result_width_agrees": 0, "result_width_differs": 0,
        "result_width_not_comparable": 0,
    })
    width_disagreements = collections.Counter()
    width_examples = {}
    tot = collections.Counter()
    for e in pool["entries"]:
        key = e["type_key"]
        k = by_key[key]
        k["entries"] += 1
        ms = []
        tuples = collections.Counter()
        rholders = collections.Counter()
        for m in e["members"]:
            unit = m["unit"]
            rec = member.get(unit)
            k["members"] += 1
            tot["members"] += 1
            if m["population"] == "interpreter":
                k["members_interpreter"] += 1
                tot["members_interpreter"] += 1
                ms.append({"unit": unit, "lang": m["lang"], "population": m["population"],
                           "rows": "none: an interpreter handler, not a compiled probe "
                                   "(its DWARF-typed key is dwarf_typed_key.json, task 24)"})
                continue
            if rec is None:
                k["members_compiled_without_rows"] += 1
                tot["members_compiled_without_rows"] += 1
                ms.append({"unit": unit, "lang": m["lang"], "population": m["population"],
                           "rows": "none: the probe was refused at anchor or its DWARF was not read "
                                   "(see types101_dwarf_rows.json per_language)"})
                continue
            k["members_with_rows"] += 1
            tot["members_with_rows"] += 1
            tup = ",".join(h or "absent" for h in rec["parameter_holders"])
            tuples[tup] += 1
            k["parameter_holder_tuples"][tup] += 1
            rh = rec["result_holder"] or "absent"
            rholders[rh] += 1
            k["result_holders"][rh] += 1
            pw = m.get("result_width")
            dbits = rec["result_byte_size"] * 8 if rec["result_byte_size"] is not None else None
            k["dwarf_result_bits"][dbits if dbits is not None else "no_size"] += 1
            if pw is None or dbits is None:
                k["result_width_not_comparable"] += 1
                agree = None
            elif int(pw) == dbits:
                k["result_width_agrees"] += 1
                agree = True
            else:
                k["result_width_differs"] += 1
                agree = False
                width_disagreements[(m["lang"], key, int(pw), dbits, rh)] += 1
                width_examples.setdefault((m["lang"], key, int(pw), dbits, rh), unit)
            ms.append({"unit": unit, "lang": m["lang"], "population": m["population"],
                       "parameter_holders": rec["parameter_holders"],
                       "parameter_kinds": rec["parameter_kinds"],
                       "result_holder": rec["result_holder"], "result_kind": rec["result_kind"],
                       "dwarf_result_bits": dbits, "pool_result_width": pw,
                       "result_width_agrees": agree})
        entries.append({
            "entry_id": e["entry_id"], "type_key": key, "languages": e["languages"],
            "member_count": e["member_count"],
            "members_with_rows": sum(1 for m in ms if "parameter_holders" in m),
            "distinct_parameter_holder_tuples": [{"holders": t, "members": n}
                                                 for t, n in tuples.most_common()],
            "distinct_result_holders": [{"holder": h, "members": n} for h, n in rholders.most_common()],
            "one_holder_tuple_for_every_typed_member": len(tuples) <= 1,
            "members": ms,
        })
    keys = []
    for key, k in sorted(by_key.items(), key=lambda kv: (-kv[1]["members"], kv[0])):
        fam, _, bits = key.partition("|")
        keys.append({
            "type_key": key,
            "arrival_register_families": fam,
            "answer_width_bits": int(bits) if bits.isdigit() else bits,
            "entries": k["entries"], "members": k["members"],
            "members_with_rows": k["members_with_rows"],
            "members_interpreter": k["members_interpreter"],
            "members_compiled_without_rows": k["members_compiled_without_rows"],
            "covered": k["members_compiled_without_rows"] == 0 and k["members_with_rows"] > 0,
            "parameter_holder_tuples": [{"holders": t, "members": n}
                                        for t, n in k["parameter_holder_tuples"].most_common()],
            "result_holders": [{"holder": h, "members": n} for h, n in k["result_holders"].most_common()],
            "dwarf_result_bits": [{"bits": b, "members": n} for b, n in k["dwarf_result_bits"].most_common()],
            "result_width_agrees": k["result_width_agrees"],
            "result_width_differs": k["result_width_differs"],
            "result_width_not_comparable": k["result_width_not_comparable"],
        })
    wd = [{"language": l, "type_key": key, "pool_result_width": pw, "dwarf_result_bits": db,
           "result_holder": rh, "members": n, "example_unit": width_examples[(l, key, pw, db, rh)]}
          for (l, key, pw, db, rh), n in width_disagreements.most_common()]
    tot["type_keys"] = len(keys)
    tot["type_keys_covered"] = sum(1 for k in keys if k["covered"])
    tot["entries"] = len(entries)
    tot["entries_with_one_holder_tuple"] = sum(1 for e in entries if e["one_holder_tuple_for_every_typed_member"])
    tot["result_width_agrees"] = sum(k["result_width_agrees"] for k in keys)
    tot["result_width_differs"] = sum(k["result_width_differs"] for k in keys)
    tot["result_width_not_comparable"] = sum(k["result_width_not_comparable"] for k in keys)
    return entries, keys, wd, tot, pool["meta"].get("generator")


# ---------------------------------------------------------------- main

def main():
    print("types101_join.py -- the join, over the rows re-read from the compiler")
    print("bound: ABORT_MEMORY_T101B at %d bytes" % ABORT_MEMORY_T101B_BYTES)
    sys.stdout.flush()
    core = core_spellings()
    R = read_rows()
    holders, off = holders_table(R)
    spellings, class_disagreements = spellings_table(R, core)
    entries, keys, width_disagreements, ptot, pool_gen = entry_holders(R)
    peak = max(R["peak"], memory_guard("the pool"))

    common = {
        "task": "t101b -- dominant types: the join of language spellings to machine holders "
                "(CORE_0_3_research §4.2 step 3), over the parameter types re-read from the "
                "compiler by types101_anchor_dwarf.py",
        "right_side": "types101_dwarf_rows.json and types101_dwarf_rows/ (one row per probe "
                      "parameter and per result, DW_AT_byte_size and DW_AT_encoding read off "
                      "the anchor build's DWARF)",
        "left_side": "type_inventory2_core2.json (per language, per scalar-core spelling, a "
                     "class and no width)",
        "the_rule": "the DWARF encoding decides the class and the width; no class and no width "
                    "is assigned from a spelling here. A type whose DWARF carries no "
                    "DW_AT_encoding hangs off a holder whose class reads DW_AT_encoding_absent.",
        "class_words": {"source": "DWARF 5 §5.1.1 table 5.1", "map": DWARF_STANDARD_CLASS,
                        "inventory_word": INVENTORY_WORD},
        "spelling_ban": "no operator token appears in any key, grouping, pairing or row "
                        "structure; groupings are by holder, language, type spelling, pool "
                        "entry and type key; the member operator label is never read",
        "memory": {"bound": "ABORT_MEMORY_T101B at 4 GB, resource.getrusage(RUSAGE_SELF)",
                   "peak_rss_mb": round(peak / (1024.0 * 1024.0), 1),
                   "method": "one shard at a time; counters and one small record per unit"},
    }

    doc = dict(common)
    doc["generated_by"] = "types101_join.py"
    doc["what_this_is"] = ("the holder table: one machine-level holder per (DWARF encoding x "
                           "byte size), with every language's spellings hanging off it and "
                           "the counts that attest them")
    doc["holders"] = holders
    doc["holder_count"] = len(holders)
    doc["holders_by_class"] = collections.Counter(h["dwarf_standard_class"] for h in holders)
    doc["rows_on_no_scalar_holder"] = off
    doc["row_totals"] = dict(R["totals"])
    doc["rows_index"] = {"per_language": R["index"]["per_language"], "totals": R["index"]["totals"],
                         "anchor_flags": R["index"]["anchor_flags"],
                         "toolchain_banners_printed_in_lane": R["index"]["toolchain_banners_printed_in_lane"]}
    write("types101_holders.json", doc)

    doc = dict(common)
    doc["generated_by"] = "types101_join.py"
    doc["what_this_is"] = ("per language, per scalar-core spelling: the holder DWARF put it on, "
                           "the DWARF spelling, the inventory's class, and the verdict")
    doc["by_language"] = spellings
    doc["totals"] = {k: sum(v[k] for v in spellings.values())
                     for k in ("scalar_core_size", "attested", "agree", "disagree", "undecidable", "unattested")}
    doc["disagreements_between_dwarf_encoding_and_the_inventory_class"] = class_disagreements
    write("types101_spellings.json", doc)

    doc = dict(common)
    doc["generated_by"] = "types101_join.py"
    doc["what_this_is"] = ("per pool entry, every member's parameter holders and result holder; "
                           "the coverage over the type keys; the DWARF result width set against "
                           "the pool's own answer width")
    doc["pool"] = {"file": "the_pool5.json", "generator": pool_gen}
    doc["totals"] = ptot
    doc["type_keys"] = keys
    doc["result_width_disagreements"] = width_disagreements
    doc["entries"] = entries
    write("types101_entry_holders.json", doc)

    print("")
    print("holders: %d  (%s)" % (len(holders), ", ".join(
        "%s %d" % (c, n) for c, n in sorted(collections.Counter(
            h["dwarf_standard_class"] for h in holders).items()))))
    print("%-6s %6s %8s %6s %8s %11s %10s" % ("lang", "core", "attested", "agree", "disagree", "undecidable", "unattested"))
    for lang in LANGS:
        v = spellings[lang]
        print("%-6s %6d %8d %6d %8d %11d %10d" % (lang, v["scalar_core_size"], v["attested"], v["agree"],
                                                 v["disagree"], v["undecidable"], v["unattested"]))
    print("pool: %d entries, %d type keys, %d covered; members with rows %d, interpreter %d, "
          "compiled without rows %d" % (ptot["entries"], ptot["type_keys"], ptot["type_keys_covered"],
                                        ptot["members_with_rows"], ptot["members_interpreter"],
                                        ptot["members_compiled_without_rows"]))
    print("result width: agrees %d, differs %d, not comparable %d" % (
        ptot["result_width_agrees"], ptot["result_width_differs"], ptot["result_width_not_comparable"]))
    print("peak RSS: %.1f MB (bound 4096.0 MB)" % (peak / (1024.0 * 1024.0)))
    return 0


def write(name, doc):
    path = os.path.join(HERE, name)
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
        fh.write("\n")
    os.replace(tmp, path)
    print("wrote %s" % path)


if __name__ == "__main__":
    sys.exit(main())
