# interp_php_handlers -- php handler slices (task 12, 2026-09-01)

Extends `interp_php.md`/`interp_php.json` (round 1, dispatch/tally
only, no arch-unit) toward what `interp_cpython.md` did for CPython.
**Result: a diagnosed dead end, not a completed pilot.** Real handler
code was disassembled, but no anchor/ship PAIR was produced -- both
slots hold the same coverage-instrumented build.  Recorded honestly
per the round-2 rule (a build that fails is recorded with its failure
text, not worked around silently).  Data: `interp_php_handlers.json`.

## the pin

- php `7.4.33` -- the same COMPROMISE pin as `interp_php.json` (8.3.0
  and 8.2.13 both fail this container's C11-atomics check; see that
  file's `pin_history` for the four build attempts of record).
- source tree reused: `/persist/php` (the round-1 coverage build).

## what was attempted

Same method as ruby: copy `/persist/php`, `make clean`, reconfigure
without `--coverage` (anchor: `CFLAGS="-O0 -g -fwrapv"`; ship: bare
`./configure`), rebuild, confirm zero `__gcov` symbols, slice handler
symbols with objdump.

## what actually happened -- THE DEFECT, pasted from the build log

Every reconfigure attempt (three separate tries, `interp_e2_handlers.sh`,
`interp_e3_php_fix.sh`, `interp_e4_php_libxml.sh`) failed the same way:

```
checking whether to build with LIBXML support... yes
checking for libxml-2.0 >= 2.7.6... no
configure: error: Package requirements (libxml-2.0 >= 2.7.6) were not met:

Package 'libxml-2.0' not found
```

Tried and failed to route around it:

- `--disable-libxml --disable-dom --disable-simplexml --disable-xml
  --disable-xmlreader --disable-xmlwriter --without-pear` -- same
  error (something else in the tree still probes for libxml-2.0
  before honoring the disable flags at PHP 7.4's configure-script
  generation).
- `apt-get update` inside the Airlock agent lane -- **exit=100**
  (network blocked for this apt mirror from inside the lane; the
  toolchain doc's "ubuntu/canonical... allowlisted" note does not
  cover whatever host this container's `/etc/apt/sources.list`
  actually points at). `apt-get install libxml2-dev` therefore never
  ran.

Because `./configure` exited nonzero, it never rewrote `config.status`
or the `Makefile` it had inherited from `/persist/php`'s ORIGINAL
`--coverage` build.  `make -j6` then exited 0 -- but it rebuilt the
SAME coverage-instrumented objects, just relinked with a new
timestamp.  Confirmed, not assumed:

```
$ nm /persist/php_anchor/sapi/cli/php | grep -c __gcov
13352
$ nm /persist/php_ship/sapi/cli/php | grep -c __gcov
13352
$ diff <(objdump -d --disassemble=add_function .../php_anchor/...) \
       <(objdump -d --disassemble=add_function .../php_ship/...)
(empty -- byte-identical)
$ md5sum .../php_anchor/sapi/cli/php .../php_ship/sapi/cli/php
0197476801cdf7349e2c7de737271579  php_anchor
30d63d71d824a956ea041d86cda36d33  php_ship
```

The md5sums differ ONLY because the embedded `--version` build
timestamp string differs (`built: Sep 1 2026 01:50:...` vs `01:51:...`);
the code bytes for every handler symbol checked are identical.  **No
optimizer-off vs optimized differentiation exists for php in this
session's artifacts.**

## the handler symbols found anyway (single build, not a pair)

`nm -C --defined-only` on the (single, coverage) binary located four
real handler symbols, none of them guessed:

- `add_function` (`Zend/zend_operators.c`) -- the generic dispatcher
  the round-1 tally's `Zend/zend_execute.c` delta pointed at.
- `ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER` -- the generated opcode
  handler for `ZEND_ADD` when both operands are temp/var/CV slots
  (the common case for `$a + $b` on two local variables), inside
  `Zend/zend_vm_execute.h` -- the file round-1's tally already named
  as carrying the largest delta.
- `ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER` /
  `ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER` --
  specialized int+int fast paths PHP's opcode generator emits
  alongside the generic handler (visible only by reading the
  generated `zend_vm_execute.h`, not from the round-1 tally).

`add_function`, first instructions, coverage build (gcov counter
increment visible -- this is the instrument, not clean code, pasted
because it is the only build that exists):

```
00000000007c4001 <add_function>:
  7c4001: endbr64
  7c4005: push   rbp
  7c4006: mov    rbp,rsp
  7c4009: sub    rsp,0x90
  7c4010: mov    QWORD PTR [rbp-0x78],rdi
  7c4014: mov    QWORD PTR [rbp-0x80],rsi
  7c4018: mov    QWORD PTR [rbp-0x88],rdx
  7c401f: mov    rax,QWORD PTR [rip+0x9af3da]        # 1173400 <__gcov0.add_function>
  7c4026: add    rax,0x1
  7c402a: mov    QWORD PTR [rip+0x9af3cf],rax        # 1173400 <__gcov0.add_function>
```

## instruction counts (single build only -- NOT anchor vs ship)

| symbol | instructions (one coverage-instrumented build) |
|---|---|
| `add_function` | 179 (includes gcov counter instructions -- not a clean count) |
| `ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER` | 195 |
| `ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER` | 74 |
| `ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER` | 49 |

These counts are real disassembly of real 7.4.33 code, but every one
of them is inflated by uncounted `__gcov0.*` counter-increment
instructions (the same defect `interp_cpython.md` names and repairs
via a clean uninstrumented build -- here it was NOT repaired). They
are not comparable to ruby's or CPython's anchor/ship counts.

## evidence classes

- the configure failure text, the `nm`/`diff`/`md5sum` proof that
  anchor and ship are the same build -- **artifact fact**.
- the four handler symbols and their addresses -- **artifact fact**
  (`nm` on the one build that exists).
- the instruction counts -- **artifact fact, but scoped**: real counts
  of a coverage-instrumented build, explicitly NOT an anchor/ship
  differential.

## what was NOT done

- **No valid anchor/ship pair** -- the core ask of this task, for php,
  is unmet. This is the headline finding, not a footnote.
- The libxml2-dev root cause was not fixed (no working apt mirror
  reachable from the agent lane, and no vendored `libxml-2.0.pc` was
  found on the filesystem to point `PKG_CONFIG_PATH` at). Whether
  that is fixable by widening `proxy/allowlist.txt` or by finding a
  `--without-libxml`-clean php 7.4 configure path is left open, not
  decided here.
- No clean (non-coverage) build exists for php in this session's
  artifacts at all -- not even a single one, since the only build
  reachable is the original coverage build with a fresh timestamp.
- No diary, no normalization, no matching, no bridge/dominance claim
  -- unreachable without a real handler slice pair.
- Scope: x86-64, one pin (php 7.4.33, itself a compromise), one build
  (coverage-instrumented), int operands, one operator (`+`).

## THE OPEN QUESTION -- moot for php until the build is fixed

`SUPPORT_scaling_design.md`'s prediction (an interpreted language's
`+` joins the operator table through bridges/dominance, not byte
identity) cannot even be TESTED for php yet: testing it needs a clean
ship-optimized slice to compare against the compiled-language
`dom_ops` cores, and none exists.  This is the honest state to hand
to the owner's ontology call, not a guess dressed as a finding.

## provenance

`provenance_is_weaker: true` on every row -- same convention as
java's and ruby's interpreter rows, doubly so here since even the
single-build counts carry gcov-instrumentation noise that was never
subtracted out.

## guard

```
$ python3 check_no_spelling_keys.py interp_php_handlers.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS interp_php_handlers.json -- no operator token in any key, grouping, pairing or row structure
```

## the lanes

| lane | wall time | did |
|---|---|---|
| `interp_e2_handlers.sh` | (shared with ruby, see `interp_ruby_handlers.md`) | first php anchor/ship attempt; found the libxml2 configure failure and the stale-Makefile symptom |
| `interp_e3_php_fix.sh` | 51.0s | retried with `--disable-libxml` and friends; same configure failure (a different code path in the same generated configure script still probes libxml-2.0) |
| `interp_e4_php_libxml.sh` | 54.7s | tried `apt-get install libxml2-dev`; `apt-get update` itself failed (exit 100, network blocked); confirmed via `diff`/`md5sum` that anchor and ship are byte-identical |
