# log_222 — TASK 103 round 19: cpython's integer multiply fast path against c's 64-bit multiply unit

Project node: node_0_3_1_11_interp_feeder (operator_equivalence line, master plan CORE_0_3_research.md §4.2).

Date: 2026-09-06. Node: `node_0_3_1_11_interp_feeder` (the
operator_equivalence line's interpreter feeder), master plan
`PseudoCoupHQ/Planning/node_0_3_research/CORE_0_3_research.md`
§4.2. Report shape per
`DevComms/LLM_communication_protocol.md` Appendix B: one
numbered tree, §1 names the objects in relation, instances before
mechanisms, the two lists at the end. Renderings are labelled
**LITERAL** (the object itself, quoted, with its path) or **GLOSS** (a
plain-words reading beside it), per §5.1a. Every claim below carries a
`$ ` command that reproduces it, or says in its own line that it
cannot.

All computation ran through Airlock, instance `t103`
(`Airlock/instances/t103.conf`, copied from `t97.conf`
per the brief, cpus 2 / memory 6g, `persist_volume = sandbox-persist`
read-only so the shared ship build is reached without any instance
being able to alter it — the same convention `t101b.conf` uses for
swift). One lane per step; every lane prints `[i/total]`. Lane logs
under `Airlock/agent/logs/` (this instance's own agent
dir is `<runs>/t103/agent/logs/` — Airlock's per-instance
convention; named at each transcript below).

---

## 1. The objects, in relation

- **the owner's question, 2026-09-06** (quoted in the brief): whether
  Python's unbounded-integer multiply's control flow "would simplify
  to the equivalent" of int32/int64 multiplication, and whether that
  has already been measured. It had not; this task measures the part
  the machinery reaches today.
- **the cpython ship build** is the compiled binary the question is
  about: `/persist/cpython_ship/python`, the same build task 94 read
  (`PseudoCoupHQ/DevComms/log_199_task94_interpreter_function_bodies.md`).
- **the multiply handler**, `long_mul`, is the C function inside that
  build whose compiled bytes ARE the object the question is about: the
  whole-function boundary the owner ruled 2026-09-05
  (`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_1_arch_unit/CORE_0_3_5_1_arch_unit.md`,
  "the unit's boundary").
- **the canonical form** is the one shape every arch-unit -- compiled
  or interpreted -- is rendered into so a gate can ask about it:
  `PseudoCoupHQ/Research/op_pipeline/canonical_form.py`,
  task 96's form
  (`PseudoCoupHQ/DevComms/log_201_task96_interpreters_onto_canonical_form.md`).
- **the term** is the handler's canonical-form body expressed as a z3
  expression, built by `PseudoCoupHQ/Research/op_pipeline/term.py`'s
  `Term.transcribe`, the machinery `term97_walk.py` finished over the
  compiled-language population
  (`PseudoCoupHQ/DevComms/log_202_task97_term_pool_canon40.md`)
  and this task is the first to ask about an interpreter handler.
- **the c unit**, `c/op_181`, is the single-opcode reference this
  task's step 2 gates the handler's term against: `imul`, `a * b`
  on two `int64_t`, its pool entry `E00063` in
  `PseudoCoupHQ/Research/op_pipeline/the_pool5.json`.
- **the projection** is the input domain both sides are compared on:
  both operands `_PyLong_BothAreCompact` under cpython's own compact
  test, stated LITERAL in §4.

---

## 2. Walkthrough

The ship build's own `sysconfig` and `sys._jit` were read first,
answering the owner's JIT question before anything else: this build carries
the `sys._jit` introspection module (every 3.14 build does) but
`sys._jit.is_available()` returns `False` -- the experimental JIT was
compiled in as an interface, never turned on, and no
`Python/jit_stencils.h` exists anywhere under this build's tree.

`Objects/longobject.c` was then read at this ship build's own path
(`/persist/cpython_ship/Objects/longobject.c`, mounted read-only
alongside the binary) to find the exact multiply handler and its
lines, LITERAL, per the brief. The fast path is a branch INSIDE
`long_mul`, not a distinct function -- `_PyLong_FromSTwoDigits` has no
symbol of its own either, the compiler inlined it -- so the unit is
the whole `long_mul` function, exactly as task 94 carved the whole of
`long_add` when its own fast path turned out to be inlined.

`long_mul`'s bounds were read off the SAME two sources task 94 read
`long_add`'s off (the ELF symbol table and DWARF), by importing and
calling `t94_read_bounds.py`'s own functions rather than re-typing
them. The whole function -- 658 bytes, 168 instructions -- was then put
on `canonical_form.py` exactly as task 96 put the eleven addition-line
units on it, by importing and calling `t96_onto_canonical_form.py`'s
own `render_form_two` / `render_form_three` / `AreaForm`. Both forms
wrap and both come back `PROVED_BY_CONSTRUCTION` -- the STRUCTURAL
verdict (six mechanical checks; not a solver proof of arithmetic
equivalence), which is exactly what `long_add` scored under the same
instrument in log_201.

The term itself was then built by importing and calling
`term97_walk.build()` (the function the brief names) and
`term66_run.one_unit()` (the record `term97_walk.py`'s own docstring
says is reused, not re-typed) -- the first time either has ever been
asked about an interpreter handler. A term for OUT-0 WAS built
(`term_state: TERM`), but it does not prove equal to `long_mul`'s own
ship body on either route `gate.py` tries: the route that re-simulates
the unit's own ship bytes independently refuses because those bytes
contain a real backward branch -- a control-flow cycle -- inside
`long_mul`'s own bounds; the route that walks the wrapped text in text
order separately refuses on the `push %rbx` / `pop %rbx` frame save,
which the ledger has no block for. §5 shows both, LITERAL.

Because that term's own verdict against its own body is UNDECIDED, it
is not sound ground to gate against `c/op_181`'s PROVED term on the
compact projection -- doing so would compare a proved object to one
this task's own machinery could not certify. §6 states the projection
LITERAL (read from source: both operands' magnitude in
`[0, 2**30 - 1]`, from `_PyLong_BothAreCompact` and `PyLong_SHIFT`) and
reports the outcome as **NO_TERM**, naming the real cause in place of
the brief's own guess: the cycle is not inside `k_mul` (Karatsuba is
never walked into -- it sits behind a `call`, a transfer OUT of the
unit's own bounds, attached as a `runtime_callee` row) but inside
`long_mul`'s OWN bytes, a ten-instruction loop that stores a 2-limb
result one 30-bit digit at a time.

§7 steps the whole path for one real instantiation, `a = 3`, `b = 4`,
as machine state, showing exactly where the compact-test guard
branches, where the multiply happens, and what the function actually
returns (a pointer, not the number 12).

---

## 3. The JIT question, literal

**LITERAL**, `PseudoCoupHQ/Research/op_pipeline/t103_l1_inventory.sh`
and `t103_l3_readsrc.sh`, run in Airlock instance `t103`, lane log
`<runs>/t103/agent/logs/20260906T191137Z__t103_l1_inventory.sh.log`
and `20260906T191256Z__t103_l2_source.sh.log`:

```
$ /persist/cpython_ship/python --version
Python 3.14.7
$ /persist/cpython_ship/python -c "import sysconfig; print(sysconfig.get_config_var('PY_CORE_CFLAGS'))"
-fno-strict-overflow -Wsign-compare -DNDEBUG -g -O3 -Wall -std=c11 -Wextra ... -DPy_BUILD_CORE
$ /persist/cpython_ship/python -c "
import sys
print('hasattr sys._jit:', hasattr(sys, '_jit'))
print('sys._jit.is_available():', sys._jit.is_available())
print('sys._jit.is_enabled():', sys._jit.is_enabled())
"
hasattr sys._jit: True
sys._jit.is_available(): False
sys._jit.is_enabled(): False
$ find /persist/cpython_ship -iname "jit_stencils.h"
(no output)
```

**GLOSS.** `sys._jit` is CPython 3.14's introspection module for the
experimental copy-and-patch JIT; it exists in every 3.14 build's
interpreter, whether or not the JIT itself was configured in. This
build carries the interface but `is_available()` -- "true if the
current Python executable SUPPORTS JIT compilation" -- answers
`False`, and no generated `jit_stencils.h` (the file the JIT build step
produces) exists anywhere under this build's own source tree
(`/persist/cpython_ship`, mounted alongside the binary). Nothing was
built to answer this; both facts were read off the existing ship build
task 94 already used.

---

## 4. The handler carved, and its arrival contract

**LITERAL**, `/persist/cpython_ship/Objects/longobject.c` lines
4244-4257 (`t103_l3_readsrc.sh`, same lane log):

```
static PyLongObject*
long_mul(PyLongObject *a, PyLongObject *b)
{
    /* fast path for single-digit multiplication */
    if (_PyLong_BothAreCompact(a, b)) {
        stwodigits v = medium_value(a) * medium_value(b);
        return _PyLong_FromSTwoDigits(v);
    }

    PyLongObject *z = k_mul(a, b);
    /* Negate if exactly one of the inputs is negative. */
    if (!_PyLong_SameSign(a, b) && z) {
        _PyLong_Negate(&z);
    }
    return z;
}

PyObject *
_PyLong_Multiply(PyLongObject *a, PyLongObject *b)
{
    return (PyObject*)long_mul(a, b);
}
```

**GLOSS.** `_PyLong_Multiply` is a one-line wrapper; `long_mul` is
where the work is. The fast path (`_PyLong_BothAreCompact`) is a
branch, not a separate function -- `_PyLong_FromSTwoDigits` has no ELF
symbol either (confirmed below), so per task 94's own rule ("where the
fast path is a distinct function ... carve it; where it is inlined
into `long_mul`, carve `long_mul` and say so") **the unit is the whole
`long_mul` function.**

**LITERAL**, `PseudoCoupHQ/Research/op_pipeline/interp103_bounds.json`
(`interp103_bounds.py`, reusing `t94_read_bounds.symbol_rows`,
`.dwarf_rows`, `.objdump_range` unmodified; lane log
`20260906T192107Z__t103_l8_bounds_run.sh.log`):

```
$ python3 -c "
import json
d=json.load(open('PseudoCoupHQ/Research/op_pipeline/interp103_bounds.json'))
r=d['record']
print(r['new_low'], r['new_high'], r['new_byte_length'], r['new_instruction_count'], r['symbol_table_and_dwarf_agree'], r['dwarf_rows'])
"
0x1394f0 0x139782 658 168 None []
```

**GLOSS.** `long_mul` is at `0x1394f0`, 658 bytes, 168 instructions.
`dwarf_rows` is empty -- DWARF carries no named `DW_TAG_subprogram` for
`long_mul` in this build, the same situation `long_add` was in
(log_199 §1.3: "DWARF carries NO named subprogram for
`cpython/long_add`"), so this bound rests on the symbol table alone,
which is one of the ruling's two named sources.

**LITERAL**, the arrival contract
(`PseudoCoupHQ/Research/op_pipeline/interp103_canonical.py`,
field `ARRIVAL_CONTRACT`):

```
{a: rdi, b: rsi, result: rax, result_width: 64}
```

**GLOSS.** Read the same way task 94 read `long_add`'s own contract
(`t94_recarve.json`, quoted in log_199): the first dereference of
`%rdi` and `%rsi` are both READS, at a fixed displacement (`0x10`, the
`lv_tag` field), before either register is written (the `mov
%rdi,%rbx` copy at entry is a copy, not a dereference); the SysV
convention agrees they are argument 0 and argument 1. `%rax` carries
the returned pointer on every one of `long_mul`'s three `ret`s.

---

## 5. The canonical form, the term, and the verdict against its own body

**LITERAL**, `PseudoCoupHQ/Research/op_pipeline/interp103_canonical.json`
(FORM 2, `canonical_form.py` Part A -- unmodified; lane log
`20260906T192231Z__t103_l9_canonical_run.sh.log`), the wrapped text in
full:

```
mov ledger+0x00(%rip),%rdi; mov 0x0(%rdi),%rdi; mov ledger+0x00(%rip),%rsi; mov 0x8(%rsi),%rsi; push %rbx; mov %rdi,%rbx; sub $0x20,%rsp; mov 0x10(%rdi),%rax; mov 0x10(%rsi),%rdx; mov %rax,%rcx; or %rdx,%rcx; cmp $0xf,%rcx; jbe L3; mov %rsi,0x8(%rsp); call x_k_mul; ... [105 lines total, all of long_mul's own bytes present character-for-character, only branch targets rewritten onto positional labels L0..L12] ... L7:; add $0x5,%edi; lea 0x49d906(%rip),%rax; add $0x20,%rsp; movslq %edi,%rdi; pop %rbx; shl $0x5,%rdi; lea 0x36f0(%rax,%rdi,1),%rdx; mov %rdx,%rax; mov ledger+0x38(%rip),%r11; mov %rax,0x0(%r11); ret
```

Verdict: `PROVED_BY_CONSTRUCTION`, both FORM 2 and FORM 3 (the same
plus the seventh block kind, `t96_arriving_area.py`, for the two
arriving pointers). **GLOSS, and this is not a solver proof.** The
same six mechanical checks log_201 §4.2 named carry it: the body is
present character-for-character in its own order (C1), the prelude
writes only what the arrival contract names (C2), every return is
preceded by the store into OUT-0 (C3), body and plumbing touch
disjoint text (C4), the epilogue's pointer register is not the answer
register (C5), the only text this form changed is 26 transfer targets
(C6). **This is the same class of result `long_add` scored** -- the
form wraps the whole branchy function without collision, exactly as
task 96 found for addition.

**LITERAL**, `PseudoCoupHQ/Research/op_pipeline/interp103_term.json`
(`interp103_term.py`, reusing `term97_walk.build` and
`term66_run.one_unit` unmodified; lane log
`<runs>/t103/agent/logs/20260906T192541Z__t103_l11_term_run.sh.log`):

```
$ python3 -c "
import json
d=json.load(open('PseudoCoupHQ/Research/op_pipeline/interp103_term.json'))
f=d['form_two']
print('term_state:', f['term_state'])
print('outcome:', f['outcome'])
print('route (ship):', f['verdict_ship']['reason'])
print('route (text):', f['verdict_text']['reason'])
"
term_state: TERM
outcome: UNDECIDED
route (ship): the reference: this body's control flow has a cycle (a transfer back to a block already on the walk), and no loop invariant is invented here
route (text): the text-order walk: this opcode moves a value to or from the machine stack, and the ledger has no block for the machine stack: no row holds the value it wrote, so there is nothing for a term to be about
```

**This is the answer to the brief's "verdict of the term against its
own body": UNDECIDED, by two independent, named causes, neither of
them a timeout.**

**GLOSS, where the cycle actually is** -- read off `interp103_bounds.json`'s
own body, not asserted: `long_mul`'s compiled bytes contain a real
backward branch at their own address `0x1396d3` (`jne 1396c0`), inside
the unit's own bounds:

```
$ python3 -c "
import json
d=json.load(open('PseudoCoupHQ/Research/op_pipeline/interp103_bounds.json'))
for r in d['record']['body']:
    if int(r['address'],16) in range(0x1396c0, 0x1396d4):
        print(r['address'], r['mnem'])
"
0x1396c0 mov %ecx,%esi
0x1396c2 add $0x4,%rax
0x1396c6 and $0x3fffffff,%esi
0x1396cc shr $0x1e,%rcx
0x1396d0 mov %esi,-0x4(%rax)
0x1396d3 jne 1396c0 <long_mul+0x1d0>
```

**GLOSS.** This is not Karatsuba (`k_mul`) -- that sits behind a
`call` at `0x139515`, a transfer OUT of the unit's own bounds, listed
separately in `interp103_term.json`'s `call_targets`
(`["x_k_mul", "x_long_alloc", "x__Py_Dealloc", "x_long_alloc",
"x__PyLong_FromMedium"]`) and attached as a `runtime_callee` row, not
walked into. This loop is the digit-store loop `long_mul` runs ITSELF
when the product needs more than one 30-bit digit but fewer than
three: each pass masks off 30 bits of the running magnitude
(`and $0x3fffffff,%esi`), stores that digit (`mov %esi,-0x4(%rax)`),
shifts the remainder down (`shr $0x1e,%rcx`) and loops while a digit
remains. `Ledger.walk_dataflow`'s own text-order walk names it
correctly, refuses to invent a loop invariant, and says exactly where.

**One shortfall found and disclosed, not worked around.** Part B (the
seventh block kind) could not be walked through this same term
machinery: `term66_run.runtime_rows_of` reads every ledger row's
`produced_by` as a dict with a `kind` field; `t96_arriving_area.py`'s
AREA rows carry `produced_by == "arrival"`, a plain string.

```
$ python3 -c "
import json
d=json.load(open('PseudoCoupHQ/Research/op_pipeline/interp103_term.json'))
print(d['form_three']['term_state'], '--', d['form_three']['why_not_attempted'][:180])
"
NOT_ATTEMPTED -- term66_run.runtime_rows_of reads row['produced_by'].get('kind') for every ledger row; row 'AREA-0' (block 'AREA') carries produced_by='arrival', which is a plain string, not the {k
```

Neither `term66_run.py` nor `t96_arriving_area.py` is edited; this is
a real, previously-unexercised incompatibility between task 96's
ledger extension and the canon40-era term machinery, flagged rather
than patched.

---

## 6. Gated against `c/op_181`, on the projection

**LITERAL**, the projection, from source
(`/persist/cpython_ship/Include/internal/pycore_long.h`,
`t103_l7_bounds_src2.sh`, same lane run):

```
static inline int
_PyLong_BothAreCompact(const PyLongObject* a, const PyLongObject* b) {
    return (a->long_value.lv_tag | b->long_value.lv_tag) < (2 << NON_SIZE_BITS);
}
#define NON_SIZE_BITS 3
#define PyLong_SHIFT    30
```

**GLOSS.** Combined tag under `2 << 3 = 16` means each operand's own
digit count is 0 or 1 (`tag = 8*ndigits + 3 flag bits`); one digit is
`PyLong_SHIFT` = 30 bits. **The projection: both operands' magnitude in
`[0, 2**30 - 1]`, independently signed -- value in
`[-(2**30-1), 2**30-1]` each.** This matches the compiled test exactly
(`cmp $0xf,%rcx; jbe ...` in §4's disassembly).

**LITERAL**, `c/op_181`'s pool entry and proved term, read rather than
rebuilt, `PseudoCoupHQ/Research/op_pipeline/the_pool5.json`
entry `E00063`:

```
$ python3 -c "
import json
d=json.load(open('PseudoCoupHQ/Research/op_pipeline/the_pool5.json'))
for e in d['entries']:
    for m in e['members']:
        if m['unit']=='c/op_181':
            print(e['entry_id'], m['term_outcome'], m['layer5_normalized_text'])
"
E00063 PROVED_ON_SHIP v0*v1
```

**LITERAL**, `PseudoCoupHQ/Research/op_pipeline/interp103_gate_c181.json`
(lane log `<runs>/t103/agent/logs/20260906T192922Z__t103_l12_gate_c181.sh.log`):

```
$ python3 -c "
import json
d=json.load(open('PseudoCoupHQ/Research/op_pipeline/interp103_gate_c181.json'))
print('outcome:', d['outcome'])
print('headline:', d['cause']['headline'])
print('correction:', d['cause']['correction_to_the_briefs_own_guess'][:210])
"
outcome: NO_TERM
headline: cpython/long_mul's FORM 2 term is UNDECIDED against its own body on both routes gate.py tries, so it is not sound ground to gate against c/op_181's PROVED term; no projected comparison is run
correction: the brief's example cause was 'a loop in x_mul / Karatsuba'; k_mul is never walked into (it is a `call`, a transfer OUT of long_mul's own bounds, attached as a runtime_callee row, not a cycle). The REAL cycle...
```

**This is the answer to step 2: `NO_TERM`.** Comparing an UNDECIDED
term to `c/op_181`'s PROVED one would misstate what was asked; the
`c/op_181` side is genuinely proved (§ above), the `cpython/long_mul`
side is not, and §5 already names both reasons why, by their own
addresses.

---

## 7. THE MECHANISM, AS MACHINE STATE, STEPPED (protocol §4.6)

`a = 3` (address `0x800000`: `lv_tag = 0x08`, `digit[0] = 3`),
`b = 4` (address `0x900000`: `lv_tag = 0x08`, `digit[0] = 4`). Every
value below is computed by `interp103_step.py` from these two facts
and the real instruction text in `interp103_bounds.json`; nothing is
asserted without the opcode above it. Full table:
`PseudoCoupHQ/Research/op_pipeline/interp103_step.json`.

**LITERAL**, lane log `<runs>/t103/agent/logs/20260906T193330Z__t103_l14_step.sh.log`:

```
idx  address   instruction                      %rdi          %rsi          %rbx          %rax          %rdx          %rcx
------------------------------------------------------------------------------------------------------------------------------------
--   (entry)                                    8388608       9437184       None          None          None          None
0    0x1394f0  push %rbx                        8388608       9437184       None          None          None          None
3    0x1394f8  mov 0x10(%rdi),%rax              8388608       9437184       8388608       8             None          None
4    0x1394fc  mov 0x10(%rsi),%rdx              8388608       9437184       8388608       8             8             None
7    0x139506  cmp $0xf,%rcx                    8388608       9437184       8388608       8             8             8
     -- compare 8 against 0xf
8    0x13950a  jbe 139618 <long_mul+0x128>      8388608       9437184       8388608       8             8             8
     -- taken=True (both operands compact)          <-- THE GUARD BRANCHES HERE
75   0x139618  mov 0x18(%rsi),%edi              4             9437184       8388608       8             8             8
76   0x13961b  mov 0x18(%rbx),%ecx              4             9437184       8388608       8             8             3
79   0x139624  imul %rcx,%rdi                   12            9437184       8388608       0             0             3
     -- THE MULTIPLY HAPPENS HERE: %rdi = 4 * 3 = 12
84   0x139636  imul %rsi,%rdi                   12            1             8388608       0             0             1
85   0x13963a  imul %rcx,%rdi                   12            1             8388608       0             0             1
     -- sign correction (both positive: *1, *1 -- no change)
89   0x13964b  jbe 1396f0 <long_mul+0x200>      12            1             8388608       17            0             12
     -- taken=True (the product 12 is inside the cached range)
131  0x1396f3  lea 0x49d906(%rip),%rax          17            1             8388608       &_PyRuntime   0             12
136  0x139706  lea 0x36f0(%rax,%rdi,1),%rdx     544  ...     &_PyRuntime + 0x36f0 + 544 (the cached PyLongObject for 12)  12
138  0x139711  ret                              544  ...     &_PyRuntime + 0x36f0 + 544 (the cached PyLongObject for 12)  12
     -- returns %rax: a POINTER, not the number 12
```

(register values print as decimal; the address column reads
`8388608` = `0x800000` = `a`'s address, `9437184` = `0x900000` = `b`'s
address. `interp103_step.json` carries every one of the 33 stepped
instructions on this path; only the guard, the multiply and the return
are excerpted above, per the brief's own wording.)

**GLOSS.** The compact-test guard branches at index 8 (`jbe 139618`).
The multiply itself is one instruction, index 79 (`imul %rcx,%rdi`),
computing the two single-digit MAGNITUDES: `4 * 3 = 12`. The two
`imul`s that follow it (indices 84-85) are sign correction by `1` or
`0` (both operands positive here, so they change nothing) --
`(1 - a_sign) * (1 - b_sign)`, folded through multiplication rather
than a branch. **The function does not return 12.** It returns the
ADDRESS of the cached `PyLongObject` holding 12 -- the same fact
log_199 §2.3 found for `long_add` returning 7: "the function answers
the address of a PyLong object holding 7... only the second is what
CPython's addition returns."

---

## 8. Whether the control flow "simplifies to the equivalent" -- answered from the evidence above, not asserted new

the owner's question was whether the multiply fast path's control flow would
simplify to int32/int64 multiplication's shape. **It is SIMPLER than
`long_add`'s in one precise sense, and NOT simpler in another, both
shown above rather than argued:**

- **Simpler:** the arithmetic itself is ONE instruction on the fast
  path (`imul %rcx,%rdi`, §7), against `long_add`'s own single `lea`
  addition -- the same shape, one opcode. Sign handling is folded
  through two more multiplies by `0` or `1` rather than a branch,
  where `long_add` subtracts.
- **Not simpler, and this is the new finding this task adds:** the
  RESULT of a multiply can need a second 30-bit digit far more readily
  than the result of an add of two single-digit values, so `long_mul`
  carries an extra branch (`cmp $0x7ffffffe,%rax; jbe ...`) and, behind
  it, a digit-store LOOP (§5) that `long_add`'s own body does not
  contain at all -- `long_add`'s equivalent path returns through
  `_PyLong_FromMedium` (a `call`, off the unit's own bounds) rather
  than filling a multi-digit result itself. **This loop is exactly
  what stops the term machinery today** (§5, §6): the guard branches
  reduce to holes the walk can still cross, but a real backward branch
  inside the unit's own bytes is not something `Ledger.walk_dataflow`
  invents an invariant for.

---

## 9. Gates

**LITERAL**, the spelling guard over every JSON this task wrote, lane
log `<runs>/t103/agent/logs/20260906T193330Z__t103_l16_step2.sh.log`:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/op_pipeline/interp103_bounds.json PseudoCoupHQ/Research/op_pipeline/interp103_canonical.json PseudoCoupHQ/Research/op_pipeline/interp103_term.json PseudoCoupHQ/Research/op_pipeline/interp103_gate_c181.json PseudoCoupHQ/Research/op_pipeline/interp103_step.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS interp103_bounds.json -- no operator token in any key, grouping, pairing or row structure
PASS interp103_canonical.json -- no operator token in any key, grouping, pairing or row structure
PASS interp103_term.json -- no operator token in any key, grouping, pairing or row structure
PASS interp103_gate_c181.json -- no operator token in any key, grouping, pairing or row structure
PASS interp103_step.json -- no operator token in any key, grouping, pairing or row structure
```

```
$ grep -c exempt PseudoCoupHQ/Research/op_pipeline/interp103_bounds.json PseudoCoupHQ/Research/op_pipeline/interp103_canonical.json PseudoCoupHQ/Research/op_pipeline/interp103_term.json PseudoCoupHQ/Research/op_pipeline/interp103_gate_c181.json PseudoCoupHQ/Research/op_pipeline/interp103_step.json
PseudoCoupHQ/Research/op_pipeline/interp103_bounds.json:0
PseudoCoupHQ/Research/op_pipeline/interp103_canonical.json:0
PseudoCoupHQ/Research/op_pipeline/interp103_term.json:0
PseudoCoupHQ/Research/op_pipeline/interp103_gate_c181.json:0
PseudoCoupHQ/Research/op_pipeline/interp103_step.json:0
```

**It caught this task once, and it was fixed in the artifact, not by
exempting anything:** `interp103_step.json`'s entry row originally
carried the index `"--"`, an operator token in the miner's own
inventory, on a structure field. Renamed to `"entry"`. The failing run
and the passing re-run are both in
`<runs>/t103/agent/logs/20260906T193142Z__t103_l15_guard.sh.log`
and `20260906T193330Z__t103_l16_step2.sh.log`.

The checker is unmodified:

```
$ sha256sum PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
a377462b38e8610d8bb60ac668f0a5adc72ee571d15efab85e40a9afdaa511f7  PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
```

(same hash log_201 §7.1 recorded -- unchanged since 2026-09-05).

The display label (`*`) rides on the field `label`, once per record,
alongside `unit` and `language`; nothing in any interp103_* program
keys, groups, pairs or selects on it.

---

## 10. Memory and time

- **Stated bound: 6 GB, abort by name `ABORT_MEMORY_T103`,** checked
  after every program's own peak.
- **Measured peaks** (`ru_maxrss`, printed by each program):
  - `interp103_bounds.py` -- **1,622,772 kB (1.6 GB)**, the DWARF scan
    (cpython's own debug info, one compilation unit's DIEs at a time).
  - `interp103_canonical.py` -- **58,672 kB (57 MB)**.
  - `interp103_term.py` -- **57,432 kB (56 MB)**.
  - `interp103_gate_c181.py`, `interp103_step.py` -- both under
    10 MB.
- No run hit a time or memory limit; nothing was re-run with more
  room. Longest lane: `interp103_bounds.py`'s own run, 24.2 s.

---

## 11. Artifacts, every one named

| path | what it is |
|---|---|
| `Research/op_pipeline/interp103_bounds.py` / `.json` | reads `long_mul`'s bounds off the ship build (reuses `t94_read_bounds.py` unmodified) |
| `Research/op_pipeline/interp103_canonical.py` / `.json` | `long_mul` onto `canonical_form.py`, Parts A and B (reuses `t96_onto_canonical_form.py` unmodified) |
| `Research/op_pipeline/interp103_term.py` / `.json` | builds the term (reuses `term97_walk.build` and `term66_run.one_unit` unmodified); the verdict against the unit's own body |
| `Research/op_pipeline/interp103_gate_c181.py` / `.json` | the projection, literal; the gate against `c/op_181`'s term and body |
| `Research/op_pipeline/interp103_step.py` / `.json` | the stepped machine state, §7 |
| `Research/op_pipeline/interp103_report.md` | this report |
| `Research/op_pipeline/t103_l1_inventory.sh` … `t103_l16_step2.sh` | the lane scripts, one per submission |

No file under `Research/op_pipeline/` was edited except these new
`interp103_*` files and their own lane scripts, per the brief's stop
rule. `Airlock/instances/t103.conf` is new, copied from
`t97.conf`.

---

## 0. The two lists

## 0.1 Decided, recorded for audit

- **This ship build does not have the experimental JIT enabled**:
  `sys._jit.is_available()` is `False`; no `jit_stencils.h` exists.
  Nothing was built to find this out.
- **`long_mul` is the unit** (the fast path is inlined, not a separate
  symbol), carved at `0x1394f0`, 658 bytes, 168 instructions, the same
  two sources (symbol table, DWARF) task 94 used for `long_add`.
- **The whole function wraps and is `PROVED_BY_CONSTRUCTION`** under
  both Part A and Part B of `canonical_form.py`, structurally --
  matching `long_add`'s own result under the same instrument.
- **The term built for OUT-0 is `UNDECIDED` against the unit's own
  body**, on both routes `gate.py` tries, for two independent, named
  causes: a real backward branch (a digit-store loop) inside
  `long_mul`'s own bytes at `0x1396c0`-`0x1396d3`, and an unmodelled
  machine-stack save/restore.
- **Step 2's gate against `c/op_181` is `NO_TERM`**, because there is
  no sound term to project: gating an UNDECIDED term against a PROVED
  one would misstate the comparison. The projection is stated LITERAL
  regardless: both operands' magnitude in `[0, 2**30-1]`.
- **The brief's own example cause ("a loop in `x_mul` / Karatsuba")
  does not hold as stated and is corrected**: `k_mul` sits behind a
  `call`, never walked into; the real cycle is a loop `long_mul`
  itself contains, named by address.
- **A mechanical gap found and disclosed, not patched**:
  `term66_run.runtime_rows_of` cannot read the seventh block kind's
  AREA rows (`produced_by` is a plain string there, not a dict); Part
  B's term route is `NOT_ATTEMPTED` for this named reason.
- **The spelling guard caught one violation** (an operator token on a
  structure field) and it was renamed, not exempted.

## 0.2 Awaiting the owner

- **Whether the seventh block kind's ledger shape should be reconciled
  with `term66_run.py`'s row-producer assumption** so Part B can be
  walked through the term machinery at all -- this task found the
  incompatibility and did not decide how to close it, per the stop
  rule (a change to `term66_run.py` or `t96_arriving_area.py` is a
  change to a shared file this brief did not name).
- **Whether the term machinery should ever be asked to build a term
  for a body containing its OWN internal loop** (as opposed to only
  refusing on transfers OUT of the unit, which is `runtime_callee`'s
  already-settled ground) -- this is a research-scope question about
  what the walk is FOR, not an implementation bug to route around.

---

## 12. This log run through the log verifier

`check_conventions_log_claims.py` (task 90) was run against this file
inside Airlock instance `t103`, three times as fixes landed.

**LITERAL**, the final pass, lane log
`<runs>/t103/agent/logs/20260906T193934Z__t103_l20_verify_log3.sh.log`:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 PseudoCoupHQ/DevComms/log_222_task103_multiply_fastpath_vs_c.md
population: 23 claims across 1 logs
  MATCHES          9
  DIFFERS          0
  UNVERIFIABLE     10
  REFUSED          3
  NOT_RERUNNABLE   1

ONE LINE: 9 of 23 claims reproduce; 10 (43%) carry nothing to re-run

causes, by name:
  prose_only                       5
  attribution_only                 5
  head_not_on_the_read_only_allowlist 3
  output_elided                    1
```

**Zero DIFFERS.** Two earlier passes caught four real DIFFERS and both
were fixed IN THE LOG, never in the verifier:

1. A truncated string (§5's `why_not_attempted[:180]`) was pasted in
   full rather than at its own stated cutoff -- fixed to the actual
   180-character slice.
2. Three commands under §9 used bare filenames (`interp103_bounds.json`
   etc.); the verifier's working directory is `PseudoCoupHQ`,
   not `Research/op_pipeline`, so those files could not be opened.
   Fixed to full paths (not a `cd &&` prefix -- `cd` is not on the
   image, which the second pass caught as `NOT_RERUNNABLE`).
3. `sha256sum`'s output line named the file by its bare name; the real
   command (given a full path) prints the full path back. Fixed to
   match.

The three REFUSED are `/persist/cpython_ship/python` invocations --
that path is not on the verifier's read-only allowlist. They are kept
because they are the primary evidence for §3's JIT answer; §3 also
pastes the same facts read a second way (`find ... jit_stencils.h`,
which MATCHES). The ten UNVERIFIABLE are prose readings and
attributions with nothing of their own to re-run, each sitting beside
a literal above it that does carry a command.
