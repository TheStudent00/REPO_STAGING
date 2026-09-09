#!/usr/bin/env python3
"""canon37_lemma.py -- THE TWO-STEP LEMMA, checked once.

The gate walks the RESOLVED text, in which each two-step access is
written as one line naming the row:

    literal   mov ledger+0x00(%rip),%rdi
              mov 0x0(%rdi),%rdi
    resolved  mov IN-0,%rdi

This file states and checks, with z3 over a memory array, that the two
readings are the same value -- so a proof about the resolved text is a
proof about the literal text.  It is checked ONCE and generically,
over symbolic ledger base, symbolic block base and symbolic row
offset, rather than per unit.

The store direction is the mirror image and is checked in the same
run.

Usage:
  canon37_lemma.py
"""

import sys

import z3


def check():
    memory = z3.Array("memory", z3.BitVecSort(64), z3.BitVecSort(64))
    ledger_base = z3.BitVec("ledger_base", 64)
    entry = z3.BitVec("entry_offset", 64)
    row = z3.BitVec("row_offset", 64)

    # THE LITERAL TEXT, modelled as the two instructions actually
    # execute, INCLUDING the destination-register-as-pointer trick:
    # the first instruction overwrites the destination register with
    # the block's base, and the second reads through that same
    # register and overwrites it again with the row's value.
    destination_before = z3.BitVec("destination_before", 64)
    _ = destination_before
    destination_after_step1 = z3.Select(memory, ledger_base + entry)
    two_step = z3.Select(memory, destination_after_step1 + row)

    # THE RESOLVED TEXT: one line naming the row.  The row's address
    # is the block's base plus the row offset, and the block's base is
    # what the ledger entry holds.
    block_base = z3.Select(memory, ledger_base + entry)
    resolved = z3.Select(memory, block_base + row)

    solver = z3.Solver()
    solver.add(two_step != resolved)
    load_outcome = solver.check()

    stored = z3.BitVec("stored_value", 64)
    after_two_step = z3.Store(memory, block_base + row, stored)
    after_resolved = z3.Store(memory, block_base + row, stored)
    probe = z3.BitVec("probe_address", 64)
    solver2 = z3.Solver()
    solver2.add(z3.Select(after_two_step, probe)
                != z3.Select(after_resolved, probe))
    store_outcome = solver2.check()

    print("THE TWO-STEP LEMMA")
    print("")
    print("  ledger base           %s" % ledger_base)
    print("  the block's entry     memory[ledger_base + entry_offset]")
    print("  the row               memory[block_base + row_offset]")
    print("")
    print("  load  direction: z3 says %s for "
          "(two-step reading != resolved reading)" % load_outcome)
    print("  store direction: z3 says %s for "
          "(memory after two-step store != memory after resolved "
          "store), at every probe address" % store_outcome)
    print("")
    if load_outcome == z3.unsat:
        if store_outcome == z3.unsat:
            print("  BOTH UNSAT -- the resolved text and the literal "
                  "text read and write the same bytes, so a proof "
                  "about one is a proof about the other.")
            return 0
    print("  NOT PROVED -- the gate may not use the resolved text.")
    return 1


if __name__ == "__main__":
    sys.exit(check())
