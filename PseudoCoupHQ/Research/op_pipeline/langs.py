#!/usr/bin/env python3
"""langs.py -- ONE source of truth for which languages are in scope,
at each of the two rings this line uses.

FINDING 1 (log_082 PART 2): downstream stages each hardcoded their own
`LANGS = ["c", "cpp", "go", "rust", "swift"]`, so java (already once
in the tables, 2026-08-26) silently fell out of every table built
since 2026-08-29 -- the hardcode never changed even though java was
added upstream.  This module exists so a language enters or leaves
every consumer by ONE edit here.

TWO RINGS, not one flat list, because the pipeline stages genuinely
split this way already (`sem_anchored.py`'s own `ABI` dict, read
2026-08-31, already carries ten languages -- java and cpython
included -- while every downstream canon/dom_ops/table driver still
reads its own five-language literal):

- LANGS_COMPILED -- the five-language line this pipeline was built
  and proved against first: compile-twice (anchor/ship), the full
  canonical-form and gate machinery.  Unchanged by this file.
- LANGS_INTERP -- the parallel branch: interpreter/JIT handler
  slices, weaker provenance (recorded per-unit, never silently
  dropped -- see `add_java.json`'s `provenance_is_weaker`).  Grows as
  pilots are folded (java, cpython here; ruby and php feed dispatch-
  only evidence and do NOT enter this list -- see FOLD NOTE below).
- LANGS_ALL -- the union, in a fixed order, for any stage that wants
  every language without caring which ring a unit came from.

FOLD NOTE, so the two folds this task adds are not mistaken for a
promotion: `fold_interp_ruby.py` / `fold_interp_php.py` write
`interp_ruby.md/.json` and `interp_php.md/.json` in the SAME shape as
the java/cpython pilots, but neither produced an arch-unit (no
handler slice was extracted -- see each file's own "what was NOT
done").  A language enters `LANGS_INTERP` only once it has reached
the arch-unit stage; ruby and php are not added here for that reason,
named rather than silently omitted.
"""

LANGS_COMPILED = ["c", "cpp", "go", "rust", "swift"]

LANGS_INTERP = ["java", "cpython"]

LANGS_ALL = LANGS_COMPILED + LANGS_INTERP
