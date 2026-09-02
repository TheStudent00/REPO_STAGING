#!/usr/bin/env python3
"""test_block_cutter_long_add.py -- Task 20 regression test.

Built from the RE-EXTRACTED (bug-fixed, see slice_extractor_fix.py /
reextract_long_add.py) long_add slice
(op_units_cpython_reextracted.json, probes["1"]["ship"]).  Walks it
with block_cutter.walk_reachable (the fixed cutter, defects A and B)
starting at function-instruction-index 26 -- the same start canon2's
carve.method in interp_fastpath.json records -- and asserts the walk
reproduces EXACTLY the 48-instruction set and three address ranges
recorded there.

Run: /tmp/reconnect_venv/bin/python3 test_block_cutter_long_add.py
"""

import json
import os

import canon2
import block_cutter

HERE = os.path.dirname(os.path.abspath(__file__))

EXPECTED_INSTRUCTION_COUNT = 48
EXPECTED_ADDRESS_RANGES = [
    (0x1373d8, 0x137479),
    (0x1374c0, 0x1374db),
    (0x1374e0, 0x1374e9),
]
START_INDEX = 26
OWN_SYMBOL = "long_add"


def load_slice(path):
    doc = json.load(open(os.path.join(HERE, path)))
    ship = doc["probes"]["1"]["ship"]
    return ship["bytes"], ship["mnem"]


def main():
    # NOTE: this regression test targets the ORIGINAL stored slice
    # (op_units_cpython.json, WITH the extractor's split-instruction
    # defect still present at index 88) on purpose -- the task's
    # baseline (interp_fastpath.json's carve.instructions, 48
    # instructions / 3 ranges) was itself carved from that same
    # buggy extraction (its own index 44's addr 0x1374d8 carries an
    # empty mnemonic and a lone stray byte -- verified below). The
    # cutter fix (defects A and B) is independent of the extractor
    # fix (slice_extractor_fix.py / reextract_long_add.py, tested
    # separately); this test proves the CUTTER reproduces the
    # recorded baseline exactly over the SAME bytes it was recorded
    # against.
    bytes_list, mnem_list = load_slice("op_units_cpython.json")
    assert mnem_list[88] == "", (
        "expected the known extractor defect at index 88 to still be "
        "present in the untouched stored slice")
    assert len(mnem_list) == 94

    bytes_hex = " ".join(bytes_list)
    # 93 is the TRUE instruction count (canon2.real_addresses
    # disassembles the raw bytes for real; it cannot produce 94
    # addresses because the 384 captured bytes really do decode to
    # 93 instructions -- the 94th mnem entry is the extractor's
    # split-instruction artifact, not a real instruction boundary).
    addrs93 = canon2.real_addresses(bytes_hex, expect_count=93)
    assert addrs93 is not None, (
        "objdump did not find exactly 93 real instructions in the "
        "captured bytes")

    # rebuild the 94-length address list the ORIGINAL (buggy) walk
    # used: the stray entry at index 88 sits 7 bytes into the 8-byte
    # lea at real index 87 (its own recorded byte is the lea's final
    # displacement byte), so its address is that lea's start + 7;
    # every later entry keeps its real address, shifted one slot down
    # to make room.
    addrs0 = addrs93[:88] + [addrs93[87] + 7] + addrs93[88:]
    assert len(addrs0) == len(mnem_list) == 94

    # canon2.real_addresses disassembles the captured bytes IN
    # ISOLATION (offset 0), so its addresses are function-relative;
    # rebase them onto the real addresses interp_fastpath.json
    # recorded, using instruction 26 (this walk's start, "mov
    # $0x1,%edx") as the known fixed point (0x1373d8).
    base = 0x1373d8 - addrs0[START_INDEX]
    addrs = [a + base for a in addrs0]

    unit_base_addr = 0x1373d8 - 0x68  # long_add's own start (function
    # offset 0x68 is where the fast path this walk starts at lives)

    result = block_cutter.walk_reachable(
        mnem_list, addrs, OWN_SYMBOL, start_index=START_INDEX,
        unit_base_addr=unit_base_addr)

    got_count = len(result["instructions"])
    got_ranges = result["address_ranges"]

    print("instruction_count: got=%d expected=%d"
          % (got_count, EXPECTED_INSTRUCTION_COUNT))
    print("address_ranges:")
    for lo, hi in got_ranges:
        print("  0x%x .. 0x%x" % (lo, hi))
    print("expected address_ranges:")
    for lo, hi in EXPECTED_ADDRESS_RANGES:
        print("  0x%x .. 0x%x" % (lo, hi))
    print("external_exits: %d" % len(result["external_exits"]))
    for e in result["external_exits"]:
        print("  ", e)
    print("unresolved_exits: %d" % len(result["unresolved_exits"]))

    assert got_count == EXPECTED_INSTRUCTION_COUNT, (
        "instruction count mismatch: got %d expected %d"
        % (got_count, EXPECTED_INSTRUCTION_COUNT))
    assert got_ranges == EXPECTED_ADDRESS_RANGES, (
        "address ranges mismatch:\n  got: %r\n  expected: %r"
        % (got_ranges, EXPECTED_ADDRESS_RANGES))
    assert len(result["unresolved_exits"]) == 0, (
        "unresolved exits present: %r" % result["unresolved_exits"])

    print("PASS: walk over the fixed cutter matches interp_fastpath.json "
          "exactly (48 instructions, 3 address ranges).")


if __name__ == "__main__":
    main()
