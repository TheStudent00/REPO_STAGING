#!/usr/bin/env python3
"""fix_cpython_type_key.py -- task 5(a): fix the cpython type key by
machine fact instead of assertion (log_082 finding 2).

THE DEFECT. `interp_feeder.py`'s `format_cpython` hardcodes
`"lhs_rep": "i32", "rhs_rep": "i32"` for the cpython `long_add` unit.
`long_add`'s own C signature is
`long_add(PyLongObject *a, PyLongObject *b)` -- two POINTERS, not two
32-bit integers.  That hardcode landed unchanged in
`sem_anchored_spill_cpython.json`'s `meta.lhs_rep` /
`meta.rhs_rep`, so the cpython unit sits in the SAME type-pair key
("i32,i32") as every genuinely-32-bit integer-addition unit from the
five compiled languages.  This is exactly the shape the int32_t
ruling exists to forbid: an unratified equation between a pointer and
a value, made by assertion rather than measurement.

THE FIX, BY MACHINE FACT. `sem_anchored_spill_cpython.json` already
carries the unit's own lifted expression (pyvex, forced by
construction from the actual compiled bytes of the anchor/ship
`long_add` -- see interp_cpython.md).  Read block 6's value, verbatim:

    Add64(5:64,
      Add64(
        Mul64(Sub64(1:64,in0:64), zx64(ld32/g0(Add64(24:64,in1:64)))),
        Mul64(
          Sub64(1:64, zx64(And32(3:32, ex32@0(ld64/g0(Add64(16:64,in0:64)))))),
          zx64(ld32/g0(Add64(24:64,in1:64))))))

Two machine facts are read off this text, not assumed:

  1. `in0` and `in1` are used DIRECTLY as 64-bit values inside 64-bit
     arithmetic (`Sub64(1:64,in0:64)`) -- so the register pyvex named
     `in0`/`in1` (the first two argument registers, %rdi/%rsi under
     the anchored naming) is itself 64 bits wide.  A genuine 32-bit
     int argument would arrive zero/sign-extended into a 64-bit
     register (`zx64(...)` or `sx64(...)` wrapping a 32-bit read),
     the way every c/cpp/go/rust/swift i32 unit in this corpus does.
     `in0`/`in1` here carry NO such extension -- they are native
     64-bit values from the moment they are read.
  2. `in0` and `in1` are the BASE of pointer-offset loads:
     `ld64/g0(Add64(16:64,in0:64))` and `ld32/g0(Add64(24:64,in1:64))`
     -- "load 64/32 bits from (in0 + 16)" and "load 32 bits from
     (in1 + 24)".  A fixed-offset load off a register is the
     dereference pattern; it is what a C compiler emits for
     `a->long_value.ob_digit[...]`-shaped field access on a struct
     pointer, never for reading a plain scalar argument.

Both facts are FORCED BY CONSTRUCTION (evidence doctrine, AgentMemory):
they rest only on the assumption that pyvex lifted the actual compiled
bytes correctly, the same assumption every other unit in this corpus
already rests on.

THE KEY. Because the register is 64 bits wide and is used as a
pointer base, the honest type key is a POINTER key, not an integer
key: `lhs_rep = "ptr64"`, `lhs_type = "PyLongObject*"` (read from the
unit's own C signature, recorded in interp_cpython.md, human
interpretation of stated design -- the weaker class, marked as such),
same for rhs.  This key is DELIBERATELY different from every
compiled-language i32 unit's `"i32,i32"` key.

IF THIS MAKES IT INCOMPARABLE, THAT IS THE CORRECT OUTCOME (per the
brief).  `ptr64,ptr64` shares no type-pair key with any `i32,i32`
class, so this unit CANNOT be pulled into an integer-addition
dominant-operator family by type coincidence.  Whether cpython's
`long_add` belongs in some OTHER family (a pointer-argument /
tagged-representation family) is an ontology question -- new family
axis -- and is flagged for the owner, not decided here (STOP RULE).

WHAT THIS SCRIPT DOES. Reads `sem_anchored_spill_cpython.json`
(unmodified, per the no-edit-existing-artifacts rule), writes a NEW
file `sem_anchored_spill_cpython_fixed.json` that is byte-identical
except for the four `meta` fields on unit "1"
(`lhs_rep`, `lhs_type`, `rhs_rep`, `rhs_type`) and a `meta_fix` block
recording what changed, why, and the evidence class.  The `sem`
block (the actual lifted machine facts) is copied verbatim -- nothing
about the measured bytes or lifted expression changes, only the
label we key on.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

SRC = os.path.join(HERE, "sem_anchored_spill_cpython.json")
OUT = os.path.join(HERE, "sem_anchored_spill_cpython_fixed.json")

EVIDENCE_NOTE = (
    "lhs_rep/rhs_rep changed from the feeder's hardcoded 'i32' (an "
    "assertion, never measured) to 'ptr64', read from the unit's own "
    "block-6 lifted expression: in0/in1 are used directly as 64-bit "
    "values (Sub64(1:64,in0:64), no zero/sign-extension wrapper -- "
    "contrast every genuine i32 unit in this corpus, which arrives "
    "wrapped in zx64/sx64) AND as the base of fixed-offset loads "
    "(ld64/g0(Add64(16:64,in0:64)), ld32/g0(Add64(24:64,in1:64))), "
    "the dereference pattern.  Evidence class: forced by construction "
    "(rests only on pyvex having lifted the actual compiled bytes "
    "correctly -- the same assumption every other unit in this corpus "
    "already carries).  lhs_type/rhs_type set to 'PyLongObject*', "
    "read from long_add's own C signature in interp_cpython.md -- "
    "human interpretation of stated design, the weaker class, marked "
    "as such here."
)


def main():
    doc = json.load(open(SRC))
    unit = doc["units"]["1"]
    meta = unit["meta"]

    before = dict(lhs_rep=meta["lhs_rep"], lhs_type=meta["lhs_type"],
                   rhs_rep=meta["rhs_rep"], rhs_type=meta["rhs_type"])

    meta["lhs_rep"] = "ptr64"
    meta["lhs_type"] = "PyLongObject*"
    meta["rhs_rep"] = "ptr64"
    meta["rhs_type"] = "PyLongObject*"

    unit["meta_fix"] = {
        "changed_by": "fix_cpython_type_key.py",
        "before": before,
        "after": dict(lhs_rep=meta["lhs_rep"], lhs_type=meta["lhs_type"],
                       rhs_rep=meta["rhs_rep"], rhs_type=meta["rhs_type"]),
        "note": EVIDENCE_NOTE,
        "evidence_class": "forced by construction (register width and "
                           "dereference pattern) plus human "
                           "interpretation of stated design (the "
                           "pointer's named C type)",
        "consequence": "type_pair key becomes 'ptr64,ptr64', which "
                        "shares no key with any i32,i32 class in the "
                        "five-language corpus.  This unit is therefore "
                        "INCOMPARABLE to the integer-addition families "
                        "by type-pair.  That is the correct outcome, "
                        "not a defect -- see module docstring.  Whether "
                        "it belongs to some OTHER family (a "
                        "pointer/tagged-representation axis) is an "
                        "ontology question flagged for the owner, not "
                        "decided here.",
    }

    doc["fix_note"] = ("meta.lhs_rep/rhs_rep/lhs_type/rhs_type on unit "
                        "'1' corrected by fix_cpython_type_key.py from "
                        "the feeder's hardcoded i32,i32 to the "
                        "machine-fact ptr64,ptr64 key.  See "
                        "units['1'].meta_fix for the full account.  "
                        "The sem block (lifted expression, blocks) is "
                        "unchanged from sem_anchored_spill_cpython.json.")

    json.dump(doc, open(OUT, "w"), indent=1)
    print("wrote", OUT)
    print("before:", before)
    print("after: ", dict(lhs_rep=meta["lhs_rep"], lhs_type=meta["lhs_type"],
                           rhs_rep=meta["rhs_rep"], rhs_type=meta["rhs_type"]))


if __name__ == "__main__":
    main()
