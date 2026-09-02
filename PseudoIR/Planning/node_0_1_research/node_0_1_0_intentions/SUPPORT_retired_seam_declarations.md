---
id: pir.intentions.support.retired_seam_declarations
status: retired
---

# SUPPORT — retired: seam declarations

the previous plan held a 585-word node specifying a "seam declaration"
— the one human judgment call before slicing became mechanical. it is
NOT projected.

why: it is the only node in the previous plan whose specification was
written in the retired backend's own vocabulary. its worked example
row and its cut policy both named that backend's internal APIs, and
its acceptance criteria were the four declarations that were removed
as mis-aimed. the schema was not merely illustrated with those
examples; it was defined by them.

what survives conceptually: the idea that one declaration names the
language, the intention, the stage, the source file, the entry symbol,
the scope filter, the stand-ins, and the cut rule. rebuilding that
against LLVM / rustc-LLVM entry points is a fresh design job, not a
projection.
