"""Dictionary -- the table keyed by (language, arch-opcode) whose entries
are proved emulations: the line's bank, regenerable from the model and
the compilers by running the system. Plan leaf: lean_proof_path.dictionary.
Read by the Hub; written only by the three passes.
"""


class Dictionary:
    """attributes: entries ((Language, ArchOpcode) -> Emulation),
    definitions_commit; methods add, find, report."""

    def __init__(self, definitions_commit):
        self.entries = {}
        self.definitions_commit = definitions_commit

    def add(self, emulation):
        self.entries[(emulation.language, emulation.opcode)] = emulation

    def find(self, language, opcode):
        return self.entries.get((language, opcode))

    def report(self):
        """the table "of N" per language, three readings where they
        differ; empty until a pass has run."""
        return {"entries": len(self.entries), "definitions_commit": self.definitions_commit}
