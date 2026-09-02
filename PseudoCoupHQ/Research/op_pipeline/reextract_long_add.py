#!/usr/bin/env python3
"""reextract_long_add.py -- Task 20 step 3: applies slice_extractor_fix
to the STORED long_add slice (op_units_cpython.json probes["1"]["ship"]),
writes a NEW re-extracted JSON, and prints the diff at the defect site
(index 88).

Run: /tmp/reconnect_venv/bin/python3 reextract_long_add.py
"""

import json
import os
import sys

import slice_extractor_fix

HERE = os.path.dirname(os.path.abspath(__file__))

SRC = os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1
                    else "op_units_cpython.json")
DST = os.path.join(HERE, sys.argv[2] if len(sys.argv) > 2
                    else "op_units_cpython_reextracted.json")

# the exact 8-byte encoding of the lea at stored index 87, confirmed
# present verbatim in the slice's own recorded flat byte stream
# (op_units_cpython.json probes["1"]["ship"]["bytes"][353:361]):
#   48 8d 84 38 f0 36 00 00  ==  lea 0x36f0(%rax,%rdi,1),%rax
LEA_BYTES = ["48", "8d", "84", "38", "f0", "36", "00", "00"]


def main():
    doc = json.load(open(SRC))
    ship = doc["probes"]["1"]["ship"]
    old_mnem = ship["mnem"]

    bad_indices = [i for i, m in enumerate(old_mnem) if m == ""]
    assert bad_indices == [88], (
        "expected exactly one empty-mnem entry at index 88, found %r"
        % bad_indices)

    new_mnem, repairs = slice_extractor_fix.repair_stored_slice(
        old_mnem, LEA_BYTES)

    assert len(repairs) == 1
    assert repairs[0]["removed_index"] == 88
    assert repairs[0]["old_text_at_prev_index"] == \
        "lea    0x36f0(%rax,%rdi,1),%rax"
    fixed_text = repairs[0]["new_text_at_prev_index"]

    print("=== defect site diff (op_units_cpython.json, "
          "probes[1].ship.mnem) ===")
    print("index 87 before: %r" % old_mnem[87])
    print("index 88 before: %r  (stray tail byte, empty mnemonic)"
          % old_mnem[88])
    print("index 89 before: %r" % old_mnem[89])
    print("---")
    print("index 87 after:  %r" % new_mnem[87])
    print("index 88 after:  %r  (was index 89 before the merge)"
          % new_mnem[88])
    print("total instructions before: %d, after: %d"
          % (len(old_mnem), len(new_mnem)))

    new_doc = json.loads(json.dumps(doc))  # deep copy
    new_doc["probes"]["1"]["ship"]["mnem"] = new_mnem
    new_doc["probes"]["1"]["ship"]["extraction_repair_log"] = [{
        "removed_index": 88,
        "old_text_at_prev_index_87": repairs[0]["old_text_at_prev_index"],
        "new_text_at_prev_index_87": fixed_text,
        "fixed_by": "slice_extractor_fix.repair_stored_slice, "
                    "re-disassembled for real via objdump on the "
                    "recorded 8-byte encoding at flat-byte offset 353",
    }]
    json.dump(new_doc, open(DST, "w"), indent=2)
    print("wrote %s" % DST)


if __name__ == "__main__":
    main()
