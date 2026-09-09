# log 157 — audit of round 11's completion logs (152–156)

Date: 2026-09-02. Auditor: the coordinating session, not a sub-agent.
Figures recomputed from `~/Programming/PseudoCoupHQ/Research/op_pipeline/`
this session; commands and outputs pasted. Renderings labelled per
protocol §5.1a.

# 1. Verdict

- All five rulings landed and the counts hold on disk. The ledger
  repair changed no verdict (30,436 proved / 642 refused, digit for
  digit), and the guard walks every canon38 file unmodified. §2.
- The pool collapsed from 5,274 to 2,247 entries, almost entirely
  through layer-3 identity once branch labels were positional (6,277
  distinct wrapped texts → 2,997). Multi-language entries rose 423 →
  632. §2.3.
- The census fell from 8,044 rows / 5,507 units to 1,719 / 1,668; the
  three predicted causes (machine stack, implicit destination, x87
  pairs) are at zero. §2.4.
- Two findings the round surfaced that are REFERENCE defects, not
  ledger defects: (a) route one's simulator computes the remainder
  with z3's `%`, which is sign-of-divisor; the machine is
  sign-of-dividend (`SRem`). I reproduced it: `7 % -3` gives
  `4294967294` (−2) under `%` and `1` under `SRem`. 415 withdrawals
  are this. (b) neither gate route models the STACK or X87 blocks, so
  5,602 units now have terms nobody can decide. §3.
- One canon38 defect the implementer reported against itself and did
  not fix: the prelude orders vector arrivals first, the ledger and
  the arrival bindings order by `arrival_families`, so `IN-i` means
  two different registers on a unit with both kinds. §3.3.
- Open calls in §4; my lean on each.

# 2. What was checked

## 2.1 canon38 outcomes and the idiv instance

LITERAL — recomputed over `canon38_wrapped_*.json`, `canon38_interp.json`,
`canon38_regen_store/*.json`:

```
canon38 {'WRAPPED_TEXT_PROVED': 30436, 'REFUSED': 642}
```

LITERAL — `canon38_wrapped_c.json`, `c/op_210`, ledger rows
(row, produced_by, operands):

```
IN-0   {"kind":"non_opcode_phrase","phrase":"arrival"}            []
IN-1   {"kind":"non_opcode_phrase","phrase":"arrival"}            []
TEMP-0 {"kind":"arch_opcode","mnem":"mov"}                        ['IN-0']
TEMP-1 {"kind":"arch_opcode","mnem":"cltd","writes_which_half":
        "the sign of the accumulator"}                            ['TEMP-0']
TEMP-2 {"kind":"arch_opcode","mnem":"idiv","writes_which_half":
        "quotient"}                                    ['TEMP-0','TEMP-1','IN-1']
TEMP-3 {... "remainder"}                               ['TEMP-0','TEMP-1','IN-1']
OUT-0  {"kind":"arch_opcode","mnem":"idiv","writes_which_half":
        "quotient"}                                               ['TEMP-2']
```

GLOSS: OUT-0 now reads the quotient half; `cltd` has a row; producers
are typed objects. Log 150 §2.2's defect is closed.

## 2.2 Positional branch labels

LITERAL — `go/op_174` vs `go/op_180` wrapped texts compared in Python:
`174==180: True`. Log 148 §4.2.2's cause B is closed.

## 2.3 the_pool3

LITERAL — `the_pool3.json` summary:

```
entries 2247   multi-language 632   compiled+interpreted 3
brief-strict 8394   distinct layer-3 texts 2997
```

LITERAL — the three largest entries (id, members, languages, distinct
wrapped texts, layer-5 text):

```
E00073 886 [c,cpp,go,rust,swift] 6  ~(~Extract(31,0,v0) | ~Extract(31,0,v1))
E00235 565 [c,cpp,rust,swift]    6  Extract(31,0,v0) << Concat(0,Extract(4,0,v1))
E00126 563 [c,cpp,go,rust,swift] 2  Extract(31,0,v0) | Extract(31,0,v1)
```

GLOSS: the largest entry is 32-bit bitwise-and (written by z3's
simplifier as a double negation of or), 886 members across five
compilers with only six distinct wrapped texts. Nothing in the top
three is an over-merge: each carries one layer-5 text.

E00029 (integer addition) is unchanged: 158 members, `v0 + v1`,
representative `go/op_319` at 35 bytes.

## 2.4 census4 and the guard

`name_census4.json`: 54 producers (log 153's figure). The producers
are now `sbb`/`adc` flag pairs, the x87 ARITHMETIC family
(`fadds`, `fmulp`, `fidivl`, …), and "the body's last write to %rax"
(303 units whose answer is a library call's return).

LITERAL — unmodified guard, my run:

```
PASS the_pool3.json / the_families3.json / name_census4.json /
     canon38_wrapped_c.json / canon38_wrapped_go.json /
     layer4c_terms_c.json  -- no operator token in any key, ...
```

No `exempt` line. `git status --porcelain | wc -l` = 0; round 11's
banking commit is `9d6235d`.

## 2.5 Airlock (log 155)

All six items done and verified on a throwaway instance `r11check`:
`down` refuses with the running lane's name and status-file path
(`--force` overrides); non-default agent tree at
`~/AirlockRuns/<name>/agent`; `doctor` lists both places; `build.sh`
ran, then `daemon_file` and both of its blocks were removed; README
paragraph added. The existing `instances/trickle/agent` tree was left
in place and pinned by an explicit `agent_dir` line so nothing moved.
Not re-run by me; the log pastes the transcripts.

# 3. The findings

## 3.1 The remainder (415 withdrawals) — reference defect, confirmed

LITERAL — `canon9_behaviour_check.py:210`, which `canon10` inherits
and `gate48.py` calls:

```
            remainder_wide = dividend % divisor_wide       # z3 SRem
```

LITERAL — my reproduction (z3-solver installed in the sandbox):

```
a%b= 4294967294  SRem= 1        # a=7, b=-3, 32 bits
```

LITERAL — `canon12_behaviour_check.py:100`:

```
                r = z3.SRem(dividend, divisor_ext)
```

GLOSS: z3py's `%` on bit-vectors is `bvsmod` (sign of the divisor).
x86 `idiv` leaves the remainder with the sign of the dividend, which
is `bvsrem`. The ledger's term uses `SRem` and is right; the reference
route is wrong at one opcode. `canon12` already has the correct model.
Fix: a new gate file that points route one at `canon12`. Log 147
§13.5's "826 of 826 spell a division opcode" is now fully explained:
410 were the quotient half (wired wrong in canon37, fixed), 415 are
the remainder half (reference wrong, open).

## 3.2 STACK and X87 have no reference — 5,602 undecided

The ledger now builds terms through push/pop and x87 rows, but neither
gate reference simulates the machine stack or the x87 stack, so
3,360 STACK-carrying and 1,405 X87-carrying units return UNDECIDED on
both routes. These are not counted as proved and are not merged on
layer 5. Work: a reference that models both — the same shape as the
ledger's own blocks.

## 3.3 IN-i ordering disagreement inside canon38

LITERAL — log 153 §9, `c/op_105` (`cvtsi2ss %edi,%xmm1; addss %xmm1,%xmm0; ret`):

```
arrival_families            ['rdi', 'xmm0', 'xmm1']
prelude_resolved            ['movdqu IN-0,%xmm0', 'movdqu IN-1,%xmm1', 'mov IN-2,%rdi']
arrival_contract_bindings   IN-0 <-> %rdi,  IN-1 <-> %xmm0,  IN-2 <-> %xmm1
```

GLOSS: the prelude loads IN-0 into `%xmm0`; the bindings and the
ledger say IN-0 is `%rdi`. Two parts of one artifact disagree about
what a row is. Layer 4 followed the ledger's wiring (and proves);
following the prelude disproves. Only units with both vector and
general arrivals are affected (count not reported — round 12 must
count it). Fix: `build_prelude` emits in `arrival_families` order.

## 3.4 The flag link cost 699 old proofs, honestly

Canon37's layer 4 kept a running "last flags" variable, so
`cmp; sbb; setl` answered `setl` from `cmp`'s flags, ignoring `sbb`
— and route two made the same substitution, so two walks agreed on
one error. Canon38 links each flag reader to the row that actually
set the flags; `sbb`/`adc` have no flag model yet, so those 699 units
went from (wrongly) proved to no-term. Correct direction; work to
return them is a flag model for `sbb`/`adc`.

# 4. Calls, with my lean

1. **`call` as a producer** (300 units; four callees `__divti3`,
   `__udivti3`, `__modti3`, `__umodti3` — 128-bit division that
   compilers outsource to a library). Lean: yes, a `call` writes the
   accumulator; producer `{"kind":"call","callee":"__divti3"}`. The
   term is then an uninterpreted function of the callee's name over
   the argument rows — honest, and two units calling the same routine
   with the same rows merge. This adds a producer kind, so it is
   yours.
2. **Route one → `canon12`** (415 units). Lean: do it; it is a
   reference correction with a reproduced counterexample. No call
   needed unless you object.
3. **A STACK/X87-aware reference** (5,602 undecided). Round 12's
   centerpiece.
4. **IN-i ordering** (§3.3). Fix, count the affected units, re-gate.
5. **`sbb`/`adc` flag model** (699 units). Round 12 work.
6. **434 lone symbolic-target units** (log 154 §13.2). Nothing wrong
   with them; no pass needed.

## CORRECTION (2026-09-03) — §4 item 1 was not a call

The `call`-as-producer question was already answered on 2026-08-15
(AgentMemory line 135, THE THREE-LAYER ANCHOR: layer 3 is "what the
COMPILER can do to a representation — the measured dynamics, never
builtins"). The 308 units that call `__divti3` / `__udivti3` /
`__modti3` / `__umodti3` are library routines and are OUT OF SCOPE;
recorded in `Research/op_pipeline/out_of_scope_library_calls.json`
(308 units: c 136, cpp 164, rust 4, swift 4). I posed as a decision
a thing already decided, because I did not check AgentMemory before
listing calls. Status: withdrawn. The next pool/proof rebuild drops
these units from its population. Earlier text above is not edited.
