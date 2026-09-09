# log 113 — task 27: ruby and php slices, carved and proved

Date: 2026-09-01. Round 5, task 27. Protocol v2 (walkthrough, then
instances, then numbers, then the file inventory).

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line — not in matching, not in \"which pairs get
compared\", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention — never from the token. The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 — the fix brief
itself reintroduced it as \"same-operator pairs\"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this line
MUST paste this paragraph verbatim."

No sub-agent was used. Every artifact below was written and run in this
session.

---

## Walkthrough — plain words, before any table

Task 21 (log_107) refused all eight ruby and php handlers for one
reason: there was nothing on disk to carve. The only ruby and php
evidence was a few hand-copied lines of disassembly inside
`interp_relations.json`. The fixed block cutter needs a full
instruction stream with addresses; an excerpt is not one.

This task made the missing material. Three things happened.

- **The slices exist now.** Every handler was disassembled out of its
  pinned build with `objdump`, parsed by task 20's FIXED extractor
  (`slice_extractor_fix.parse_objdump_text`, so the split-instruction
  defect cannot recur), and written in the same record shape
  `op_units_cpython.json` carries: `probes{n:{meta, anchor, ship}}`,
  byte and mnemonic columns per side. Two new files:
  `op_units_ruby.json`, `op_units_php.json`. Both carry
  `provenance_is_weaker: true` on the artifact and on every record.

- **php got a real, uninstrumented pair for the first time.** log_095
  recorded php as a dead end: configure insisted on `libxml-2.0`,
  the package is absent from the container, `apt-get` cannot reach a
  mirror, so `make` relinked the same coverage-instrumented objects
  into both the "anchor" and "ship" paths — 13,359 `gcov` symbols in
  each. Two flags got past that wall this session: `--disable-all`, so
  configure never reaches the libxml probe at all, and `-std=gnu17`,
  so this container's gcc stops rejecting php 7.4 era empty parameter
  lists. Both builds finished with `gcov` symbol count **0**. The
  contaminated pair is still on disk and is named in the new artifact
  as the superseded record; not one slice comes from it.

- **The carve and the proofs ran for real, and refused where they
  should.** `lineage_carve.py` implements the owner's 2026-08-31 rule — the
  boundary is the first instruction whose super-chain includes BOTH
  lineages, arrival is the maximal prefix touching one lineage only.
  Eleven of twenty handler-and-build records carved. Three of them
  have a computation part that is z3-proved equal to compiled units;
  the other eight are recorded TYPE_INCOMPARABLE with the measured
  reason, never forced.

Two things in that account are worth naming as findings rather than
steps.

- **Ruby's optimised handler puts its slow path at LOWER addresses
  than its fast path.** The first version of the carve propagated
  lineages in address order and reported "the lineages never meet" for
  `rb_fix_plus` — because a `call do_coerce` on the coercion path,
  which sits earlier in memory, clobbered the lineage before the walk
  ever reached the fast path's own `add`. The fix is the mechanism,
  not the case: propagation now runs along CONTROL FLOW to a fixpoint,
  joining by union over reachable super-nodes, using block_cutter's
  own classifier and its checked jump-target resolver.

- **php's specialized handlers refuse a typed key at the CLEAN build
  too.** Task 24 read zero formal parameters for all three ZEND_ADD
  handlers out of the contaminated binary. That could have been an
  artifact of that build. It is not: the same read over the clean
  anchor AND the clean ship binary returns zero formal parameters
  again. The absence is the measured fact about php, not about the
  build.

---

## Instance 1 — ruby's optimised fast path, carved

The slice, verbatim from the ship build's own disassembly
(`/persist/ruby_ship/ruby`, symbol `rb_fix_plus` at `0x104750`):

```
  104766:	48 89 f0             	mov    %rsi,%rax
  104769:	83 e6 01             	and    $0x1,%esi
  10476c:	0f 85 be 00 00 00    	jne    104830 <rb_fix_plus+0xe0>
  ...
  104830:	48 83 e8 01          	sub    $0x1,%rax
  104834:	48 01 f8             	add    %rdi,%rax
  104837:	71 8e                	jno    1047c7 <rb_fix_plus+0x77>
```

The carve's own record for that unit:

```
ship     rb_fix_plus       CARVED   boundary=0x104834 add %rdi,%rax
```

- ARRIVAL is 49 instructions, ending at `0x104830 sub $0x1,%rax` —
  ruby's Fixnum tag strip, which touches the second lineage only.
- The BOUNDARY is `add %rdi,%rax` at `0x104834`, and the record names
  which place carries which lineage:

```
{"rax": ["argument_lineage_2"], "rdi": ["argument_lineage_1"]}
```

- The COMPUTATION CORE is that one instruction. Everything after it —
  `jno`, the stack-guard check, the tail jump to `rb_int2big` — is
  recorded under `after_the_answer`, the same separation
  `interp_fastpath.json` made when it kept cpython's boxing out of the
  computation.

This is exactly the case the owner's correction was about: the ORIGINALS
never meet. `a` meets `b − 1`, not `b`.

## Instance 2 — the computation part, proved against compiled units

`prove_interp_computation.py` renders the core in the canonical
runnable form (traced values in their designated registers, the
adapter move on its own line) and hands it to
`cross_unit_prover.prove_pair`, imported unmodified.

```
core             : add %rdi,%rax
canonical text   : mov %rsi,%rax; add %rdi,%rax; ret
candidates       : 88 compiled 0-branch units whose class key is a
                   64-bit integer pair with a 64-bit integer result
counts           : {'proved': 8, 'disproved': 70, 'undecided': 10, 'refused': 0}
```

The eight it proved equal to, with their own canonical texts:

```
c/op_109     mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret
c/op_116     mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret
cpp/op_109   mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret
cpp/op_116   mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret
go/op_319    mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret
go/op_326    mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret
rust/op_541  mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret
rust/op_548  mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret
```

The prover's own words on each edge:

```
z3 proved bit-level equality for every value of every register either
text reads before writing (fpToIEEEBV/BitVec comparison, 12000ms
timeout)
```

How the 88 candidates were chosen, since this is where a spelling key
would sneak in: the interpreter side qualifies from its own DWARF
typed key — `VALUE,VALUE` — and `VALUE` was resolved through DWARF to
`long unsigned int`, `DW_ATE_unsigned` (encoding 7), 8 bytes, measured
in both ruby binaries:

```
$ podman exec sandbox-runner bash -lc 'python3 /persist/resolve_value.py /persist/ruby_anchor/ruby VALUE; python3 /persist/resolve_value.py /persist/ruby_ship/ruby VALUE'
VALUE -> DW_TAG_base_type(long unsigned int) -> encoding=7 size=8
VALUE -> DW_TAG_base_type(long unsigned int) -> encoding=7 size=8
```

The candidate set is then every compiled unit whose class key is
`('u64,u64','u64')` or `('i64,i64','i64')`. No token participates, and
the artifact carries no display label on any proof row — see the guard
section below, where it caught exactly that.

## Instance 3 — php's clean pair, and its ten-instruction handler

The build, from the lane's own log
(`Airlock/agent/logs/20260901T154246Z__t27_php_clean_build2.sh.log`):

```
php clean anchor configure exit=0
php clean anchor make exit=0
-rwxr-xr-x 1 root root 20805096 Sep  1 15:43 /persist/php_c_anchor/sapi/cli/php
php clean ship configure exit=0
php clean ship make exit=0
-rwxr-xr-x 1 root root 26418688 Sep  1 15:43 /persist/php_c_ship/sapi/cli/php
=== /persist/php_c_anchor/sapi/cli/php
2287ee0fa7e43f0d589ef7750d01fa9f  /persist/php_c_anchor/sapi/cli/php
gcov symbols: 0
PHP 7.4.33 (cli) (built: Sep  1 2026 15:43:04) ( NTS )
=== /persist/php_c_ship/sapi/cli/php
gcov symbols: 0
PHP 7.4.33 (cli) (built: Sep  1 2026 15:43:35) ( NTS )
```

The pin is `7.4.33`, quoted from `interp_php.json`'s own
`meta.pin.tag`, and its COMPROMISE history is carried into the new
artifact verbatim from that file: 8.3.0 and 8.2.13 both failed the
build in this container because `Zend/zend_atomic.h`'s C11 atomic
intrinsics are used without the matching declaration under this
compiler; 7.4 predates that file.

The whole ship handler, ten instructions:

```
00000000002257b6 <ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER>:
  2257b6:	f3 0f 1e fa          	endbr64
  2257ba:	49 63 4f 08          	movslq 0x8(%r15),%rcx
  2257be:	49 63 47 0c          	movslq 0xc(%r15),%rax
  2257c2:	49 83 c7 20          	add    $0x20,%r15
  2257c6:	49 63 57 f0          	movslq -0x10(%r15),%rdx
  2257ca:	49 8b 04 06          	mov    (%r14,%rax,1),%rax
  2257ce:	49 03 04 0e          	add    (%r14,%rcx,1),%rax
  2257d2:	49 89 04 16          	mov    %rax,(%r14,%rdx,1)
  2257d6:	41 c7 44 16 08 04 00 	movl   $0x4,0x8(%r14,%rdx,1)
  2257df:	c3                   	ret
```

The carve on it:

- arrival: `endbr64`, the three slot reads, the frame advance, and the
  first value load `mov (%r14,%rax,1),%rax`;
- boundary: `add (%r14,%rcx,1),%rax`, reading `slot_lineage_1` through
  `%rcx` and `slot_lineage_2` in `%rax`;
- after the answer: `mov %rax,(%r14,%rdx,1)`, `movl $0x4,...` (writing
  the result's type tag) and `ret`.

The seed rule here is not the SysV one, and it is not a guess: php's
specialized handlers take no formal parameters, so a lineage is seeded
at each distinct operand-slot displacement read out of the instruction
word, found by first tracing which places hold that word. One
mechanism covers both builds — at `-O0` the same handler reads
`mov %r15,%rax; mov 0x8(%rax),%eax` instead of `0x8(%r15)` directly,
and the trace follows the copy.

## Instance 4 — the refusals, each with its measured reason

The php proof records, verbatim:

```
php/add_function
  the declared operand type is a POINTER pair (zval*,zval*).  The
  compiled classes in the comparable set carry integer operands;
  matching a pointer pair to them would be inventing a type, so no
  proof is attempted.

php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER
  no typed key could be read for this unit at this build, so there is
  no measured operand type to match against a compiled class key.  The
  DWARF refusal, verbatim: the DIE was found and carries 0 formal
  parameter(s); a two-operand typed key is not expressible from
  parameter types for this handler -- the operands reach it another
  way (php's specialized executor handlers read them through the
  execute_data frame)
```

The two ruby handlers that did not carve, verbatim:

```
anchor vm_opt_plus
  no instruction in this unit reads both lineages: the lineages leave
  this unit through a call, so the confluence is inside a callee, not
  here.  Call instructions reached: call 24c993 <FIXNUM_2_P>; call
  2437a5 <rb_fix_plus_fix>; call 24c9c7 <FLONUM_2_P>; ...

ship vm_opt_plus
  no slice exists for this symbol at this build: the symbol's label
  line is absent from the dump -- the build has no body for this symbol

anchor rb_big_plus
  no instruction in this unit reads both lineages: the lineages leave
  this unit through a call ... call 3cf3da <bigsub_int>; call 3cf69f
  <bigadd_int ...
```

`rb_big_plus` is the unbounded-width route, and its refusal reads
exactly as `SUPPORT_scaling_design.md` predicted it would: the work is
in a digit-loop callee, not in the handler's own bytes.

Following those `call` operands is also how two extra symbols entered
this task — `fix_plus` and `rb_fix_plus_fix`. Machine-form evidence,
one edge at a time, never a token. `rb_fix_plus_fix` is where the
anchor build's bounded-width computation actually lives, and it carved
and proved like the ship units. It is kept OUT of the nine, in its own
section of the new proposal, so the set the owner ratifies does not change
shape under him.

## The guard caught this session's own work, and the fix was the source

The first output of `prove_interp_computation.py` FAILED:

```
FAIL prove_interp_computation.json -- 24 spelling-keyed place(s)
     $.records[0].proved_equal_to[0].display_label_on_the_compiled_member
         operator token '+' on a structure field -- this is a grouping/row key, not a per-unit label
```

It was right. A token sitting on a proof ROW is a row structure, not a
per-unit label. The field was removed from the artifact — not the
finding suppressed, not the guard adjusted. The compiled unit's id
names the member; its label lives on the record that owns it.

The guard is now wired INTO the programs, per the mechanical-guard
requirement: each of `build_op_units_ruby.py`, `build_op_units_php.py`,
`lineage_carve.py`, `prove_interp_computation.py` and
`build_proposal_representation_dimension3.py` runs
`check_no_spelling_keys.py` over its own output and exits nonzero on
failure.

---

## Commands and their output

Verified: no coverage instrumentation in the ruby binaries, and the
count for the contaminated php pair, read live.

```
$ podman exec sandbox-runner bash -lc '
for b in /persist/ruby_anchor/ruby /persist/ruby_ship/ruby /persist/php_anchor/sapi/cli/php /persist/php_ship/sapi/cli/php; do
  echo "== $b"; md5sum $b; nm $b 2>/dev/null | grep -c gcov;
done'
== /persist/ruby_anchor/ruby
ba7392ece825301dad32b2f729c742fa  /persist/ruby_anchor/ruby
0
== /persist/ruby_ship/ruby
4c25be5cef6e84b307e8e7d15d8ed8a7  /persist/ruby_ship/ruby
0
== /persist/php_anchor/sapi/cli/php
0197476801cdf7349e2c7de737271579  /persist/php_anchor/sapi/cli/php
13359
== /persist/php_ship/sapi/cli/php
30d63d71d824a956ea041d86cda36d33  /persist/php_ship/sapi/cli/php
13359
```

Verified: the ruby slices were built.

```
$ /tmp/reconnect_venv/bin/python3 build_op_units_ruby.py
wrote PseudoCoupHQ/Research/op_pipeline/op_units_ruby.json
vm_opt_plus      anchor=165  ship=0
rb_fix_plus      anchor=13   ship=126
rb_int_plus      anchor=37   ship=190
fix_plus         anchor=68   ship=0
rb_fix_plus_fix  anchor=33   ship=0
rb_big_plus      anchor=85   ship=132
gcov: anchor=0 ship=0
ABSENT ship/vm_opt_plus -- the symbol's label line is absent from the dump -- the build has no body for this symbol
ABSENT ship/fix_plus -- the symbol's label line is absent from the dump -- the build has no body for this symbol
ABSENT ship/rb_fix_plus_fix -- the symbol's label line is absent from the dump -- the build has no body for this symbol
PASS op_units_ruby.json -- no operator token in any key, grouping, pairing or row structure
```

The four anchor counts (165 / 13 / 37 / 85) are the same numbers
log_095 measured for the same four symbols in round 2 — an independent
agreement, not a copy: this session re-disassembled the binaries and
re-parsed them with a different extractor.

Verified: the php slices were built, from the clean pair.

```
$ /tmp/reconnect_venv/bin/python3 build_op_units_php.py
wrote PseudoCoupHQ/Research/op_pipeline/op_units_php.json
add_function                                             anchor=146  ship=55
ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER                  anchor=157  ship=48
ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER             anchor=61   ship=20
ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER anchor=42   ship=10
gcov: clean anchor=0 clean ship=0 ; contaminated pair=13359 each
PASS op_units_php.json -- no operator token in any key, grouping, pairing or row structure
```

Verified: the typed keys were re-read from the binaries these carves
actually use (the clean php pair, and ruby's ship build, neither of
which task 24 read).

```
$ podman exec -e DWARF_T27_OUT=/persist/dwarf_typed_key_t27.json sandbox-runner \
    bash -lc 'cd PseudoCoupHQ/Research/op_pipeline && timeout 900 python3 dwarf_typed_key_t27.py'
wrote /persist/dwarf_typed_key_t27.json
php    add_function                                             READ     zval*,zval*
php    ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER                  REFUSED  None
php    ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER             REFUSED  None
php    ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER REFUSED  None
php    add_function                                             READ     zval*,zval*
php    ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER                  REFUSED  None
php    ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER             REFUSED  None
php    ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER REFUSED  None
ruby   vm_opt_plus                                              READ     VALUE,VALUE
ruby   rb_fix_plus                                              READ     VALUE,VALUE
ruby   rb_int_plus                                              READ     VALUE,VALUE
ruby   rb_big_plus                                              READ     VALUE,VALUE
ruby   fix_plus                                                 READ     VALUE,VALUE
ruby   rb_fix_plus_fix                                          READ     VALUE,VALUE
ruby   vm_opt_plus                                              READ     VALUE,VALUE
ruby   rb_fix_plus                                              READ     VALUE,VALUE
ruby   rb_int_plus                                              READ     VALUE,VALUE
ruby   rb_big_plus                                              READ     VALUE,VALUE
ruby   fix_plus                                                 READ     VALUE,VALUE
ruby   rb_fix_plus_fix                                          READ     VALUE,VALUE
summary: {'symbols_considered': 20, 'keys_read': 14, 'refused': 6}
```

(The first four lines are the clean ANCHOR build, the next four the
clean SHIP build; the php refusal reproduces at both, which is the
point of reading both.)

Verified: the carve.

```
$ /tmp/reconnect_venv/bin/python3 lineage_carve.py
wrote PseudoCoupHQ/Research/op_pipeline/lineage_carve.json
anchor   vm_opt_plus                                              REFUSED  ...
ship     vm_opt_plus                                              REFUSED  ...
anchor   rb_fix_plus                                              REFUSED  ...
ship     rb_fix_plus                                              CARVED   boundary=0x104834 add %rdi,%rax
anchor   rb_int_plus                                              REFUSED  ...
ship     rb_int_plus                                              CARVED   boundary=0xfac1f add %rbx,%rax
anchor   fix_plus                                                 REFUSED  ...
ship     fix_plus                                                 REFUSED  ...
anchor   rb_fix_plus_fix                                          CARVED   boundary=0x30 add %rdx,%rax
ship     rb_fix_plus_fix                                          REFUSED  ...
anchor   rb_big_plus                                              REFUSED  ...
ship     rb_big_plus                                              REFUSED  ...
anchor   add_function                                             CARVED   boundary=0x5e3e01 or %edx,%eax
ship     add_function                                             CARVED   boundary=0x40c05b or 0x8(%rdx),%al
anchor   ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER                  CARVED   boundary=0x6db4b2 add (%rsi),%rax
ship     ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER                  CARVED   boundary=0x228ca1 add (%rsi),%rax
anchor   ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER             CARVED   boundary=0x6dcb82 add (%rsi),%rax
ship     ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER             CARVED   boundary=0x2257fc add (%rcx),%rax
anchor   ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER CARVED   boundary=0x6dcae9 add %rax,%rdx
ship     ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER CARVED   boundary=0x2257ce add (%r14,%rcx,1),%rax
summary: {'records': 20, 'carved': 11, 'refused': 9}
PASS lineage_carve.json -- no operator token in any key, grouping, pairing or row structure
```

One reading worth stating rather than leaving in the table: php's
GENERIC routine `add_function` has its first confluence at
`or %edx,%eax` — the two operands' TYPE TAGS joined for the dispatch,
not their values. Under the owner's rule that is genuinely the boundary
(it is the first node whose super-chain holds both lineages), and it
says something real about php: the generic routine's first joint act
is a type decision, not an arithmetic one.

Verified: the proofs.

```
$ /tmp/reconnect_venv/bin/python3 prove_interp_computation.py
wrote PseudoCoupHQ/Research/op_pipeline/prove_interp_computation.json
ship   rb_fix_plus                                              PROVED   proved against 8 of 88 candidates
ship   rb_int_plus                                              PROVED   proved against 8 of 88 candidates
anchor rb_fix_plus_fix                                          PROVED   proved against 8 of 88 candidates
anchor add_function                                             TYPE_INCOMPARABLE
ship   add_function                                             TYPE_INCOMPARABLE
anchor ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER                  TYPE_INCOMPARABLE
ship   ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER                  TYPE_INCOMPARABLE
anchor ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER             TYPE_INCOMPARABLE
ship   ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER             TYPE_INCOMPARABLE
anchor ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER TYPE_INCOMPARABLE
ship   ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER TYPE_INCOMPARABLE
summary: {'carved_units_considered': 11, 'proved': 3, 'type_incomparable': 8, 'not_renderable': 0, 'undecided': 0, 'no_match': 0}
PASS prove_interp_computation.json -- no operator token in any key, grouping, pairing or row structure
```

Verified: the extended proposal was written and passes the guard.

```
$ /tmp/reconnect_venv/bin/python3 build_proposal_representation_dimension3.py
wrote PseudoCoupHQ/Research/op_pipeline/proposal_representation_dimension3.json
summary: {
 "handlers_considered": 9,
 "handlers_with_a_real_carve_at_some_build": 6,
 "handlers_with_a_proved_computation_part": 3,
 "handlers_type_incomparable": 4,
 "additional_route_symbols": 2
}
PASS proposal_representation_dimension3.json -- no operator token in any key, grouping, pairing or row structure
```

Verified: zero regressions. No prior artifact was modified, and no
unit file was opened by this task at all. Two counts are shown, so
neither is mistaken for the other: the canon29 baseline this task's
prover population sits behind reads 1,561 converged, unchanged; task
26's newer canon31 files, written in parallel with this task, read
1,635 recorded (1,622 honest after its own withdrawals) and were not
touched here.

```
$ cd PseudoCoupHQ && git status --porcelain Research/op_pipeline/
?? Research/op_pipeline/build_proposal_representation_dimension3.py
?? Research/op_pipeline/proposal_representation_dimension3.json

$ md5sum Research/op_pipeline/proposal_representation_dimension.json Research/op_pipeline/proposal_representation_dimension2.json Research/op_pipeline/dwarf_typed_key.json
1c222af06f3eb5b8fb32b75c6396901e  Research/op_pipeline/proposal_representation_dimension.json
3757fd146cca0b59d5f8b8ef5abc0939  Research/op_pipeline/proposal_representation_dimension2.json
b78c39651ca28ee36dcb45bde5de5537  Research/op_pipeline/dwarf_typed_key.json
$ git show HEAD:Research/op_pipeline/proposal_representation_dimension.json | md5sum
1c222af06f3eb5b8fb32b75c6396901e  -
$ git show HEAD:Research/op_pipeline/proposal_representation_dimension2.json | md5sum
3757fd146cca0b59d5f8b8ef5abc0939  -
$ git show HEAD:Research/op_pipeline/dwarf_typed_key.json | md5sum
b78c39651ca28ee36dcb45bde5de5537  -

$ /tmp/reconnect_venv/bin/python3 -c "
import json
langs=['c','cpp','go','rust','swift']
total=0
for lang in langs:
    d=json.load(open('canon29_units_%s.json'%lang))
    for n,u in d['units'].items():
        if u.get('status')=='converged':
            total+=1
print('converged total:', total)
"
converged total: 1561

$ /tmp/reconnect_venv/bin/python3 -c "
import json,glob
tot=0
for f in sorted(glob.glob('Research/op_pipeline/canon31_units_*.json')):
    d=json.load(open(f))
    tot+=sum(1 for n,u in d['units'].items() if u.get('status')=='converged')
print('canon31 converged total:',tot)
"
canon31 converged total: 1635

$ git diff --stat -- Research/op_pipeline/canon2.py Research/op_pipeline/block_cutter.py Research/op_pipeline/slice_extractor_fix.py Research/op_pipeline/cross_unit_prover.py Research/op_pipeline/check_no_spelling_keys.py Research/op_pipeline/dwarf_typed_key.py Research/op_pipeline/interp_ruby.json Research/op_pipeline/interp_php.json Research/op_pipeline/dominant_table24.json Research/op_pipeline/dom_ops22.json
(no output -- untouched)
```

The two files shown as untracked are this task's own new files at the
moment the check ran; the daemon commits them. Everything else this
task wrote had already been auto-committed by the daemon by then,
which is why it does not appear — banking is the posterity message,
not a commit.

---

## Numbers, each with its breakdown

**Slices, by symbol and build.** 17 slices exist out of 20
symbol-and-build combinations: ruby anchor 6 (vm_opt_plus 165,
rb_fix_plus 13, rb_int_plus 37, fix_plus 68, rb_fix_plus_fix 33,
rb_big_plus 85), ruby ship 3 (rb_fix_plus 126, rb_int_plus 190,
rb_big_plus 132), php 8 (anchor 146/157/61/42, ship 55/48/20/10).
6 + 3 + 8 = 17 slices; the 3 missing are ruby's ship build, where
`vm_opt_plus`, `fix_plus` and `rb_fix_plus_fix` have no body at all —
the optimiser absorbed them, and each absence is recorded as an
absence with its reason.

**Carve outcomes, 20 records.** 11 CARVED = ruby 3 (rb_fix_plus ship,
rb_int_plus ship, rb_fix_plus_fix anchor) + php 8 (all four symbols at
both builds). 9 REFUSED = 3 "no slice at this build" (ruby ship
vm_opt_plus, fix_plus, rb_fix_plus_fix) + 6 "the lineages leave
through a call" (ruby anchor vm_opt_plus, rb_fix_plus, rb_int_plus,
fix_plus; ruby anchor and ship rb_big_plus). 11 + 9 = 20.

**Proof outcomes, 11 carved records.** 3 PROVED, 8
TYPE_INCOMPARABLE. The 8: php's four symbols at two builds each
(4 × 2 = 8) — two of them because the declared type is a pointer pair,
six because no formal parameters exist to declare a type at all.
0 UNDECIDED, 0 unrenderable, 0 no-match.

**Per proved unit: 8 proved of 88 candidates**, with 70 disproved and
10 undecided in each case. The 70 are units in the same class key that
compute something else — the class key is a type pair and a result
family, so it holds every 64-bit integer operation, and the prover
separating them is the machinery working, not a problem.

**The nine-handler proposal, after this task.** 6 of the 9 now carry a
real carve at some build (ruby 2, php 4), against 1 before (cpython).
3 carry a proved computation part (cpython, plus ruby's two), against
1 before. 4 are TYPE_INCOMPARABLE (php's four). 2 route symbols were
added in their own section and are not part of the nine.

---

## Complete file inventory

Created this session; nothing existing was edited.

- `PseudoCoupHQ/Research/op_pipeline/t27_ruby_dump.sh` —
  the Airlock lane that disassembled ruby's handlers out of both pinned
  builds. 1311 bytes.
- `PseudoCoupHQ/Research/op_pipeline/t27_php_clean_build.sh`
  — the first clean-php attempt: it got configure past libxml for the
  first time and stopped in `make` on `ext/standard/scanf.c`. Kept on
  disk as the record of that step. 4099 bytes.
- `PseudoCoupHQ/Research/op_pipeline/t27_php_clean_build2.sh`
  — the lane that built the clean php pair (adds `-std=gnu17`) and
  dumped ruby's `rb_fix_plus_fix`. 2832 bytes.
- `PseudoCoupHQ/Research/op_pipeline/build_op_units_ruby.py`
  — ruby slice builder. 11137 bytes.
- `PseudoCoupHQ/Research/op_pipeline/op_units_ruby.json`
  — ruby slices, op_units shape. 75171 bytes.
- `PseudoCoupHQ/Research/op_pipeline/build_op_units_php.py`
  — php slice builder. 11935 bytes.
- `PseudoCoupHQ/Research/op_pipeline/op_units_php.json`
  — php slices, op_units shape, from the clean pair. 52470 bytes.
- `PseudoCoupHQ/Research/op_pipeline/dwarf_typed_key_t27.py`
  — the typed-key read over the binaries this task carves. 5950 bytes.
- `PseudoCoupHQ/Research/op_pipeline/dwarf_typed_key_t27.json`
  — its output, 20 records. 19433 bytes.
- `PseudoCoupHQ/Research/op_pipeline/lineage_carve.py` —
  the lineage-confluence carve. 31128 bytes.
- `PseudoCoupHQ/Research/op_pipeline/lineage_carve.json`
  — its output, 20 records. 290208 bytes.
- `PseudoCoupHQ/Research/op_pipeline/prove_interp_computation.py`
  — the computation-part prover driver. 13496 bytes.
- `PseudoCoupHQ/Research/op_pipeline/prove_interp_computation.json`
  — its output, 11 records. 18567 bytes.
- `PseudoCoupHQ/Research/op_pipeline/build_proposal_representation_dimension3.py`
  — the proposal extender. 14382 bytes.
- `PseudoCoupHQ/Research/op_pipeline/proposal_representation_dimension3.json`
  — **the artifact for the owner's ratification**, nine handlers plus the two
  route symbols. 79102 bytes.
- `PseudoCoupHQ/DevComms/log_113_task27_ruby_php_slices.md`
  — this log.
- A dated entry appended to
  `PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/PROGRESS.md`.

Inside the sandbox container, not in any repo:
`/persist/php_c_src/`, `/persist/php_c_anchor/`, `/persist/php_c_ship/`
(the clean php source and builds), `/persist/dwarf_typed_key_t27.json`,
`/persist/resolve_value.py` (the typedef resolver quoted above), and
the lane products under `Airlock/agent/out/t27/`.

Read but never written: `proposal_representation_dimension.json`,
`proposal_representation_dimension2.json`, `dwarf_typed_key.json`,
`dwarf_typed_key.py`, `interp_ruby.json`, `interp_php.json`,
`interp_cpython.json`, `interp_fastpath.json`, `block_cutter.py`,
`slice_extractor_fix.py`, `canon.py`, `canon2.py`,
`cross_unit_prover.py`, `check_no_spelling_keys.py`, and the four
pinned binaries.

---

## Evidence class, per claim

- The slices, the instruction counts, the gcov counts, the carves and
  the proofs: **forced by construction** — each is derived from the
  binaries' own bytes by a deterministic program whose transcript is
  pasted above.
- The typed keys and the `VALUE` resolution: **the tool's own
  testimony** raised as far as it goes — the compiler's own DWARF,
  emitted by the same compile that produced the bytes.
- The seed policies: the SysV one is **human interpretation of stated
  design** (the calling convention), cross-checked against each
  handler's DWARF formal-parameter list; php's frame-slot policy is
  **forced by construction** (the instruction word's own reads, traced).
- `provenance_is_weaker: true` stays on every ruby and php record: the
  handlers were located by reading source and symbol tables and by
  following call operands, not by the probe-generator pipeline, and
  the anchor/ship pairing is a build convention rather than the
  DWARF-anchored method the compiled track uses.

## What this does and does not gate

- It DOES complete the nine-handler evidence the owner asked for before
  ratifying option B / option B-with-A: every one of the nine now has
  either a real carve or a named mechanical refusal, and three carry a
  proved computation part.
- It does NOT change any table membership. `dominant_table24.json` and
  `dom_ops22.json` were not opened.
