"""ArchOpcode -- one machine instruction the compiler can write, keyed by
mnemonic, operand form and width, with its definition as a Lean
expression taken from the model. Plan leaf: lean_proof_path.arch_opcode.

The identity of a cell is its key and its definition; the mnemonic is
the display label the spelling ban allows, in the field `mnem` the guard
exempts as machine form. Built by SailModel.definitions, never by hand.
"""


class ArchOpcode:
    """attributes: key (mnem, operand_form, width), definition (LeanExpr
    or a named refusal), source_clause (the emitted clause's name, for
    the audit trail)."""

    def __init__(self, key, definition, source_clause):
        self.key = key
        self.definition = definition
        self.source_clause = source_clause

    def as_row(self):
        return {"mnem": self.key["mnem"],
                "operand_form": self.key["operand_form"],
                "width": self.key["width"],
                "from_clause": self.source_clause,
                "definition": self.definition}
