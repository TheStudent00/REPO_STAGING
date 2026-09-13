# Task cov2 — the proof followed upwards: which compiler-operators, at which types, transpile faithfully through EVERY language today; and the round trip stated per operator

Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, ALL of it.
Then `Research/GLOSSARY.md`, `log_266` (cov1: the per-unit cells and
the per-(cell, target) proofs are already joined in
`Research/oracle/coverage/` — `bank_x86.json`, `bank_riscv64.json`, the
units stores `build_join.py` writes; REUSE them, no compile, no z3),
`log_270` (the progress report), the corpus manifests that name each
unit's source operator and holder pair (`probe_manifest_<lang>.json`,
`op_units_<lang>.json` under `Research/op_pipeline/` — READ; the
operator token is a DISPLAY LABEL, never a key: the spelling ban),
`Research/oracle/hub/hub2.py` and `log_25x` (Hub v2: the composed
round trip on go units into c, 290 of 590 proved). Instance
`cov1.conf` (reuse). Artifact folder `Research/oracle/coverage/`;
lanes under `lanes_cov2/`.

## 1. the owner's question, 2026-09-12, verbatim
"we have a lot of the arch-opcodes fully emulated -- meaning that we
could theoretically emulate every arch-unit from every language for
all the arch-units that only use the emulated arch-opcodes. those
arch-units originate from their respective compiler-operators. those
compiler-operators are what people use to program things in a high
level language. this proof following upwards would show us what we
can use at a high level for programming and have it transpile
faithfully through every language."

`compiler-operator`
- one source-level operator at one holder pair in one language
  (`a + b` on int32 and int32 in c; `a / b` on i64 in rust): the thing
  a person writes. Its arch-unit is the compiled body the corpus holds
  for it.
`faithful through every language`
- the operator's arch-unit is expressible (every arch-opcode it holds
  proved) on EVERY compiled target language of that architecture.
`round trip`
- x → y → x is proved for an operator when its unit is expressible in y
  and the certificate's term equals the unit's own term: the term is
  architecture- and language-neutral, so the composition closes by the
  certificates alone. Hub v2's gate over the composed body is the
  second check, run where a body exists.

```
for arch in (x86_64, riscv64):
    for x in languages_with_a_corpus(arch):
        for unit in units_of(x, arch):                       # one compiler-operator at one holder pair
            op = manifest[unit].operator, manifest[unit].holders    # display label + the types
            targets_ok = {y for y in targets(arch) if expressible(unit, y)}   # from cov1's join
            if targets_ok == all targets(arch):
                vocabulary[x].add(op)                        # usable at the high level, faithfully everywhere
            elif targets_ok:
                partial[x].add((op, targets_ok))
            else:
                blocked[x].add((op, blocking cells))
```

## 2. Report, every table with "N of M"
1. per architecture and source language: the VOCABULARY — the
   compiler-operators, grouped by operator kind and holder pair, whose
   unit is faithful on every target; "N of M operators" per language.
   Both readings (destination, strict).
2. the partial set: operators faithful on some targets, with the
   targets; and the blocked set with the blocking cells (the same
   four structural cells are expected: `cmp`, `test`, `push`,
   `movslq`; say how many operators only those block).
3. the round trip per operator in the vocabulary: the certificate ids
   on each target and, where Hub v2 has a composed body, its gate
   verdict; the count of operators with a composed-body check beside
   the count with certificates only.
4. a one-page discipline sheet per architecture: the vocabulary as a
   person would read it — "integer add, sub, and, or, xor, shifts,
   compares at 8/16/32/64; float add/sub/mul/div at 32/64; ..." — and
   the exclusions with their cause.
Guard over every json (keys are machine triples and unit ids; the
operator token rides as `operator`, a label); log (next free number);
verifier lane; PROGRESS on the autopoly node and the architecture
nodes; sync-back; instance down. Memory bound 6g, abort
`ABORT_MEMORY_COV2`. Nothing under `Research/op_pipeline/` is written.
