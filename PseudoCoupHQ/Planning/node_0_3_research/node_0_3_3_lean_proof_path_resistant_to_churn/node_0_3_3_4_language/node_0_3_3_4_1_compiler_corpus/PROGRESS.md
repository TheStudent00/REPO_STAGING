---
id: hq.research.lean_proof_path_resistant_to_churn.language.compiler_corpus.progress
status: living
---

# PROGRESS — compiler_corpus

- 2026-09-14: planned (status: planned). Written fresh at the owner's order of 2026-09-14 ("start over. in a different research node ... the parts that are fucked up are deleted before you start them over again"); nothing of the superseded node's `compiler_corpus` was copied.
- 2026-09-14: coded as `leanpath/compiler_corpus.py` (`python3 -m leanpath probes`): c's 750 probes written as walk units under `Research/oracle/riscv/leanpath/runs/handful_c/`; lanes l49 (every certificate failed: `Sail.Vector` in the unfold list, fixed in `strip.library_refs`) and l50 (rerun) on the tower (status: in-progress).
- 2026-09-15: the units file passes the spelling guard (the probe's label now sits on an object naming its unit and language; log 281 §4.4) (status: done for c).
- 2026-09-15: cpp, rust, go: their manifests written as units (`runs/corpus_<lang>/units.json`, holders carried, guard PASS); the cpp ship line is the one that lowered cpp on the tower on 2026-09-14 (the C++ headers come from the gcc toolchain); lane l65 submitted: the three corpora compiled, decoded, composed, certified, one language after another (status: in-progress).
- 2026-09-15: cpp, rust, go lowered for riscv64 and read through Sail (lane l65, 43 min): cpp 1,002 probes, 418 meanings certified (584 refused: 326 float probes the pruned decoder does not know, 232 the compiler refused, 15 walk shapes); rust 858, 90 certified (768 refused: 733 the compiler refused, mismatched holders, 23 float, 4 ABI reads, 8 other); go 744, 21 certified (723 refused: 40 calls into the runtime (JALR), the rest the compiler refused or shapes the walk does not read). `runs/corpus_<lang>/walk_[0-3]/walk.json` (status: done).
