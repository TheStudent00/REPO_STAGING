#!/usr/bin/env python3
"""l3_cart_read_v2.py -- re-fold `matrices_cart_v2/` from the SAME raw
lane output `matrices_cart/` was built from, now that the ruby `Float`
canon fault is fixed (log_057, 2026-08-22):

  - `canon_output_printed` (l3_per_op_matrices.py) no longer reads a
    binary float/double's printed text as an EXACT DECIMAL; it goes
    through the double (`Fraction(float(text))`) for FLOAT_TYPES, and
    keeps the direct decimal parse for genuinely decimal types
    (BigDecimal, Rational, ...) where the printed text already IS the
    exact value.
  - `ruby_canon` (l3_interval_read.py) now carries a self-check that
    fails loudly if a `Float:` payload's canon is not independently
    reproducible from `float(text)`.

NO NEW PROBE IS RUN.  This is a pure re-fold of the same lane output
`matrices_cart/` read, through the fixed conversion.  `matrices_cart/`
stays on disk, byte-for-byte unchanged, as the pre-fix audit trail.

Mechanically: a thin wrapper around the settled `l3_cart_read.py` --
its logic is reused unmodified, only its output directory is
repointed, in the same spirit `l3_per_op_matrices_v2.py` reused v1.

VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree; the
OS-stopped outcome is ABORT.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l3_cart_read as R                                      # noqa: E402

R.OUT_DIR = os.path.join(HERE, "matrices_cart_v2")

if __name__ == "__main__":
    print("CARTESIAN matrices v2 -- re-fold with the log_057 ruby Float "
          "canon fix; matrices_cart/ is untouched, output -> %s"
          % R.OUT_DIR)
    R.main()
