# interp_jvm — the JVM pilot of the JIT track

Ordered second by the owner, 2026-08-26 (SUPPORT_scaling_design, JIT track).
The question: for a Java addition on ints, what the bytecode middle
form is; what machine code the JIT produced for the warmed method; what
guards are visible in that dump; and what the warm-up recipe had to
cost. Data: `interp_jvm.json`. Built by `fold_interp_jvm.py` from the
Airlock lane outputs, which are archived under `lane_out_jvm/`. The
lane scripts themselves are archived under `lanes/`.

## the instrument, said plainly first

There is no hsdis in this JDK, so nothing disassembled the compiled
method for us. What `-XX:CompileCommand=print` gives instead is the
nmethod's **machine code as hex bytes**, plus the JVM's own annotation
lines. Those bytes were carved out and handed to **objdump**.

So every listing below is **two evidence classes stacked, kept apart**:

- the **bytes** and the annotation lines (`{poll_return}`,
  `{runtime_call UncommonTrapBlob}`, the scope lines) are the JVM's own
  testimony about its own output;
- the **mnemonics** are objdump's reading of those bytes — a second
  tool's testimony, not the JVM's.

Where the two agree the agreement is worth something, and it is said so
rather than merged into one voice.

## the pin

- `openjdk version "25.0.3" 2026-04-21`
- `OpenJDK Runtime Environment (build 25.0.3+9-2-26.04.2-Ubuntu)`
- `OpenJDK 64-Bit Server VM (build 25.0.3+9-2-26.04.2-Ubuntu, mixed mode, sharing)`
- `javac 25.0.3`; `java.vendor = Ubuntu`; `os.arch = amd64`
- disassembler: `GNU objdump (GNU Binutils for Ubuntu) 2.46`
- evidence class: artifact fact (the tools' own banners)

## which dump plan worked

| plan | outcome |
|---|---|
| A — hsdis ships with the JDK | **REFUSED.** A find over the whole JDK for `hsdis*` returned nothing. Every PrintAssembly run logged `[0.011s][warning][os] Loading hsdis library failed`. |
| B — build hsdis | **NOT ATTEMPTED, preconditions measured absent.** The container has gcc, make, git and objdump 2.46, but a filesystem-wide find for `dis-asm.h` returned nothing and `autoconf` is MISSING. hsdis's binutils backend needs both. Stated as a refusal, not smoothed into "didn't work". |
| C — `-XX:+PrintOptoAssembly` | **NOT NEEDED.** The flag was accepted by this product build without error, but was never used for the recorded unit. |
| the route actually used — printed bytes + objdump | **WORKED.** |

The load-bearing discovery, because it changes the shape of this whole
track: **`-XX:CompileCommand=print` prints the machine code bytes even
when hsdis is missing.** Only the mnemonics are absent. Pasted, exactly
as the JVM emitted it:

```
[MachCode]
[Verified Entry Point]
  # {method} {0x00007f9908400428} 'af' '(II)I' in 'Probe'
  # parm0:    rsi       = int
  # parm1:    rdx       = int
  #           [sp+0x20]  (sp of caller)
  0x00007f99346aa400: 4881 ec18 | 0000 0048 | 896c 2410 | 4181 7f20 | 0000 0000 | 0f85 2900 | 0000 8d04 | 1648 83c4 
```

## the configuration choice

**`-XX:-TieredCompilation`** — C2 only, so the dumped nmethod is the
final tier with no C1 profiling version in the way. The full dump
command:

```
java -Xbatch -XX:-TieredCompilation \
  -XX:+UnlockDiagnosticVMOptions \
  -XX:CompileCommand=print,Probe::af \
  -XX:CompileCommand=print,Probe::af2 \
  -XX:CompileCommand=dontinline,Probe::af \
  -XX:CompileCommand=dontinline,Probe::af2 \
  Probe 200000
```

`dontinline` is a choice that shapes the recorded unit and is stated
rather than hidden: without it C2 folds the method into its caller and
there is no standalone unit to record.

## the bytecode middle form (pasted, javap -c -p)

```
  static int af(int, int);
    Code:
         0: iload_0
         1: iload_1
         2: iadd
         3: ireturn

  static int af2(int, int);
    Code:
         0: iload_0
         1: iload_1
         2: idiv
         3: ireturn
```

Evidence class: the tool's own testimony (`javap`).

## the tier-transition lines (pasted, -XX:+PrintCompilation)

With tiering off, n=200000:

```
12    5 %           Probe::main @ 17 (111 bytes)
13    4             Probe::af (4 bytes)
13    5 %           Probe::main @ 17 (111 bytes)   made not entrant: uncommon trap
13    6             Probe::main (111 bytes)
14    7             Probe::af2 (4 bytes)
15    8 %           Probe::main @ 46 (111 bytes)
15    8 %           Probe::main @ 46 (111 bytes)   made not entrant: uncommon trap
```

With default tiers, same driver:

```
11    8       3       Probe::af (4 bytes)
11    9       4       Probe::af (4 bytes)
11    8       3       Probe::af (4 bytes)   made not entrant: not used
13   10 %     3       Probe::main @ 17 (111 bytes)
13   11       3       Probe::main (111 bytes)
13   12 %     4       Probe::main @ 46 (111 bytes)
```

Read literally: the probed method goes 3 (C1, profiled) then 4 (C2),
and the C1 version is retired `made not entrant: not used`. The two
`made not entrant: uncommon trap` lines in the C2-only log are a deopt
observed in the log itself — on the driver loop, **not** on either
probed method.

## the arch-unit — the addition

104 bytes recovered, one contiguous run. objdump's reading, first 12
instructions:

```
7f99346aa400:	48 81 ec 18 00 00 00 	sub    $0x18,%rsp
7f99346aa407:	48 89 6c 24 10       	mov    %rbp,0x10(%rsp)
7f99346aa40c:	41 81 7f 20 00 00 00 	cmpl   $0x0,0x20(%r15)
7f99346aa413:	00
7f99346aa414:	0f 85 29 00 00 00    	jne    0x7f99346aa443
7f99346aa41a:	8d 04 16             	lea    (%rsi,%rdx,1),%eax
7f99346aa41d:	48 83 c4 10          	add    $0x10,%rsp
7f99346aa421:	5d                   	pop    %rbp
7f99346aa422:	49 3b 67 28          	cmp    0x28(%r15),%rsp
7f99346aa426:	0f 87 01 00 00 00    	ja     0x7f99346aa42d
7f99346aa42c:	c3                   	ret
7f99346aa42d:	49 ba 22 a4 6a 34 99 	movabs $0x7f99346aa422,%r10
```

The computation itself is **one instruction**: `lea (%rsi,%rdx,1),%eax`.
The JVM's own comment lines say `parm0: rsi` and `parm1: rdx`; the
result lands in `%eax`. Everything else is frame setup, the entry
barrier, the return poll, and the standing stubs.

Note for anyone reaching for the canonical runnable form: the JVM's
calling registers are **not** the C ones (parm0 is `%rsi`, not `%rdi`;
`%r15` holds the thread). No normalisation was done here.

## the division case — guard or implicit trap?

**An explicit guard, not an implicit hardware trap.** The check sits in
the instruction stream before the divide. objdump's reading of the
relevant stretch:

```
7f99346a9b1a:	44 8b da             	mov    %edx,%r11d
7f99346a9b1d:	85 d2                	test   %edx,%edx
7f99346a9b1f:	74 25                	je     0x7f99346a9b46
7f99346a9b21:	8b c6                	mov    %esi,%eax
7f99346a9b23:	3d 00 00 00 80       	cmp    $0x80000000,%eax
7f99346a9b28:	75 08                	jne    0x7f99346a9b32
7f99346a9b2a:	33 d2                	xor    %edx,%edx
7f99346a9b2c:	41 83 fb ff          	cmp    $0xffffffff,%r11d
7f99346a9b30:	74 04                	je     0x7f99346a9b36
7f99346a9b32:	99                   	cltd
7f99346a9b33:	41 f7 fb             	idiv   %r11d
```

and the branch target of that first `je`:

```
7f99346a9b46:	8b ee                	mov    %esi,%ebp
7f99346a9b48:	be 7e ff ff ff       	mov    $0xffffff7e,%esi
7f99346a9b4d:	66 90                	xchg   %ax,%ax
7f99346a9b4f:	e8 8c 3d ff ff       	call   0x7f993469d8e0
```

The JVM's own annotation on that call site and the instruction after
it, pasted from the dump:

```
  0x00007f99346a9b4c: ;   {runtime_call UncommonTrapBlob}
  0x00007f99346a9b50: ; ImmutableOopMap {}
                      ;*idiv {reexecute=0 rethrow=0 return_oop=0}
                      ; - Probe::af2@2 (line 6)
```

So: the divisor is tested against itself, and equal-to-zero branches to
a block that loads a trap-request constant into `%esi` and calls the
blob the JVM itself names `UncommonTrapBlob`, with a scope annotation
naming the exact bytecode index it re-enters at (`Probe::af2@2`). The
two evidence classes agree — objdump found a branch, and the JVM
labelled the branch's target.

The second guard is different in kind: `cmp $0x80000000` on the
dividend and `cmp $0xffffffff` on the divisor, clearing the quotient
register and skipping the divide when both match. That is the overflow
case the hardware divide would fault on, and it is handled **in place**
— no deopt, no exit from the compiled code.

## the modes recorded

Both units carry the standing modes; only the division carries the
trap.

| unit | mode | response kind |
|---|---|---|
| both | nmethod-entry barrier (`cmpl $0x0,0x20(%r15)` / `jne` to `Stub::method_entry_barrier`) | call-out-and-return |
| both | return safepoint poll (`cmp 0x28(%r15),%rsp` / `ja`, annotated `{poll_return}`) | call-out-and-return |
| both | exception handler and deoptimization stubs at the tail (`{runtime_call ExceptionBlob}`, `{runtime_call DeoptimizationBlob}`) | **deopt-continue-elsewhere** |
| division only | zero-divisor check into `{runtime_call UncommonTrapBlob}` | **deopt-continue-elsewhere** |
| division only | most-negative-over-minus-one check | branch-around-in-place |

`deopt-continue-elsewhere` is the vocabulary entry SUPPORT_scaling_design
reserved for exactly this. It is now used against measured dumps.

**Marked unverified:** the divisor was never zero in any run here, so
the trap path was read off the instruction stream and never executed.
Nothing here measures what the deopt actually does at run time.

## the warm-up recipe — the deliverable the owner asked for

Configuration `-XX:-TieredCompilation`, static calls with two int
arguments, three repetitions per point:

| calls | addition compiled by C2 | division compiled by C2 |
|---|---|---|
| 5000 | 0 of 3 | 0 of 3 |
| 6000 | 0 of 3 | 0 of 3 |
| 7000 | 3 of 3 | 2 of 3 |
| 8000 and up | 3 of 3 | 3 of 3 |

So the recipe is: **at least 7000 calls with the (int,int) pair, tiering
off, and `dontinline` on the probed method.** 8000 buys the division
case too.

**A discrepancy, recorded rather than explained away.** The VM reports
`intx CompileThreshold = 10000 {pd product} {default}` about itself, but
the observed boundary is between 6000 and 7000. The two do not agree.
No experiment in this pilot explains the gap; the mechanism is
**unverified**.

With tiering left on, for contrast: tier 3 (C1, profiled) by 500 calls,
tier 4 (C2) by 5000 calls but not by 2000 — which does match the
reported `Tier3InvocationThreshold = 200` and
`Tier4InvocationThreshold = 5000`.

The dump run also printed each method's own counters at exit, for a
driver of 200000 calls:

```
static Probe::af(II)I
  interpreter_invocation_count:        6784
  invocation_counter:                  6784
  backedge_counter:                       0
  decompile_count:                        0
```

They stop at 6784 because calls made from compiled code do not
increment the interpreter counter. That this number sits near the
observed 6000–7000 boundary is consistent with it; it is **not** proof
of the threshold and is not offered as one.

## the cost answer — the owner's instinct, tested

SUPPORT_scaling_design records the instinct as unconfirmed: "JVM likely
the heavier lift (hsdis plugin build, warm-up ceremony)."

**Refuted, on these numbers.**

| track | total lane wall time |
|---|---|
| CPython pilot | about 106 s |
| JVM pilot | about **5.6 s** |

Nothing had to be built. The JDK was installed; the probe compiled in
well under a second; a fully warmed run of 200000 calls through both
methods costs about **26 ms** end to end (five timed reps: 0.028, 0.026,
0.025, 0.025, 0.026 s). CPython had to build the interpreter three
times.

What the instinct got right: the **ceremony** is real — a warm-up
count, a tier choice, a `dontinline`, and a missing disassembler. It is
just cheap in seconds, and the one thing that genuinely refused (hsdis)
was routed around at no cost.

**Wrong in brief, stated plainly:** the brief said `-XX:+PrintAssembly`
"requires the hsdis disassembler plugin". It does not require it to
print anything — it requires it only for mnemonics. The bytes come out
regardless, and that is what made this pilot cheap.

## the lanes

| lane | wall time | did |
|---|---|---|
| `jvm_smoke.sh` | 2.5 s | java/javac versions, the hsdis search, the binutils inventory, the probe compiling, and a first look at what PrintAssembly prints without hsdis |
| `jvm_a_dump.sh` | 1.1 s | thresholds, the coarse warm-up sweep, the tier logs, the dump — but its carver matched no byte lines and produced an empty disassembly |
| `jvm_b_carve.sh` | 0.4 s | the carver repaired, plus the full dump and disassembly |
| `jvm_c_recipe.sh` | 1.6 s | the fine warm-up sweep with three reps per point, the default-tier contrast, five timed warmed runs |

**The defect in lane A, stated because it would otherwise be
invisible.** Lane A's disassembly section came out empty while its
annotation section came out correct, which looked like a partial
success. The cause was in the pattern that reads byte lines: the JVM
prints the hex as bar-separated groups that each contain a space
(`4881 ec18 | 0000 0048`), and lane A's pattern required each group to
be an unbroken hex run. Nothing matched, so no bytes reached objdump.
Lane B takes every hex token after the colon instead.

## evidence classes on the claims

- pin, flags, byte counts, hex bytes — **artifact fact**.
- the bytecode listing, the tier log, the `{...}` annotations, the
  `parm0/parm1` comments, the reported thresholds — **the tool's own
  testimony** (javap, PrintCompilation, the JVM's dump).
- every mnemonic — **objdump's testimony** about those bytes, a
  separate tool, never merged with the JVM's voice.
- "the zero check branches to the trap" — **forced by construction**:
  the branch target is the address the JVM itself annotated
  `{runtime_call UncommonTrapBlob}`.
- the warm-up boundary — **sampled observation**, 3 reps per point on
  one machine. It refutes ("not compiled at 6000 in three tries"); it
  does not prove a threshold.
- the flag-versus-observation gap — **unexplained, marked unverified**.

## what was NOT done — marked

- No hsdis, so no JVM-native mnemonics to cross-check objdump against.
- No normalisation to the canonical runnable form. The JVM's parameter
  registers differ from the C convention and were left as found.
- No matching against the compiled-language units, no bridge, no
  dominance claim.
- No second type pair. The recorded unit is int32 by int32 only —
  which is exactly the point of the warm-up recipe.
- The deopt path was never executed, only read.
- Scope: amd64, one JDK, one vendor build, one architecture.

## guard

`check_no_spelling_keys.py interp_jvm.json` ->
`PASS interp_jvm.json -- no operator token in any key, grouping,
pairing or row structure` (exit 0).
