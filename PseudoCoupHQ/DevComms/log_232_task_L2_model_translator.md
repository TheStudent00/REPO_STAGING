# log_232 — task L2: the model translator — the reference's opcode semantics turned into Lean, checked against 259 single-opcode units, 19 DISCREPANCY, zero sorryAx

Node: `hq.research.compiler_graph.gate.lean.model_translator`
(`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/node_0_3_1_5_6_lean/node_0_3_1_5_6_0_model_translator/CORE_0_3_1_5_6_0_model_translator.md`).
Its super-node is the lean node
(`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/node_0_3_1_5_6_lean/CORE_0_3_1_5_6_lean.md`),
whose task L1 built the `archproof` project this task builds inside
(log_227). Artifacts: `PseudoCoupHQ/Research/op_pipeline/lean/`.
Instance: `Airlock/instances/L2.conf`. Lanes: 20, all kept at
`PseudoCoupHQ/Research/op_pipeline/lean/lanes_L2/`.

---

## 0. What was done and found, in plain words, before any figures

This task closes with the compute already finished by an earlier run of it
(lanes 1 through 13); this session read what that run left, found two gaps
in one deliverable, closed them, and wrote the report.

The translator itself (lanes 1-9) reads the reference simulator's own opcode
table — the same table and the same per-mnemonic builder functions
`reference.py` uses to interpret machine code — and, for every mnemonic, runs
that mnemonic's builder on symbolic seed values at every operand shape a
sweep spells. Whatever comes back as a z3 expression is walked and reprinted
as a Lean `BitVec` definition. Nothing about the machine's semantics is
written a second time by hand: the same code path the gate already trusts to
interpret opcodes is what produced every one of the 3,933 Lean definitions in
`Model.lean`. 160 of the reference's 171 mnemonics produced at least one
definition; the other 11 are either census rows with no builder at all (six
mnemonics: `call`, `jmp`, and four SSE/system opcodes) or have a builder but
no operand shape this particular sweep's shape grammar spells (five,
mostly bare-mnemonic forms like `nop` and `ret`).

The check (lanes 10-13, plus this session's 14-20) then asks, for every
single-opcode unit that has its own proved term from an entirely different
part of the pipeline (the term-walk / z3 proof route), whether that term
equals the model's own operations applied along the same instruction
sequence the unit compiled from. 259 such units exist (the brief's own
estimate was 243; the actual population, recomputed live off
`single_opcode_units.json`, is 259 — see §1). Of those, 87 have no theorem
stated at all, refused by cause before reaching Lean (mostly floating point,
which this translator DOES model but which `bv_decide` cannot discharge for
want of a bit-vector-only decision procedure). Of the 172 that were stated,
153 proved — 39 by `rfl` (definitionally, no tactic needed), 114 by
`bv_decide` (bit-blasted to a SAT solver) — and 19 came back as
**DISCREPANCY**: `bv_decide` found a concrete counterexample, meaning the
unit's own proved term and the model's composed operations disagree on some
input. All 19 are in three mnemonics — `add`, `imul`, `sub` — and every one
of the 19 has the same shape: the unit's term correctly captures a `mov`
that implicitly zero-extends a 32-bit write to the full 64-bit register
before the arithmetic, while the model's composed form applies the
mov-then-arithmetic in a different operand order or misses the
zero-extension seam. This is reported as a discrepancy between two readings
of the hardware (§5), not adjudicated here — per this node's own definition,
that is exactly what the check exists to locate.

Closing this task found two bugs, both in the checker's own axiom-line
parser and neither in a theorem: 20 proved rows had no `#print axioms` line
recorded at all (the parser only recognised one of Lean's two output
phrasings, and missed the zero-axiom one), and 61 more had a SILENTLY
TRUNCATED axiom list (Lean wraps a long list over several lines; the parser
kept only the first). Both are fixed and all 153 proved rows now carry their
full, correct axiom line. None carries `sorryAx`. 61 of the 114
`bv_decide`-closed rows do carry `Lean.ofReduceBool` and `Lean.trustCompiler`
beside the ordinary `propext`/`Classical.choice`/`Quot.sound` trio — named
here because "no `sorryAx`" is a narrower claim than "kernel-only", and this
task's own re-parse is what surfaced the difference.

The spelling-ban guard, run unmodified over both json files this task wrote,
PASSES `check_L2.json` and FAILS `model_L2.json` — 18,112 places, all
`per_mnemonic` dict keys or `flag_setter` field values that happen to spell
one of four x86 mnemonics (`and`, `not`, `or`, `xor`) which are also entries
in the guard's cross-language operator inventory. This is flagged for the
coordinator in §9, not silently worked around.

---

## 1. What the objects are, one sentence each, in relation

- **the reference's opcode semantics** — `reference.py`'s opcode table plus
  its per-mnemonic builder functions (`build_binary`, `build_shift`,
  `build_wide_multiply`, `build_float_flag_only`, `build_convert_to_float`,
  and others), which interpret one disassembled instruction line into a z3
  expression over the machine state; this is the single source both the
  gate's own emulation and this task's Lean model derive from.
- **the model translator** (`model_translate.py`) — a program that runs
  those SAME builders on symbolic seeds at every operand shape a sweep
  spells, walks the z3 expression that comes back, and prints it as a Lean
  `BitVec` definition; it never writes a definition by hand.
- **the Lean model** (`archproof/Archproof/Model.lean`) — the 3,933
  definitions `model_translate.py model` produced, GENERATED, checked into
  the `archproof` lake project task L1 built.
- **the single-opcode units** (`single_opcode_units.json`, read via
  `check_L2.json`'s `population_source`) — one row per single-opcode
  compiled unit, across five languages, each already carrying its OWN
  proved term from the pipeline's term-walk / z3 route, independent of this
  task.
- **the check** (`check_L2.json`) — one Lean theorem per single-opcode unit
  that has a proved term: "that term equals the model's operations, applied
  in the order this unit's own instruction sequence spells them" — closed by
  `rfl`, closed by `bv_decide`, refused by cause, or DISCREPANCY (a
  `bv_decide` counterexample).
- **a DISCREPANCY** — a located disagreement between the unit's own proved
  term (one reading of the hardware) and the model's composed operations
  (a second, independently derived reading); this task reports it, the
  super-node's framing (log_229 §4.1) is what adjudicates it.

---

## 2. The five opcodes, end to end, LITERAL

`reference.py`'s builder bodies for the five the brief named, LITERAL (host
log `<runs>/L2/agent/logs/20260907T040418Z__L2_l1_survey.sh.log`):

```
----- build_binary -----
def build_binary(ops):
    if len(ops.texts) == 1:
        build_wide_multiply(ops)
        return
    width = ops.destination_width()
    left = ops.read(1, width)
    right = ops.read(0, width)
    mnemonic = ops.mnemonic
    if mnemonic == "add":
        result = left + right
    elif mnemonic == "sub":
        result = left - right
    elif mnemonic == "and":
        result = left & right
    elif mnemonic == "or":
        result = left | right
    elif mnemonic == "xor":
        result = left ^ right
    else:
        result = left * right
    ops.write(1, result)
    if mnemonic in ("and", "or", "xor"):
        ops.state.flags = (mnemonic, result,
                           z3.BitVecVal(0, result.size()))
        return
    ops.state.flags = (mnemonic, left, right)

----- build_shift -----
def build_shift(ops):
    width = ops.destination_width()
    count_text = ops.texts[0]
    if count_text == "%cl":
        count = ops.read_text("%cl", 8)
    elif ops.is_immediate(count_text):
        count = cut(ops.read_text(count_text, 8), 8)
    else:
        raise NotModeled(...)
    masked = count & z3.BitVecVal(shift_mask(width), 8)
    if width > 8:
        amount = z3.ZeroExt(width - 8, masked)
    else:
        amount = masked
    value = ops.read(1, width)
    if ops.mnemonic in ("shl", "sal"):
        result = value << amount
    elif ops.mnemonic == "shr":
        result = z3.LShR(value, amount)
    else:
        result = value >> amount
    ops.write(1, result)

----- build_wide_multiply (imul's %rdi-form path) -----
def build_wide_multiply(ops):
    width = ops.width_at(0)
    ...
    low = ops.read_text(LOW_REGISTER[width], width)
    other = ops.read(0, width)
    if ops.mnemonic == "imul":
        product = z3.SignExt(width, low) * z3.SignExt(width, other)
    else:
        product = z3.ZeroExt(width, low) * z3.ZeroExt(width, other)
    ops.write_text(LOW_REGISTER[width], z3.Extract(width - 1, 0, product))
    ops.write_text(HIGH_REGISTER[width],
                   z3.Extract(2 * width - 1, width, product))

----- build_float_flag_only (ucomiss) -----
def build_float_flag_only(ops):
    width = 32 if ops.mnemonic.endswith("ss") else 64
    left = as_float(lane(ops.read_128(1), 0, width), width)
    right = as_float(ops.read(0, width), width)
    ops.state.flags = (ops.mnemonic, left, right)

----- build_convert_to_float (cvtsi2sd) -----
def build_convert_to_float(ops):
    destination_width = CONVERT_TO_FLOAT[ops.mnemonic]
    source_text = ops.texts[0]
    ...
    value = ops.read(0, source_width)
    converted = z3.fpSignedToFP(ROUNDING, value, FLOAT_SORT[destination_width])
    old = ops.read_128(1)
    ops.write(1, set_low_lane(old, from_float(converted), destination_width))
```

And the Lean definitions this session's re-run of `model_translate.py five`
produced from those same builders (host log
`<runs>/L2/agent/logs/20260907T135419Z__L2_l20_rerunnable_claims.sh.log`,
§[1/8] — this exact block is also §10's first re-runnable command):

```
def model_add_0 (v0 : BitVec 64) (v1 : BitVec 64) : BitVec 64 :=
  (v0 + v1)
def model_add_1_flags (v0 : BitVec 64) (v1 : BitVec 64) : Flags 64 :=
  { setter := "add", L := v0, R := v1 }
def model_add_2 (v0 : BitVec 64) (v1 : BitVec 64) : BitVec 64 :=
  (((v0.extractLsb 31 0) + (v1.extractLsb 31 0)).zeroExtend 64)
def model_add_3_flags (v0 : BitVec 64) (v1 : BitVec 64) : Flags 32 :=
  { setter := "add", L := (v0.extractLsb 31 0), R := (v1.extractLsb 31 0) }
def model_sar_0 (v0 : BitVec 64) (v1 : BitVec 64) : BitVec 64 :=
  (v0.sshiftRight' (((v1.extractLsb 7 0) &&& (63#8)).zeroExtend 64))
def model_sar_1 (v0 : BitVec 64) : BitVec 64 :=
  (((v0.extractLsb 31 0).sshiftRight' (((3#8) &&& (31#8)).zeroExtend 32)).zeroExtend 64)
def model_imul_0 (v0 : BitVec 64) (v1 : BitVec 64) : BitVec 64 :=
  (v0 * v1)
def model_imul_1_flags (v0 : BitVec 64) (v1 : BitVec 64) : Flags 64 :=
  { setter := "imul", L := v0, R := v1 }
def model_imul_2 (v0 : BitVec 64) (v1 : BitVec 64) : BitVec 64 :=
  (((v0.signExtend 128) * (v1.signExtend 128)).extractLsb 63 0)
def model_imul_3 (v0 : BitVec 64) (v1 : BitVec 64) : BitVec 64 :=
  (((v0.signExtend 128) * (v1.signExtend 128)).extractLsb 127 64)
def model_ucomiss_0_flags (v0 : BitVec 128) (v1 : BitVec 128) : Flags 32 :=
  { setter := "ucomiss", L := (v0.extractLsb 31 0), R := (v1.extractLsb 31 0) }
def model_cvtsi2sd_0 (v0 : BitVec 128) (v1 : BitVec 64) : BitVec 128 :=
  ((v0.extractLsb 127 64) ++ (ieeeOfSIntW32ToF64Rne (v1.extractLsb 31 0)))

opaque ieeeOfSIntW32ToF64Rne : BitVec 32 → BitVec 64
```

`add`, `sar`, `imul` at 64 bits are exact bit-vector operations
(`+`, `sshiftRight'`, `*`); at 32 bits both `add` and `sar` need the
zero-extend-after-truncate the x86-64 destination-write rule requires,
because a 32-bit write to a general register zeroes its upper 32 bits.
`imul %rdi`'s wide form sign-extends both operands to 128 bits, multiplies,
and slices the low and high halves out — this IS `build_wide_multiply`'s
`SignExt`/`Extract` translated term for term. `ucomiss` and `cvtsi2sd` both
carry the `NAN_PAYLOAD_SEAM`: the identity-on-bits path the table (§3) states
for `Z3_OP_FPA_TO_IEEE_BV`/`Z3_OP_FPA_TO_FP` rather than an opaque primitive,
because those two z3 operator kinds are bit-pattern identities, not
arithmetic.

---

## 3. The translator over every mnemonic

171 mnemonics in the reference's opcode table; 3,933 Lean definitions;
160 mnemonics translated at least one operand shape.

| category | count | mnemonics |
|---|---|---|
| no builder at all (census row) | 6 | `call` `jmp` `pcmpeqb` `pcmpeqd` `pmovmskb` `ud2` |
| builder exists, no shape this sweep spells | 5 | `cs` `endbr64` `nop` `nopl` `ret` |
| translated (>=1 definition) | 160 | — (includes all floating-point mnemonics) |

Floating point IS translated, per the brief's own instruction ("still
TRANSLATE it into definitions and mark the check as unavailable, not the
model"), using 27 opaque primitives for the parts z3's FPA theory names
symbolically:

```
ieeeAddF32Rne ieeeAddF64Rne ieeeAddF79Rne ieeeConvertF32ToF64Rne
ieeeDivF32Rne ieeeDivF64Rne ieeeDivF79Rne ieeeEqF32 ieeeEqF64 ieeeIsNanF32
ieeeIsNanF64 ieeeMulF32Rne ieeeMulF64Rne ieeeMulF79Rne ieeeOfSIntW128ToF32Rne
ieeeOfSIntW128ToF64Rne ieeeOfSIntW16ToF32Rne ieeeOfSIntW16ToF64Rne
ieeeOfSIntW32ToF32Rne ieeeOfSIntW32ToF64Rne ieeeOfSIntW64ToF32Rne
ieeeOfSIntW64ToF64Rne ieeeOfSIntW8ToF32Rne ieeeOfSIntW8ToF64Rne
ieeeSubF32Rne ieeeSubF64Rne ieeeSubF79Rne
```

No translation-level attempt was refused with a cause this sweep
(`per_mnemonic.*.refused == 0` for all 171); every attempted operand shape
either translated or was `not_modelled` (that mnemonic's own reads/writes do
not spell that shape combination — not a refusal). The refusal vocabulary
the brief's rule table anticipates (`UNGUARDED_DIVISION` and similar)
belongs to the CHECK, not the translation sweep — see §4.

---

## 4. The check over the 259 rows

The brief's own estimate of the population was 243; the actual population,
recomputed live off `single_opcode_units.json` by lane 1
(`<runs>/L2/agent/logs/20260907T040418Z__L2_l1_survey.sh.log`, §[5/5]),
is 259 — 83 c, 82 cpp, 27 go, 48 rust, 19 swift, over 26 distinct mnemonics.
This is stated, not reconciled; nothing in this task's scope explains the
243 estimate's origin.

| outcome | count |
|---|---|
| `REFUSED` (no theorem stated) | 87 |
| `STATED`, closed by `rfl` | 39 |
| `STATED`, closed by `bv_decide` | 114 |
| `STATED`, `bv_decide` counterexample — **DISCREPANCY** | 19 |
| **total** | **259** |

REFUSED, by cause:

| cause | count | mnemonics |
|---|---|---|
| `FLOATING_POINT` | 44 | addsd(7) addss(7) divsd(5) divss(5) mulsd(5) mulss(5) subsd(5) subss(5) |
| `STATEFUL_PLACE_NOT_COMPOSED` | 21 | lea(16) movb(5) |
| `NO_PROVED_TERM` | 16 | call(16) |
| `WIDTH_UNRESOLVED` | 4 | xorps(4) |
| `RIP_CONSTANT_POSITIONAL` | 2 | pxor(2) |

`FLOATING_POINT` is exactly the brief's anticipated case: the model exists
(§3) but `bv_decide` has no floating-point theory, so the theorem is stated
as unavailable rather than closed. The other four causes are non-float
gaps this task's check surfaced: `lea`/`movb` write a place the check's own
term-composition does not yet model as composed; `call` units have no
proved term to check against at all; `xorps` hits an unresolved operand
width; `pxor`'s constant operand is RIP-relative and positional in a way
this check does not yet read.

Wall clock and peak RSS are per-theorem fields on every row
(`check_L2.json.rows[*].wall_seconds/.peak_kb`, from `os.wait4` on that
theorem's own `lake env lean` process — not a running maximum). Over the 153
proved theorems: `rfl` closes in 0.14-0.24s at 373-385 MB peak; `bv_decide`
closes in 0.21-0.75s at 456-499 MB peak, the wider bit-blasts (`sub`/`imul`
at 64 bits) at the top of that range. Full per-theorem numbers are in
`check_L2.json`, one row per theorem; they are not retyped here because
there are 259 of them and the json is the object.

---

## 5. Every DISCREPANCY, LITERAL

19 rows, three mnemonics, one shape each — `bv_decide` returned a concrete
counterexample for all 19 (host log
`<runs>/L2/agent/logs/20260907T135419Z__L2_l20_rerunnable_claims.sh.log`,
§[5/8]):

| theorem | mnem | unit | left (the unit's own proved term) | right (the model, composed) |
|---|---|---|---|---|
| ModelCheck_c_0 | add | c/op_113 | `(((0#32) ++ (v0.extractLsb 31 0)) + v1)` | `(model_add_52 (model_mov_15 v1) v0)` |
| ModelCheck_c_1 | add | c/op_133 | `(((0#32) ++ (v0.extractLsb 31 0)) + v1)` | `(model_add_52 (model_mov_15 v1) v0)` |
| ModelCheck_c_22 | imul | c/regen_8997 | `(((0#32) ++ (v0.extractLsb 31 0)) * v1)` | `(model_imul_52 (model_mov_15 v1) v0)` |
| ModelCheck_c_23 | imul | c/regen_9822 | `(((0#32) ++ (v0.extractLsb 31 0)) * v1)` | `(model_imul_52 (model_mov_15 v1) v0)` |
| ModelCheck_c_68 | sub | c/op_138 | `(((v0.extractLsb 31 0) * (4294967295#32)) + (v1.extractLsb 31 0))` | `((model_sub_39 (model_mov_15 v0) v1).extractLsb 31 0)` |
| ModelCheck_c_69 | sub | c/op_145 | `((v0 * (18446744073709551615#64)) + v1)` | `(model_sub_51 (model_mov_19 v0) v1)` |
| ModelCheck_c_70 | sub | c/op_149 | `((((0#32) ++ (v0.extractLsb 31 0)) * (18446744073709551615#64)) + v1)` | `(model_sub_51 (model_mov_19 v0) (model_mov_15 v1))` |
| ModelCheck_cpp_0 | add | cpp/op_113 | `(((0#32) ++ (v0.extractLsb 31 0)) + v1)` | `(model_add_52 (model_mov_15 v1) v0)` |
| ModelCheck_cpp_1 | add | cpp/op_133 | `(((0#32) ++ (v0.extractLsb 31 0)) + v1)` | `(model_add_52 (model_mov_15 v1) v0)` |
| ModelCheck_cpp_22 | imul | cpp/regen_8581 | `(((0#32) ++ (v0.extractLsb 31 0)) * v1)` | `(model_imul_52 (model_mov_15 v1) v0)` |
| ModelCheck_cpp_23 | imul | cpp/regen_8966 | `(((0#32) ++ (v0.extractLsb 31 0)) * v1)` | `(model_imul_52 (model_mov_15 v1) v0)` |
| ModelCheck_cpp_67 | sub | cpp/op_138 | `(((v0.extractLsb 31 0) * (4294967295#32)) + (v1.extractLsb 31 0))` | `((model_sub_39 (model_mov_15 v0) v1).extractLsb 31 0)` |
| ModelCheck_cpp_68 | sub | cpp/op_145 | `((v0 * (18446744073709551615#64)) + v1)` | `(model_sub_51 (model_mov_19 v0) v1)` |
| ModelCheck_cpp_69 | sub | cpp/op_149 | `((((0#32) ++ (v0.extractLsb 31 0)) * (18446744073709551615#64)) + v1)` | `(model_sub_51 (model_mov_19 v0) (model_mov_15 v1))` |
| ModelCheck_go_20 | sub | go/op_348 | `(((v0.extractLsb 31 0) * (4294967295#32)) + (v1.extractLsb 31 0))` | `((model_sub_39 v0 v1).extractLsb 31 0)` |
| ModelCheck_go_21 | sub | go/op_355 | `((v0 * (18446744073709551615#64)) + v1)` | `(model_sub_51 v0 v1)` |
| ModelCheck_rust_39 | sub | rust/op_570 | `(((v0.extractLsb 31 0) * (4294967295#32)) + (v1.extractLsb 31 0))` | `((model_sub_39 (model_mov_15 v0) v1).extractLsb 31 0)` |
| ModelCheck_rust_40 | sub | rust/op_577 | `((v0 * (18446744073709551615#64)) + v1)` | `(model_sub_51 (model_mov_19 v0) v1)` |
| ModelCheck_rust_41 | sub | rust/regen_1043 | `(((v0.extractLsb 7 0) * (255#8)) + (v1.extractLsb 7 0))` | `((model_sub_0 (model_mov_15 v0) v1).extractLsb 7 0)` |

The shape is the same across all 19: `4294967295#32` is `-1` at 32 bits and
`18446744073709551615#64` is `-1` at 64 bits, so every `left` reads as
`x - y` written as `x + (-y)` — a subtraction (or, for the `add`/`imul` rows,
a zero-extended-32-bit-write-then-op) the unit's own term states correctly.
Every `right` composes the SAME model definitions (`model_add_52`,
`model_imul_52`, `model_sub_39`, `model_sub_51`, `model_sub_0`, each an
existing, individually-checked definition in `Model.lean`) but in an order
or with an operand pairing that does not match how the unit's instruction
sequence actually threads its `mov` steps into the arithmetic — visible
directly in rows like ModelCheck_go_20/21 and ModelCheck_c_69, where the
`right` term is MISSING a `model_mov_*` wrapper the corresponding `c`/`cpp`
row (same mnemonic, e.g. ModelCheck_c_68/cpp_67) DOES carry, for what reads
as the same instruction shape. This is a discrepancy located between the
unit's own reading and the model's composed reading, per this node's
definition (§1) — not adjudicated in this task, which has no brief to change
either the term-walk route or the check's own step-composition order.

---

## 6. `lake build`, `#print axioms`, and the two parser bugs this session fixed

`lake build` of the whole project: **exit 0**, 318 jobs (host log
`<runs>/L2/agent/logs/20260907T135104Z__L2_l19_final_guard.sh.log`,
§[1/5]). `grep -rn '\bsorry\b'` over every `.lean` file in the project: no
match (same log, §[2/5]) — the only way `sorryAx` can appear in a
`#print axioms` trace is if a `sorry` term or tactic exists somewhere in the
proof or a dependency it imports, so a clean grep over the whole project is
what makes "no `sorryAx`" checkable without reading 153 traces by eye.

All 153 proved theorems carry a `#print axioms` line (host log
`<runs>/L2/agent/logs/20260907T134623Z__L2_l18_axioms_refresh.sh.log`);
**zero carry `sorryAx`**:

| axiom set | count | closed by |
|---|---|---|
| (none — zero-axiom proof) | 20 | `rfl` |
| `propext, Quot.sound` | 19 | `rfl` |
| `propext, Classical.choice, Quot.sound` | 53 | `bv_decide` |
| `propext, Classical.choice, Lean.ofReduceBool, Lean.trustCompiler, Quot.sound` | 61 | `bv_decide` |

`Lean.ofReduceBool` and `Lean.trustCompiler` are `bv_decide`'s own trust
axioms for the LRAT certificate path when it needs native evaluation rather
than pure kernel reduction — present on 61 of 114 `bv_decide`-closed
theorems, absent from the other 53. Named here because "zero `sorryAx`" and
"kernel-only, no bit-blasting trust assumption" are different claims, and
this task's own re-parse (below) is what surfaced the distinction rather
than leaving it inside a line nobody reads.

**Two bugs, both in `model_translate.py`'s `axiom_line` function (the
checker's OWN parser of `#print axioms`'s output), neither in a theorem:**

1. 20 proved rows (all `rfl`-closed) came back with `row["axioms"] == None`.
   Lane 15's probe (`<runs>/L2/agent/logs/20260907T134328Z__L2_l15_probe.sh.log`)
   ran `lake env lean` directly on `ModelCheck_c_21.lean` and found:
   ```
   'Archproof.ModelCheck_c_21' does not depend on any axioms
   ```
   — a DIFFERENT phrasing than `axiom_line`'s only pattern, `"depends on
   axioms"`. All 20 use no axiom at all (the strongest possible outcome).
   Fixed by matching both phrasings; lane 16
   (`<runs>/L2/agent/logs/20260907T134416Z__L2_l16_axioms_gap2.sh.log`)
   re-ran the 20 and filled them, 0 still missing.
2. 61 `bv_decide`-closed rows recorded a TRUNCATED axiom list, e.g.
   `"'Archproof.ModelCheck_c_9' depends on axioms: [propext,"` with no
   closing bracket. Lane 17's probe
   (`<runs>/L2/agent/logs/20260907T134514Z__L2_l17_probe2.sh.log`)
   found Lean wraps a long axiom list over several lines:
   ```
   'Archproof.ModelCheck_c_9' depends on axioms: [propext,
    Classical.choice,
    Lean.ofReduceBool,
    Lean.trustCompiler,
    Quot.sound]
   ```
   and `axiom_line` kept only the opening line — silently dropping
   `Lean.ofReduceBool` and `Lean.trustCompiler` from every one of those 61
   rows' recorded axioms, which is exactly the fact `#print axioms` exists
   to surface. Fixed by joining every wrapped line up to the one holding
   `]`; lane 18 refreshed all 153 proved rows with the corrected parser (0
   missing, 0 `sorryAx`, same log as above).

Neither fix touched a theorem file, a tactic, `Model.lean`, or `reference.py`
— both are read-only re-runs of `lake env lean` on files already on disk,
correcting only how their (already-correct) output was parsed into
`check_L2.json`.

---

## 7. The spelling-ban guard, pasted verbatim as required

> **THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
> second violation).** No operator token may appear in ANY key, grouping,
> pairing, row structure, candidate selection, or comparison scope, anywhere
> in this line — not in matching, not in "which pairs get compared", not in
> report rows, not in dropdowns. The candidate set for comparison comes from
> machine-form evidence (clusters, connections, type pairs) or from ratified
> intention — never from the token. The token appears exactly once per unit:
> as a display label on the member. HISTORY OF VIOLATIONS, so the pattern is
> visible: (1) the arch campaign's cross-language matrix (caught by the owner
> 2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25 — the
> fix brief itself reintroduced it as "same-operator pairs"). MECHANICAL
> GUARD REQUIRED: every pipeline stage that groups or pairs units must run
> the spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
> its own output on failure. A brief handed to any subagent for this line
> MUST paste this paragraph verbatim.

Run, unmodified, over both json files this task wrote (host log
`<runs>/L2/agent/logs/20260907T135104Z__L2_l19_final_guard.sh.log`,
§[3/5]):

```
FAIL model_L2.json -- 18112 spelling-keyed place(s)
     $.per_mnemonic.and       dict key is the operator token 'and'
     $.per_mnemonic.not       dict key is the operator token 'not'
     $.per_mnemonic.or        dict key is the operator token 'or'
     $.per_mnemonic.xor       dict key is the operator token 'xor'
     $.rows[320].flag_setter  operator token 'and' on a structure field --
                              this is a grouping/row key, not a per-unit label
     ... and 18092 more (all `flag_setter` values equal to `and`, `not`,
         `or` or `xor`)
PASS check_L2.json -- no operator token in any key, grouping, pairing or
     row structure
```

`grep -c exempt` over every file this task added (`model_translate.py`,
`model_L2.json`, `check_L2.json`, `Model.lean`, every `ModelCheck_*.lean`):
**0** (same log, §[4/5]).

`check_L2.json` passes outright. `model_L2.json` fails on two shapes, both
this task's OWN domain object rather than a cross-language matching
artifact: `per_mnemonic` is keyed by the reference's own opcode mnemonics
(required by the brief's own deliverable — "table: mnemonics modelled /
translated / refused by cause"), and `flag_setter` names which mnemonic's
flag-setting rule a given flags definition uses (a fact the Lean model needs
to render correctly, read straight off `reference.py`'s own `ops.state.flags
= (mnemonic, ...)` calls in §2). Four of the reference's 171 mnemonic
spellings (`and`, `not`, `or`, `xor`) happen to also be entries in the
guard's 91-token cross-language operator inventory. This task did not rename
those keys or restructure `model_L2.json` to route around the finding — the
guard is never modified and a blocker here is a flag, not a license to
redesign a json this task's own brief requires shaped this way — so it is
reported LITERAL, unresolved, in §9.

---

## 8. What was NOT done, by this task's own stop rules

- **`reference.py` was never edited** — every builder body in §2 is quoted,
  not modified.
- **`Model.lean` was never hand-edited** — every one of its 3,933
  definitions came from `model_translate.py model`; the two parser bugs in
  §6 were fixed in `model_translate.py`, which only changes how
  `check_L2.json`'s `axioms` field is populated, not any theorem.
- **No Mathlib, no network** — `L2.conf` runs `proxy = no`; `lake build`
  built 318 jobs with no route out.
- **The spelling guard was not modified**, and its `model_L2.json` failure
  was not worked around by renaming or restructuring — see §7/§9.
- **The 19 DISCREPANCY rows were not adjudicated** (deciding whether the
  fault is in the term-walk route's composition or the check's own
  step-ordering is out of this task's brief) and none of the failing
  theorem files' tactics or statements were altered to make them pass.
- **Nothing under `Research/op_pipeline/` outside `lean/` was changed.**

---

## 9. Two lists

**Decided, recorded for audit:**

- The population is 259 rows, not the brief's estimated 243 — taken as
  found off `single_opcode_units.json`, not adjusted to match the estimate.
- `axiom_line`'s two bugs (§6) are fixed in `model_translate.py` because they
  are bugs in THIS task's own checker, not in `reference.py`, `Model.lean`,
  or any theorem; both fixes are read-only re-runs, recorded as lanes 14-18.
- The 19 DISCREPANCY rows are reported as located findings (§5), per this
  node's own definition of what a discrepancy is, and left unadjudicated.
- `model_L2.json`'s guard failure (§7) is reported, not worked around: no
  key was renamed, no field restructured.

**Awaiting the owner:**

- Whether the spelling-ban guard's scope covers `model_L2.json`'s
  `per_mnemonic` keys and `flag_setter` values — this task's own domain
  object, naming the reference's own opcode mnemonics, coincidentally
  overlapping four of the guard's 91 cross-language operator tokens — or
  whether the guard (or this json's schema) needs a stated exemption for the
  model-translator line specifically.
- Whether the 19 DISCREPANCY rows' cause is the term-walk route's
  step-composition order or the check's own composition of `Model.lean`
  definitions along a unit's instruction sequence — located in §5, not
  adjudicated here.
- Whether the population mismatch (259 actual vs. 243 estimated) traces to
  a stale estimate in the brief or a change in `single_opcode_units.json`
  since the estimate was written.

---

## 10. The same facts as commands that re-run

Run in `L2_l20_rerunnable_claims.sh` (host log
`<runs>/L2/agent/logs/20260907T135419Z__L2_l20_rerunnable_claims.sh.log`);
working directory `PseudoCoupHQ/Research/op_pipeline/lean`.

**[1/8] The five opcodes, end to end** — quoted in full in §2 (attribution,
lane 20 §[1/8]; `model_translate.py five`'s definition-name COUNTER is local
to the invocation, so it is not pasted here a second time as a fresh MATCH
claim).

**[2/8] The translator's census over all 171 mnemonics** (lane 22, host log
`<runs>/L2/agent/logs/20260907T140035Z__L2_l22_rerunnable_claims2.sh.log`,
§[1/6] — absolute path, in place of lane 20's relative path which only
resolved from `lean/` and not from the checker's own working directory):

```
$ python3 -c '
import json
d = json.load(open("PseudoCoupHQ/Research/op_pipeline/lean/model_L2.json"))
pm = d["per_mnemonic"]
print("mnemonics_in_the_table", d["mnemonics_in_the_table"])
print("definitions", d["definitions"])
print("opaque_float_primitives", len(d["opaque_float_primitives"]))
no_builder = sorted(m for m, v in pm.items() if v["no_builder"])
nothing = sorted(m for m, v in pm.items() if not v["no_builder"] and not v["translated"])
translated = sorted(m for m, v in pm.items() if v["translated"])
print("no_builder", no_builder)
print("builder_but_nothing_translated", nothing)
print("translated_count", len(translated))
'
mnemonics_in_the_table 171
definitions 3933
opaque_float_primitives 27
no_builder ['call', 'jmp', 'pcmpeqb', 'pcmpeqd', 'pmovmskb', 'ud2']
builder_but_nothing_translated ['cs', 'endbr64', 'nop', 'nopl', 'ret']
translated_count 160
```

**[3/8] The check's outcome tally over the 259 rows** (lane 22, §[2/6]):

```
$ python3 -c '
import json, collections
d = json.load(open("PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json"))
rows = d["rows"]
print("total_rows", len(rows))
tally = collections.Counter()
for r in rows:
    key = r.get("closed_by") or r.get("outcome")
    tally[key] += 1
for k in sorted(tally, key=str):
    print(" ", k, tally[k])
'
total_rows 259
  DISCREPANCY 19
  REFUSED 87
  bv_decide 114
  rfl 39
```

**[4/8] REFUSED, by cause and mnemonic** (lane 22, §[3/6]):

```
$ python3 -c '
import json, collections
d = json.load(open("PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json"))
rows = [r for r in d["rows"] if r["outcome"] == "REFUSED"]
pm = collections.defaultdict(collections.Counter)
for r in rows:
    pm[r.get("cause")][r["mnem"]] += 1
for cause in sorted(pm):
    print(cause, dict(pm[cause]))
'
FLOATING_POINT {'addsd': 7, 'addss': 7, 'divsd': 5, 'divss': 5, 'mulsd': 5, 'mulss': 5, 'subsd': 5, 'subss': 5}
NO_PROVED_TERM {'call': 16}
RIP_CONSTANT_POSITIONAL {'pxor': 2}
STATEFUL_PLACE_NOT_COMPOSED {'lea': 16, 'movb': 5}
WIDTH_UNRESOLVED {'xorps': 4}
```

**[5/8] Every DISCREPANCY row** — quoted in full in §5 (attribution, lane 20
§[5/8]).

**[6/8] The axioms-line shape distribution over all 153 proved rows** (lane
22, §[4/6] — `chr(39)` in place of an escaped `'` inside the python source,
which the checker's own command-splitter could not find the closing quote
of):

```
$ python3 -c '
import json, re, collections
d = json.load(open("PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json"))
proved = [r for r in d["rows"] if r.get("closed_by")]
print("proved_total", len(proved))
print("missing_axioms", sum(1 for r in proved if not r.get("axioms")))
print("sorryAx_count", sum(1 for r in proved if "sorryAx" in (r.get("axioms") or "")))
pats = collections.Counter()
for r in proved:
    a2 = re.sub(chr(39) + "[^" + chr(39) + "]+" + chr(39), "THEOREM", r["axioms"])
    pats[(r["closed_by"], a2)] += 1
for k in sorted(pats, key=str):
    print(" ", pats[k], k)
'
proved_total 153
missing_axioms 0
sorryAx_count 0
  61 ('bv_decide', 'THEOREM depends on axioms: [propext, Classical.choice, Lean.ofReduceBool, Lean.trustCompiler, Quot.sound]')
  53 ('bv_decide', 'THEOREM depends on axioms: [propext, Classical.choice, Quot.sound]')
  19 ('rfl', 'THEOREM depends on axioms: [propext, Quot.sound]')
  20 ('rfl', 'THEOREM does not depend on any axioms')
```

**[7/8] `lake build` (whole project)** — attribution only: `lake` is not on
`check_conventions_log_claims.py`'s own `ALLOWED_HEADS`, so it can never be
a re-runnable claim through that checker. Exit 0, 318 jobs, quoted in §6,
host log
`<runs>/L2/agent/logs/20260907T135104Z__L2_l19_final_guard.sh.log`.
**The sorry keyword, whole project** (lane 22, §[5/6] — absolute paths, no
`cd`, which the checker calls `tool_absent` because it resolves through
`shutil.which` to nothing):

```
$ grep -rln "sorry" \
    PseudoCoupHQ/Research/op_pipeline/lean/archproof/Archproof/*.lean \
    PseudoCoupHQ/Research/op_pipeline/lean/archproof/Edges/*.lean \
    PseudoCoupHQ/Research/op_pipeline/lean/archproof/Main.lean \
    PseudoCoupHQ/Research/op_pipeline/lean/archproof/Archproof.lean
(no output, grep exit 1 -- no file matched, no sorry anywhere)
```

**[8/8] The spelling-ban guard over every json this task wrote** (lane 22,
§[6/6] — absolute paths on both arguments):

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    PseudoCoupHQ/Research/op_pipeline/lean/model_L2.json \
    PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json 2>&1 \
    | grep -E "^(FAIL|PASS)"
FAIL model_L2.json -- 18112 spelling-keyed place(s)
PASS check_L2.json -- no operator token in any key, grouping, pairing or row structure
```

---

## 11. Verifier tally

Three passes, `check_conventions_log_claims.py` unmodified, run FROM the L2
instance, each over section 10's commands (the only shell transcripts in
this log). Pass 1 (`L2_l21_verify.sh`, host log
`<runs>/L2/agent/logs/20260907T135759Z__L2_l21_verify.sh.log`)
found 3 DIFFERS, over an EARLIER draft: two commands used a path
(`'check_L2.json'`) that only resolves from `lean/`, not from the checker's
own fixed working directory (`PseudoCoupHQ`, stated in its own
banner); the third used a relative path in the guard invocation. Section 10
above is the FIXED version — absolute paths throughout, plus two unrelated
fixes the same pass surfaced (a bare `>` inside python source the checker's
naive splitter read as a shell redirect; a backslash-escaped `'` its
splitter could not find the close of). Pass 2
(`L2_l23_verify2.sh`, host log
`<runs>/L2/agent/logs/20260907T140212Z__L2_l23_verify2.sh.log`)
confirmed 0 DIFFERS over the fixed commands, with one NOT_RERUNNABLE — this
section's own self-referential verifier command, which at that point still
carried a live `$ ` line pointing at its own pasted output (a claim
comparing itself to itself). That line was removed (see the note that
replaced it, two paragraphs up) and pass 3, the final one, from
`L2_l24_verify3.sh` (host log
`<runs>/L2/agent/logs/20260907T140327Z__L2_l24_verify3.sh.log`,
command
`python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 PseudoCoupHQ/DevComms/log_232_task_L2_model_translator.md`
— not pasted as a live `$ ` transcript for the same self-reference reason):

```
population: 20 claims across 1 logs
  MATCHES          5
  DIFFERS          0
  UNVERIFIABLE     14
  REFUSED          1
  NOT_RERUNNABLE   0
ONE LINE: 5 of 20 claims reproduce; 14 (70%) carry nothing to re-run
causes, by name:
  prose_only                       9
  pasted_without_source            3
  attribution_only                 2
  log_unreachable                  1
check_conventions_log_claims.py exit 0
```

**TALLY LINE: claims 20 | MATCHES 5 | DIFFERS 0 | UNVERIFIABLE 14 | REFUSED 1
| NOT_RERUNNABLE 0. Zero DIFFERS.** The five MATCHES are section 10's
commands [2/8], [3/8], [4/8], [6/8] and [8/8] (the census, the outcome
tally, REFUSED-by-cause, the axioms distribution, and the guard). The one
REFUSED is [7/8]'s sorry-keyword `grep` — the checker's `log_unreachable`
rule checks each bare path token with `os.path.exists`, which a shell GLOB
(`archproof/Archproof/*.lean`) fails literally even though the shell that
actually ran it (lane 22) expanded it correctly and found no match; this is
the checker reading its own path-existence rule over a glob it does not
expand, not a disagreement about the underlying fact (no `sorry` anywhere,
independently confirmed by lane 19's whole-project `grep` in §6). The 14
UNVERIFIABLE are prose, two attributions, and three bare pastes, each
already carrying its host log path per the standing convention.

---

## 12. See also

- `PseudoCoupHQ/Research/op_pipeline/lean/MODEL_README.md` —
  what is in the artifact folder, restated as reference documentation.
- `PseudoCoupHQ/Research/op_pipeline/lean/model_translate.py`
  — the translator and the checker, six commands (`table`, `five`, `model`,
  `check`, `run`, `imports`, plus `axioms_gap`/`axioms_refresh` added this
  session).
- `PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json` —
  the 259-row population, every outcome, every `left`/`right` term pair,
  every proved theorem's axioms line.
- `PseudoCoupHQ/Research/op_pipeline/lean/model_L2.json` —
  the 171-mnemonic census, and the guard's failure (§7).
- `PseudoCoupHQ/Research/op_pipeline/lean/lanes_L2/` — all 20
  lane scripts, in submission order.
- `PseudoCoupHQ/DevComms/log_227_task_L1_lean_second_discharger.md`
  — the `archproof` project and its own proof, which this task's `lake
  build` (§6) extends without touching.
- `PseudoCoupHQ/DevComms/log_229_operator_mapping_proof_system_purpose.md`
  §4.1 — the framing this task implements: level 0 DERIVED from the
  reference, never written twice.
