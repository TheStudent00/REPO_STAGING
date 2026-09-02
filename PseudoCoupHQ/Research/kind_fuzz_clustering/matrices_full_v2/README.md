# full-grid matrices

the owner's ruling of 2026-08-21 (log 054): every profile is inflated to the FULL X set of its form and level, so every profile of one (form_pair, level) carries the SAME key set, always.  A cell whose key involves an operand the holder cannot represent carries the distinct static token `UNREPRESENTABLE` -- no probe was run for it, none was needed, and it is NOT a decline (the language was never asked).

Assembly over `matrices_cart/` through the probe-index rule applied verbatim (level 1 `p = i0*|Xb| + i1`, level 2 `p = ((i0*|Xb| + i1)*|Xa| + i2)*|Xb| + i3`); every measured cell is copied byte-for-byte and `matrices_cart/` stays on disk unchanged for the audit.

Columns are the matrices_cart pattern plus three: `n_unrepresentable` (the static fills in the row) and `src_x_set_a` / `src_x_set_b` (the measured run's own set ids, so every cell traces to its source).  `x_set_a` / `x_set_b` now name the FULL form-level sets recorded in `index.json`.
