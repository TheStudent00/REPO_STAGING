# Tools

PseudoIR's tools. HIGH change threshold — no litter. Same rule as
PseudoCoup's: one tool, one folder, self-contained, with a falsifiable
acceptance test beside it.

## borrowing from the other project

Two modules here reach into PseudoCoup, which is the borrow the plan
licenses — PseudoCoup lends PseudoIR its toolchain.

- `insert/cross_border.py` takes the canonical i64 range from
  PseudoCoup's `Tools/polyfill/wrap_fixed_width.py`.
- `intentions/validate_form.py` takes the parser from PseudoCoup's
  `Tools/ledgerer/tree_sitter/parse_source.py`.

Both resolve PseudoCoup through `PSEUDOCOUP_ROOT`, defaulting to
`~/Programming/PseudoCoup_v6`, and refuse with a named error if it is
not there. That is the same environment-variable pattern the suites
used before their fixtures were vendored in (2026-07-31).

Run:

    PSEUDOCOUP_ROOT=~/Programming/PseudoCoup_v6 \
        python3 -m pytest ~/Programming/PseudoIR/Tools -q
