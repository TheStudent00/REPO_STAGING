#!/usr/bin/env python3
"""l3_cart_full_v2.py -- re-fold `matrices_full_v2/` from
`matrices_cart_v2/` (the log_057-fixed re-fold), via the EXISTING
`l3_cart_full.py` -- reused unmodified, only its input/output
directories are repointed.  NO NEW PROBE IS RUN.  `matrices_cart/` and
`matrices_full/` (the pre-fix generations) stay on disk unchanged for
audit.

VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree; the
OS-stopped outcome is ABORT.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l3_cart_full as F                                      # noqa: E402

F.CART = os.path.join(HERE, "matrices_cart_v2")
F.OUT = os.path.join(HERE, "matrices_full_v2")

if __name__ == "__main__":
    print("FULL GRIDS v2 -- re-fold matrices_cart_v2/ (log_057-fixed) "
          "into matrices_full_v2/; matrices_cart/ and matrices_full/ are "
          "untouched.")
    F.main()
