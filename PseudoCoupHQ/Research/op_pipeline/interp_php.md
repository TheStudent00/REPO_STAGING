# interp_php -- the php pilot of the interpreter track

Folded 2026-08-31 by `fold_interp_php.py`, task 5(d), from the Airlock lane outputs under `~/Programming/Airlock/agent/out/interp_php_b/` (real gcov deltas, dated 2026-08-31: 344 lines with a positive delta across 9 files for the smallint probe -- the number log_082 named as measured-and-orphaned).  Data: `interp_php.json`.

## the pin -- a COMPROMISE, recorded in full

| tried | outcome | detail |
|---|---|---|
| PHP 8.3.0 | FAILED | `implicit declaration of function '__c11_atomic_exchange'`, stopped at `ext/date/php_date.lo` |
| PHP 8.2.13 | FAILED | `implicit declaration of function '__c11_atomic_exchange'`, stopped at `ext/date/php_date.lo` |
| PHP 8.2.13 | FAILED | `implicit declaration of function '__c11_atomic_init'`, stopped at `Zend/zend_execute_API.lo` |
| PHP 7.4.33 (first attempt) | FAILED | `make error (unrelated to atomics)`, stopped at `ext/standard/scanf.lo` |
| PHP 7.4.33 (second attempt) | SUCCEEDED | `PHP 7.4.33 (cli) (built: Aug 31 2026 05:25:57) ( NTS )`, 30.7s |

8.3.0 and 8.2.13 both fail the SAME way: `Zend/zend_atomic.h`'s C11 atomic intrinsics (`__c11_atomic_exchange`/`_load`/`_store`) are used without a declaration this container's compiler accepts.  7.4 predates that file's C11-atomics path, so it is unaffected -- not a coincidence, a version boundary.  7.4.33 is therefore a COMPROMISE pin: the first version that BUILT, not the first version tried. Any claim in this file is scoped to 7.4.33.

## the instrument, said plainly

Same as the ruby and cpython pilots: a **TALLY** (gcov line counters), not a diary.

## the method

Differential coverage, 100000 calls per probe. `p0_baseline` returns the first argument without adding.  `p1_smallint` adds two PHP ints (3, 4).  `p2_float` adds two floats (1.2345e+100, 6.7890e+100) -- PHP has no arbitrary-precision integer in core, so this pilot's 'big value' probe is a FLOAT probe, not a bignum probe, unlike cpython's and ruby's.

## the measured dispatch path (top lines, pasted from the delta)

### smallint (3 + 4)

| file | lines w/ delta | sum_delta |
|---|---|---|
| `Zend/zend_vm_execute.h` | 24 | 1300011 |
| `Zend/zend_execute.c` | 4 | 400000 |
| `Zend/zend_language_parser.c` | 57 | 211 |
| `Zend/zend_language_scanner.c` | 64 | 122 |
| `Zend/zend_compile.c` | 97 | 112 |
| `Zend/zend_ast.c` | 45 | 61 |
| `Zend/zend_opcode.c` | 36 | 37 |
| `Zend/zend_hash.c` | 14 | 14 |
| `Zend/zend_string.c` | 3 | 4 |

### float (1.2345e+100 + 6.7890e+100)

| file | lines w/ delta | sum_delta |
|---|---|---|
| `Zend/zend_vm_execute.h` | 58 | 3200057 |
| `Zend/zend_execute.c` | 4 | 400000 |
| `Zend/zend_strtod.c` | 332 | 1700 |
| `Zend/zend_language_parser.c` | 72 | 896 |
| `Zend/zend_language_scanner.c` | 123 | 727 |
| `Zend/zend_compile.c` | 154 | 471 |
| `Zend/zend_alloc.c` | 93 | 236 |
| `Zend/zend_hash.c` | 61 | 234 |
| `Zend/zend_ast.c` | 54 | 214 |
| `Zend/zend_string.c` | 41 | 151 |
| `Zend/zend_opcode.c` | 19 | 37 |
| `Zend/zend_execute_API.c` | 18 | 36 |

Reading (interpretation, not measured order): Zend/zend_vm_execute.h carries the largest delta (sum_delta=1,300,011 over 100000 calls) -- this is Zend's generated opcode handler table, the interpreted-VM analogue of cpython's generated_cases.c.h and ruby's vm.inc.  Zend/zend_execute.c follows (400,000) -- the ZEND_ADD opcode handler's call site.  Parser/scanner/compiler files carry much smaller deltas, read as one-time compile-time cost, not the addition itself.

## evidence classes on the claims

- pin history, build banner -- **artifact fact** (pasted straight from the build logs).
- the dispatch path -- **tally, per-run**: fact for these runs on this build, no order.
- the file-name reading above -- **interpretation**.

## what was NOT done

- NO arch-unit extracted -- no anchor/ship compiled pair, no objdump slice, no instruction bytes for the ZEND_ADD opcode handler (zend_vm_execute.h's generated ZEND_ADD_SPEC_* cases / zend_operators.c's add_function fast paths).  This pilot stops at the dispatch layer.
- no diary -- order is unmeasured.
- no normalization to canonical form, no matching against the compiled-language units, no bridge or dominance claim.
- no bignum probe -- PHP core has no arbitrary-precision integer type; the 'big value' probe uses floats instead (see method.probe_note).
- the 8.3.0 / 8.2.13 coverage-build failure was not chased to a fix (patching zend_atomic.h or the compiler's C11-atomics visibility) -- 7.4.33 was taken as the working pin instead.  Whether that failure is worth fixing so a newer PHP can be measured is left open, not decided here.
- scope: x86-64, one pin (php 7.4.33, a compromise), int and float operands only, one operator (+).

## why php does not enter a LANGS list

Same reason as ruby (see `interp_ruby.md`): no arch-unit was extracted, and `langs.py`'s `LANGS_INTERP` requires reaching that stage.

## guard

`check_no_spelling_keys.py interp_php.json` -> see the run recorded in log_087.

