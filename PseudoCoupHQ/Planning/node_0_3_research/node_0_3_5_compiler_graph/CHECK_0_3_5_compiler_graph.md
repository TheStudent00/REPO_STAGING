---
id: hq.research.compiler_graph.check
---

# CHECK — compiler_graph

- [x] static graph of a compiler region, as data, 0 parse errors — 2026-08-24
- [x] runtime evidence joined onto static ids (tally stopgap) — 2026-08-24
- [x] path query answering the acceptance question — 2026-08-24
- [x] the diary: id-emission run with visit ORDER — 2026-08-24; 56 spots, 329 events, chain order proven, agrees with the tally's counts
- [x] diary records carry WHICH function was being compiled — 2026-08-24; subject column proves the af iterations; also caught and corrected lap one's "never interleaved" claim
- [x] follow-the-dot resolution — 2026-08-24; declared-type rule closed 8,424 of 19,447 selector dead-ends; abi now CONNECTED to amd64 (24 hops)
- [x] forward-only dataflow (store/literal-to-field, field-to-read, call/return binding) — 2026-08-24; register ASSIGNMENT proven moving abi -> ssagen -> amd64, forward only, diary-corroborated with subject af
- [x] close the index chain — 2026-08-24; 36 bindings corrected + 1,100 more selectors resolved; the index travels 25 forward hops to regalloc.go:1040, where the ABI index selects the physical register
- [x] the identity-observation solution RULED: the optimizer OFF SWITCH (clang -O0 / rustc opt-level=0 / go -N -l / swiftc -Onone) — every named variable gets a memory home, operands arrive from their homes, name->home stated by the compiler's own debug table (log_073) — 2026-08-24
- [ ] the allocator's choice on the SHIP build: bracketed by anchor + forced probe; compose the diff (anchor vs ship) as the record
- [ ] second language on unchanged machinery
- [ ] probes generated from operator_arity.json, no hand-written probe
