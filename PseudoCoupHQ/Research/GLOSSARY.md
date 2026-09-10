# Glossary of the arch-opcode emulation line (the owner's form: name, what it is, how it is built)

Every word below is load-bearing. A reply to the owner that uses one of them
defines it in place, in this form, before it carries weight. Keep this
file and the replies consistent; add here when a new name is coined.

`arch_opcode`
- one machine instruction the compiler can write, keyed by three things:
  its mnemonic (the name, `add`), its operand form (what it reads: two
  registers, a register and a constant, memory, ...), its width (how
  many bits it works on: 8, 16, 32, 64, 128).
- built: put every arch-unit of every language in one file, list every
  instruction line, keep those three fields, reduce to one instance per
  triple.

`cell`
- one `arch_opcode` as a row of the model table. The table is mnemonics
  down, (form, width) across; one box of that grid is one cell.
- built: the reduction above. 253 cells are attested (some unit uses
  them); 205 of them have units in all four compiled languages and are
  the population the three readings count over.

`arch_unit`
- the machine code the compiler produced for one source operator at
  one type pair: the body of `a + b` for (int32, int32), cut out of the
  binary at its function symbol.

`singleton`
- an `arch_unit` whose body is one instruction and a return. The
  opcode's mapping is visible alone.

`reference simulator`, `level 0`
- `reference.py`: for every `arch_opcode`, its mapping written as a z3
  function from input bit-vectors to output bit-vectors. Everything
  rests on it, so it is level 0.
- `level 0 check`: the reference compared against a formal model of the
  ISA written by others (x86: the K-framework semantics; RISC-V: the
  Sail model). A disagreement is a defect in the reference.

`term`
- the meaning of a body or an opcode as one formula: for every output
  bit, a formula over the input bits.
- built: give the inputs unknown bit-vector values, apply each
  instruction's mapping in order, read the outputs. Two things with
  equal terms compute the same function.

`lifter`
- the piece that walks an instruction list through the reference and
  returns its `term`. `reference.py` for x86, `riscv_reference.py` for
  RISC-V.

`carve`
- cutting the compiled function's body out of the binary at its symbol:
  the instruction list from entry to return.

`Term.normalize`
- rewriting a term to a canonical text, so two equal terms print the
  same. "identical after normalize" means same text; if the texts
  differ, z3 decides equality.

`emulation`, `find_emulation(cell, lang)`
- a piece of source in `lang` which, compiled at ship flags, computes
  the cell's term.
- built: print the term in the language's own operators (tier 1); if the
  language has no operator at that width or kind, build one from `& | ^ ~`,
  a conditional and variables at the language's widest word (tier 2);
  compile; carve; prove the body's term equals the cell's term.

`tier 1`, `tier 2`, `schema`
- tier 1: the emulation is the term printed in the language.
- tier 2: the emulation is a construction from primitives. A `schema`
  is one construction pattern general in (width, word), for instance
  add-with-carry at width w from words of size k, proved once in Lean
  for all w and k, then instantiated per cell.

`gate`
- the z3 question "body term == cell term?" with a budget of 3,000 ms,
  asked per output. Answers: equal (proved), differ (a counterexample
  is shown), undecided (the budget ran out).

`certificate`, `bank`
- a certificate: one emulation with its cell, language, source,
  compiler and flags, verdict, and the version of the code that made
  it. The bank is the file of all certificates (24,758 after t2).
- a banked cell is never re-proved unless the code version changed; a
  5% sample is re-run each pass as an audit, and any differing verdict
  is an alarm.

`readings` (three, always reported together)
- strict: a cell counts when every written place of its emulation is
  proved, flags included.
- destination-only: the cell counts when the destination register's
  value is proved; flags not required.
- corpus-needed: the cell counts when the places some arch-unit in the
  corpus actually goes on to read are proved.

`attestation`
- which corpus units contain a cell. A cell is attested if at least
  one unit contains it. This is the evidence that the cell occurs in
  real compiled code.

`guard`
- `check_no_spelling_keys.py`: refuses any json whose rows are keyed by
  a spelling (a source token like `+`, or a mnemonic alone) instead of
  the machine triple. Never modified.

`collapse`
- whether the compiler turned a source emulation back into the one
  instruction the cell names (LANDED) or left it as several (NOT
  COLLAPSED).

`the claim` (RISC-V)
- for one source unit compiled for both architectures, the x86 body's
  term equals the riscv64 body's term. Measured by z3 per unit.

`surface`
- the number of lines that had to be written to run the pipeline on a
  new architecture, counted per layer. The measure of "does solving one
  architecture solve the rest".

`the loop`
```
set_of_cells        # every (mnemonic, form, width) any compiler emitted
set_of_languages    # c cpp rust go swift, and the interpreted ones
bank                # every emulation already proved or refused, with its verdict

for cell in set_of_cells:
    for lang in set_of_languages:
        if bank.has(cell, lang) and code_unchanged(cell, lang):
            continue                                  # banked, never re-proved
        source = render(cell.term, lang)              # tier 1
        if source is None:                            # no operator at this width or kind
            source = construct(cell.term, lang)       # tier 2
        body = carve(compile(source, lang, ship_flags))
        verdict = gate(term_of(body) == cell.term)    # z3, per output
        bank.add(cell, lang, source, verdict)
```
