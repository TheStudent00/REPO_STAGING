# interp_ruby -- the ruby pilot of the interpreter track

Folded 2026-08-31 by `fold_interp_ruby.py`, task 5(d), from the Airlock lane outputs under `Airlock/agent/out/interp_ruby_b/` (real gcov deltas, dated 2026-08-31: 1,050 lines with a positive delta across 27 files for the smallint probe -- the number log_082 named as measured-and-orphaned).  Data: `interp_ruby.json`.

## the pin

- ruby `3.3.0`
- the built interpreter says: `ruby 3.3.0 (2023-12-25 revision 5124f9ac75) [x86_64-linux]`
- evidence class: artifact fact (the binary's own `-v` banner)

## the instrument, said plainly

Same as `interp_cpython.md`: a **TALLY** (gcov line counters), not a diary. Order is not measured.

## the method

Differential coverage.  `p0_baseline` returns the first argument without adding; the delta between a probe run and the baseline run is what the addition reached.  Probes: `p0_baseline`, `p1_smallint` (3+4), `p2_bigint` ((1<<100)+12345 and (1<<100)+67890), `p3_disasm`.

## the bytecode (pasted, `dis`'s own testimony)

```
== disasm: #<ISeq:af@/persist/interp_ruby_b/probes/p3_disasm.rb:1 (1,0)-(3,3)>
local table (size: 2, argc: 2 [opts: 0, rest: -1, post: 0, block: -1, kw: -1@-1, kwrest: -1])
[ 2] a@0<Arg>   [ 1] b@1<Arg>
0000 getlocal_WC_0                          a@0                       (   2)[LiCa]
0002 getlocal_WC_0                          b@1
0004 opt_plus                               <calldata!mid:+, argc:1, ARGS_SIMPLE>[CcCr]
0006 leave                                                            (   3)[Re]
```

Unchanged after warm-up (pasted):

```
== disasm: #<ISeq:af@/persist/interp_ruby_b/probes/p3_disasm.rb:1 (1,0)-(3,3)>
local table (size: 2, argc: 2 [opts: 0, rest: -1, post: 0, block: -1, kw: -1@-1, kwrest: -1])
[ 2] a@0<Arg>   [ 1] b@1<Arg>
0000 getlocal_WC_0                          a@0                       (   2)[LiCa]
0002 getlocal_WC_0                          b@1
0004 opt_plus                               <calldata!mid:+, argc:1, ARGS_SIMPLE>[CcCr]
0006 leave                                                            (   3)[Re]
```

`opt_plus` is ruby's INLINE-CACHED call site for `+` -- comparable in role to cpython's `BINARY_OP_ADD_INT`, but emitted at compile time rather than installed after a warm-up trip (disasm is identical before/after here, unlike cpython's).

## the measured dispatch path (top lines, pasted from the delta)

### smallint (3 + 4)

| file | lines w/ delta | sum_delta |
|---|---|---|
| `vm.inc` | 22 | 2200000 |
| `vm_insnhelper.c` | 13 | 1300000 |
| `defs/opt_operand.def` | 1 | 100000 |
| `st.c` | 53 | 4008 |
| `compile.c` | 357 | 607 |
| `parse.y` | 224 | 451 |
| `parse.c` | 64 | 271 |
| `node.c` | 32 | 96 |
| `string.c` | 57 | 67 |
| `gc.c` | 47 | 53 |
| `hash.c` | 1 | 41 |
| `shape.c` | 24 | 38 |

### bignum ((1<<100)+12345 + (1<<100)+67890)

| file | lines w/ delta | sum_delta |
|---|---|---|
| `gc.c` | 1503 | 18575292 |
| `vm_insnhelper.c` | 204 | 10000946 |
| `bignum.c` | 230 | 7900687 |
| `vm.inc` | 60 | 4600116 |
| `shape.c` | 24 | 3829436 |
| `variable.c` | 58 | 1310802 |
| `class.c` | 6 | 600096 |
| `numeric.c` | 30 | 400161 |
| `include/ruby/internal/intern/error.h` | 3 | 300015 |
| `defs/opt_operand.def` | 3 | 300004 |
| `id_table.c` | 102 | 148102 |
| `st.c` | 189 | 101931 |

Reading (interpretation, not measured order): vm.inc and vm_insnhelper.c carry the largest deltas (2,200,000 and 1,300,000 sum_delta over 100000 calls) -- the opt_plus handler and its inline-cache-check machinery live there.  st.c and compile.c carry much smaller deltas and are read as parse/compile-time noise from the harness itself, not the addition.

for the (1<<100)+k pair, bignum.c enters with a large delta (7,900,687) alongside gc.c (18,575,292) and shape.c (3,829,436) -- read as Bignum allocation and object-shape transitions the Fixnum path never takes.  This is INTERPRETATION of the tally, not measured order (no diary).

## evidence classes on the claims

- pin, build banner -- **artifact fact**.
- the bytecode listing -- **the tool's own testimony** (`RubyVM::InstructionSequence#disasm`).
- the dispatch path -- **tally, per-run**: fact for these runs on this build, no order.
- the smallint/bignum readings above -- **interpretation**, read off file names, not measured order.

## what was NOT done

- NO arch-unit extracted -- no anchor/ship compiled pair, no objdump slice, no instruction bytes for opt_plus's C implementation (vm_insnhelper.c's vm_opt_plus / rb_int_plus).  This pilot stops at the bytecode/dispatch layer.
- no diary -- order is unmeasured, same caveat as interp_cpython.md.
- no normalization to canonical form, no matching against the compiled-language units, no bridge or dominance claim -- there is no arch-unit to normalize.
- the fiddle and psych extensions did not build (missing libffi); unrelated to Integer#+, unused by these probes.
- scope: x86-64, one pin (ruby 3.3.0), Fixnum and Bignum operands only, one operator (+).

## why ruby does not enter a LANGS list

`langs.py`'s `LANGS_INTERP` is defined as "reached the arch-unit stage".  ruby has NO arch-unit (see above), so it stays out of every tree_match / dom_ops LANGS list.  This is not an oversight -- entering those lists with no arch-unit would mean matching on nothing, which is worse than being honestly absent.

## guard

`check_no_spelling_keys.py interp_ruby.json` -> see the run recorded in log_087.  (Formality for a single-language pilot record: no grouping or pairing occurs in this file.)

