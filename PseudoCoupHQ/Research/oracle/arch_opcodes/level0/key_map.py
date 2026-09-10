#!/usr/bin/env python3
"""key_map.py -- the join between the two readings' keys, and nothing else.

WHAT THIS IS, in relation.  The K-framework x86-64 semantics states one rule
file per instruction VARIANT and names it in the assembler's own spelling:
`addl_r32_r32.k`.  Our model table
(`PRIVATE/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json`)
states one row per (mnem, operand shape, key_width) -- the machine-form key of
the ruling of 2026-09-08.  This program is the map between the two, and it is
built from the two sides' own tables: their rule HEAD gives the operand list,
our `reference.py`'s `opcode_table` says which mnemonic spelling it registers,
and our `model_table.json` says which rows exist and translated.

THE OPERAND ORDER, stated because it is the one thing a reader would get
wrong.  Their FILE NAME lists the operands in the reverse of their RULE HEAD:
`addl_r32_imm32.k`'s head is `execinstr (addl Imm32:Imm, R2:R32, .Operands)`,
and `shll_r32_cl.k`'s head is `execinstr (shll %cl, R2:R32, .Operands)`.  The
head is in the arch text's own order -- source first, destination last -- and
that is the order our own `reference.Operands` reads too, so THE SHAPE IS
DERIVED FROM THE HEAD and never from the name.  The name stays what it is:
their identifier for the variant, and the key of this map.

WHAT A MATCH IS.  A variant matches when
  (a) their mnemonic token, whole or with one AT&T size letter removed, is a
      mnemonic our reference's table registers with a builder;
  (b) their rule head's operand list is one our sweep also spells, as
      `shape_of_head` below; and
  (c) our model table carries a TRANSLATED row at that (mnem, shape) and at
      the width their operand list names.
Everything else is listed BY CAUSE, on whichever side it fails, and counted.

THE SPELLING BAN.  Every key of the json this writes is a machine form: their
variant name (an instruction identifier, never an operator token), or our
(mnem, shape, key_width) triple with the mnemonic in the field `mnem`, which
the guard's own PROSE_FIELDS already reads as a machine form under the ruling
of 2026-09-08.  No list ever holds a bare mnemonic; a mnemonic is always a
field of a record.

usage:
    python3 key_map.py <their semantics folder> <our model_table.json> \
                       <the key_map.json to write>
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
PIPELINE = os.path.abspath(
    os.path.join(HERE, "..", "..", "..", "op_pipeline"))
if PIPELINE not in sys.path:
    sys.path.insert(0, PIPELINE)

import k_to_z3                                             # noqa: E402
import reference as R                                      # noqa: E402


# ==================================================================
# section 1: their rule head -> our operand shape
# ==================================================================
#
# The right-hand column is the shape name `model_translate.shapes_for`
# gives that spelling, quoted from that file rather than invented here:
#
#   gpr_gpr              ("gpr_gpr", [b, a])          %esi,%edi
#   gpr_one              ("gpr_one", [a])             %edi
#   cl_gpr               ("cl_gpr", ["%cl", a])       %cl,%edi
#   imm_gpr              ("imm_gpr", ["$0x3", a])     $0x3,%edi
#   imm_symbolic_gpr     ("imm_symbolic_gpr",[c, a])  a free symbol,%edi
#   mem_gpr              ("mem_gpr", ["(%rsi)", a])   (%rsi),%edi
#   gpr_mem              ("gpr_mem", [b, "(%rax)"])   %esi,(%rax)
#   mem_one              ("mem_one", ["(%rsi)"])      (%rsi)
#   xmm_xmm / gpr_xmm / xmm_gpr / mem_xmm / xmm_mem / none


def shape_of_head(operands):
    """their rule head's operand list -> (our shape name, the width our
    sweep runs it at, how their immediate binds), or (None, None, the
    cause it fails on).

    THE IMMEDIATE BINDING, stated because it decides what the check
    means.  Our sweep spells an immediate operand two ways and the map
    uses both:
      `imm_symbolic_gpr` puts a REGISTER in the immediate's slot, so
      the mapping's immediate is a free symbol -- and their rule's
      `Imm` variable binds to that same symbol, giving a comparison
      over EVERY immediate.  Used when their immediate is as wide as
      the operand it is applied to.
      `imm_gpr` bakes the literal `$0x3` in, so their `Imm` binds to
      the literal 3 and the comparison holds at that one immediate.
      Used when their immediate is NARROWER than the operand, where our
      sweep has no symbolic spelling of a narrow immediate.
    """
    kinds = [operand.get("kind") for operand in operands]
    widths = [operand.get("width") for operand in operands]

    if not operands:
        return "none", None, None

    if len(operands) == 1:
        if kinds[0] == "gpr":
            return "gpr_one", widths[0], None
        if kinds[0] == "mem":
            return "mem_one", widths[0], None
        if kinds[0] == "high":
            return None, None, ("a high-byte operand form our sweep "
                                "never spells")
        return None, None, ("an operand form our sweep never spells: "
                            "one %s operand" % kinds[0])

    if len(operands) != 2:
        return None, None, ("an operand form our sweep never spells: "
                            "%d operands" % len(operands))

    source, destination = kinds
    source_width, destination_width = widths

    if "high" in kinds:
        return None, None, ("a high-byte operand form our sweep never "
                            "spells")
    if "ymm" in kinds:
        return None, None, ("an operand form our sweep never spells: a "
                            "256-bit vector register")
    if "register" in kinds:
        return None, None, ("an operand form our sweep never spells: "
                            "the head names a register outright")

    if source == "gpr" and destination == "gpr":
        if source_width != destination_width:
            return None, None, ("an operand form our sweep never "
                                "spells: two registers of unlike width")
        return "gpr_gpr", destination_width, None
    if source == "cl" and destination == "gpr":
        return "cl_gpr", destination_width, None
    if source == "imm" and destination == "gpr":
        if source_width == destination_width:
            return "imm_symbolic_gpr", destination_width, "symbol"
        return "imm_gpr", destination_width, "literal"
    if source == "mem" and destination == "gpr":
        if source_width != destination_width:
            return None, None, ("an operand form our sweep never "
                                "spells: a memory source of unlike "
                                "width")
        return "mem_gpr", destination_width, None
    if source == "gpr" and destination == "mem":
        if source_width != destination_width:
            return None, None, ("an operand form our sweep never "
                                "spells: a memory destination of "
                                "unlike width")
        return "gpr_mem", source_width, None
    if source == "cl" and destination == "mem":
        return None, None, ("an operand form our sweep never spells: a "
                            "memory destination shifted by %cl")
    if source == "imm" and destination == "mem":
        return None, None, ("an operand form our sweep never spells: a "
                            "memory destination and an immediate")
    if source == "xmm" and destination == "xmm":
        return "xmm_xmm", 128, None
    if source == "gpr" and destination == "xmm":
        return "gpr_xmm", source_width, None
    if source == "xmm" and destination == "gpr":
        return "xmm_gpr", destination_width, None
    if source == "mem" and destination == "xmm":
        return "mem_xmm", 128, None
    if source == "xmm" and destination == "mem":
        return "xmm_mem", 128, None
    return None, None, ("an operand form our sweep never spells: %s "
                        "then %s" % (source, destination))


# ==================================================================
# section 2: their mnemonic token -> our registered mnemonic
# ==================================================================


SIZE_LETTERS = ("b", "w", "l", "q")


def our_mnem(token, table):
    """(our mnemonic, which rule fired, the cause it fails on).

    The two rules, in order, both decided against OUR reference's own
    table rather than by a spelling rule of this file's own:
      1. the whole token, when the table registers it (`movl`);
      2. the token with one trailing AT&T size letter removed, when the
         table registers THAT (`addl` -> `add`).
    """
    if token in table.entries:
        return token, "the table registers their spelling whole", None
    if len(token) > 1 and token[-1] in SIZE_LETTERS:
        stem = token[:-1]
        if stem in table.entries:
            return stem, ("the table registers the stem, their last "
                          "letter being the AT&T size suffix"), None
    return None, None, ("a mnemonic our reference's table does not "
                        "register")


# ==================================================================
# section 3: the map
# ==================================================================


def their_variants(folder):
    """every variant the third-party semantics states, as (the folder it
    is filed under, the variant name, its full path)."""
    out = []
    for sub in sorted(os.listdir(folder)):
        path = os.path.join(folder, sub)
        if not os.path.isdir(path):
            continue
        for name in sorted(os.listdir(path)):
            if not name.endswith(".k"):
                continue
            out.append((sub, name[:-2], os.path.join(path, name)))
    return out


def our_rows(model_table_path):
    """our model table's TRANSLATED rows, indexed by (mnem, shape,
    width) -- the sweep's own loop width, which is the width their
    operand list names -- with each row's key_width carried."""
    document = json.load(open(model_table_path))
    index = {}
    by_pair = {}
    triples = set()
    for row in document["rows"]:
        if row.get("outcome") != "TRANSLATED":
            continue
        key = (row["mnem"], row["shape"], row["width"])
        triples.add((row["mnem"], row["shape"], row["key_width"]))
        record = {
            "row_id": row["row_id"],
            "key_width": row["key_width"],
            "width": row["width"],
            "preseeded": row.get("preseeded", False),
            "operands": row.get("operands", []),
            "attestation_ledger_rows":
                row.get("attestation", {}).get("ledger_rows", 0),
            "attestation_units":
                row.get("attestation", {}).get("units", 0),
        }
        if key not in index:
            index[key] = record
        by_pair.setdefault((row["mnem"], row["shape"]), []).append(
            record)
    return index, by_pair, triples


VECTOR_SHAPES = frozenset(["xmm_xmm", "mem_xmm", "xmm_mem",
                           "xmm_same"])
"""the shapes whose OPERAND width is 128 whatever the sweep's loop
variable says.  Our table's `width` field IS that loop variable and its
`key_width` field is the operation's own lane width (task m1b's one
width rule), so a vector cell is looked up by the (mnem, shape) pair
rather than by a width their operand list cannot state."""


def look_up(index, by_pair, mnem, shape, width):
    """our model table's row for one of their variants, and how it was
    found.

    Three rules, in order, each stated because each says something
    different about what the comparison then means:
      1. a vector shape is looked up by the (mnem, shape) PAIR, because
         its operand is 128 bits whatever the sweep's loop variable was
         (VECTOR_SHAPES above).  If the pair's rows carry more than one
         key_width the look-up refuses rather than picking one.
      2. `imm_symbolic_gpr` falls back to `imm_gpr` when our table
         carries no symbolic-immediate row -- which is the state of the
         table this task inherited, whose sweep predates those four
         spellings.  The fallback changes what the check proves: the
         comparison then holds at the ONE immediate our shape bakes in
         rather than at every immediate, and the cell says so in its
         `immediate_binding`.
      3. everything else is looked up by (mnem, shape, width).
    """
    if shape in VECTOR_SHAPES:
        rows = by_pair.get((mnem, shape))
        if not rows:
            return None, shape, None, None
        key_widths = set(row["key_width"] for row in rows)
        if len(key_widths) != 1:
            return None, shape, None, None
        return rows[0], shape, rows[0]["key_width"], None
    row = index.get((mnem, shape, width))
    if row is not None:
        return row, shape, width, None
    if shape == "imm_symbolic_gpr":
        row = index.get((mnem, "imm_gpr", width))
        if row is not None:
            return row, "imm_gpr", width, "literal"
    return None, shape, width, None


def build(semantics_folder, model_table_path):
    table = R.REFERENCE.opcode_table
    index, by_pair, our_triples = our_rows(model_table_path)
    matched = {}
    unmatched_theirs = []
    causes_theirs = {}
    seen_ours = set()

    def refuse(variant, folder, token, cause, extra=None):
        record = {"variant": variant, "folder": folder,
                  "mnem": token, "reason": cause}
        if extra:
            record.update(extra)
        unmatched_theirs.append(record)
        causes_theirs[cause] = causes_theirs.get(cause, 0) + 1

    for folder, variant, path in their_variants(semantics_folder):
        token = variant.split("_")[0]
        mnem, rule_fired, cause = our_mnem(token, table)
        if mnem is None:
            refuse(variant, folder, token, cause)
            continue
        entry = table.entries[mnem]
        if entry.build is None:
            refuse(variant, folder, token,
                   "our reference registers the mnemonic with no "
                   "builder, so our table states no mapping for it")
            continue
        try:
            parsed = k_to_z3.parse_file(path)
        except k_to_z3.Refused as refusal:
            refuse(variant, folder, token,
                   "their rule: %s" % refusal.cause,
                   {"detail": refusal.detail})
            continue
        shape, width, binding = shape_of_head(parsed.operands)
        if shape is None:
            refuse(variant, folder, token, binding)
            continue
        row, shape, width, rebound = look_up(index, by_pair, mnem,
                                             shape, width)
        if rebound is not None:
            binding = rebound
        if row is None:
            refuse(variant, folder, token,
                   "our model table has no translated row at that "
                   "operand form and width",
                   {"shape": shape, "width": width})
            continue
        seen_ours.add((mnem, shape, row["key_width"]))
        matched[variant] = {
            "folder": folder,
            "mnem": mnem,
            "their_mnem": token,
            "shape": shape,
            "width": width,
            "key_width": row["key_width"],
            "row_id": row["row_id"],
            "operands": row["operands"],
            "preseeded": row["preseeded"],
            "immediate_binding": binding,
            "their_operand_kinds": [operand.get("kind")
                                    for operand in parsed.operands],
            "reason": rule_fired,
            "attestation_ledger_rows": row["attestation_ledger_rows"],
            "attestation_units": row["attestation_units"],
        }

    unmatched_ours = []
    for mnem, shape, key_width in sorted(our_triples):
        if (mnem, shape, key_width) in seen_ours:
            continue
        unmatched_ours.append({"mnem": mnem, "shape": shape,
                               "key_width": key_width,
                               "reason": ("no variant of theirs states "
                                          "this mnemonic at this "
                                          "operand form and width")})
    return {
        "meta": {
            "what": ("the map from the K-framework x86-64 semantics' "
                     "variant names to our model table's (mnem, "
                     "operand shape, key_width) keys"),
            "their_source": semantics_folder,
            "their_licence": ("University of Illinois/NCSA Open Source "
                              "License; read from /sources, nothing "
                              "copied into this repository"),
            "our_model_table": model_table_path,
            "operand_order": k_to_z3.THE_ORDER,
        },
        "counts": {
            "their_variants": len(matched) + len(unmatched_theirs),
            "matched": len(matched),
            "unmatched_theirs": len(unmatched_theirs),
            "our_translated_triples": len(our_triples),
            "our_triples_reached": len(seen_ours),
            "unmatched_ours": len(unmatched_ours),
        },
        "causes_theirs": [{"count": causes_theirs[c], "reason": c}
                          for c in sorted(causes_theirs,
                                          key=lambda c:
                                          -causes_theirs[c])],
        "matched": matched,
        "unmatched_theirs": unmatched_theirs,
        "unmatched_ours": unmatched_ours,
    }


def main(argv):
    if len(argv) != 4:
        print(__doc__)
        return 2
    document = build(argv[1], argv[2])
    with open(argv[3], "w") as handle:
        json.dump(document, handle, indent=1, sort_keys=True)
    counts = document["counts"]
    print("their variants %d, matched %d, unmatched %d"
          % (counts["their_variants"], counts["matched"],
             counts["unmatched_theirs"]))
    print("our translated triples %d, reached %d, unmatched %d"
          % (counts["our_translated_triples"],
             counts["our_triples_reached"], counts["unmatched_ours"]))
    print("their side's causes, by count:")
    for record in document["causes_theirs"]:
        print("%8d  %s" % (record["count"], record["reason"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
