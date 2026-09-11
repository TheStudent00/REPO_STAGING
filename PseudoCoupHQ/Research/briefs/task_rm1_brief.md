# Task rm1 — rewrite rules mined from emulator arch-units: which segments of an emulation's compiled body equal one of the language's own arch-units, proved, and what the compiler left on the table

Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, ALL of it (the
layout: real paths on the laptop, flat on the tower; waits in short
calls). Then `Research/GLOSSARY.md` (backstop, emulator arch-unit,
segment, live interface, rewrite rule), `log_257` (t2: the compiler
collapsed 0 of 14 constructions), `log_255` (ap6: 31% of tier-1
emulations LANDED on their own opcode; the rest did not), the bank
(`certificates.jsonl`: source, compiler, flags, verdict, `code_version`
— and the carved body per certificate where the bank holds it, else
re-carve from the source), the pool and the canon stores (every
arch-unit of c cpp rust go swift with its term text), `Term.normalize`,
`Research/oracle/hub/dictionary2.json` (terms keyed at cell, pair and
body level). Instance `rm1.conf` (copy `t3.conf`). Artifact folder:
`Research/oracle/cross_construction/emulation/rules/`; lanes under
`lanes_rm1/`. INDEPENDENT of t4: reads the bank and the stores as they
are, writes only its own folder.

## 1. What this is, in the owner's words (2026-09-11)
"the generation of emulated arch opcodes using high level operators
gets lowered to arch opcodes, which qualifies as an arch-unit (emulator
arch-unit). we know those emulator arch-units can be simplified but
compilers might not be smart enough to find the path to simplifying
it down to the correct arch-opcode. analyzing an emulator arch-unit of
language_x to determine if lang_x's other arch-units can replace
segments of the emulator arch-unit."

## 2. The algorithm
```
units_x   = every arch-unit of lang_x with its term          # the canon store, M of them
index     = {}                                                # fingerprint -> [units]
for u in units_x:
    index[fingerprint(u.term)].append(u)                      # k concrete points, edge values first

for E in emulator_arch_units(lang_x):                         # every proved emulation's compiled body
    body = E.instructions                                     # N of them
    for i in range(N):
        state = fresh symbolic state
        for j in range(i, N):
            state = reference.step(state, body[j])            # walk forward once per i: O(N^2) steps in all
            live  = live_interface(body, i, j)                # reads before i, writes read after j
            t     = project(state, live)                      # the segment's term on its interface
            for u in index.get(fingerprint(t), []):           # usually 0 or 1 candidates
                if Term.normalize(t) == Term.normalize(u.term):     verdict = IDENTICAL
                else:                                                verdict = gate(t == u.term)   # z3, 3,000 ms
                if verdict in (IDENTICAL, PROVED):
                    rules.add(E, i, j, u, verdict, certificate)
```
Cost, stated: walking every segment is O(N²) reference steps per body
(the walk from i is shared by every j), fingerprinting is O(k) per
segment, and z3 is called only on fingerprint collisions — the number
of z3 calls is the number to REPORT, beside N, M and the segment count.
This is peephole superoptimization (Bansal & Aiken 2006; Souper; STOKE)
with two differences that are the claim: the candidates are the
language's OWN proved arch-units, and every rule carries a certificate.

## 3. What to measure, in this order
1. per language: emulator arch-units read (N distribution), units
   indexed (M), segments walked, fingerprint collisions, z3 calls,
   rules found (IDENTICAL / PROVED), rules per body.
2. THE COLLAPSE THE COMPILER MISSED: for every body that did NOT land on
   its own opcode (ap6, t2), whether a rule (or a chain of rules) reduces
   it to the one instruction the cell names — count, and the chain
   lengths. This is the number that says what the compiler left on the
   table.
3. the rules as a table keyed by (lang, cell, i, j, unit), with the
   segment's live interface and the certificate id; guard over it.
4. the cost line: seconds per body, peak RSS, z3 time total.
Memory bound 6g, sample 20 bodies first with peak RSS pasted, abort
`ABORT_MEMORY_RM1`; z3 3,000 ms per call, 30 s hard. Guard over every
json/jsonl; log (next free number); verifier lane; PROGRESS on the
autopoly node and the research node; sync-back; instance down. Shared
files: none; `reference.py` and `term.py` are READ. Never delete
anything under `<runs>/` or `PUBLIC/Airlock/`.
Reply with the per-language table, the collapse-missed count, the
z3-call count beside the segment count, the cost line, every flag
LITERAL.
