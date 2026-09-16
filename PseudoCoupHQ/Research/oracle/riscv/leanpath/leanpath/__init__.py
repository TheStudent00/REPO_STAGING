"""leanpath -- the Lean proof path for RISC-V, as the plan names it.

Node: hq.research.lean_proof_path_resistant_to_churn
(Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/;
started over 2026-09-14 at the owner's order, log 280). One class per
`code (class)` sub-node, one method per `code (method)` leaf, under the
plan's own names (plan_and_code.md section 1). Written top-down, logic
last (section 2): a method carries logic only where it can be reviewed
by running it; every other method is its signature, its docstring (the
leaf's definition), and a named refusal saying what it awaits.

What the objects are, one sentence each, in relation:
  * `SailModel` is the ratified Sail RISC-V model at one commit, read by
    the sail compiler's Lean backend; its `definitions` are one
    `ArchOpcode` per `execute` clause of the emitted Lean.
  * `ArchOpcode` is one machine instruction keyed by (mnemonic, operand
    form, width), with its definition as a `LeanExpr` taken from the
    model.
  * `LeanExpr` is an expression in Lean over unknowns of fixed width; the
    one question of any two is `equals`.
  * `ArchUnit` is one compiled body cut out at its symbol, with its
    `meaning` computed by Sail's own decoder and `execute`, composed in
    Lean.
  * `Language` is one language with its compiler at ship flags, its
    corpus of units, and the swap table `operator_for` that pass A fills.
  * `Emulation` is one proved answer: an arch-opcode, a language, the
    unit, the Lean theorem file.
  * `Dictionary` is the table keyed by (language, arch-opcode) of proved
    emulations, regenerable by running `System`.
  * `System` is the three passes, in one `run`.

State as of 2026-09-14 (task lp1, second launch; log 276): the emitted
model does not build under the toolchain and library it pins (sail
5745ea9e's Lean backend prints a Sail type-level function application,
`is_sv32_mode(k_v)`, that Lean 4 cannot parse; log 276 section 4). So
the only logic here is the part that needs no built model:
`SailModel.definitions` and `SailModel.key_of`, which LIST the execute
clauses and read their keys from the emitted text. Every method that
composes, unfolds or proves in Lean refuses with `AWAITS_BUILT_MODEL`.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

How this module obeys it: a key is (mnemonic, operand form, width) read
from the model's own assembly clause and `instruction` inductive; the
mnemonic sits in the field `mnem`, the guard's exempt machine-form
field; nothing here branches on a mnemonic, and no method is keyed by
an opcode's name. the owner's test, 2026-09-13: `written once` (this module;
it names no opcode, compiler or language version) against `never
written` (anything per opcode, per compiler, per release).
"""

from .sail_model import SailModel
from .arch_opcode import ArchOpcode
from .lean_expr import LeanExpr
from .arch_unit import ArchUnit
from .emulation import Emulation
from .dictionary import Dictionary

AWAITS_BUILT_MODEL = "AWAITS_BUILT_MODEL"

__all__ = [
    "SailModel", "ArchOpcode", "LeanExpr", "ArchUnit", "Language",
    "Emulation", "Dictionary", "System", "AWAITS_BUILT_MODEL",
]
