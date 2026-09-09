# Task ap4 — closing the four languages: the contract for a value that is not in a register, and the loop's fourth pass

Law: `PseudoCoupHQ/Research/LAW.md`, ALL of it. Then
`task_ap3_brief.md`, `task_ap2_brief.md` beside this file and their logs
`DevComms/log_245` (§"Awaiting the owner", the x87 finding, the fix-1
measurement), `log_244`, `log_242` §7–§8 (the arrival-contract finding as
first stated); the driver `.../emulation/handful/handful.py` (its check,
where "the IN rows cannot be aligned" is raised, ~line 2110) and
`.../emulation/autopoly/autopoly.py`; `Research/op_pipeline/ledger.py`
(`build_epilogue` ~line 1570: the "no answer home" refusal; `wrap_unit`
~2061/2132: how arrivals are loaded and the answer stored) and
`canonical_form.py`; `Research/op_pipeline/lean/model_translate.py`
(`preseeded_state`: the reference already models the x87 stack as places).
Instance `ap4.conf` (copy from `Airlock/instances/ap4.conf`;
mounts `sandbox-persist` read-only). Artifact folder: `.../emulation/autopoly/`,
writing `autopoly4_*`; lanes under `lanes_ap4/`.

## 1. The ruling this task carries out (the owner, 2026-09-09)
"Proceed with closing the four languages." The one question ap1–ap3 left
is a value the machine holds somewhere other than a fresh register:
| case | runs | what the contract could not say |
|---|---|---|
| a derived arrival: `idiv` reads three arrivals where `/` reads two (the high half is `cltd` of the low); `xor %eax,%eax` reads one where `^` reads two; `mov $imm` reads none where `=` reads one | 38 places, 12 cells | an input that is a function of another input, or absent |
| the x87 cells on c: `long double` renders, compiles, carves to `faddp %st,%st(1)` — and the canonical form names no answer home for `st(0)` and no arrival for a value on the stack | 92 | a place that is not a register family |
| register-to-register copies whose compiled body is empty (`movaps`, `movdqa`) | 23 | the answer IS the arrival |
the owner's ruling: the contract may state a place by a CONSTRAINT, not only by a
register name. One extension, in the layer that owns each half.

## 2. The three changes, and where each lives
1. **Derived arrivals — in the DRIVER's check, as a region.** When the
   cell reads more arrivals than the emulation (or fewer), do not align row
   by row: substitute. The relation is read from the cell's own setup: an
   arrival the corpus always produces by a zero-operand setup instruction
   (`cltd`/`cqto`: IN-high = sign-extend(IN-low); the widening tables in
   `reference.SPREAD_SIGN`/`ACCUMULATOR_WIDEN`) is replaced in the cell's
   term by that function of the other arrival; `gpr_same` cells (`xor
   %eax,%eax`, `sub %eax,%eax`, `test %eax,%eax`) bind both operands to the
   one arrival; an immediate is a constant. Then pose cell(term with the
   substitution) == emulation over the shared arrivals, and record the
   REGION as a sentence in the run (`"on the region IN-2 = SignExt(IN-1)"`).
   A cell whose extra arrival has no such relation in the attestation
   stays refused, with the cause naming the arrival.
2. **The x87 stack — in the CANONICAL FORM, as loads and stores at the
   edges, which is what the canonical form is for.** Authorised, minimal,
   in `ledger.py`: an answer whose home is `st(0)` gets an epilogue that
   stores it to OUT-0 as ten bytes (`fstpt OUT-0`), and an arrival of that
   kind gets a prelude that loads it from its IN row (`fldt IN-k`); the body
   stays verbatim between them, as ruled 2026-09-02. `result_family` for
   such a unit is the x87 family the ledger already names for its rows.
   Guards: `check_L2` (259 / 172 / 87), o8's 243-row totals
   (243/197/155/216), and the h2 handful, all unchanged — paste all three.
   Then the 30 x87 c rows re-run; rust, go and swift stay refused by
   nature.
3. **The identity — in the DRIVER.** An emulation whose carved body is
   empty is the identity on its arrival: pose cell == IN-0 (the arrival of
   the answer's family and width) and record `composition = []`,
   `landing = IDENTITY`. No new outcome name: the gate's own words carry
   the verdict; `IDENTITY` is a landing, like LANDED.

## 3. The loop, fourth pass
Exactly ap3's loop over the same cells, writing `autopoly4_*`; the
per-target table; the all-four count and share across four passes; the
change table (ap3 → ap4) per cause with where each run went; every run
that carries a REGION sentence listed with its verdict; every new `sat`
with its counterexample; runs ap3 proved that ap4 does not (expected 0,
and a non-zero is a stop).

## 4. Deliverable
`autopoly4.md`; the three guards' tallies; guard over every json; log
(next free number, check right before writing); verifier lane; PROGRESS on
the autopoly node; sync-back; instance down. Memory: bound 6g, sample 20,
peak RSS, abort `ABORT_MEMORY_AP4`. Stop rules per LAW; the only shared
file this brief authorises is `ledger.py` (and `canonical_form.py` only if
the refusal text lives there too), for change 2, with the three guards.
Never delete anything under `<runs>/` or `Airlock/`.
Reply with the per-target table, the four-pass all-four line, the change
table, the region list's totals by verdict, the three guard tallies, the
tally, the two lists.
