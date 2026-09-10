"""ur — Universal Rich AST definitions. THE vocabulary of the ledgerer.

Plan node: pcv5.tools.ledgerer.ur
    PRIVATE/PseudoCoup_v5/Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_0_ur/CORE_0_0_0_0_ur.md
Generated 2026-08-06, top-down per plan_and_code §2: THIS PASS IS
SHAPE ONLY. Attributes and method signatures mirror the plan's
structural overviews; logic is written in a later pass, after the
shape is reviewed. A stub body raising NotImplementedError is a
stub on purpose, not an accident.

The module defines forms and nothing else. `ledger` instantiates
these forms and adds mechanics (keying, durability, merge); the
mappers (`ts_to_ur`, `ur_to_ledger`) fill them; the `builder`
sequences the mappers. This module imports NOTHING from any of
them, and not tree_sitter either — a TsOrigin carries tree-sitter
FACTS as plain data, so the vocabulary stays parser-free.
"""

from dataclasses import dataclass, field
from typing import Any, Optional


# ---------------------------------------------------------------- kinds
# pcv5.tools.ledgerer.ur `kinds` (code (variable), in-file by rule).
# Two tiers, RULED 2026-08-06 (coupled; see the CORE's design section
# and log_015). Append-only in spirit: buckets are superseded by
# addition, never removed. The per-language ts_kind -> ur_kind MAPS
# are ts_to_ur's data, not here — this is the destination vocabulary.
KINDS = {
    # intention tier — the 11 minimum-set objects...
    # ...plus four empirically-grounded additions RULED 2026-08-12
    # from the ecosystem basis report (PCHQ log_015; rulings in
    # PCHQ log_016 §6 walk): `import` (M1, 155 languages),
    # `try` (M2, the error-clause family, absorbs G's grammar
    # remnant), `pair` (M3, 152 languages, key-with-value),
    # `interpolation` (M9, 121 languages). Names follow the owner's
    # Python-naming rule: no universal claim -> Python's word.
    # Superseded by addition, never removal.
    "objects": (
        "value", "name", "operation", "sequence", "choice",
        "repetition", "function", "record", "collection",
        "mutation", "service call",
        "import", "try", "pair", "interpolation",
    ),
    # ...and the 10 differentiator categories A-J
    # (PRIVATE/PseudoIR/Tools/intentions/pc_intentions.json).
    "categories": {
        "A": "suspension", "B": "channels", "C": "optionals",
        "D": "pattern matching", "E": "dispatch", "F": "generics",
        "G": "scoped cleanup", "H": "events",
        "I": "operator overloading", "J": "metaprogramming",
    },
    # form tier — syntax that carries no run-time intention.
    # `proof-form` ruled 2026-08-06: the source language's proof
    # apparatus (reference_expression, lifetime, ...).
    # `container-form` RULED 2026-08-12 (basis report M4/M5:
    # body-lists 82 languages, document roots 397): position-holding
    # containers are their own form, retiring the NONE question.
    "forms": ("type-form", "declarative-form", "proof-form",
              "container-form"),
}
# Standing fact, RULED 2026-08-12 (P6, ecosystem-verified): the
# categories A/B/C/E/G/H/I are SHAPE-INVISIBLE — real intentions
# with no grammar clusters of their own anywhere in 411 grammars.
# They are ledger-resolved, never grammar-resolved: their ur_kind
# realizations arrive as duals on shape buckets, in the intention
# layer. Classification is two-layered by ruling: shape now
# (grammar evidence), intention later (resolution) — one ruling
# replacing 42 per-row DUAL tie-breaks (PCHQ log_016).


# --------------------------------------------------------------- origins
# Origin is an attachment, not baked-in fields (ruled 2026-08-05):
# a node carries only what is true of every node; origin-specific
# facts live in one of these classes, held on Node.origin.

@dataclass
class TsOrigin:
    """The tree-sitter facts, for nodes whose origin is a parse.

    For PARSED nodes the strictly-richer rule lives here: nothing
    tree-sitter knows is lost. All plain data — no tree-sitter
    objects are held, so the vocabulary never imports the parser."""
    ts_kind: str                 # grammar kind, e.g. "function_item"
    named: bool                  # named vs anonymous token
    fields: dict[str, Any]       # the grammar's role names -> sub-node(s)
    span: tuple                  # (start_byte, end_byte, start_point, end_point)
    language: str                # which grammar produced it
    # Content-bearing leaves carry their own text (identifiers,
    # literals, string/comment content — measured: 14 leaf kinds,
    # 37.6% of leaf instances). Kind-determined tokens (`;`, `fn` —
    # 62.4%) carry None: the pack's stencils know them. Ruled
    # 2026-08-07 (the owner: "definitely drop `source_bytes`") — the
    # ledger stores the FACTS the file states, never a file copy.
    text: Optional[str] = None
    # The classifier for kinds whose anonymous tokens VARY by
    # instance (binary_expression's operator, expression_statement's
    # trailing `;`, generic_type's turbofish): the varying token(s),
    # READ from the tree at mint time, never inferred. What any
    # target emitter needs to pick proper tokens (the owner, 2026-08-07).
    variant: Optional[str] = None
    # The source file, set by the mapper on each file's ROOT node at
    # least (None below it is fine). Ruled 2026-08-06 (the owner: "file
    # name is needed"): without it, merge's same-source triage has
    # no flag to raise — a double ingestion would merge SUCCESSFULLY
    # and sit in the ledger twice, unnoticed. Follows the harvested
    # record shape, which carried `file` per row.
    path: Optional[str] = None


@dataclass
class GeneratedOrigin:
    """For nodes produced by macro expansion, not by a parse."""
    producer_id: "Id"            # the invocation that generated this
    template: str                # which macro/template produced it


@dataclass
class AbstractOrigin:
    """For declared nodes with no text anywhere (the to-be wrapper)."""
    declared_by: str             # which writer declared it, and why


# ------------------------------------------------------------------- id
@dataclass(frozen=True)
class Id:
    """The identity value — the spacetime id.

    Plan node: pcv5.tools.ledgerer.ur.id (CORE_0_0_0_0_2_id.md).
    Unique by exclusion: no two admissions occupy the same cell.
    (batch, ordinal) is a two-level LOGICAL clock assigned by the
    builder's sequencer; `frame` joins only across independent
    ledger instances (merge); `recipe_version` makes the id
    re-derivable when the toolchain moves. Frozen: an identity that
    can mutate is not an identity."""
    batch: int                   # admission batch (a tree's build)
    ordinal: int                 # position within the batch
    frame: Optional[str] = None  # ledger instance; None within one frame
    recipe_version: str = "1"    # the id recipe, versioned like the toolchain


# ------------------------------------------------------------- connector
@dataclass
class Connector:
    """The static graph object joining two nodes by id.

    Plan node: pcv5.tools.ledgerer.ur.connector
    (CORE_0_0_0_0_1_connector.md). Every writer that extends a
    ledger after its build writes THESE against existing ids —
    definition<->instance, instance->abstract, the meta-programming
    connectors, runtime, expansion, supersedes. Kinds are open-set
    data by design (the carrying capacity)."""
    kind: str                    # from the connector-kind vocabulary
    from_id: Id
    to_id: Id                    # a real node's id, or an abstract node's
    payload: dict[str, Any] = field(default_factory=dict)
    provenance: Optional[str] = None  # which writer, when, from what evidence


# ------------------------------------------------------------------ node
@dataclass
class Node:
    """The UR node — one shape in four layers, each layer owned by a
    different writer, none replacing the one beneath it.

    Plan node: pcv5.tools.ledgerer.ur.node (CORE_0_0_0_0_0_node.md).
    universal:  id, ur_kind, sub_nodes, semantic, connectors
    origin:     TsOrigin | GeneratedOrigin | AbstractOrigin
    Writers: ts_to_ur writes id/ur_kind/origin/sub_nodes at mapping
    time; ur_to_ledger fills semantic and connectors; late writers
    (tracer, expansion pass) extend connectors against existing ids.

    Opacity rule: a token_tree becomes ONE node marked opaque
    (ur_kind stays honest, never silently empty); re-parsed content
    hangs beneath it with sub-addressed ids, marked injected."""
    id: Id
    ur_kind: str                          # from KINDS; the dominant object
    sub_nodes: list["Node"] = field(default_factory=list)
    semantic: dict[str, Any] = field(default_factory=dict)
    connectors: list[Connector] = field(default_factory=list)
    origin: TsOrigin | GeneratedOrigin | AbstractOrigin | None = None

    def text(self) -> Optional[str]:
        """The node's own stored content text, if it carries any.
        Content leaves (identifiers, literals, string content)
        answer; structural nodes and kind-determined tokens answer
        None — their text is the pack's to rebuild at unparse.
        There is no source copy to slice (ruled 2026-08-07):
        unparse is faithful CONVERGENCE, not reproduction — the
        first pass normalizes, every later pass is a fixed point."""
        if not isinstance(self.origin, TsOrigin):
            return None
        return self.origin.text

    def field(self, role: str) -> Optional["Node"]:
        """The sub-node playing the grammar's named role (`name`,
        `body`, ...), read from the origin's fields — ask by role,
        never by position. A role the grammar allows to repeat
        (e.g. several `parameter`s) answers with its FIRST holder;
        the full list stays readable on origin.fields directly."""
        if not isinstance(self.origin, TsOrigin):
            return None
        held = self.origin.fields.get(role)
        if held is None:
            return None
        if isinstance(held, list):
            return held[0] if held else None
        return held

    def walk(self):
        """Yield this node then every node beneath it, depth-first
        in address order — the same order the ids were minted in,
        so a walk and an admission sequence agree."""
        yield self
        for sub in self.sub_nodes:
            yield from sub.walk()


# ------------------------------------------------------------------ tree
@dataclass
class Tree:
    """The per-file container (in-file class by rule; serialization
    RULED 2026-08-06: in-memory only, rebuilt by re-parsing — the
    ledger is the durable store, so this class grows no format).

    Holds NO source copy (ruled 2026-08-07): content lives on the
    nodes (`TsOrigin.text`), form tokens live in the pack's
    stencils, whitespace is nobody's — unparse converges on the
    pack's canonical formatting. `grammar_version` makes the pin
    checkable at runtime. `Builder.ur` is an instance."""
    language: str
    grammar_version: str         # e.g. "0.24.2" — checked against the pin
    root: Optional[Node] = None
