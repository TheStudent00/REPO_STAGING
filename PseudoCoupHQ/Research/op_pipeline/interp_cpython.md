# interp_cpython — the CPython pilot of the interpreter track

Ruled first by the owner, 2026-08-26 (SUPPORT_scaling_design, interpreter
track). The question: for a Python addition on ints, which
interpreter handler actually executes; what the bytecode middle form
is; and what the handler looks like as a slice of the interpreter
binary. Data: `interp_cpython.json`. Built by
`fold_interp_cpython.py` from the Airlock lane outputs.

## the instrument, said plainly first

The runtime record here is a **TALLY** — gcov line counters. It says
how many times a line ran, never in what order. The standing rule of
this node prefers a **DIARY** (id-emission into the interpreter's own
source, order preserved). For this pilot the tally is accepted as
the first instrument; the diary is a later lap and is **not done
here**. Every ordering statement below is read off the source text,
which is interpretation, not measurement.

## the pin

- cpython `v3.14.7`, commit `823f0323ee6ec1402088b73bce1a38473cac36dc`
- `Include/patchlevel.h`: PY_MAJOR 3 / PY_MINOR 14 / PY_MICRO 7 / FINAL
- the built interpreter says:
  `3.14.7 (tags/v3.14.7:823f032, Aug 26 2026, 13:05:58) [GCC 15.2.0]`
- evidence class: artifact fact (git, and the binary's own banner)

## the three builds

| build | configure | used for |
|---|---|---|
| coverage | `./configure --disable-test-modules CFLAGS="--coverage -O0 -g -fwrapv" LDFLAGS="--coverage"` | the dispatch measurement |
| anchor | `./configure --disable-test-modules CFLAGS="-O0 -g -fwrapv"` | the arch-unit, optimizer off |
| ship | `./configure --disable-test-modules` (OPT `-DNDEBUG -g -O3 -Wall`) | the arch-unit, optimized |

The compile line that actually ran, pasted from the make log rather
than assumed:

```
gcc -c -fno-strict-overflow -Wsign-compare -DNDEBUG -g -O3 -Wall --coverage -O0 -g -fwrapv   -std=c11 ... -DPy_BUILD_CORE -o Objects/longobject.o Objects/longobject.c
```

CPython's own `OPT` (`-O3`) is placed **before** the flags we passed,
so the trailing `-O0` is the level that took effect.

## the method

Differential coverage. A baseline probe runs the same loop shape
without the probed addition; the addition probes run the same loop
with it; the difference in line counts is what the addition reached.

Honest caveat, because it shows up in every number below: the
baseline is **not** addition-free — its loop counter step is itself
an addition. That is why baseline counts on the handler lines sit
near 100000 rather than 0. The **delta** is still exactly the
100000 probed calls.

Probes: `p0_baseline` (returns the first argument), `p1_smallint`
(returns the sum, ints 3 and 4), `p2_bigint` (same, two 2000-bit
values), `p3_disasm` (the bytecode listing).

## the bytecode middle form (pasted)

```
=== dis.dis(af) -- as compiled, before any run ===
  3           RESUME                   0

  4           LOAD_FAST_BORROW_LOAD_FAST_BORROW 1 (a, b)
              BINARY_OP                0 (+)
              RETURN_VALUE
=== warming: 100000 calls with (int,int) ===
=== dis.dis(af, adaptive=True) -- after warm-up ===
  3           RESUME_CHECK             0

  4           LOAD_FAST_BORROW_LOAD_FAST_BORROW 1 (a, b)
              BINARY_OP_ADD_INT        0 (+)
              RETURN_VALUE
```

`co_code` length: 18 bytes. Evidence class: the tool's own testimony
(`dis`, on this build).

## the measured dispatch path

The counts are `delta = count(probe run) - count(baseline run)`.
Full listing in the JSON; the load-bearing lines, pasted:

```
Python/generated_cases.c.h:142   delta=99999   probe=200005  baseline=100006  |  TARGET(BINARY_OP_ADD_INT) {
Python/generated_cases.c.h:161   delta=99999   probe=200005  baseline=100006  |    if (!PyLong_CheckExact(value_o)) {
Python/generated_cases.c.h:171   delta=99999   probe=200005  baseline=100006  |    if (!PyLong_CheckExact(left_o)) {
Python/generated_cases.c.h:187   delta=99999   probe=200005  baseline=100006  |    PyObject *res_o = _PyLong_Add((PyLongObject *)left_o, (PyLongObject *)right_o);
Objects/longobject.c:3771        delta=99999   probe=200005  baseline=100006  |_PyLong_Add(PyLongObject *a, PyLongObject *b)
Objects/longobject.c:3773        delta=99999   probe=200005  baseline=100006  |    return (PyObject*)long_add(a, b);
Objects/longobject.c:3738        delta=100000  probe=200079  baseline=100079  |long_add(PyLongObject *a, PyLongObject *b)
Objects/longobject.c:3740        delta=100000  probe=200079  baseline=100079  |    if (_PyLong_BothAreCompact(a, b)) {
Objects/longobject.c:3741        delta=100000  probe=200012  baseline=100012  |        stwodigits z = medium_value(a) + medium_value(b);
Objects/longobject.c:3742        delta=100000  probe=200012  baseline=100012  |        return _PyLong_FromSTwoDigits(z);
Objects/longobject.c:307         delta=100000  probe=200020  baseline=100020  |_PyLong_FromSTwoDigits(stwodigits x)
Objects/longobject.c:309         delta=100000  probe=200020  baseline=100020  |    if (IS_SMALL_INT(x)) {
Objects/longobject.c:310         delta=100000  probe=100267  baseline=267     |        return (PyLongObject*)get_small_int((sdigit)x);
Objects/longobject.c:59          delta=100001  probe=101409  baseline=1408    |get_small_int(sdigit ival)
Objects/longobject.c:62          delta=100001  probe=101409  baseline=1408    |    return (PyObject *)&_PyLong_SMALL_INTS[_PY_NSMALLNEGINTS + ival];
```

And the one-shot generic route, measured, not inferred:

```
Objects/abstract.c:1128          delta=1  probe=85  baseline=84   |PyNumber_Add(PyObject *v, PyObject *w)
Objects/abstract.c:964           delta=1  probe=158 baseline=157  |        x = slotv(v, w);
Python/specialize.c:2607         delta=1  probe=4   baseline=3    |            if (PyLong_CheckExact(lhs)) {
Python/specialize.c:2608         delta=1  probe=4   baseline=3    |                specialize(instr, BINARY_OP_ADD_INT);
```

### did it match the long_add expectation, or surprise?

Both. `long_add` was reached — the expectation held. It was reached
**one call deeper and through a different door** than the brief
stated: not the generic `BINARY_OP` dispatch, but the specialized
case `TARGET(BINARY_OP_ADD_INT)`, installed after exactly **one**
trip through the generic path. The generic path shows delta=1;
the specialized case shows delta=99999. `Python/ceval.c` itself
contributes almost nothing (delta 34 on the recursion-limit check);
the interpreter body lives in the generated header
`Python/generated_cases.c.h`, which is where the measurement points.

### the small-int fast path

Visible in the counts, not asserted. For the small pair `long_add`
took the compact branch (`_PyLong_BothAreCompact` delta 100000,
`medium_value(a) + medium_value(b)` delta 100000), handed to
`_PyLong_FromSTwoDigits`, which hit `IS_SMALL_INT` (delta 100000)
and returned a pointer into the preallocated `_PyLong_SMALL_INTS`
table (delta 100001). `x_add` was **not entered at all** for the
small pair — no delta on it. No allocation, no digit loop.

### the growth path (the large-int pair)

Same bytecode instruction, same specialized case, same `long_add` —
the divergence is inside it:

```
Objects/longobject.c:3765  delta=100002   |            z = x_add(a, b);
Objects/longobject.c:3650  delta=100002   |x_add(PyLongObject *a, PyLongObject *b)
Objects/longobject.c:3667  delta=6800004  |    for (i = 0; i < size_b; ++i) {
Objects/longobject.c:3668  delta=6700002  |        carry += a->long_value.ob_digit[i] + b->long_value.ob_digit[i];
Objects/longobject.c:3669  delta=6700002  |        z->long_value.ob_digit[i] = carry & PyLong_MASK;
Objects/longobject.c:3670  delta=6700002  |        carry >>= PyLong_SHIFT;
Objects/longobject.c:3678  delta=100002   |    return long_normalize(z);
Objects/longobject.c:157   delta=100004   |long_alloc(Py_ssize_t size)
```

67 digit steps per call, 100000 calls. This is the `growing` mode
the SUPPORT file predicted; here it is measured. Evidence class:
tally, per-run.

## the handler arch-units

**A defect found and repaired, stated because it would otherwise be
invisible.** The first slices were taken from the coverage binary,
and every one of them opened with a gcov counter increment:

```
315996  48 8b 05 03 1a 95 00  mov    0x951a03(%rip),%rax        # c673a0 <__gcov0.long_add>
31599d  48 83 c0 01           add    $0x1,%rax
```

That is the instrument, not the handler. The arch-units recorded in
`interp_cpython.json` come from separate **uninstrumented** builds of
the same pin, checked with `nm` to carry zero `__gcov` symbols.

| symbol | anchor (-O0) | ship (-O3) |
|---|---|---|
| `_PyLong_Add` | 13 | 95 |
| `long_add` | 78 | 94 |
| `x_add` | 92 | 106 |
| `_PyLong_FromSTwoDigits` | 28 | absorbed |
| `long_normalize` | 41 | absorbed |
| `long_alloc` | 63 | 66 |
| `_PyEval_EvalFrameDefault` | 28811 | 16821 |

(instruction counts; nothing truncated — the full instruction lists,
bytes and mnemonics, are in the JSON.)

Frontier, named rather than guessed at: `_PyLong_FromSTwoDigits` and
`long_normalize` are static and carry no symbol in the ship build.
They exist at the anchor. Their ship-build code is somewhere inside
their callers; this pilot did not chase it.

`long_add`, ship build, first 12 instructions:

```
137370  48 83 ec 28           sub    $0x28,%rsp
137374  48 8b 47 10           mov    0x10(%rdi),%rax
137378  48 8b 56 10           mov    0x10(%rsi),%rdx
13737c  48 89 f1              mov    %rsi,%rcx
13737f  49 89 c0              mov    %rax,%r8
137382  48 89 d6              mov    %rdx,%rsi
137385  48 09 d0              or     %rdx,%rax
137388  41 83 e0 03           and    $0x3,%r8d
13738c  83 e6 03              and    $0x3,%esi
13738f  48 83 f8 0f           cmp    $0xf,%rax
137393  76 43                 jbe    1373d8 <long_add+0x68>
137395  49 83 f8 02           cmp    $0x2,%r8
```

`long_add`, anchor build, first 12 instructions:

```
170a1b  f3 0f 1e fa           endbr64
170a1f  55                    push   %rbp
170a20  48 89 e5              mov    %rsp,%rbp
170a23  53                    push   %rbx
170a24  48 83 ec 28           sub    $0x28,%rsp
170a28  48 89 7d d8           mov    %rdi,-0x28(%rbp)
170a2c  48 89 75 d0           mov    %rsi,-0x30(%rbp)
170a30  48 8b 55 d0           mov    -0x30(%rbp),%rdx
170a34  48 8b 45 d8           mov    -0x28(%rbp),%rax
170a38  48 89 d6              mov    %rdx,%rsi
170a3b  48 89 c7              mov    %rax,%rdi
170a3e  e8 81 71 ff ff        call   167bc4 <_PyLong_BothAreCompact>
```

## the three-layer model, proved

1. **probe** — `def af(a, b): return a + b`, called 100000 times.
2. **bytecode** — one `BINARY_OP` instruction, which after warm-up
   is `BINARY_OP_ADD_INT`.
3. **handler slice** — `TARGET(BINARY_OP_ADD_INT)` inside the
   interpreter loop, calling `_PyLong_Add` -> `long_add`, extracted
   from the interpreter binary as instruction bytes.

## evidence classes on the claims

- pin, build flags, instruction bytes and counts — **artifact fact**.
- the bytecode listing — **the tool's own testimony** (`dis`).
- the dispatch path — **tally, per-run**: fact for these runs on this
  build. It does not bound all runs. A different warm-up, a
  different type pair, or a build with specialization disabled would
  land somewhere else, and this file does not say where.
- the brief's expectation (ceval dispatch + `long_add`) — recorded as
  **interpretation**, for comparison against what was measured.
- "the case runs before `_PyLong_Add`" and every other ordering — read
  off source text, so **interpretation**. The tally has no order.

## what was NOT done — marked

- No diary. Order is unmeasured.
- No carving of the `BINARY_OP_ADD_INT` case out of
  `_PyEval_EvalFrameDefault` as its own address range — **unverified**
  whether that is even cleanly possible with computed gotos.
- No normalization to the canonical runnable form, no matching
  against the compiled-language units, no bridge or dominance claim.
- Scope: x86-64, gcc 15.2.0, one pin, one operator intention, two
  type pairs, GIL build only. Free-threaded not touched.

## guard

`check_no_spelling_keys.py interp_cpython.json` ->
`PASS interp_cpython.json -- no operator token in any key, grouping,
pairing or row structure` (exit 0).

## the lanes

| lane | wall time | did |
|---|---|---|
| `interp_smoke.sh` | 0.6 s | preflight; the release-tag listing the pin was chosen from |
| `interp_a_build.sh` | 31.4 s | clone at the pin + coverage build |
| `interp_b_dispatch.sh` | 3.4 s | bytecode capture; first coverage attempt — gcov ran from the output directory, could not find the sources, produced header-only captures |
| `interp_b2_parse.sh` | 0.0 s | showed the header-only bytes, diagnosing the above |
| `interp_b3_dispatch.sh` | 4.6 s | the dispatch measurement, gcov run from the build tree |
| `interp_c_slice.sh` | 1.6 s | annotation of the measured lines; the polluted slice that exposed the gcov-counter problem |
| `interp_d_clean.sh` | 64.3 s | uninstrumented anchor + ship builds and their slices |

Total, all lanes: about 106 seconds. The 3600 s cap was never in
danger; splitting configure from make was unnecessary. Persistent
state at Airlock `/persist/cpython`, `/persist/cpython_anchor`,
`/persist/cpython_ship`.
