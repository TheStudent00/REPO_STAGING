"""ts_to_ur — maps tree-sitter parses into ur. Per-language DATA,
one universal mapper.

Plan node: pcv5.tools.ledgerer.ts_to_ur
    PRIVATE/PseudoCoup_v5/Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_2_ts_to_ur/CORE_0_0_0_2_ts_to_ur.md
Shape pass 2026-08-11; logic pass 2026-08-12.

The design's spine (all ruled, see the CORE's design section):
- one named tree-sitter node -> one ur.Node; anonymous tokens are
  NEVER materialized — the pack's grammar-authored tables rebuild
  them, and instance-varying tokens land on `TsOrigin.variant`.
- the token tables' AUTHOR is the pinned grammar source (closed
  enumeration, complete by construction); the corpus census is
  frequency/oracle material only. judges: the reconstruction oracle
  (faithful convergence), then compile-as-oracle (logs 018/019).
- this module is the single owner of parser construction (the v0
  parse.py pattern): nothing else constructs a parser.

Open edges carried, by log_017 number (documented, not guessed):
q1 kind-map ratification (unknown ts_kind -> Refused, by name),
q3 macros (mark_opaque owns only the opaque node; injected
sub-addresses unpicked), q4 residual ERROR handling (mirror-the-pin
ruled 2026-08-12; ERROR still refuses here), q6 pack file layout.
"""

from dataclasses import dataclass, field
from typing import Any, Optional

import ur


class Refused(Exception):
    """Mapping refused, with the reason named. Same doctrine as
    ledger.Refused, declared separately so the mapper never imports
    the store (this node produces UR; ur_to_ledger derives)."""


# --------------------------------------------------------- language pack
@dataclass
class LanguagePack:
    """Per-language DATA, no per-language code: adding language two
    means writing a pack, not code.

    Plan node: pcv5.tools.ledgerer.ts_to_ur `language_pack`
    (realize: false; designed in the CORE). All tables are
    grammar-authored (ruled 2026-08-11): derived from the pinned
    grammar source's closed enumeration, never from a corpus."""
    language: str                       # e.g. "rust"
    grammar_version: str                # e.g. "0.24.2" — the pin of record
    kind_map: dict[str, str] = field(default_factory=dict)
    #   ts_kind -> ur_kind (rust: 163 rows; ratification is log_017 q1)
    stencils: dict[str, tuple] = field(default_factory=dict)
    #   named kind -> its fixed anonymous-token pattern, from the
    #   grammar rule that admits it (e.g. field_declaration: name ':' type)
    variant_roles: dict[str, str] = field(default_factory=dict)
    #   kind -> the grammar role naming its varying token
    #   (e.g. "binary_expression" -> "operator"); kinds with variance
    #   but no role fall back to the mapper's anon scan
    queries: dict[str, str] = field(default_factory=dict)
    #   the grammar's shipped query files (injections.scm is the
    #   macro re-parse map), as text

    def check_pin(self, runtime_version: str) -> None:
        """Refuse (by name, never silently) if the runtime grammar's
        version disagrees with this pack's pin. Grammar version is
        upstream of id stability (survey addendum §1a); this is the
        runtime half of log_017 q5."""
        if runtime_version != self.grammar_version:
            raise Refused(
                f"grammar pin mismatch for {self.language!r}: pack pins "
                f"{self.grammar_version!r}, runtime is {runtime_version!r}"
            )

    def check_level(self, grammar_tokens: set, reference_tokens: set) -> set:
        """The staleness check (ruled in 2026-08-12; log_018): is the
        pinned grammar level with the LANGUAGE, not merely the version
        we recorded? `reference_tokens` is an independent authority's
        alphabet (for rust: rustc's post-glue TokenKind list, and the
        reference's keyword list) minus its known purpose-explained
        divergences. Answers the set of tokens the reference knows and
        the grammar lacks — empty means level; non-empty is the pin
        falling behind (the `safe` finding), reported rather than
        refused, since stale != wrong for already-parseable source.
        NAME provisional (the owner's to change)."""
        return reference_tokens - grammar_tokens


# --------------------------------------------------------------- mapper
class Mapper:
    """Walks one tree-sitter parse, mints ur.Node per named node.

    Plan node: pcv5.tools.ledgerer.ts_to_ur `mapper` (realize:
    false; designed in the CORE). Holds the pack it reads and the
    sequencer that assigns ids — the mapper mints ids, ur defines
    them, the ledger is their reference frame. `sequencer` is any
    object answering `mint() -> ur.Id` (the builder's, when the
    builder exists; tests supply a minimal one)."""

    def __init__(self, language_pack: LanguagePack, sequencer: Any):
        self.language_pack = language_pack
        self.sequencer = sequencer

    def map_file(self, path: str, source: bytes, ts_tree: Any) -> "ur.Tree":
        """One parsed file -> one ur.Tree. Takes the tree-sitter tree
        rather than parsing here so the single-owner rule stays with
        the parser frontend; `source` is read for leaf text and then
        DISCARDED — nothing retains it (no-source-copy, 2026-08-07).
        Sets TsOrigin.path on the root node. Refuses BEFORE minting
        if the parse contains ERROR nodes — the pin message must win
        over any downstream unknown-kind refusal, so the scan comes
        first."""
        errors = _error_spans(ts_tree.root_node)
        if errors:
            raise Refused(
                f"{len(errors)} ERROR node(s) in {path!r} at byte spans "
                f"{errors[:5]}: source does not fit the pinned grammar "
                f"({self.language_pack.language} "
                f"{self.language_pack.grammar_version}) — likely newer "
                f"syntax; the ruled response is a pin bump (2026-08-12)"
            )
        root = self._map_node(ts_tree.root_node, source)
        root.origin.path = path
        return ur.Tree(
            language=self.language_pack.language,
            grammar_version=self.language_pack.grammar_version,
            root=root,
        )

    def _map_node(self, ts_node: Any, source: bytes) -> "ur.Node":
        """Depth-first: mint this named node, then its named
        sub-nodes in tree order — so a walk of the result and the
        minting sequence agree. Anonymous sub-tokens are consumed
        (variant reading) and never materialized. token_tree routes
        to mark_opaque (the opacity rule)."""
        if ts_node.type == "token_tree":
            return self.mark_opaque(ts_node, source)
        node = self.mint_node(ts_node, source)
        for sub in ts_node.children:
            if sub.is_named:
                node.sub_nodes.append(self._map_node(sub, source))
        # the grammar's role names, filled AFTER sub-minting so roles
        # reference ur nodes, not tree-sitter ones. A role held by an
        # anonymous token (e.g. operator) is already on `variant`.
        # keyed by (span, kind), NOT object identity: py-tree-sitter
        # answers a fresh wrapper object on every access, so id()
        # never matches across two reads of the same node.
        origin = node.origin
        named_subs = [c for c in ts_node.children if c.is_named]
        by_key = {(ts.start_byte, ts.end_byte, ts.type): mapped
                  for ts, mapped in zip(named_subs, node.sub_nodes)}
        for role in _roles_of(ts_node):
            holder = ts_node.child_by_field_name(role)
            if holder is not None and holder.is_named:
                key = (holder.start_byte, holder.end_byte, holder.type)
                if key in by_key:
                    origin.fields[role] = by_key[key]
        return node

    def mint_node(self, ts_node: Any, source: bytes) -> "ur.Node":
        """One named tree-sitter node -> one ur.Node. Unknown ts_kind
        -> Refused by name (q1 pending; ERROR lands here too, which
        under the mirror-the-pin ruling reads as: this source is
        newer than the pin). Content leaves (named, no named
        sub-nodes) carry their text; all other text is the pack's
        tables' to rebuild."""
        kind = ts_node.type
        ur_kind = self.language_pack.kind_map.get(kind)
        if ur_kind is None:
            raise Refused(
                f"ts_kind {kind!r} has no row in the "
                f"{self.language_pack.language!r} kind map (q1 unratified)"
            )
        is_content_leaf = not any(c.is_named for c in ts_node.children)
        origin = ur.TsOrigin(
            ts_kind=kind,
            named=True,
            fields={},
            span=(ts_node.start_byte, ts_node.end_byte,
                  tuple(ts_node.start_point), tuple(ts_node.end_point)),
            language=self.language_pack.language,
            text=(source[ts_node.start_byte:ts_node.end_byte].decode(
                "utf-8", "replace") if is_content_leaf else None),
            variant=self.read_variant(ts_node, source),
        )
        return ur.Node(id=self.sequencer.mint(), ur_kind=ur_kind,
                       origin=origin)

    def read_variant(self, ts_node: Any, source: bytes) -> Optional[str]:
        """The varying token(s) of a variant-bearing kind, read from
        the parse at mint time, never inferred. By the grammar's role
        name where the pack names one (verified 2026-08-11:
        tree-sitter's `child_by_field_name` — their name — answers
        anonymous tokens); else the anonymous sub-tokens that the
        kind's stencil does not already fix, joined in order."""
        pack = self.language_pack
        role = pack.variant_roles.get(ts_node.type)
        if role is not None:
            holder = ts_node.child_by_field_name(role)
            if holder is not None and not holder.is_named:
                return source[holder.start_byte:holder.end_byte].decode(
                    "utf-8", "replace")
        if ts_node.type in pack.stencils:
            return None                      # fixed pattern; nothing varies
        anon = [source[c.start_byte:c.end_byte].decode("utf-8", "replace")
                for c in ts_node.children if not c.is_named]
        return " ".join(anon) if anon else None

    def mark_opaque(self, ts_node: Any, source: bytes) -> "ur.Node":
        """The opacity rule executed: a token_tree becomes ONE node
        marked opaque — never silently empty. Its full text is kept
        (a token_tree's interior is content the stencils cannot
        rebuild — macro arguments are not grammar). Injected
        re-parses (q3, open) will hang beneath it later,
        sub-addressed and marked injected."""
        kind = ts_node.type
        ur_kind = self.language_pack.kind_map.get(kind)
        if ur_kind is None:
            raise Refused(
                f"ts_kind {kind!r} has no row in the "
                f"{self.language_pack.language!r} kind map (q1 unratified)"
            )
        origin = ur.TsOrigin(
            ts_kind=kind, named=True, fields={},
            span=(ts_node.start_byte, ts_node.end_byte,
                  tuple(ts_node.start_point), tuple(ts_node.end_point)),
            language=self.language_pack.language,
            text=source[ts_node.start_byte:ts_node.end_byte].decode(
                "utf-8", "replace"),
        )
        node = ur.Node(id=self.sequencer.mint(), ur_kind=ur_kind,
                       origin=origin)
        node.semantic["opaque"] = True
        return node


def _error_spans(ts_root: Any) -> list:
    """(start_byte, end_byte) of every ERROR node beneath the root,
    in tree order. Zero-cost when the parse is clean."""
    spans, stack = [], [ts_root]
    while stack:
        n = stack.pop()
        if n.type == "ERROR":
            spans.append((n.start_byte, n.end_byte))
        stack.extend(reversed(n.children))
    return spans


def _roles_of(ts_node: Any):
    """The grammar role names this node actually uses, discovered
    from the node itself (tree-sitter exposes per-sub-node field
    names; collecting them beats holding a static role table the
    grammar already carries)."""
    roles = []
    for i in range(ts_node.child_count):
        name = ts_node.field_name_for_child(i)
        if name is not None and name not in roles:
            roles.append(name)
    return roles
