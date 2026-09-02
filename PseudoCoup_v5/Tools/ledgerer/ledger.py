"""ledger — the store. A deliberately dumb table, three doctrine-bearing operations.

Plan node: pcv5.tools.ledgerer.ledger
    <WORKSPACE_DIR>/PseudoCoup_v5/Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_1_ledger/CORE_0_0_0_1_ledger.md
Shape pass 2026-08-06; logic pass the same day.

The ledger defines no second vocabulary: every entry is a `ur.Node`
(connectors ride on their nodes, never rows of their own — the owner,
2026-08-06, log_016). Machinery is module-level functions taking the
table as an argument (protocol §2b, ontological independence): data
stays in the object, behaviour stays movable. This module imports
`ur` and the standard library, nothing else — parser-free, like the
vocabulary it stores.
"""

import json
from dataclasses import dataclass, field, replace

from ur import AbstractOrigin, GeneratedOrigin, Id, Node, TsOrigin

# The dump format is load-bearing data: a dump names its version, or
# re-derivation is impossible (the same rule as the id recipe and the
# toolchain version).
FORMAT_VERSION = "1"

# Which `semantic` slots each phase defines. Phase 1 is the minimal
# core; a record claiming a slot no phase defines is refused by name
# rather than stored hopefully. DATA, and the owner's to extend — a slot
# arrives when its writer does.
PHASE_SLOTS = {
    1: frozenset({"type", "fqdn"}),
}

# The honest marker. An ingestor that cannot resolve a slot writes
# this; it never omits the slot and never writes None.
UNRESOLVABLE = "unresolvable"


class Refused(Exception):
    """Admission refused, with the reason named. Loud over
    permissive: a refusal that cannot say why is a silence."""


# ----------------------------------------------------------------- table
@dataclass
class Table:
    """The static store-able value, and nothing else.

    Plan: `table`, in-file by rule (the ledger CORE's design
    section). What `dump` writes; what the round-trip reconstruction
    oracle fixes on (log_015 §2); what `Builder.ledger` holds.
    Row order IS admission order — the sequencer's order — which is
    what makes serialization deterministic for free."""
    frame: str                          # this ledger instance's frame id
    entries: list[Node] = field(default_factory=list)


def _all_nodes(table: Table):
    """Every node the table holds: each entry, plus everything
    beneath it. An entry may be a whole tree's root or a lone node;
    walking covers both, since a lone node's walk yields itself."""
    for entry in table.entries:
        yield from entry.walk()


# ------------------------------------------------------------ operations
def admit(table: Table, node: Node, phase: int = 1) -> None:
    """The gate — the one write path into a ledger.

    Plan: pcv5.tools.ledgerer.ledger.admit (code (function), rule).
    Enforces its CORE's four rules; every refusal names its cause."""
    known = PHASE_SLOTS.get(phase)
    if known is None:
        raise Refused(f"unknown phase {phase!r}: no slot set defined")

    for admitted in node.walk():
        # `unresolvable` is a value, never an omission. A slot present
        # with None is the silent emptiness the posture forbids.
        for slot, value in admitted.semantic.items():
            if value is None:
                raise Refused(
                    f"id {admitted.id}: slot {slot!r} is None — write "
                    f"{UNRESOLVABLE!r} instead; a slot is never silently empty")
            if slot not in known:
                raise Refused(
                    f"id {admitted.id}: slot {slot!r} is not defined in "
                    f"phase {phase} — its writer does not exist yet")

    # Append-only, and ids are unique by construction: a repeat means
    # the sequencer was bypassed or a frame was mixed in un-merged.
    seen = {n.id for n in _all_nodes(table)}
    for admitted in node.walk():
        if admitted.id in seen:
            raise Refused(f"id {admitted.id} already admitted — "
                          f"admission is append-only, never a rewrite")
        seen.add(admitted.id)

    # Admission order IS id order, as received from the sequencer.
    table.entries.append(node)


def index_by_id(table: Table) -> dict[Id, Node]:
    """Table -> {Id: node}. DERIVED — rebuilt, never serialized
    (the derived-not-serialized rule expressed structurally)."""
    return {node.id: node for node in _all_nodes(table)}


def index_by_fqdn(table: Table) -> dict[str, list[Id]]:
    """Table -> {fqdn: [Id, ...]} — the secondary index, for call
    sites that only know a name. Resolves THROUGH the id: the values
    are ids, and the caller goes on to index_by_id. A name may hold
    several ids (an unresolved overload, a redeclaration), so the
    value is a list in admission order, never a last-writer-wins
    single — that collapse is the defect the survey recorded against
    bare-name keying."""
    out: dict[str, list[Id]] = {}
    for node in _all_nodes(table):
        fqdn = node.semantic.get("fqdn")
        if fqdn and fqdn != UNRESOLVABLE:
            out.setdefault(fqdn, []).append(node.id)
    return out


# --------------------------------------------------------- serialization
def _plain(value):
    """Any value as its deterministic plain form: sets become sorted
    arrays, tuples become arrays, mappings keep sorted keys (json's
    sort_keys does that half). Recursive, because a semantic payload
    may nest."""
    if isinstance(value, (set, frozenset)):
        return sorted(_plain(v) for v in value)
    if isinstance(value, tuple):
        return [_plain(v) for v in value]
    if isinstance(value, list):
        return [_plain(v) for v in value]
    if isinstance(value, dict):
        return {k: _plain(v) for k, v in value.items()}
    return value


def _id_out(i: Id) -> dict:
    return {"batch": i.batch, "ordinal": i.ordinal,
            "frame": i.frame, "recipe_version": i.recipe_version}


def _id_in(d: dict) -> Id:
    return Id(batch=d["batch"], ordinal=d["ordinal"],
              frame=d["frame"], recipe_version=d["recipe_version"])


# Origin classes carry a tag so load knows which one it is reading.
# The tag is the class name: one fact, not a second vocabulary.
_ORIGINS = {c.__name__: c for c in (TsOrigin, GeneratedOrigin, AbstractOrigin)}


def _origin_out(origin):
    if origin is None:
        return None
    out = {"kind": type(origin).__name__}
    for slot, value in vars(origin).items():
        if slot == "fields" and isinstance(value, dict):
            # a role's holder is a NODE REFERENCE (ts_to_ur fills
            # these). Serialized by id — the node itself is already
            # in sub_nodes once; embedding it again would fork the
            # data. load() resolves the ids back to references.
            out[slot] = {role: _id_out(n.id)
                         for role, n in value.items() if n is not None}
        elif isinstance(value, Id):
            out[slot] = _id_out(value)
        else:
            out[slot] = _plain(value)
    return out


def _origin_in(d):
    if d is None:
        return None
    cls = _ORIGINS.get(d["kind"])
    if cls is None:
        raise Refused(f"unknown origin kind {d['kind']!r}")
    args = {k: v for k, v in d.items() if k != "kind"}
    if cls is TsOrigin:
        args["span"] = tuple(args["span"][:2]) + tuple(
            tuple(p) for p in args["span"][2:])
        # roles come back as Id values; load() re-links them to the
        # actual nodes once the whole table is in memory.
        args["fields"] = {role: _id_in(v)
                          for role, v in args.get("fields", {}).items()}
    if cls is GeneratedOrigin:
        args["producer_id"] = _id_in(args["producer_id"])
    return cls(**args)


def _node_out(node: Node) -> dict:
    return {
        "id": _id_out(node.id),
        "ur_kind": node.ur_kind,
        "semantic": _plain(node.semantic),
        "connectors": [
            {"kind": c.kind, "from_id": _id_out(c.from_id),
             "to_id": _id_out(c.to_id), "payload": _plain(c.payload),
             "provenance": c.provenance}
            for c in node.connectors],
        "origin": _origin_out(node.origin),
        "sub_nodes": [_node_out(s) for s in node.sub_nodes],
    }


def _node_in(d: dict) -> Node:
    from ur import Connector
    return Node(
        id=_id_in(d["id"]),
        ur_kind=d["ur_kind"],
        semantic=d["semantic"],
        connectors=[
            Connector(kind=c["kind"], from_id=_id_in(c["from_id"]),
                      to_id=_id_in(c["to_id"]), payload=c["payload"],
                      provenance=c["provenance"])
            for c in d["connectors"]],
        origin=_origin_in(d["origin"]),
        sub_nodes=[_node_in(s) for s in d["sub_nodes"]],
    )


def dump(table: Table) -> bytes:
    """Serialize a table to its durable form.

    Plan: pcv5.tools.ledgerer.ledger.dump (code (function), rule).
    Deterministic and byte-identical: rows in admission order, keys
    sorted, sets as sorted arrays, tuples as arrays, no timestamps in
    the payload (the wall-clock provenance stamp is data IN a row,
    never metadata OF the dump). Derived values — the indexes — are
    never written. the owner's reconstruction oracle fixes on this output,
    so nondeterminism here breaks the oracle first."""
    payload = {
        "format_version": FORMAT_VERSION,
        "frame": table.frame,
        "entries": [_node_out(e) for e in table.entries],
    }
    text = json.dumps(payload, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"))
    return text.encode("utf-8")


def load(data: bytes) -> Table:
    """Dump's format, read backwards. In-file by rule: dump's CORE
    fully determines this function — nothing here is invented.
    Refuses a payload whose format version it does not know, rather
    than guessing at a shape."""
    payload = json.loads(data.decode("utf-8"))
    seen = payload.get("format_version")
    if seen != FORMAT_VERSION:
        raise Refused(f"dump format version {seen!r} is not "
                      f"{FORMAT_VERSION!r} — refusing to guess at the shape")
    table = Table(frame=payload["frame"],
                  entries=[_node_in(e) for e in payload["entries"]])
    # second pass: re-link role holders (serialized as ids) back to
    # node references, so `Node.field` answers identically before a
    # dump and after a load.
    by_id = {n.id: n for n in _all_nodes(table)}
    for n in _all_nodes(table):
        if isinstance(n.origin, TsOrigin) and n.origin.fields:
            n.origin.fields = {
                role: by_id[i] for role, i in n.origin.fields.items()
                if i in by_id}
    return table


# ----------------------------------------------------------------- merge
def _stamp(node: Node, frame: str) -> None:
    """Re-address a node and everything beneath it into `frame`.
    Ids are re-ADDRESSED, never re-derived: batch and ordinal are
    untouched, so nothing about admission history is rewritten."""
    for n in node.walk():
        n.id = replace(n.id, frame=frame)
        n.connectors = [
            replace(c,
                    from_id=replace(c.from_id, frame=c.from_id.frame or frame),
                    to_id=replace(c.to_id, frame=c.to_id.frame or frame))
            for c in n.connectors]


def merge(tables: list[Table], frame: str) -> Table:
    """Join ledgers built by independent sequencers into one frame.

    Plan: pcv5.tools.ledgerer.ledger.merge (code (function)).
    Coordinate-frame reconciliation, not content comparison: each
    input's frame joins its rows' identity, and rows are
    re-addressed into the merged frame. The builder CALLS this; the
    mechanics live here.

    TWO THINGS THIS DOES NOT DO YET, both flagged rather than
    guessed:
      - same-source discovery (the three-layer triage) needs a
        source-file name on a row to raise its flag, and no `ur`
        form carries one today — `TsOrigin` has kind/span/language,
        `Tree` has bytes/language/grammar_version. Raised for the owner
        rather than papered over with an invented field.
      - the TRUE FORK (two frames admitted the same source, the
        fingerprints disagree, neither supersedes) is OPEN in the
        CORE, leaning refusal. Unreachable until the flag above
        exists."""
    merged = Table(frame=frame)
    for table in tables:
        for entry in table.entries:
            _stamp(entry, table.frame)
            merged.entries.append(entry)
    return merged
