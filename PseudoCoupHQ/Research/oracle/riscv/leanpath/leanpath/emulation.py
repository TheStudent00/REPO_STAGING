"""Emulation -- one proved answer: an arch-opcode, a language, the
compiled unit that computes the arch-opcode's definition, and the Lean
theorem file that proves it. Plan leaf: lean_proof_path.emulation.
Built by pass A (found) or pass B (built); never without a checked
proof.
"""


class Emulation:
    """attributes: opcode, language, unit, proof (the Lean theorem file,
    kernel-checked), found_or_built, definitions_commit."""

    def __init__(self, opcode, language, unit, proof, found_or_built, definitions_commit):
        self.opcode = opcode
        self.language = language
        self.unit = unit
        self.proof = proof
        self.found_or_built = found_or_built
        self.definitions_commit = definitions_commit
