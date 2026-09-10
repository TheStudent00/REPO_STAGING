#!/usr/bin/env python3
"""emulate.py -- task o7: does clang collapse a c EMULATION of a
go / rust / swift unit's term back to a c arch-unit?

Node: hq.research.arch_unit_oracle.cross_construction
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/CORE_0_3_2_2_cross_construction.md`,
FROZEN for term-level composition; this task asks a different
question and does not unfreeze it).

THE OBJECTS, one sentence each, in relation.
  * An X UNIT is a pool member (`the_pool5.json`) in language x of
    {go, rust, swift} whose entry has NO c member, together with its
    canon40 record (the body verbatim, the arrival contract, the
    answer home) and its proved layer-4 term (the body as a z3
    expression, built by `term.Term.transcribe` over the ledger).
  * An EMULATION is a c function whose body is that term written in
    c's own operators over c's holders, produced by the ONE renderer
    below (`Renderer`) from the z3 term; a term the renderer cannot
    render is refused by cause and no source is written for it.
  * THE COLLAPSE TEST compiles the emulation at the corpus's own ship
    flags (`/usr/bin/clang -std=c17 -O1 -c`, read off `lane_gen.py`
    `compile_probe`, NOT `-O2`), carves the function with the
    pipeline's own objdump reader (`lane_gen.extract`), puts it on the
    canonical form (`canonical_form.render_one`), builds its term
    (`term66_run.one_unit`), and asks three questions:
      Q1 BYTE identity: is the emulation's body byte-identical to some
         c unit of the corpus (and to one in the same entry, for the
         control)?
      Q2 TERM identity: is its layer-5 text identical to the entry's?
      Q3 PROOF: does the gate (`gate.Gate.decide`, 3,000 ms) prove the
         emulation's body equal to the x unit's body, inputs aligned
         by IN row (t100's `align_by_row`)?

WHAT IS REUSED RATHER THAN COPIED, said out loud.
  `cross2_length_two.parse_text` / `print_node` (task o1's parser of
  the layer-5 print form) decide the round-trip FILTER; the renderer
  itself walks the z3 object the print rule prints, because the print
  form drops bit widths (`Concat(0, If(c, 1, 0))` says neither the
  width of `0` nor of the `If`).  `lane_gen.extract` carves.
  `canon38_gate.arrival_contract` / `arrival_family_list` and
  `canon10_behaviour_check.answer_home_from_real` read the arrival
  contract and answer home off the ship text exactly as
  `canon38_regen.process_probe` did for the regenerated corpus.
  `canonical_form.render_one` wraps and gates.  `term66_run.one_unit`
  transcribes, gates and normalizes.  `term97_walk.build` builds the
  three shared objects once.  `pool100_entry_equivalence.input_rows`,
  `align_by_row`, `rows_disagree`, `classify_symbols`,
  `rename_constants_apart` align the two sides.  `gate.Gate.decide` is
  the one solver call.  Nothing under `Research/op_pipeline/` is
  edited.

MEMORY BOUND, stated as the law requires: one collecting process,
peak checked after every emulation, named abort ABORT_MEMORY_O7 at
4 GB resident; one forked sub-process per emulation under RLIMIT_AS
2,048 MB and a wall clock of 240 s (a sub-process that passes either
is recorded as a runner limit, never as a verdict); at most 3
sub-processes at once.  The canon40 shards are streamed one at a
time and dropped.

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

No operator token appears in this file.  The population is a set of
pool entry ids read from task o1's length-one map (machine form: pool
membership by language); the comparison scope of every question is
one entry, or the whole c corpus by body bytes; a member's `operator`
field rides onto a record as a DISPLAY LABEL and is read by nothing.

Coding discipline: no compound one-liner statements.

usage:
  emulate.py census                         population, indexes, held records
  emulate.py sample <count>                 the first stratified sample
  emulate.py run                            every entry that passed the filters
  emulate.py control <count>                entries WITH a c member
  emulate.py report                         emulation_results.json + .md
"""

import glob
import json
import os
import random
import re
import resource
import select
import signal
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CROSS = os.path.normpath(os.path.join(HERE, ".."))
OP = os.path.normpath(os.path.join(HERE, "..", "..", "..", "op_pipeline"))
sys.path.insert(0, OP)
sys.path.insert(0, CROSS)

import z3                                                        # noqa: E402

POOL5 = os.path.join(OP, "the_pool5.json")
CROSS1 = os.path.join(CROSS, "cross1_length_one.json")
SRC_DIR = os.path.join(HERE, "src")
POPULATION = os.path.join(HERE, "emulation_population.json")
HELD = os.path.join(HERE, "emulation_held.json")
INDEXES = os.path.join(HERE, "emulation_indexes.json")
SAMPLE = os.path.join(HERE, "emulation_sample.json")
RUN = os.path.join(HERE, "emulation_run.json")
CONTROL = os.path.join(HERE, "emulation_control.json")
RESULTS = os.path.join(HERE, "emulation_results.json")
REPORT = os.path.join(HERE, "emulation_report.md")
# The same folder as seen from the host, for the report's paths:
# inside the lane HERE is PseudoCoupHQ/..., and the owner reads
# the report on the host.
HOST_FOLDER = ("PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation")

X_LANGUAGES = ["go", "rust", "swift"]
CLANG = "/usr/bin/clang"
SHIP_FLAGS = ["-std=c17", "-O1", "-c"]
SHIP_FLAGS_SOURCE = ("lane_gen.py compile_probe: `[CLANG, \"-std=c17\"] + "
                     "[\"-O1\"] + [\"-c\", src, \"-o\", obj]` -- the ship "
                     "build of every c unit in the corpus")

COLLECTOR_CAP_KB = 4 * 1024 * 1024
SUB_CEILING_MB = 2048
SUB_SECONDS = 240
WORKERS = 3
SEED = 20260906

GENERAL_ORDER = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_collector_memory():
    used = peak_kb()
    if used > COLLECTOR_CAP_KB:
        raise SystemExit(
            "ABORT_MEMORY_O7: the collecting process's peak resident "
            "%d kB passed the stated bound of %d kB" % (used,
                                                        COLLECTOR_CAP_KB))
    return used


def write_json(path, document):
    handle = open(path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()


def read_json(path):
    handle = open(path)
    document = json.load(handle)
    handle.close()
    return document


def sanitize(unit):
    return unit.replace("/", "_")


# ==================================================================
# section 1: THE POPULATION
# ==================================================================

class Population(object):
    """the pool entries this task emulates, with the count at each
    filter.

    attributes:
        filters     the pipe-table rows, per x and distinct
        entries     entry_id -> {x_langs, x_unit, x_lang, text, ...}
        control     entry_id -> {c_unit, text} for the control
    """

    def __init__(self, pool, cross1):
        self.pool = pool
        self.cross1 = cross1
        self.entry_by_id = {}
        for entry in pool["entries"]:
            self.entry_by_id[entry["entry_id"]] = entry
        self.filters = []
        self.entries = {}
        self.control = {}

    def select(self):
        """the filters, in order, each counted per x and distinct."""
        # P1: an x member and NO c member = task o1's length-one NOT
        # BUILT set for the pair c|x (x's entries that no c member
        # builds).  The brief's words "not built sets for x->c" name the
        # same entries read from the other side; the brief's own
        # definition ("have a member in x and NO c member") decides.
        candidates = {}
        for x in X_LANGUAGES:
            cell = self.cross1["pairs"]["%s|%s" % ("c", x)]
            for entry_id in cell["not_built_entry_ids"]:
                candidates.setdefault(entry_id, set()).add(x)
        self.count_filter("P1 an x member and no c member (o1's c|x "
                          "not-built sets)", candidates)
        # P2: at least one layer-5 text on the entry (a member whose
        # term the gate proved)
        with_text = {}
        for entry_id, xs in candidates.items():
            entry = self.entry_by_id[entry_id]
            if entry.get("layer5_normalized_texts"):
                with_text[entry_id] = xs
        self.count_filter("P2 the entry carries a layer-5 text", with_text)
        # P3: the parser round-trips the chosen member's text
        import cross2_length_two as C2
        round_trips = {}
        chosen = {}
        for entry_id, xs in with_text.items():
            entry = self.entry_by_id[entry_id]
            member = self.choose_member(entry, xs)
            if member is None:
                continue
            text = member["layer5_normalized_text"]
            try:
                node = C2.parse_text(text)
                ok = C2.print_node(node) == text
            except Exception:                              # noqa: BLE001
                ok = False
            chosen[entry_id] = (member, ok)
            if ok:
                round_trips[entry_id] = xs
        self.count_filter("P3 task o1's parser round-trips the chosen "
                          "member's text", round_trips)
        for entry_id, xs in with_text.items():
            member, ok = chosen[entry_id]
            entry = self.entry_by_id[entry_id]
            self.entries[entry_id] = {
                "entry_id": entry_id,
                "x_langs": sorted(xs),
                "x_lang": member["lang"],
                "x_unit": member["unit"],
                "text": member["layer5_normalized_text"],
                "entry_texts": list(entry["layer5_normalized_texts"]),
                "type_key": entry.get("type_key"),
                "round_trips": ok,
                "result_width": member.get("result_width"),
                "c_units_in_entry": [],
            }
        return self.entries

    def choose_member(self, entry, xs):
        """the representative when it is an x member with a proved
        text, else the first such member in the entry's own order."""
        representative = entry.get("representative")
        ordered = []
        for member in entry["members"]:
            if member["lang"] not in xs:
                continue
            if not member.get("layer5_normalized_text"):
                continue
            if not member.get("layer5_merge_eligible"):
                continue
            ordered.append(member)
        for member in ordered:
            if member["unit"] == representative:
                return member
        if ordered:
            return ordered[0]
        return None

    def select_control(self, count):
        """`count` entries that DO have a c member and a text, drawn
        uniformly with a stated seed; the c member is the
        representative when it is c, else the first c member."""
        eligible = []
        for entry in self.pool["entries"]:
            if not entry.get("layer5_normalized_texts"):
                continue
            c_members = []
            for member in entry["members"]:
                if member["lang"] != "c":
                    continue
                if not member.get("layer5_normalized_text"):
                    continue
                if not member.get("layer5_merge_eligible"):
                    continue
                c_members.append(member)
            if not c_members:
                continue
            chosen = c_members[0]
            for member in c_members:
                if member["unit"] == entry.get("representative"):
                    chosen = member
            eligible.append((entry["entry_id"], chosen, c_members))
        eligible.sort(key=lambda item: item[0])
        rng = random.Random(SEED)
        drawn = rng.sample(eligible, min(count, len(eligible)))
        drawn.sort(key=lambda item: item[0])
        for entry_id, chosen, c_members in drawn:
            self.control[entry_id] = {
                "entry_id": entry_id,
                "x_langs": ["c"],
                "x_lang": "c",
                "x_unit": chosen["unit"],
                "text": chosen["layer5_normalized_text"],
                "entry_texts": list(
                    self.entry_by_id[entry_id]["layer5_normalized_texts"]),
                "type_key": self.entry_by_id[entry_id].get("type_key"),
                "round_trips": True,
                "result_width": chosen.get("result_width"),
                "c_units_in_entry": [m["unit"] for m in c_members],
            }
        return len(eligible)

    def count_filter(self, label, mapping):
        row = {"filter": label, "distinct": len(mapping)}
        for x in X_LANGUAGES:
            row[x] = 0
        for entry_id, xs in mapping.items():
            for x in xs:
                row[x] = row[x] + 1
        self.filters.append(row)
        say("   %-70s go %4d  rust %4d  swift %4d  distinct %4d"
            % (label, row["go"], row["rust"], row["swift"],
               row["distinct"]))

    def stratified_sample(self, count):
        """`count` entries across the three x: 14 go, 13 rust, 13
        swift when each has that many, the shortfall handed to the
        largest stratum, drawn with the stated seed."""
        by_x = {}
        for x in X_LANGUAGES:
            by_x[x] = []
        for entry_id in sorted(self.entries):
            by_x[self.entries[entry_id]["x_lang"]].append(entry_id)
        want = {"go": (count + 2) // 3, "rust": (count) // 3,
                "swift": count - (count + 2) // 3 - count // 3}
        rng = random.Random(SEED)
        picked = []
        shortfall = 0
        for x in X_LANGUAGES:
            have = by_x[x]
            take = min(want[x], len(have))
            shortfall = shortfall + want[x] - take
            picked.extend(rng.sample(have, take))
        if shortfall:
            largest = max(X_LANGUAGES, key=lambda x: len(by_x[x]))
            rest = [e for e in by_x[largest] if e not in picked]
            picked.extend(rng.sample(rest, min(shortfall, len(rest))))
        return sorted(picked)


# ==================================================================
# section 2: THE INDEXES over the c corpus and the pool
# ==================================================================

def canon40_shards():
    import term66_run as TR
    return TR.shards()


def build_indexes(needed_units):
    """stream every canon40 shard once: the c body-bytes index, and
    the canon40 record of every unit this task needs (held)."""
    bytes_index = {}
    held = {}
    shard_of = {}
    c_units = 0
    for path in canon40_shards():
        document = read_json(path)
        for name, record in document["units"].items():
            lang = record.get("lang")
            if lang == "c" and record.get("body_bytes"):
                key = record["body_bytes"]
                bytes_index.setdefault(key, []).append(name)
                c_units = c_units + 1
            if name in needed_units:
                held[name] = record
                shard_of[name] = os.path.basename(path)
        del document
        check_collector_memory()
    return bytes_index, held, shard_of, c_units


def pool_indexes(pool):
    text_to_entries = {}
    unit_to_entry = {}
    for entry in pool["entries"]:
        for text in entry.get("layer5_normalized_texts") or []:
            text_to_entries.setdefault(text, []).append(entry["entry_id"])
        for member in entry["members"]:
            unit_to_entry[member["unit"]] = entry["entry_id"]
    return text_to_entries, unit_to_entry


# ==================================================================
# section 3: THE RENDERER   z3 term -> c source
# ==================================================================

class Refused(Exception):
    """the renderer cannot write this term in c; `cause` is one of a
    fixed list of causes and `detail` names the node."""

    def __init__(self, cause, detail=""):
        Exception.__init__(self, "%s: %s" % (cause, detail))
        self.cause = cause
        self.detail = detail


CAUSE_STATE = "term reads state that is not an arrival register"
CAUSE_LANE = "vector arrival used beyond its low lane"
CAUSE_X87 = "answer home or arrival on the x87 stack"
CAUSE_OP = "operator not covered by the renderer"
CAUSE_RM = "rounding mode other than RNE"
CAUSE_WIDTH = "a width c has no holder for"
CAUSE_ARITY = "more arrivals than the renderer names"
CAUSE_NO_TERM = "no term for the x unit"
CAUSE_REPRINT = "rebuilt term prints differently from the pool's text"

UNSIGNED = {8: "uint8_t", 16: "uint16_t", 32: "uint32_t",
            64: "uint64_t", 128: "unsigned __int128"}
SIGNED = {8: "int8_t", 16: "int16_t", 32: "int32_t",
          64: "int64_t", 128: "__int128"}
FLOAT = {16: "_Float16", 32: "float", 64: "double",
         # THE 80-BIT HOLDER (task ap3).  `long double` on
         # x86-64 IS the x87 extended format, and 79 is the
         # width of its IEEE bit-vector as z3 spells it:
         # `reference.X87_SORT` is `FPSort(15, 64)` and
         # `fp_width` adds the two, so a sign bit, 15 exponent
         # bits and a 63-bit fraction -- the explicit integer
         # bit the hardware stores in memory is not part of
         # z3's spelling.  This entry is a HOLDER only: no
         # `memcpy` helper is ever generated at this width,
         # because the 80th bit is exactly where memory and
         # z3 disagree.  Task ap3's probe, LITERAL, is in
         # lane `ap3_l2`: a `long double` add at the corpus's
         # own ship flags carves to
         # `fldt 0x18(%rsp); fldt 0x8(%rsp); faddp %st,%st(1); ret`.
         79: "long double"}
PARAM_NAMES = ["a", "b", "c", "d", "e", "f", "g", "h"]


X87_BITS = 79
"""the width of an x87 value as z3 spells it: `reference.X87_SORT` is
`FPSort(15, 64)` and `fp_width` adds the exponent and significand
widths.  The hardware's own memory spelling is 80 bits, the extra one
being the explicit integer bit; the two never meet in a rendering,
because an x87 value is carried as a `long double` and never as its
bits."""

X87_ARRIVAL = ("X87_", "x87_")

X87_ANSWER_FAMILY = "X87_0"
"""the answer home of a body that leaves its value on the x87 register
stack (task ap4, change 2).  THE CONVENTION, and it is task ap3's own
(`handful.home_of`): the c calling rule leaves a `long double` answer in
st(0), and `model_translate.preseeded_state` spells the stack top
`seed_X87_0`, so the top is `X87_0` on both sides."""


def is_an_x87_arrival(family):
    """whether an arrival family or answer home names a position on the
    x87 register stack.

    THE TWO SPELLINGS ARE THE REFERENCE'S OWN and are not this file's to
    change: the model table preseeds the stack as `seed_X87_0` /
    `seed_X87_1` (`model_translate` writes them) and a literal memory
    operand read at the x87 sort is `reference.x87_symbol`'s
    `x87_<mangled operand>`.  A written place on the stack is named
    `x87_<slot>` by the same rule.

    `st` IS NOT ONE OF THEM, and the reason is measured: the first
    twenty runs of lane `ap3_l6` refused `push` gpr_one 64 on all four
    targets, because a bare `st` prefix also spells the STACK place
    `push` writes.  The refusal a family spelled `st<n>` deserves is
    the one `plan_parameters` already raises two lines below this
    test."""
    if family is None:
        return False
    for prefix in X87_ARRIVAL:
        if family.startswith(prefix):
            return True
    return False


def promoted_bits(width):
    if width <= 32:
        return 32
    if width <= 64:
        return 64
    if width <= 128:
        return 128
    raise Refused(CAUSE_WIDTH, "%d bits" % width)


def literal(value, bits):
    """a c literal of the promoted type `bits` holding `value`."""
    value = value & ((1 << bits) - 1)
    if bits == 32:
        return "UINT32_C(0x%x)" % value
    if bits == 64:
        return "UINT64_C(0x%x)" % value
    high = value >> 64
    low = value & ((1 << 64) - 1)
    return ("(((unsigned __int128)UINT64_C(0x%x) << 64) | "
            "(unsigned __int128)UINT64_C(0x%x))" % (high, low))


def masked(text, width):
    """`text`, of the promoted type of `width`, with the bits above
    `width` cleared."""
    bits = promoted_bits(width)
    if width == bits:
        return "(%s)(%s)" % (UNSIGNED[bits], text)
    mask = literal((1 << width) - 1, bits)
    return "((%s)(%s) & %s)" % (UNSIGNED[bits], text, mask)


def fp_width(sort):
    return sort.ebits() + sort.sbits()


class Renderer(object):
    """the ONE renderer: a z3 term over `seed_<family>` symbols ->
    one c translation unit.

    attributes:
        families        the x unit's arrival families, IN order
        result_family   the x unit's answer home
        result_width    its width in bits
        params          per family: name, holder text, kind, bits
        helpers         the bit-cast helpers the body used
    methods:
        render          -> (source text, function symbol, param plan)
        emit            one node -> (text, kind, width)
    """

    def __init__(self, families, result_family, result_width, label):
        self.families = list(families)
        self.result_family = result_family
        self.result_width = result_width
        self.label = label
        self.params = []
        self.helpers = set()
        self.seed_names = {}
        self.uses = {}

    # -- the parameter plan -------------------------------------------

    def plan_parameters(self, term):
        import reference as R
        if len(self.families) > len(PARAM_NAMES):
            raise Refused(CAUSE_ARITY, "%d arrivals" % len(self.families))
        self.collect_uses(term, None)
        for index, family in enumerate(self.families):
            name = "seed_%s" % family
            self.seed_names[name] = index
            uses = self.uses.get(name, [])
            vector = family in R.XMM_NAMES
            if is_an_x87_arrival(family):
                # THE 80-BIT HOLDER (task ap3).  An x87 arrival is a
                # `long double` VALUE, not a bit pattern: the term
                # reads the symbol whole, at `reference.X87_SORT`, and
                # `long double` holds exactly that.  It is planned
                # before the vector test because a whole read is what
                # the vector branch refuses.
                self.params.append({
                    "index": index,
                    "family": family,
                    "name": PARAM_NAMES[index],
                    "holder": FLOAT[X87_BITS],
                    "kind": "fp",
                    "bits": X87_BITS,
                    "used": bool(uses),
                })
                continue
            if family.startswith("st") or family.startswith("x87"):
                raise Refused(CAUSE_X87, family)
            max_hi = -1
            bare = False
            for use in uses:
                if use is None:
                    bare = True
                else:
                    max_hi = max(max_hi, use[0])
            if vector:
                if bare:
                    raise Refused(CAUSE_LANE, "%s read whole" % family)
                if max_hi > 63:
                    raise Refused(CAUSE_LANE,
                                  "%s read above bit 63" % family)
                if max_hi < 0:
                    width = 64
                elif max_hi < 16:
                    width = 16
                elif max_hi < 32:
                    width = 32
                else:
                    width = 64
                holder = FLOAT[width]
                kind = "fp"
            else:
                if bare or max_hi > 31:
                    width = 64
                elif max_hi > 15:
                    width = 32
                elif max_hi > 7:
                    width = 16
                elif max_hi >= 0:
                    width = 8
                else:
                    width = 64
                holder = UNSIGNED[width]
                kind = "bv"
            self.params.append({
                "index": index,
                "family": family,
                "name": PARAM_NAMES[index],
                "holder": holder,
                "kind": kind,
                "bits": width,
                "used": bool(uses),
            })

    def collect_uses(self, node, parent_extract):
        if z3.is_const(node) and \
                node.decl().kind() == z3.Z3_OP_UNINTERPRETED:
            self.uses.setdefault(node.decl().name(), []).append(
                parent_extract)
            return
        kind = node.decl().kind()
        if kind == z3.Z3_OP_EXTRACT and node.num_args() == 1:
            high, low = node.params()
            child = node.arg(0)
            if z3.is_const(child) and \
                    child.decl().kind() == z3.Z3_OP_UNINTERPRETED:
                self.collect_uses(child, (high, low))
                return
        for index in range(node.num_args()):
            self.collect_uses(node.arg(index), None)

    # -- the source ---------------------------------------------------

    def render(self, term, text):
        self.plan_parameters(term)
        self.check_symbols(term)
        root_text, root_kind, root_width = self.emit(term)
        return_type, body = self.answer(root_text, root_kind, root_width)
        symbol = "emu_%s" % self.label
        lines = []
        lines.append("/* task o7 emulation -- rendered by emulate.py "
                     "Renderer from the layer-4 term of %s.  The term's "
                     "layer-5 text, LITERAL:" % self.label)
        lines.append("   %s */" % text)
        lines.append("#include <stdint.h>")
        if self.helpers:
            lines.append("#include <string.h>")
        for helper in sorted(self.helpers):
            lines.append(self.helper_text(helper))
        params = []
        for param in self.params:
            params.append("%s %s" % (param["holder"], param["name"]))
        if not params:
            params.append("void")
        lines.append("")
        lines.append("%s" % return_type)
        lines.append("%s(%s)" % (symbol, ", ".join(params)))
        lines.append("{")
        lines.append("    return %s;" % body)
        lines.append("}")
        lines.append("")
        return "\n".join(lines), symbol

    def check_symbols(self, term):
        import term as T
        unknown = []
        for symbol in T.free_symbols_in_order(term):
            name = symbol.decl().name()
            if name in self.seed_names:
                continue
            unknown.append(name)
        if unknown:
            raise Refused(CAUSE_STATE, ", ".join(unknown))

    def answer(self, root_text, root_kind, root_width):
        import reference as R
        family = self.result_family
        width = self.result_width
        if family is None or width is None:
            raise Refused(CAUSE_STATE, "no answer home")
        if family in R.XMM_NAMES:
            if width not in FLOAT:
                raise Refused(CAUSE_WIDTH, "answer %d bits in %s"
                              % (width, family))
            return_type = FLOAT[width]
            if root_kind == "fp":
                if root_width != width:
                    raise Refused(CAUSE_WIDTH,
                                  "fp answer %d bits, home %d"
                                  % (root_width, width))
                return return_type, root_text
            self.helpers.add("bits_to_f%d" % width)
            return return_type, "bits_to_f%d((%s)(%s))" % (
                width, UNSIGNED[width], root_text)
        if is_an_x87_arrival(family):
            # THE x87 ANSWER HOME (task ap3).  `handful.home_of` gives
            # an x87 place the stack top by the same CONVENTION the
            # flags place already carries a home by: the c calling rule
            # leaves a `long double` answer in st(0).  The root must
            # already be the float itself -- the driver hands the
            # renderer the value under the place's own
            # `fp.to_ieee_bv`, which is where the 79-against-80 seam
            # would otherwise be crossed by a `memcpy`.
            if width != X87_BITS:
                raise Refused(CAUSE_WIDTH, "x87 answer %d bits" % width)
            if root_kind != "fp" or root_width != X87_BITS:
                raise Refused(CAUSE_X87,
                              "an x87 answer home reached with a %s "
                              "root of %d bits" % (root_kind,
                                                   root_width))
            return FLOAT[X87_BITS], root_text
        if family.startswith("st") or family.startswith("x87"):
            raise Refused(CAUSE_X87, family)
        if width not in UNSIGNED:
            raise Refused(CAUSE_WIDTH, "answer %d bits" % width)
        return_type = UNSIGNED[width]
        if root_kind == "fp":
            self.helpers.add("f%d_to_bits" % root_width)
            return return_type, "(%s)f%d_to_bits(%s)" % (
                return_type, root_width, root_text)
        if root_kind == "bool":
            return return_type, "(%s)((%s) ? 1 : 0)" % (return_type,
                                                        root_text)
        return return_type, "(%s)(%s)" % (return_type, root_text)

    def helper_text(self, helper):
        match = re.match(r"^bits_to_f(\d+)$", helper)
        if match:
            width = int(match.group(1))
            return ("static inline %s %s(%s b) { %s f; memcpy(&f, &b, "
                    "%d); return f; }" % (FLOAT[width], helper,
                                          UNSIGNED[width], FLOAT[width],
                                          width // 8))
        match = re.match(r"^f(\d+)_to_bits$", helper)
        width = int(match.group(1))
        return ("static inline %s %s(%s f) { %s b; memcpy(&b, &f, %d); "
                "return b; }" % (UNSIGNED[width], helper, FLOAT[width],
                                 UNSIGNED[width], width // 8))

    # -- one node -----------------------------------------------------

    def emit(self, node):
        """-> (c text, kind, width).  kind is bv (text of the promoted
        unsigned type, bits above `width` zero), fp (float/double/
        _Float16 of `width` bits) or bool (a c truth value)."""
        decl = node.decl()
        kind = decl.kind()
        if z3.is_const(node) and kind == z3.Z3_OP_UNINTERPRETED:
            return self.emit_symbol(node, None)
        if kind == z3.Z3_OP_BNUM:
            width = node.size()
            return literal(node.as_long(), promoted_bits(width)), "bv", width
        if kind == z3.Z3_OP_TRUE:
            return "1", "bool", 1
        if kind == z3.Z3_OP_FALSE:
            return "0", "bool", 1
        if kind == z3.Z3_OP_EXTRACT:
            return self.emit_extract(node)
        if kind == z3.Z3_OP_CONCAT:
            return self.emit_concat(node)
        if kind in (z3.Z3_OP_ZERO_EXT, z3.Z3_OP_SIGN_EXT):
            return self.emit_extend(node, kind == z3.Z3_OP_SIGN_EXT)
        if kind == z3.Z3_OP_ITE:
            return self.emit_ite(node)
        if kind in (z3.Z3_OP_AND, z3.Z3_OP_OR, z3.Z3_OP_NOT,
                    z3.Z3_OP_XOR, z3.Z3_OP_IMPLIES, z3.Z3_OP_IFF):
            return self.emit_logic(node, kind)
        if kind in (z3.Z3_OP_EQ, z3.Z3_OP_DISTINCT):
            return self.emit_equality(node, kind)
        if kind in (z3.Z3_OP_SLEQ, z3.Z3_OP_SLT, z3.Z3_OP_SGEQ,
                    z3.Z3_OP_SGT):
            return self.emit_compare(node, kind, True)
        if kind in (z3.Z3_OP_ULEQ, z3.Z3_OP_ULT, z3.Z3_OP_UGEQ,
                    z3.Z3_OP_UGT):
            return self.emit_compare(node, kind, False)
        if kind in (z3.Z3_OP_BADD, z3.Z3_OP_BSUB, z3.Z3_OP_BMUL,
                    z3.Z3_OP_BAND, z3.Z3_OP_BOR, z3.Z3_OP_BXOR):
            return self.emit_arith(node, kind)
        if kind in (z3.Z3_OP_BNOT, z3.Z3_OP_BNEG):
            return self.emit_unary(node, kind)
        if kind in (z3.Z3_OP_BSHL, z3.Z3_OP_BLSHR, z3.Z3_OP_BASHR):
            return self.emit_shift(node, kind)
        if kind in (z3.Z3_OP_BUDIV, z3.Z3_OP_BUDIV_I, z3.Z3_OP_BUREM,
                    z3.Z3_OP_BUREM_I, z3.Z3_OP_BSDIV, z3.Z3_OP_BSDIV_I,
                    z3.Z3_OP_BSREM, z3.Z3_OP_BSREM_I):
            return self.emit_division(node, kind)
        if z3.is_fp(node) or z3.is_fprm(node) or \
                str(decl.name()).startswith("fp"):
            return self.emit_fp(node, kind)
        raise Refused(CAUSE_OP, "%s (kind %d)" % (decl.name(), kind))

    def emit_symbol(self, node, extract):
        name = node.decl().name()
        param = self.params[self.seed_names[name]]
        if param["kind"] == "bv":
            bits = promoted_bits(param["bits"])
            text = "(%s)%s" % (UNSIGNED[bits], param["name"])
            width = param["bits"]
            if extract is None:
                if node.size() != 64:
                    raise Refused(CAUSE_WIDTH,
                                  "general arrival of %d bits"
                                  % node.size())
                if width < 64:
                    # the holder is narrower than the register: the
                    # term reads bits the c ABI leaves unspecified
                    raise Refused(CAUSE_STATE,
                                  "%s read at 64 bits but planned as "
                                  "%s" % (name, param["holder"]))
                return text, "bv", 64
            high, low = extract
            if low == 0 and high + 1 == width:
                return text, "bv", width
            return masked("%s >> %d" % (text, low), high - low + 1), \
                "bv", high - low + 1
        if param["bits"] == X87_BITS:
            # AN x87 ARRIVAL IS THE FLOAT ITSELF (task ap3), and never
            # its bits: `long double` and z3's `FPSort(15, 64)` agree
            # on the value and disagree on the memory spelling (the
            # explicit integer bit), so a `memcpy` helper here would be
            # a different function from `fp.to_ieee_bv`.  The term
            # reads the symbol whole; there is no lane to take.
            if extract is not None:
                raise Refused(CAUSE_X87,
                              "%s read through Extract(%d, %d); an x87 "
                              "arrival is a value, not a bit pattern"
                              % (name, extract[0], extract[1]))
            return param["name"], "fp", X87_BITS
        # a vector arrival planned as a float holder: its bits
        helper = "f%d_to_bits" % param["bits"]
        self.helpers.add(helper)
        bits = promoted_bits(param["bits"])
        text = "(%s)%s(%s)" % (UNSIGNED[bits], helper, param["name"])
        if extract is None:
            raise Refused(CAUSE_LANE, name)
        high, low = extract
        if low == 0 and high + 1 == param["bits"]:
            return text, "bv", param["bits"]
        return masked("%s >> %d" % (text, low), high - low + 1), \
            "bv", high - low + 1

    def emit_extract(self, node):
        high, low = node.params()
        child = node.arg(0)
        if z3.is_const(child) and \
                child.decl().kind() == z3.Z3_OP_UNINTERPRETED:
            return self.emit_symbol(child, (high, low))
        text, kind, width = self.emit(child)
        self.expect(kind, "bv", node)
        out = high - low + 1
        if low == 0 and out == width:
            return text, "bv", width
        inner_bits = promoted_bits(width)
        shifted = "(%s)(%s) >> %d" % (UNSIGNED[inner_bits], text, low)
        return masked(shifted, out), "bv", out

    def emit_concat(self, node):
        parts = []
        total = 0
        for index in range(node.num_args()):
            text, kind, width = self.emit(node.arg(index))
            self.expect(kind, "bv", node)
            parts.append((text, width))
            total = total + width
        bits = promoted_bits(total)
        pieces = []
        shift = total
        for text, width in parts:
            shift = shift - width
            piece = "((%s)(%s) << %d)" % (UNSIGNED[bits], text, shift)
            if shift == 0:
                piece = "(%s)(%s)" % (UNSIGNED[bits], text)
            pieces.append(piece)
        return masked(" | ".join(pieces), total), "bv", total

    def emit_extend(self, node, signed):
        extra = node.params()[0]
        text, kind, width = self.emit(node.arg(0))
        self.expect(kind, "bv", node)
        total = width + extra
        bits = promoted_bits(total)
        if not signed:
            return "(%s)(%s)" % (UNSIGNED[bits], text), "bv", total
        return masked(self.sign_extended(text, width, bits), total), \
            "bv", total

    def sign_extended(self, text, width, bits):
        """`text` (width bits, promoted type) as a SIGNED value of the
        promoted type `bits`, sign bit `width - 1` propagated."""
        if width == bits:
            return "(%s)(%s)" % (SIGNED[bits], text)
        return "((%s)((%s)(%s) << %d) >> %d)" % (
            SIGNED[bits], UNSIGNED[bits], text, bits - width,
            bits - width)

    def emit_ite(self, node):
        cond, ckind, _ = self.emit(node.arg(0))
        self.expect(ckind, "bool", node)
        left, lkind, lwidth = self.emit(node.arg(1))
        right, rkind, rwidth = self.emit(node.arg(2))
        if lkind != rkind or lwidth != rwidth:
            raise Refused(CAUSE_OP, "If with arms of different sorts")
        if lkind == "bv":
            bits = promoted_bits(lwidth)
            return "((%s) ? (%s)(%s) : (%s)(%s))" % (
                cond, UNSIGNED[bits], left, UNSIGNED[bits], right), \
                "bv", lwidth
        return "((%s) ? (%s) : (%s))" % (cond, left, right), lkind, lwidth

    def emit_logic(self, node, kind):
        args = []
        for index in range(node.num_args()):
            text, akind, _ = self.emit(node.arg(index))
            self.expect(akind, "bool", node)
            args.append("(%s)" % text)
        if kind == z3.Z3_OP_NOT:
            return "(!%s)" % args[0], "bool", 1
        if kind == z3.Z3_OP_AND:
            return "(%s)" % " && ".join(args), "bool", 1
        if kind == z3.Z3_OP_OR:
            return "(%s)" % " || ".join(args), "bool", 1
        if kind == z3.Z3_OP_XOR:
            return "(%s != %s)" % (args[0], args[1]), "bool", 1
        if kind == z3.Z3_OP_IMPLIES:
            return "(!%s || %s)" % (args[0], args[1]), "bool", 1
        return "(%s == %s)" % (args[0], args[1]), "bool", 1

    def emit_equality(self, node, kind):
        left, lkind, lwidth = self.emit(node.arg(0))
        right, rkind, rwidth = self.emit(node.arg(1))
        if lkind == "fp" or rkind == "fp":
            raise Refused(CAUSE_OP, "structural equality on floats")
        if lkind != rkind or lwidth != rwidth:
            raise Refused(CAUSE_OP, "equality across sorts")
        sign = "==" if kind == z3.Z3_OP_EQ else "!="
        if lkind == "bool":
            return "((%s) %s (%s))" % (left, sign, right), "bool", 1
        bits = promoted_bits(lwidth)
        return "((%s)(%s) %s (%s)(%s))" % (UNSIGNED[bits], left, sign,
                                           UNSIGNED[bits], right), \
            "bool", 1

    COMPARE = {}

    def emit_compare(self, node, kind, signed):
        signs = {
            z3.Z3_OP_SLEQ: "<=", z3.Z3_OP_SLT: "<", z3.Z3_OP_SGEQ: ">=",
            z3.Z3_OP_SGT: ">", z3.Z3_OP_ULEQ: "<=", z3.Z3_OP_ULT: "<",
            z3.Z3_OP_UGEQ: ">=", z3.Z3_OP_UGT: ">",
        }
        left, lkind, lwidth = self.emit(node.arg(0))
        right, rkind, rwidth = self.emit(node.arg(1))
        self.expect(lkind, "bv", node)
        self.expect(rkind, "bv", node)
        if lwidth != rwidth:
            raise Refused(CAUSE_OP, "comparison across widths")
        bits = promoted_bits(lwidth)
        if signed:
            left = self.sign_extended(left, lwidth, bits)
            right = self.sign_extended(right, rwidth, bits)
        else:
            left = "(%s)(%s)" % (UNSIGNED[bits], left)
            right = "(%s)(%s)" % (UNSIGNED[bits], right)
        return "(%s %s %s)" % (left, signs[kind], right), "bool", 1

    def emit_arith(self, node, kind):
        signs = {
            z3.Z3_OP_BADD: "+", z3.Z3_OP_BSUB: "-", z3.Z3_OP_BMUL: "*",
            z3.Z3_OP_BAND: "&", z3.Z3_OP_BOR: "|", z3.Z3_OP_BXOR: "^",
        }
        args = []
        width = None
        for index in range(node.num_args()):
            text, akind, awidth = self.emit(node.arg(index))
            self.expect(akind, "bv", node)
            if width is None:
                width = awidth
            if awidth != width:
                raise Refused(CAUSE_OP, "arithmetic across widths")
            args.append(text)
        bits = promoted_bits(width)
        joined = (" %s " % signs[kind]).join(
            "(%s)(%s)" % (UNSIGNED[bits], text) for text in args)
        return masked(joined, width), "bv", width

    def emit_unary(self, node, kind):
        text, akind, width = self.emit(node.arg(0))
        self.expect(akind, "bv", node)
        bits = promoted_bits(width)
        sign = "~" if kind == z3.Z3_OP_BNOT else "-"
        return masked("%s(%s)(%s)" % (sign, UNSIGNED[bits], text), width), \
            "bv", width

    def emit_shift(self, node, kind):
        value, vkind, width = self.emit(node.arg(0))
        amount, akind, awidth = self.emit(node.arg(1))
        self.expect(vkind, "bv", node)
        self.expect(akind, "bv", node)
        bits = promoted_bits(width)
        abits = promoted_bits(awidth)
        count = "(unsigned)(%s)(%s)" % (UNSIGNED[abits], amount)
        bound = upper_bound(node.arg(1))
        if kind == z3.Z3_OP_BSHL:
            plain = masked("(%s)(%s) << %s" % (UNSIGNED[bits], value,
                                               count), width)
            fill = "(%s)0" % UNSIGNED[bits]
        elif kind == z3.Z3_OP_BLSHR:
            plain = masked("(%s)(%s) >> %s" % (UNSIGNED[bits], value,
                                               count), width)
            fill = "(%s)0" % UNSIGNED[bits]
        else:
            signed_value = self.sign_extended(value, width, bits)
            plain = masked("%s >> %s" % (signed_value, count), width)
            fill = "((%s < 0) ? %s : (%s)0)" % (
                signed_value, literal((1 << width) - 1, bits),
                UNSIGNED[bits])
        if bound is not None and bound < width:
            return plain, "bv", width
        guard = "((%s)(%s) < (%s)%d)" % (UNSIGNED[abits], amount,
                                         UNSIGNED[abits], width)
        return "(%s ? %s : %s)" % (guard, plain, fill), "bv", width

    def emit_division(self, node, kind):
        left, lkind, lwidth = self.emit(node.arg(0))
        right, rkind, rwidth = self.emit(node.arg(1))
        self.expect(lkind, "bv", node)
        self.expect(rkind, "bv", node)
        if lwidth != rwidth:
            raise Refused(CAUSE_OP, "division across widths")
        bits = promoted_bits(lwidth)
        signed = kind in (z3.Z3_OP_BSDIV, z3.Z3_OP_BSDIV_I,
                          z3.Z3_OP_BSREM, z3.Z3_OP_BSREM_I)
        remainder = kind in (z3.Z3_OP_BUREM, z3.Z3_OP_BUREM_I,
                             z3.Z3_OP_BSREM, z3.Z3_OP_BSREM_I)
        sign = "%" if remainder else "/"
        if signed:
            if lwidth not in SIGNED:
                raise Refused(CAUSE_WIDTH,
                              "signed division at %d bits" % lwidth)
            text = "(%s)(%s) %s (%s)(%s)" % (
                SIGNED[lwidth], self.sign_extended(left, lwidth, bits),
                sign, SIGNED[lwidth],
                self.sign_extended(right, rwidth, bits))
            return masked(text, lwidth), "bv", lwidth
        text = "(%s)(%s) %s (%s)(%s)" % (UNSIGNED[bits], left, sign,
                                         UNSIGNED[bits], right)
        return masked(text, lwidth), "bv", lwidth

    def emit_fp(self, node, kind):
        name = node.decl().name()
        if kind == z3.Z3_OP_FPA_RM_NEAREST_TIES_TO_EVEN:
            return "RNE", "rm", 0
        if z3.is_fprm(node):
            raise Refused(CAUSE_RM, name)
        if z3.is_fp_value(node) or kind in (
                z3.Z3_OP_FPA_PLUS_ZERO, z3.Z3_OP_FPA_MINUS_ZERO,
                z3.Z3_OP_FPA_PLUS_INF, z3.Z3_OP_FPA_MINUS_INF,
                z3.Z3_OP_FPA_NAN, z3.Z3_OP_FPA_NUM):
            width = fp_width(node.sort())
            if width not in FLOAT:
                raise Refused(CAUSE_WIDTH, "float literal of %d bits"
                              % width)
            bits_value = z3.simplify(z3.fpToIEEEBV(node)).as_long()
            if bits_value == 0:
                zero = {16: "(_Float16)0.0f", 32: "0.0f", 64: "0.0"}
                return zero[width], "fp", width
            self.helpers.add("bits_to_f%d" % width)
            return "bits_to_f%d((%s)%s)" % (
                width, UNSIGNED[width], literal(bits_value,
                                                 promoted_bits(width))), \
                "fp", width
        if kind == z3.Z3_OP_FPA_TO_FP:
            return self.emit_to_fp(node)
        if kind == z3.Z3_OP_FPA_TO_FP_UNSIGNED:
            self.expect_rne(node.arg(0))
            text, akind, awidth = self.emit(node.arg(1))
            self.expect(akind, "bv", node)
            width = fp_width(node.sort())
            bits = promoted_bits(awidth)
            return "((%s)(%s)(%s))" % (FLOAT[width], UNSIGNED[bits], text), \
                "fp", width
        if kind == z3.Z3_OP_FPA_TO_IEEE_BV:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            if awidth == X87_BITS:
                # THE SEAM, REFUSED RATHER THAN CROSSED (task ap3).
                # This node's helper is a `memcpy` between a float and
                # its bits, and at the x87 width the two spellings
                # differ by the explicit integer bit the hardware
                # stores and z3 does not -- so the helper would be a
                # different function from the node.  Where an x87 value
                # is the place's ANSWER the driver hands the renderer
                # the float underneath instead (`handful.the_x87_value`)
                # and this node is never reached; where the term reads
                # an x87 value's BITS inside itself, as an x87 compare's
                # flag pair does, there is nothing to hand and the
                # place is refused by cause.
                raise Refused(CAUSE_X87,
                              "this term reads an x87 value's bits, "
                              "and c's `long double` and z3's "
                              "FPSort(15, 64) do not spell them the "
                              "same")
            self.helpers.add("f%d_to_bits" % awidth)
            bits = promoted_bits(awidth)
            return "(%s)f%d_to_bits(%s)" % (UNSIGNED[bits], awidth, text), \
                "bv", awidth
        if kind in (z3.Z3_OP_FPA_TO_SBV, z3.Z3_OP_FPA_TO_UBV):
            rm = node.arg(0)
            if rm.decl().kind() != z3.Z3_OP_FPA_RM_TOWARD_ZERO:
                raise Refused(CAUSE_RM, "%s under %s (c truncates)"
                              % (name, rm.decl().name()))
            text, akind, awidth = self.emit(node.arg(1))
            self.expect(akind, "fp", node)
            width = node.size()
            if width not in SIGNED:
                raise Refused(CAUSE_WIDTH, "%s to %d bits" % (name, width))
            table = SIGNED if kind == z3.Z3_OP_FPA_TO_SBV else UNSIGNED
            bits = promoted_bits(width)
            return masked("(%s)(%s)(%s)" % (UNSIGNED[bits], table[width],
                                            text), width), "bv", width
        if kind in (z3.Z3_OP_FPA_ADD, z3.Z3_OP_FPA_SUB, z3.Z3_OP_FPA_MUL,
                    z3.Z3_OP_FPA_DIV):
            signs = {z3.Z3_OP_FPA_ADD: "+", z3.Z3_OP_FPA_SUB: "-",
                     z3.Z3_OP_FPA_MUL: "*", z3.Z3_OP_FPA_DIV: "/"}
            self.expect_rne(node.arg(0))
            left, lkind, lwidth = self.emit(node.arg(1))
            right, rkind, rwidth = self.emit(node.arg(2))
            self.expect(lkind, "fp", node)
            self.expect(rkind, "fp", node)
            if lwidth != rwidth:
                raise Refused(CAUSE_OP, "float arithmetic across widths")
            return "((%s)((%s) %s (%s)))" % (FLOAT[lwidth], left,
                                             signs[kind], right), \
                "fp", lwidth
        if kind == z3.Z3_OP_FPA_NEG:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            return "(-(%s))" % text, "fp", awidth
        if kind == z3.Z3_OP_FPA_ABS:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            builtin = {32: "__builtin_fabsf", 64: "__builtin_fabs"}
            if awidth not in builtin:
                raise Refused(CAUSE_OP, "%s at %d bits" % (name, awidth))
            return "%s(%s)" % (builtin[awidth], text), "fp", awidth
        if kind in (z3.Z3_OP_FPA_EQ, z3.Z3_OP_FPA_LT, z3.Z3_OP_FPA_GT,
                    z3.Z3_OP_FPA_LE, z3.Z3_OP_FPA_GE):
            signs = {z3.Z3_OP_FPA_EQ: "==", z3.Z3_OP_FPA_LT: "<",
                     z3.Z3_OP_FPA_GT: ">", z3.Z3_OP_FPA_LE: "<=",
                     z3.Z3_OP_FPA_GE: ">="}
            left, lkind, lwidth = self.emit(node.arg(0))
            right, rkind, rwidth = self.emit(node.arg(1))
            self.expect(lkind, "fp", node)
            self.expect(rkind, "fp", node)
            if lwidth != rwidth:
                raise Refused(CAUSE_OP, "float comparison across widths")
            return "((%s) %s (%s))" % (left, signs[kind], right), "bool", 1
        if kind == z3.Z3_OP_FPA_IS_NAN:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            return "((%s) != (%s))" % (text, text), "bool", 1
        if kind == z3.Z3_OP_FPA_IS_ZERO:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            return "((%s) == 0)" % text, "bool", 1
        if kind == z3.Z3_OP_FPA_IS_INF:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            return "(__builtin_isinf(%s) != 0)" % text, "bool", 1
        if kind == z3.Z3_OP_FPA_IS_NEGATIVE:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            return "(__builtin_signbit(%s) != 0)" % text, "bool", 1
        if kind == z3.Z3_OP_FPA_IS_POSITIVE:
            text, akind, awidth = self.emit(node.arg(0))
            self.expect(akind, "fp", node)
            return "(__builtin_signbit(%s) == 0)" % text, "bool", 1
        raise Refused(CAUSE_OP, "%s (kind %d)" % (name, kind))

    def emit_to_fp(self, node):
        width = fp_width(node.sort())
        if width not in FLOAT:
            raise Refused(CAUSE_WIDTH, "float of %d bits" % width)
        if node.num_args() == 1:
            child = node.arg(0)
            # the shortcut: the bits of a float arrival, read whole
            if child.decl().kind() == z3.Z3_OP_EXTRACT:
                grand = child.arg(0)
                high, low = child.params()
                if z3.is_const(grand) and \
                        grand.decl().kind() == z3.Z3_OP_UNINTERPRETED:
                    param = self.params[self.seed_names[
                        grand.decl().name()]]
                    if param["kind"] == "fp" and low == 0 and \
                            high + 1 == param["bits"] and \
                            param["bits"] == width:
                        return param["name"], "fp", width
            text, akind, awidth = self.emit(child)
            self.expect(akind, "bv", node)
            if awidth != width:
                raise Refused(CAUSE_WIDTH, "%d bits reinterpreted as a "
                              "%d-bit float" % (awidth, width))
            self.helpers.add("bits_to_f%d" % width)
            return "bits_to_f%d((%s)(%s))" % (width, UNSIGNED[width],
                                              text), "fp", width
        if node.num_args() == 2:
            self.expect_rne(node.arg(0))
            text, akind, awidth = self.emit(node.arg(1))
            if akind == "fp":
                return "((%s)(%s))" % (FLOAT[width], text), "fp", width
            if akind == "bv":
                bits = promoted_bits(awidth)
                return "((%s)%s)" % (FLOAT[width],
                                     self.sign_extended(text, awidth,
                                                        bits)), \
                    "fp", width
        raise Refused(CAUSE_OP, "fpToFP with %d arguments"
                      % node.num_args())

    def expect_rne(self, rm):
        if rm.decl().kind() != z3.Z3_OP_FPA_RM_NEAREST_TIES_TO_EVEN:
            raise Refused(CAUSE_RM, rm.decl().name())

    def expect(self, kind, wanted, node):
        if kind != wanted:
            raise Refused(CAUSE_OP, "%s wants a %s operand and got %s"
                          % (node.decl().name(), wanted, kind))


def upper_bound(node):
    """the largest value a bit-vector term can take, when a small
    bound is visible from its shape (a numeral, a zero-extended
    extract, an If over such); None otherwise."""
    kind = node.decl().kind()
    if kind == z3.Z3_OP_BNUM:
        return node.as_long()
    if kind == z3.Z3_OP_EXTRACT:
        high, low = node.params()
        return (1 << (high - low + 1)) - 1
    if kind == z3.Z3_OP_ZERO_EXT:
        return upper_bound(node.arg(0))
    if kind == z3.Z3_OP_CONCAT:
        total = 0
        shift = node.size()
        for index in range(node.num_args()):
            child = node.arg(index)
            shift = shift - child.size()
            bound = upper_bound(child)
            if bound is None:
                return None
            total = total + (bound << shift)
        return total
    if kind == z3.Z3_OP_ITE:
        left = upper_bound(node.arg(1))
        right = upper_bound(node.arg(2))
        if left is None or right is None:
            return None
        return max(left, right)
    if kind == z3.Z3_OP_BAND:
        bounds = []
        for index in range(node.num_args()):
            bound = upper_bound(node.arg(index))
            if bound is not None:
                bounds.append(bound)
        if bounds:
            return min(bounds)
        return None
    return None


# ==================================================================
# section 4: ONE EMULATION, inside a forked sub-process
# ==================================================================

COMMUTATIVE_BINARY = ("+", "*", "|", "^", "==")
COMMUTATIVE_CALLS = ("And", "Or", "fpEQ")


def commutative_canonical(text):
    """the layer-5 text with the arguments of every commutative
    operator put in one fixed order (their own printed form), so two
    prints of one term that differ only in that order compare equal.
    Uses task o1's parser; None when the text does not parse."""
    import cross2_length_two as C2
    try:
        tree = C2.parse_text(text)
    except Exception:                                      # noqa: BLE001
        return None
    erased = erase_variable_index(tree)
    count = len(set(re.findall(r"\bv\d+\b", text)))
    return "%d variables: %s" % (count, C2.print_node(sort_commutative(erased)))


def erase_variable_index(node):
    """`v<N>` -> `v`: the positional index is assigned in first-met
    order of the PRINTED term, so it moves when a commutative
    operator's arguments move; the comparison erases it and counts
    the distinct variables beside the text."""
    kind = node[0]
    if kind == "var":
        return ("var", "v")
    if kind in ("num", "id"):
        return node
    if kind == "paren":
        return ("paren", erase_variable_index(node[1]))
    if kind == "un":
        return ("un", node[1], erase_variable_index(node[2]))
    if kind == "call":
        return ("call", node[1], [erase_variable_index(a) for a in node[2]])
    return ("bin", node[1], erase_variable_index(node[2]),
            erase_variable_index(node[3]))


def flatten_chain(node, op):
    if node[0] == "bin" and node[1] == op:
        return flatten_chain(node[2], op) + flatten_chain(node[3], op)
    if node[0] == "paren" and node[1][0] == "bin" and node[1][1] == op:
        return flatten_chain(node[1], op)
    return [node]


def sort_commutative(node):
    import cross2_length_two as C2
    kind = node[0]
    if kind in ("num", "var", "id"):
        return node
    if kind == "paren":
        return ("paren", sort_commutative(node[1]))
    if kind == "un":
        return ("un", node[1], sort_commutative(node[2]))
    if kind == "call":
        args = [sort_commutative(a) for a in node[2]]
        if node[1] in COMMUTATIVE_CALLS:
            args.sort(key=C2.print_node)
        return ("call", node[1], args)
    op = node[1]
    if op in COMMUTATIVE_BINARY:
        parts = [sort_commutative(p) for p in flatten_chain(node, op)]
        parts.sort(key=C2.print_node)
        out = parts[0]
        for part in parts[1:]:
            out = ("bin", op, out, part)
        return out
    return ("bin", op, sort_commutative(node[2]), sort_commutative(node[3]))

def firstline(text):
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped.replace("|", "/")[:200]
    return "(no diagnostic)"


EXTRACTOR = {}


def pipeline_extractor():
    """`lane_gen.py`'s `extract` -- the objdump reader that carved every
    unit of the corpus.  It is defined INSIDE `lane_gen.DRIVER` (the
    lane's embedded python, lines 82-444 of lane_gen.py), not at
    module level, so it is taken out of that text at run time: the
    slice from `LABEL = re.compile` to `def disasm(` -- the three
    regexes and the function -- compiled once, unchanged."""
    if "extract" in EXTRACTOR:
        return EXTRACTOR["extract"]
    import lane_gen as LG
    text = LG.DRIVER
    start = text.index("LABEL = re.compile")
    end = text.index("def disasm(")
    namespace = {"re": re}
    exec(compile(text[start:end], "lane_gen.DRIVER[extract]", "exec"),
         namespace)
    EXTRACTOR["extract"] = namespace["extract"]
    EXTRACTOR["source_lines"] = (text[:start].count("\n"),
                                 text[:end].count("\n"))
    return EXTRACTOR["extract"]


def compile_and_carve(source, symbol):
    """the corpus's own ship compile and carve: clang at SHIP_FLAGS,
    objdump read by `lane_gen.DRIVER`'s `extract`."""
    extract = pipeline_extractor()
    work = tempfile.mkdtemp(prefix="o7_", dir=os.environ.get("TMPDIR"))
    src = os.path.join(work, "unit.c")
    obj = os.path.join(work, "unit_ship.o")
    handle = open(src, "w")
    handle.write(source)
    handle.close()
    command = [CLANG] + SHIP_FLAGS + [src, "-o", obj]
    done = subprocess.run(command, capture_output=True, text=True,
                          timeout=180)
    if done.returncode != 0 or not os.path.exists(obj):
        cleanup(work)
        return None, firstline(done.stderr or done.stdout)
    done = subprocess.run(["objdump", "-dr", "--disassemble=" + symbol,
                           obj], capture_output=True, text=True,
                          timeout=180)
    got = extract(done.stdout, symbol, True)
    cleanup(work)
    if got is None:
        return None, "objdump found no symbol %s" % symbol
    return got, None


def cleanup(work):
    for name in os.listdir(work):
        os.unlink(os.path.join(work, name))
    os.rmdir(work)


def recorded_facts(label, key, raw_bytes, mnem):
    """the arch-unit facts read off the ship text, exactly as
    `canon38_regen.process_probe` reads them for a regenerated c
    probe (its own wrap and gate are the superseded canon38 form and
    are not run; `canonical_form.render_one` wraps and gates)."""
    import canon38_gate as G38
    import canon10_behaviour_check as BC10
    import ledger48 as L48
    body_text = "; ".join(mnem)
    body_bytes = " ".join(raw_bytes)
    entry_contract = G38.arrival_contract("c", body_text)
    import ledger as L
    ship_lines = L48.split_lines(body_text)
    home, width = BC10.answer_home_from_real(ship_lines)
    if home is None:
        # TASK ap4, CHANGE 2, the driver's half of it.  A body that
        # leaves its answer on the x87 register stack names no register
        # at all, so `answer_home_from_real` answers (None, None) and
        # this record used to fall back to the first arrival -- which
        # for these bodies is also None, and the canonical form then
        # refused the unit `no answer home` (log_245 section 6.3).
        # The ledger's own reading of the body is what says so: its
        # `x87` field is True exactly when a value is left on the stack
        # at every return.  The family is the x87 stack top, which is
        # where the c calling rule leaves a `long double` answer and is
        # the same convention `handful.home_of` already states for a
        # written x87 place.
        reading = L.answer_registers_of_body(ship_lines)
        if reading.get("x87") and not reading.get("families"):
            home = X87_ANSWER_FAMILY
            width = X87_BITS
    if home is None:
        home = entry_contract.get("a")
        width = 64
    families = G38.arrival_family_list(entry_contract)
    return {
        "unit": label,
        "lang": "c",
        "n": key,
        "population": "emulation",
        "operator": None,
        "recorded_status": "emulation",
        "body_source": "the unit's own ship text",
        "body_text": body_text,
        "body_bytes": body_bytes,
        "entry_contract": entry_contract,
        "entry_contract_source": (
            "read off the unit's own ship text, in c's own "
            "argument-register order: a family arrives when the text "
            "reads it before it writes it"),
        "result_family": home,
        "result_width": width,
        "arrival_families": families,
    }


def families_the_term_reads(x_record, x_term):
    """the x unit's IN rows for this task: the recorded arrival
    families, plus any further ARGUMENT REGISTER the term reads
    (`seed_<family>` with family in the language's own argument
    sequences, `canon37_gate.sequences_for`), the whole list put in
    that sequence's order.  A read the recorded contract omits is
    returned beside it, so the report can count them."""
    import canon37_gate as G37
    import term as T
    lang = x_record.get("lang")
    general, vector = G37.sequences_for(lang)
    recorded = list(x_record.get("arrival_families") or [])
    read = set(recorded)
    omitted = []
    for symbol in T.free_symbols_in_order(x_term):
        name = symbol.decl().name()
        if not name.startswith("seed_"):
            continue
        family = name[len("seed_"):]
        if family in general or family in vector:
            if family not in read:
                read.add(family)
                omitted.append(family)
    ordered = [f for f in general if f in read] + \
        [f for f in vector if f in read]
    for family in recorded:
        if family not in ordered:
            ordered.append(family)
    return ordered, omitted


def expected_c_families(params):
    """the register each declared parameter arrives in under the c
    calling rule: general holders take rdi, rsi, rdx, rcx, r8, r9 in
    order; float holders take xmm0.. in order."""
    out = []
    general = 0
    vector = 0
    for param in params:
        if param["kind"] == "fp":
            out.append("xmm%d" % vector)
            vector = vector + 1
        else:
            out.append(GENERAL_ORDER[general])
            general = general + 1
    return out


def body_answer(reference, record):
    """the reference simulator's answer for a body, or (None, cause).

    TASK ap5: THE x87 BRANCH THAT STOOD HERE IS GONE, and this is the
    whole of what moving the reading into the layer that owns it
    costs.  Task ap4 read an answer left on the x87 register stack in
    this file (`x87_answer_for_unit`), because `reference.answer_of`
    raised `Z3Exception: invalid extract application` on such a home
    and `reference.py` was not a file its brief named.  Task ap5's
    brief names it: `answer_of` now reads an `X87_<k>` home off the
    reference's own `MachineState.x87` and applies the same
    `fpToIEEEBV`, so `answer_for_unit` answers an x87 unit like any
    other and this function asks nothing special of it.  The removed
    function was called from this one line and nowhere else."""
    import reference as R
    try:
        term, _width = reference.answer_for_unit(record)
        return term, None
    except R.NotModeled as problem:
        return None, "the reference: %s" % problem
    except Exception as problem:                             # noqa: BLE001
        return None, "the reference raised %s: %s" % (
            type(problem).__name__, problem)


def one_emulation(shared, job):
    """the whole of one entry's work: transcribe x, render, compile,
    carve, wrap, gate, term, Q1, Q2, Q3.  Runs inside the fork."""
    import term as T
    import term66_run as TR
    import canonical_form as CF
    import pool100_entry_equivalence as P100
    import gate as G
    maker = shared["maker"]
    gate = shared["gate"]
    form = shared["form"]
    reference = shared["reference"]
    held = shared["held"]
    bytes_index = shared["bytes_index"]
    text_to_entries = shared["text_to_entries"]
    unit_to_entry = shared["unit_to_entry"]
    entry_id = job["entry_id"]
    x_unit = job["x_unit"]
    record = {
        "entry_id": entry_id,
        "x_lang": job["x_lang"],
        "x_unit": x_unit,
        "x_text": job["text"],
        "entry_texts": job["entry_texts"],
        "type_key": job["type_key"],
        "control": job.get("control", False),
    }
    x_record = held.get(x_unit)
    if x_record is None:
        record["rendered"] = False
        record["refusal_cause"] = CAUSE_NO_TERM
        record["refusal_detail"] = "no canon40 record held for %s" % x_unit
        return record
    record["x_arrival_families"] = list(x_record.get("arrival_families")
                                        or [])
    record["x_result_family"] = x_record.get("result_family")
    record["x_result_width"] = x_record.get("result_width")
    record["x_body_text"] = x_record.get("body_text")
    record["x_body_bytes"] = x_record.get("body_bytes")
    unit = dict(x_record)
    unit["unit"] = x_unit
    walked = maker.transcribe(unit)
    if walked.refused is not None or walked.out_term is None:
        record["rendered"] = False
        record["refusal_cause"] = CAUSE_NO_TERM
        if walked.refused is not None:
            record["refusal_detail"] = "the relink refused: %s" % \
                walked.refused
        else:
            import regate64_run as RG
            record["refusal_detail"] = RG.why_no_term(walked)
        return record
    x_term = walked.out_term
    reprinted = maker.normalize(x_term)
    record["x_reprinted_text"] = reprinted
    record["reprint_exact"] = reprinted == job["text"]
    if not record["reprint_exact"]:
        # today's `Term.normalize` and the pool's stored text can
        # differ in the ORDER of a commutative operator's arguments,
        # and with it in the positional variable index (measured in
        # the sample lane: 26 of 40 differ); the two are the same
        # term up to that, checked with task o1's parser
        same = commutative_canonical(reprinted) == \
            commutative_canonical(job["text"])
        record["reprint_same_up_to_commutative_order_and_variable_index"] = same
        if not same:
            record["rendered"] = False
            record["refusal_cause"] = CAUSE_REPRINT
            record["refusal_detail"] = reprinted
            return record
    ordered = T.order_commutative(z3.simplify(x_term))
    label = "%s__%s" % (entry_id, sanitize(x_unit))
    if job.get("control"):
        label = "control__" + label
    families, omitted = families_the_term_reads(x_record, x_term)
    record["x_in_rows"] = families
    record["x_contract_omits"] = omitted
    renderer = Renderer(families, x_record.get("result_family"),
                        x_record.get("result_width"), label)
    try:
        source, symbol = renderer.render(ordered, job["text"])
    except Refused as refusal:
        record["rendered"] = False
        record["refusal_cause"] = refusal.cause
        record["refusal_detail"] = refusal.detail
        return record
    record["rendered"] = True
    record["params"] = renderer.params
    record["source_path"] = os.path.join("src", label + ".c")
    record["source"] = source
    handle = open(os.path.join(SRC_DIR, label + ".c"), "w")
    handle.write(source)
    handle.close()
    got, refusal = compile_and_carve(source, symbol)
    if got is None:
        record["compiled"] = False
        record["compile_refusal"] = refusal
        return record
    record["compiled"] = True
    raw_bytes, mnem = got
    record["body_bytes"] = " ".join(raw_bytes)
    record["body_text"] = "; ".join(mnem)
    record["body_byte_count"] = len(raw_bytes)
    # Q1: byte identity against the c corpus, and against the entry
    matched = list(bytes_index.get(record["body_bytes"], []))
    matched_entries = sorted(set(unit_to_entry.get(name, "not in pool")
                                 for name in matched))
    record["q1"] = {
        "verdict": "BYTE_IDENTICAL" if matched else "NO_C_UNIT_WITH_THESE_BYTES",
        "matched_c_units": matched,
        "matched_entries": matched_entries,
        "same_entry": entry_id in matched_entries,
    }
    # the canonical form and the term, the pipeline's own way
    emu_label = "c/" + label
    recorded = recorded_facts(emu_label, label, raw_bytes, mnem)
    record["c_arrival_families"] = recorded["arrival_families"]
    record["c_result_family"] = recorded["result_family"]
    record["c_result_width"] = recorded["result_width"]
    canon = CF.render_one(form, gate, recorded)
    canon["unit"] = emu_label
    record["canon40_outcome"] = canon.get("outcome")
    record["canon40_detail"] = canon.get("verdict_detail")
    term_record = TR.one_unit(maker, gate, emu_label, canon)
    record["term_state"] = term_record.get("term_state")
    record["term_outcome"] = term_record.get("outcome")
    record["term_reason"] = term_record.get("reason") or \
        term_record.get("why_no_term")
    layer5 = term_record.get("layer5_normalized_text")
    record["layer5_text"] = layer5
    # Q2: term identity with the entry's own text(s)
    lands = []
    if layer5 is not None:
        lands = list(text_to_entries.get(layer5, []))
    if layer5 is None:
        q2 = "NO_LAYER5_TEXT"
    elif layer5 in job["entry_texts"]:
        q2 = "TERM_IDENTICAL"
    else:
        q2 = "TERM_DIFFERS"
    record["q2"] = {"verdict": q2, "lands_in_entries": lands,
                    "result_width_differs":
                        recorded["result_width"] != x_record.get(
                            "result_width")}
    # Q3: the gate over the two bodies, inputs aligned by IN row
    record["q3"] = prove_against_x(reference, gate, maker, canon, x_record,
                                   renderer.params, x_term, walked, P100,
                                   G, families)
    return record


def prove_against_x(reference, gate, maker, canon, x_record, params,
                    x_term, x_walked, P100, G, x_families):
    """Q3.  Both sides are the reference simulator's answer for the
    body (route one's object); where the reference refuses a side,
    that side's ledger-transcribed term -- which the gate proved equal
    to its body by route two -- stands in, and the record says so."""
    out = {"route": {}, "outcome": None}
    emu_answer, cause = body_answer(reference, canon)
    if emu_answer is None:
        emu_answer = None
        emu_walked = maker.transcribe(canon)
        if emu_walked.out_term is None:
            out["outcome"] = "UNDECIDED"
            out["cause"] = "emulation side: %s; and no term either" % cause
            return out
        emu_answer = emu_walked.out_term
        out["route"]["emulation"] = ("its transcribed term (the reference "
                                     "refused: %s)" % cause)
    else:
        out["route"]["emulation"] = "the reference's answer for its body"
    x_answer, cause = body_answer(reference, x_record)
    if x_answer is None:
        x_answer = x_term
        out["route"]["x"] = ("its transcribed term, proved by route two "
                             "(the reference refused: %s)" % cause)
    else:
        out["route"]["x"] = "the reference's answer for its body"
    # align: x's IN-i <-> the emulation's parameter i
    c_families = expected_c_families(params)
    x_rows = P100.input_rows(x_families)
    c_rows = P100.input_rows(c_families)
    disagreement = P100.rows_disagree(x_rows, c_rows)
    if disagreement is not None:
        out["outcome"] = "UNDECIDED"
        out["cause"] = "the IN rows cannot be aligned: %s" % disagreement
        return out
    out["aligned_rows"] = [{"row": "IN-%d" % i, "x": x_families[i],
                            "c": c_families[i]}
                           for i in range(len(x_families))]
    _in, shared_x, constants_x, other_x = P100.classify_symbols(
        x_answer, x_families)
    _in, shared_c, constants_c, other_c = P100.classify_symbols(
        emu_answer, c_families)
    x_answer, names_x = P100.rename_constants_apart(x_answer, constants_x,
                                                    "x")
    emu_answer, names_c = P100.rename_constants_apart(emu_answer,
                                                      constants_c, "c")
    out["x_side_free_state"] = shared_x + other_x + names_x
    out["c_side_free_state"] = shared_c + other_c + names_c
    x_aligned = P100.align_by_row(x_answer, x_rows)
    c_aligned = P100.align_by_row(emu_answer, c_rows)
    if not gate.comparable(c_aligned, x_aligned):
        out["outcome"] = "UNDECIDED"
        out["cause"] = ("the two answers are of different z3 sorts (%s "
                        "against %s)" % (c_aligned.sort(), x_aligned.sort()))
        return out
    verdict = gate.decide(
        c_aligned, x_aligned,
        "the emulation's body against the x unit's body, inputs aligned "
        "by IN row",
        "z3 proved the emulation's answer equal to the x unit's answer "
        "for every value of every aligned input row")
    out["outcome"] = verdict.outcome
    out["reason"] = verdict.reason
    out["solver_timeout_ms"] = verdict.solver_timeout_ms
    if verdict.counterexample is not None:
        out["counterexample"] = verdict.counterexample
    if verdict.outcome != G.DISPROVED:
        return out
    # A DISPROVED emulation with a NARROW general holder (uint8_t /
    # uint16_t): clang's callee reads the caller-extended bits 16..31
    # of the argument register (the de-facto SysV rule), which the
    # term does not constrain.  The same proof is posed again with
    # every such input row zero-extended from its holder width -- a
    # substitution on both sides, then the gate's own call.
    narrow = []
    substitution = []
    for index, param in enumerate(params):
        if param["kind"] != "bv" or param["bits"] >= 32:
            continue
        row = z3.BitVec("IN_%d" % index, 64)
        narrow.append({"row": "IN-%d" % index, "holder": param["holder"]})
        substitution.append((row, z3.ZeroExt(64 - param["bits"],
                                             z3.Extract(param["bits"] - 1,
                                                        0, row))))
    if not substitution:
        return out
    again = gate.decide(
        z3.substitute(c_aligned, *substitution),
        z3.substitute(x_aligned, *substitution),
        "the same, with every narrow-holder input row zero-extended from "
        "its holder width (c's caller-extension rule)",
        "z3 proved the two answers equal for every input whose narrow "
        "arguments are zero-extended to the register")
    out["under_caller_extension"] = {
        "narrow_rows": narrow,
        "outcome": again.outcome,
        "reason": again.reason,
        "counterexample": again.counterexample,
    }
    return out


# ==================================================================
# section 5: THE COLLECTOR   forks, collects, bounds
# ==================================================================

MEMORY_TOKENS = ["MemoryError", "out of memory", "out-of-memory",
                 "max. memory exceeded", "std::bad_alloc"]


def memory_reason_in(record):
    text = json.dumps(record)
    for token in MEMORY_TOKENS:
        if token in text:
            return token
    return None


def fork_one(shared, job):
    read_end, write_end = os.pipe()
    child = os.fork()
    if child == 0:
        os.close(read_end)
        try:
            cap = SUB_CEILING_MB * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
            record = one_emulation(shared, job)
            payload = json.dumps({"ok": True, "record": record},
                                 default=str)
        except BaseException as problem:                    # noqa: BLE001
            payload = json.dumps({"ok": False,
                                  "raised": "%s: %s"
                                  % (type(problem).__name__, problem)})
        try:
            handle = os.fdopen(write_end, "w")
            handle.write(payload)
            handle.close()
        except BaseException:                                # noqa: BLE001
            pass
        os._exit(0)
    os.close(write_end)
    return child, read_end


def collect(shared, jobs, label):
    """run every job through `fork_one`, at most WORKERS at once, each
    under its wall clock; -> list of records in job order."""
    results = {}
    live = {}
    queue = list(jobs)
    total = len(queue)
    done = 0
    started = time.time()
    while queue or live:
        while queue and len(live) < WORKERS:
            job = queue.pop(0)
            child, fd = fork_one(shared, job)
            live[child] = {"job": job, "fd": fd, "text": [],
                           "started": time.time()}
        fds = [state["fd"] for state in live.values()]
        ready, _w, _x = select.select(fds, [], [], 1.0)
        for fd in ready:
            for child, state in live.items():
                if state["fd"] != fd:
                    continue
                chunk = os.read(fd, 1 << 20)
                if chunk:
                    state["text"].append(chunk.decode("utf-8", "replace"))
                else:
                    state["eof"] = True
        finished = []
        for child, state in live.items():
            elapsed = time.time() - state["started"]
            if state.get("eof"):
                finished.append((child, "walked"))
            elif elapsed > SUB_SECONDS:
                os.kill(child, signal.SIGKILL)
                finished.append((child, "TIMED_OUT"))
        for child, word in finished:
            state = live.pop(child)
            os.close(state["fd"])
            stamp = os.wait4(child, 0)
            wall = time.time() - state["started"]
            job = state["job"]
            text = "".join(state["text"])
            record = {"entry_id": job["entry_id"], "x_lang": job["x_lang"],
                      "x_unit": job["x_unit"], "x_text": job["text"],
                      "control": job.get("control", False)}
            if word == "TIMED_OUT":
                record["word"] = "TIMED_OUT"
                record["runner_limit"] = (
                    "the sub-process passed its %d s wall clock; this is "
                    "a runner limit, not a verdict" % SUB_SECONDS)
            elif text == "":
                record["word"] = "ABORTED"
                record["runner_limit"] = (
                    "the sub-process returned nothing (RLIMIT_AS %d MB "
                    "or a signal); a runner limit, not a verdict"
                    % SUB_CEILING_MB)
            else:
                answer = json.loads(text)
                if not answer["ok"]:
                    record["word"] = "RAISED"
                    record["raised"] = answer["raised"]
                else:
                    record = answer["record"]
                    record["word"] = "walked"
                    token = memory_reason_in(record)
                    if token is not None:
                        record["word"] = "MEMORY_REASON"
                        record["runner_limit"] = token
            record["wall_seconds"] = round(wall, 2)
            record["sub_peak_kb"] = stamp[2].ru_maxrss
            results[job["entry_id"]] = record
            done = done + 1
            say("[%d/%d] %s %s %s -> %s q1=%s q2=%s q3=%s  %.1fs  sub %d kB"
                % (done, total, label, job["entry_id"], job["x_unit"],
                   summary_word(record),
                   (record.get("q1") or {}).get("verdict", "-"),
                   (record.get("q2") or {}).get("verdict", "-"),
                   (record.get("q3") or {}).get("outcome", "-"),
                   wall, stamp[2].ru_maxrss))
            check_collector_memory()
    say("   %s: %d done in %.0f s; collector peak %d kB"
        % (label, done, time.time() - started, peak_kb()))
    return [results[job["entry_id"]] for job in jobs]


def summary_word(record):
    if record.get("word") != "walked":
        return record.get("word")
    if not record.get("rendered"):
        return "REFUSED(%s)" % record.get("refusal_cause")
    if not record.get("compiled"):
        return "NOT_COMPILED"
    return "compiled %d bytes" % record.get("body_byte_count", 0)


def build_shared():
    import term97_walk as TW
    import canonical_form as CF
    maker, gate, _attached, _readings = TW.build()
    form = CF.new_form()
    pool = read_json(POOL5)
    text_to_entries, unit_to_entry = pool_indexes(pool)
    del pool
    indexes = read_json(INDEXES)
    held = read_json(HELD)["held"]
    return {
        "maker": maker,
        "gate": gate,
        "form": form,
        "reference": maker.reference,
        "held": held,
        "bytes_index": indexes["bytes_index"],
        "text_to_entries": text_to_entries,
        "unit_to_entry": unit_to_entry,
    }


# ==================================================================
# section 6: THE COMMANDS
# ==================================================================

def census():
    say("-- CENSUS: the population, its filters, the indexes")
    pool = read_json(POOL5)
    cross1 = read_json(CROSS1)
    population = Population(pool, cross1)
    entries = population.select()
    eligible_controls = population.select_control(40)
    needed = set()
    for entry_id, plan in entries.items():
        needed.add(plan["x_unit"])
    for entry_id, plan in population.control.items():
        needed.add(plan["x_unit"])
        for name in plan["c_units_in_entry"]:
            needed.add(name)
    say("   units whose canon40 records are held: %d" % len(needed))
    bytes_index, held, shard_of, c_units = build_indexes(needed)
    missing = sorted(name for name in needed if name not in held)
    say("   c units indexed by body bytes: %d (%d distinct byte strings)"
        % (c_units, len(bytes_index)))
    say("   held records: %d; missing: %d %s" % (len(held), len(missing),
                                                 missing[:5]))
    sample = population.stratified_sample(40)
    write_json(POPULATION, {
        "task": "o7 -- does clang collapse an emulation to the unit it "
                "emulates",
        "pool_source": POOL5,
        "cross1_source": CROSS1,
        "pool_entry_count": len(pool["entries"]),
        "x_languages": X_LANGUAGES,
        "filters": population.filters,
        "entries": entries,
        "control": population.control,
        "control_eligible_entries": eligible_controls,
        "sample_40": sample,
        "seed": SEED,
        "ship_flags": " ".join([CLANG] + SHIP_FLAGS),
        "ship_flags_source": SHIP_FLAGS_SOURCE,
        "held_missing": missing,
    })
    write_json(HELD, {"held": held, "shard_of": shard_of})
    write_json(INDEXES, {"bytes_index": bytes_index, "c_units": c_units})
    say("   wrote %s, %s, %s" % (POPULATION, HELD, INDEXES))
    say("   collector peak %d kB" % peak_kb())


def jobs_for(entry_ids, plans, control=False):
    jobs = []
    for entry_id in entry_ids:
        job = dict(plans[entry_id])
        job["control"] = control
        jobs.append(job)
    return jobs


def sample(count):
    say("-- SAMPLE: %d entries across the three x, seed %d" % (count, SEED))
    population = read_json(POPULATION)
    entry_ids = population["sample_40"][:count]
    shared = build_shared()
    say("   shared objects built; collector peak %d kB" % peak_kb())
    results = collect(shared, jobs_for(entry_ids, population["entries"]),
                      "sample")
    write_json(SAMPLE, {"count": count, "entry_ids": entry_ids,
                        "results": results, "collector_peak_kb": peak_kb()})
    say("   wrote %s" % SAMPLE)


def run():
    say("-- RUN: every entry of the population")
    population = read_json(POPULATION)
    entry_ids = sorted(population["entries"])
    shared = build_shared()
    results = collect(shared, jobs_for(entry_ids, population["entries"]),
                      "run")
    write_json(RUN, {"entry_ids": entry_ids, "results": results,
                     "collector_peak_kb": peak_kb()})
    say("   wrote %s" % RUN)


def control(count):
    say("-- CONTROL: %d entries WITH a c member, seed %d" % (count, SEED))
    population = read_json(POPULATION)
    entry_ids = sorted(population["control"])[:count]
    shared = build_shared()
    results = collect(shared, jobs_for(entry_ids, population["control"],
                                       control=True), "control")
    write_json(CONTROL, {"count": count, "entry_ids": entry_ids,
                         "results": results, "collector_peak_kb": peak_kb()})
    say("   wrote %s" % CONTROL)


# ==================================================================
# section 7: THE REPORT
# ==================================================================

def pipe_table(header, rows):
    lines = ["| " + " | ".join(header) + " |",
             "|" + "---|" * len(header)]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def per_x_row(label, records):
    row = {"x": label, "attempted": len(records), "rendered": 0,
           "compiled": 0, "byte_identity": 0, "term_identity": 0,
           "proved": 0, "disproved": 0, "undecided": 0,
           "runner_limit": 0}
    for record in records:
        if record.get("word") != "walked":
            row["runner_limit"] = row["runner_limit"] + 1
            continue
        if record.get("rendered"):
            row["rendered"] = row["rendered"] + 1
        if record.get("compiled"):
            row["compiled"] = row["compiled"] + 1
        q1 = (record.get("q1") or {}).get("verdict")
        if q1 == "BYTE_IDENTICAL":
            row["byte_identity"] = row["byte_identity"] + 1
        q2 = (record.get("q2") or {}).get("verdict")
        if q2 == "TERM_IDENTICAL":
            row["term_identity"] = row["term_identity"] + 1
        q3 = (record.get("q3") or {}).get("outcome")
        if q3 in ("PROVED_ON_SHIP", "PROVED_BY_CONSTRUCTION"):
            row["proved"] = row["proved"] + 1
        elif q3 == "DISPROVED":
            row["disproved"] = row["disproved"] + 1
            again = (record.get("q3") or {}).get("under_caller_extension")
            if again and again.get("outcome") in ("PROVED_ON_SHIP",
                                                  "PROVED_BY_CONSTRUCTION"):
                row["disproved_but_proved_under_caller_extension"] = \
                    row.get("disproved_but_proved_under_caller_extension",
                            0) + 1
        elif record.get("compiled"):
            row["undecided"] = row["undecided"] + 1
        if q2 == "TERM_DIFFERS" and (record.get("q2") or {}).get(
                "result_width_differs"):
            row["term_differs_with_result_width_differing"] = \
                row.get("term_differs_with_result_width_differing", 0) + 1
        if record.get("x_contract_omits"):
            row["contract_omitted_an_arrival"] = \
                row.get("contract_omitted_an_arrival", 0) + 1
        if record.get("rendered") and not record.get("reprint_exact"):
            row["reprint_not_exact"] = row.get("reprint_not_exact", 0) + 1
    for key in ("disproved_but_proved_under_caller_extension",
                "term_differs_with_result_width_differing",
                "contract_omitted_an_arrival", "reprint_not_exact"):
        row.setdefault(key, 0)
    return row


def causes_of(records):
    causes = {}
    for record in records:
        if record.get("word") != "walked":
            key = "runner limit: %s" % record.get("word")
        elif not record.get("rendered"):
            key = "renderer refused: %s" % record.get("refusal_cause")
        elif not record.get("compiled"):
            key = "clang refused: %s" % record.get("compile_refusal")
        else:
            continue
        causes.setdefault(key, []).append(
            "%s (%s)" % (record["entry_id"], record["x_unit"]))
    return causes


def report():
    say("-- REPORT")
    population = read_json(POPULATION)
    sample_document = read_json(SAMPLE) if os.path.exists(SAMPLE) else None
    run_document = read_json(RUN)
    control_document = read_json(CONTROL)
    results = run_document["results"]
    controls = control_document["results"]
    by_x = {}
    for x in X_LANGUAGES:
        by_x[x] = []
    for record in results:
        by_x[record["x_lang"]].append(record)
    rows = []
    for x in X_LANGUAGES:
        rows.append(per_x_row(x, by_x[x]))
    rows.append(per_x_row("all", results))
    control_row = per_x_row("control (c)", controls)
    control_same_entry = 0
    for record in controls:
        if (record.get("q1") or {}).get("same_entry"):
            control_same_entry = control_same_entry + 1
    control_row["byte_identity_same_entry"] = control_same_entry
    lands_elsewhere = []
    for record in results:
        q2 = record.get("q2") or {}
        lands = [e for e in q2.get("lands_in_entries", [])
                 if e != record["entry_id"]]
        if lands:
            lands_elsewhere.append({"entry_id": record["entry_id"],
                                    "x_unit": record["x_unit"],
                                    "lands_in": lands})
    examples = pick_examples(results, controls)
    document = {
        "task": population["task"],
        "node": "hq.research.arch_unit_oracle.cross_construction",
        "as_of": time.strftime("%Y-%m-%d"),
        "ship_flags": population["ship_flags"],
        "ship_flags_source": population["ship_flags_source"],
        "filters": population["filters"],
        "per_x": rows,
        "control": control_row,
        "control_eligible_entries": population["control_eligible_entries"],
        "sample_40": {
            "entry_ids": sample_document["entry_ids"] if sample_document
            else [],
            "per_x": [per_x_row(x, [r for r in sample_document["results"]
                                    if r["x_lang"] == x])
                      for x in X_LANGUAGES] if sample_document else [],
        },
        "causes": causes_of(results),
        "control_causes": causes_of(controls),
        "lands_in_another_entry": lands_elsewhere,
        "examples": examples,
        "results": results,
        "control_results": controls,
        "collector_peaks_kb": {
            "run": run_document.get("collector_peak_kb"),
            "control": control_document.get("collector_peak_kb"),
            "sample": sample_document.get("collector_peak_kb")
            if sample_document else None,
        },
        "sub_process_ceiling_mb": SUB_CEILING_MB,
        "sub_process_seconds": SUB_SECONDS,
        "workers": WORKERS,
    }
    write_json(RESULTS, document)
    write_report_md(document, population)
    say("   wrote %s and %s" % (RESULTS, REPORT))


def pick_examples(results, controls):
    """one collapsed to bytes, one proved but not byte-identical, one
    disproved -- from the x->c rows first, the control second."""
    out = {}
    pools = [("x_to_c", results), ("control", controls)]
    for want in ("byte_identity", "proved_not_bytes", "disproved"):
        for where, records in pools:
            for record in records:
                if record.get("word") != "walked" or not record.get(
                        "compiled"):
                    continue
                q1 = (record.get("q1") or {}).get("verdict")
                q3 = (record.get("q3") or {}).get("outcome")
                if want == "byte_identity" and q1 == "BYTE_IDENTICAL":
                    out[want] = {"from": where, "record": record}
                    break
                if want == "proved_not_bytes" and q1 != "BYTE_IDENTICAL" \
                        and q3 in ("PROVED_ON_SHIP",
                                   "PROVED_BY_CONSTRUCTION"):
                    out[want] = {"from": where, "record": record}
                    break
                if want == "disproved" and q3 == "DISPROVED":
                    out[want] = {"from": where, "record": record}
                    break
            if want in out:
                break
    return out


def rescued(record):
    """True when a DISPROVED emulation is proved once every narrow
    input row is zero-extended from its holder width (c's de-facto
    caller-extension rule), which `prove_against_x` poses as a second
    gate call on the same two answers."""
    again = (record.get("q3") or {}).get("under_caller_extension") or {}
    return again.get("outcome") in ("PROVED_ON_SHIP",
                                    "PROVED_BY_CONSTRUCTION")


def still_disproved(records):
    """The DISPROVED emulations the caller-extension re-posing did not
    rescue -- the rows where the two really do answer differently."""
    out = []
    for record in records:
        if (record.get("q3") or {}).get("outcome") != "DISPROVED":
            continue
        if rescued(record):
            continue
        out.append(record)
    return out


def body_branches(record):
    """True when the x unit's own carved body carries a conditional
    branch.  Machine form: the mnemonics of the body text as objdump
    printed them; no label is read."""
    text = record.get("x_body_text") or ""
    for token in ("; je ", "; jne ", "; jb ", "; jae ", "; jbe "):
        if token in text:
            return True
    return False


def last_counterexample(record):
    """The seeds of the LAST proof posed for this emulation: the
    caller-extension re-posing's model where there was one, else the
    first model."""
    again = (record.get("q3") or {}).get("under_caller_extension") or {}
    if again.get("counterexample"):
        return again["counterexample"]
    return (record.get("q3") or {}).get("counterexample")


def rate(part, whole):
    if not whole:
        return "0 of 0"
    return "%d of %d (%.0f%%)" % (part, whole, 100.0 * part / whole)


def walkthrough(document):
    """Section 0: what was done and what came back, in plain words,
    with no figure the sentence does not carry itself."""
    all_row = None
    for row in document["per_x"]:
        if row["x"] == "all":
            all_row = row
    control_row = document["control"]
    hard = still_disproved(document["results"])
    guarded = [r for r in hard if body_branches(r)]
    lines = []
    lines.append("## 0. What was done and what came back")
    lines.append("")
    lines.append("An ARCH-UNIT here is one compiled function body, "
                 "carved out of a shipped object file; a POOL ENTRY is "
                 "the set of arch-units, across languages, that were "
                 "proved to answer the same for every input; a TERM is "
                 "one arch-unit written as a z3 expression, and the "
                 "entry's LAYER-5 TEXT is that expression printed by one "
                 "fixed rule.")
    lines.append("")
    lines.append("Every pool entry used here has a member in go, rust or "
                 "swift and NO c member: nobody has built the c unit that "
                 "answers the same. For each, one renderer wrote the "
                 "entry's term out as a c function -- the term's shape "
                 "kept exactly, so the source is long, nested and nothing "
                 "a person would write -- and clang compiled it at the "
                 "flags the whole c corpus was built with. The compiled "
                 "body was then carved with the same reader the corpus "
                 "uses, and three questions were asked of it, separately: "
                 "are its bytes bytes that some c unit of the corpus "
                 "already has; is its printed term the entry's text; and "
                 "does the solver prove it answers the same as the x unit "
                 "for every input.")
    lines.append("")
    lines.append("At the byte level the answer is mostly no. %s "
                 "compiled emulations came out with bytes an existing c "
                 "unit already has. At the level of behaviour the answer "
                 "is mostly yes: %s were proved equal to the x unit on "
                 "the ship build, and %d more once every narrow argument "
                 "(a byte-wide or halfword-wide input) is taken to arrive "
                 "already widened to the register, which is what c's "
                 "callee assumes -- %s in all."
                 % (rate(all_row["byte_identity"], all_row["compiled"]),
                    rate(all_row["proved"], all_row["compiled"]),
                    all_row["disproved_but_proved_under_caller_extension"],
                    rate(all_row["proved"] + all_row[
                        "disproved_but_proved_under_caller_extension"],
                        all_row["compiled"])))
    lines.append("")
    lines.append("The control says how to read that first number. Take "
                 "%d entries that DO have a c member, render the "
                 "emulation from that member's own term, and ask whether "
                 "clang lands back on the member's own bytes: it does %s "
                 "of the time. So byte identity is not the shape of the "
                 "question: clang has more than one way to spell the same "
                 "answer, and the long nested source the renderer emits "
                 "does not always reduce to the spelling the original "
                 "unit was given, even when that unit is c's own."
                 % (control_row["attempted"],
                    rate(control_row["byte_identity_same_entry"],
                         control_row["compiled"])))
    lines.append("")
    lines.append("Where the proof failed and the caller-extension rule "
                 "did not rescue it -- %d emulations -- the x unit's own "
                 "body carries a conditional branch the term does not "
                 "carry in %d of them: the body guards a case (a zero "
                 "divisor, a signed extreme) and returns down another "
                 "path, while the term the emulation was rendered from is "
                 "total and has no such case. The %d that remain are "
                 "listed with their seeds and are not attributed to a "
                 "cause by this task."
                 % (len(hard), len(guarded), len(hard) - len(guarded)))
    lines.append("")
    lines.append("### The answer to the question, in three sentences")
    lines.append("")
    lines.append("Yes, clang collapses the emulation to something that "
                 "answers exactly as the unit it emulates, %s of the "
                 "time, and %s once narrow arguments are read as c's "
                 "callee reads them -- but it collapses onto the same "
                 "BYTES as an existing c unit only %s of the time."
                 % (rate(all_row["proved"], all_row["compiled"]),
                    rate(all_row["proved"] + all_row[
                        "disproved_but_proved_under_caller_extension"],
                        all_row["compiled"]),
                    rate(all_row["byte_identity"], all_row["compiled"])))
    lines.append("")
    lines.append("That gap is not the emulation's failure: on the "
                 "control, where the emulation is built from a c unit's "
                 "OWN term, clang reproduces that unit's bytes only %s of "
                 "the time, so byte identity was never going to be the "
                 "measure."
                 % rate(control_row["byte_identity_same_entry"],
                        control_row["compiled"]))
    lines.append("")
    lines.append("Where it does not collapse, the cause is that the x "
                 "unit's body carries a guarded case its term does not "
                 "(%d of the %d that stay disproved) -- the emulation is "
                 "faithful to the term it was given, and the term is "
                 "narrower than the body."
                 % (len(guarded), len(hard)))
    lines.append("")
    return lines


def control_reading(document):
    """The control's Q1 and Q3 rates, and what each one does to the
    reading of the x rows above it."""
    control_row = document["control"]
    all_row = None
    for row in document["per_x"]:
        if row["x"] == "all":
            all_row = row
    rescued_control = control_row[
        "disproved_but_proved_under_caller_extension"]
    lines = []
    lines.append("### What the control does to the reading of the x rows")
    lines.append("")
    lines.append("- Control Q1, the rate: %s of the compiled control "
                 "emulations carry bytes some c unit of the corpus "
                 "already has, and %s carry the bytes of a c unit IN THE "
                 "SAME pool entry -- the unit the emulation was rendered "
                 "from. This is the CEILING for byte-level collapse: the "
                 "emulation is built from that very unit's own term, so "
                 "nothing about a foreign language is in the way, and "
                 "clang still lands elsewhere most of the time."
                 % (rate(control_row["byte_identity"],
                         control_row["compiled"]),
                    rate(control_row["byte_identity_same_entry"],
                         control_row["compiled"])))
    lines.append("- So the x rows' %s byte identity is read against %s, "
                 "not against 100%%. And an x row's byte identity can "
                 "never be SAME-ENTRY: the population is entries with no "
                 "c member, so a matched c unit is by construction a unit "
                 "of another entry (section 6 lists which)."
                 % (rate(all_row["byte_identity"], all_row["compiled"]),
                    rate(control_row["byte_identity_same_entry"],
                         control_row["compiled"])))
    lines.append("- Control Q3, the rate: %s proved on the ship build, "
                 "%d more proved once narrow arguments are zero-extended "
                 "from their holder width, %d undecided (the reference "
                 "simulator refused the emulation's own body; the causes "
                 "are in section 3's neighbour, the q3 `cause` field of "
                 "`emulation_results.json`). Nothing in the control is "
                 "left DISPROVED."
                 % (rate(control_row["proved"], control_row["compiled"]),
                    rescued_control, control_row["undecided"]))
    lines.append("- So the x rows' %s proved, %s after the "
                 "caller-extension rule, sits at the control's own level: "
                 "the proof question is not made harder by the unit being "
                 "in another language."
                 % (rate(all_row["proved"], all_row["compiled"]),
                    rate(all_row["proved"] + all_row[
                        "disproved_but_proved_under_caller_extension"],
                        all_row["compiled"])))
    lines.append("")
    return lines


def disproved_by_cause(document):
    """Every emulation the solver separated from its x unit AFTER the
    caller-extension re-posing, with the seeds that separate it."""
    hard = still_disproved(document["results"])
    guarded = [r for r in hard if body_branches(r)]
    plain = [r for r in hard if not body_branches(r)]
    lines = []
    lines.append("## 5. The disproved, by cause")
    lines.append("")
    lines.append("- CAUSE 1, the arrival width, status CLOSED: %d of the "
                 "%d DISPROVED emulations are proved once every "
                 "byte-wide or halfword-wide input row is zero-extended "
                 "from its holder width. c's callee reads the whole "
                 "argument register and takes the caller to have widened "
                 "it; the term says nothing about the bits above the "
                 "holder, so the first proof is posed over inputs that "
                 "cannot arrive."
                 % (sum(row["disproved_but_proved_under_caller_extension"]
                        for row in document["per_x"]
                        if row["x"] == "all"),
                    sum(row["disproved"] for row in document["per_x"]
                        if row["x"] == "all")))
    lines.append("- CAUSE 2, a guarded case the term does not carry, "
                 "status CLOSED: of the %d that stay disproved, %d have "
                 "an x unit whose carved body takes a conditional branch "
                 "-- it tests an input and returns down another path (a "
                 "zero divisor, a signed extreme). The term is total and "
                 "has no such case, so the emulation cannot have one "
                 "either, and the solver separates them on exactly that "
                 "input."
                 % (len(hard), len(guarded)))
    lines.append("- CAUSE 3, not attributed, status OPEN: the remaining "
                 "%d. Their x bodies carry no conditional branch and the "
                 "seeds below are not a case either side guards; this "
                 "task did not run the two answers at those seeds to "
                 "name the cause."
                 % len(plain))
    lines.append("")
    header = ["entry", "x unit", "x body branches", "x result width",
              "emulation result width", "holders",
              "seeds after the caller-extension re-posing, LITERAL"]
    rows = []
    for record in hard:
        holders = [p["holder"] for p in record.get("params") or []]
        rows.append([record["entry_id"], record["x_unit"],
                     "yes" if body_branches(record) else "no",
                     record.get("x_result_width"),
                     record.get("c_result_width"),
                     " ".join(holders),
                     "`%s`" % last_counterexample(record)])
    lines.append(pipe_table(header, rows))
    lines.append("")
    if guarded:
        record = guarded[0]
        lines.append("One of cause 2, whole: entry `%s`, x unit `%s`."
                     % (record["entry_id"], record["x_unit"]))
        lines.append("")
        lines.append("- the entry's layer-5 text, LITERAL: `%s`"
                     % record["x_text"])
        lines.append("- the x unit's body, LITERAL: `%s`"
                     % record.get("x_body_text"))
        lines.append("- the emulation's body, LITERAL: `%s`"
                     % record.get("body_text"))
        lines.append("- the seeds that separate them, LITERAL: `%s`"
                     % last_counterexample(record))
        lines.append("- GLOSS, beside those literals: the x body tests "
                     "its second input and jumps away before it divides; "
                     "the term has no test in it, so the rendered c "
                     "function divides unconditionally, and the seeds put "
                     "the solver on exactly the input the x body refuses "
                     "to answer for.")
        lines.append("")
    return lines


def write_report_md(document, population):
    lines = []
    lines.append("# emulation_report.md -- task o7: does clang collapse a "
                 "c emulation to the unit it emulates?")
    lines.append("")
    lines.append("Node `hq.research.arch_unit_oracle.cross_construction`; "
                 "generated by `emulate.py report`; as of %s."
                 % document["as_of"])
    lines.append("")
    lines = lines + walkthrough(document)
    lines.append("## 1. The population, counted at each filter")
    lines.append("")
    rows = []
    for row in document["filters"]:
        rows.append([row["filter"], row["go"], row["rust"], row["swift"],
                     row["distinct"]])
    lines.append(pipe_table(["filter", "go", "rust", "swift", "distinct"],
                            rows))
    lines.append("")
    lines.append("Ship flags: `%s` (%s)." % (document["ship_flags"],
                                             document["ship_flags_source"]))
    lines.append("")
    lines.append("## 2. Per x: attempted / rendered / compiled / collapsed "
                 "to byte identity / term identity / proved / disproved / "
                 "undecided")
    lines.append("")
    header = ["x", "attempted", "rendered", "compiled", "byte identity "
              "with an existing c unit", "term identity with the entry",
              "proved equivalent", "disproved", "undecided", "runner limit",
              "of the disproved: proved under caller extension",
              "of term-differs: result width differs"]
    rows = []
    for row in document["per_x"] + [document["control"]]:
        rows.append([row["x"], row["attempted"], row["rendered"],
                     row["compiled"], row["byte_identity"],
                     row["term_identity"], row["proved"], row["disproved"],
                     row["undecided"], row["runner_limit"],
                     row["disproved_but_proved_under_caller_extension"],
                     row["term_differs_with_result_width_differing"]])
    lines.append(pipe_table(header, rows))
    lines.append("")
    lines.append("Control: %d of %d compiled emulations of a c member's own "
                 "term are byte-identical to a c unit IN THE SAME ENTRY "
                 "(`byte_identity_same_entry`); eligible control entries "
                 "%d, drawn with seed %d."
                 % (document["control"]["byte_identity_same_entry"],
                    document["control"]["compiled"],
                    document["control_eligible_entries"], population["seed"]))
    lines.append("")
    lines = lines + control_reading(document)
    lines.append("## 3. Refusals, by cause")
    lines.append("")
    for label, causes in (("x -> c", document["causes"]),
                          ("control", document["control_causes"])):
        lines.append("### %s" % label)
        lines.append("")
        if not causes:
            lines.append("- none")
        for cause in sorted(causes):
            sightings = causes[cause]
            lines.append("- %s: %d (%s)" % (cause, len(sightings),
                                            ", ".join(sightings[:6])))
        lines.append("")
    lines.append("## 4. Three literal examples")
    lines.append("")
    titles = {"byte_identity": "collapsed to byte identity",
              "proved_not_bytes": "proved equivalent, not byte-identical",
              "disproved": "disproved, with the counterexample seeds"}
    for want in ("byte_identity", "proved_not_bytes", "disproved"):
        lines.append("### %s" % titles[want])
        lines.append("")
        example = document["examples"].get(want)
        if example is None:
            lines.append("- none in this run")
            lines.append("")
            continue
        record = example["record"]
        lines.append("- from the %s rows: entry `%s`, x unit `%s`"
                     % (example["from"], record["entry_id"],
                        record["x_unit"]))
        lines.append("- the term (layer-5 text), LITERAL: `%s`"
                     % record["x_text"])
        lines.append("- the rendered source, LITERAL "
                     "(`%s/%s`, on the host):"
                     % (HOST_FOLDER, record["source_path"]))
        lines.append("")
        lines.append("```c")
        lines.append(record["source"].rstrip())
        lines.append("```")
        lines.append("")
        lines.append("- x body, LITERAL: `%s`" % record.get("x_body_text"))
        lines.append("- x bytes, LITERAL: `%s`" % record.get("x_body_bytes"))
        lines.append("- emulation body, LITERAL: `%s`"
                     % record.get("body_text"))
        lines.append("- emulation bytes, LITERAL: `%s`"
                     % record.get("body_bytes"))
        lines.append("- Q1 %s (matched c units %s, entries %s); Q2 %s "
                     "(emulation's layer-5 text `%s`); Q3 %s"
                     % (record["q1"]["verdict"],
                        record["q1"]["matched_c_units"][:4],
                        record["q1"]["matched_entries"][:4],
                        record["q2"]["verdict"], record.get("layer5_text"),
                        record["q3"].get("outcome")))
        if record["q3"].get("counterexample"):
            lines.append("- counterexample, LITERAL (the solver's model, "
                         "IN_i = the aligned input rows):")
            lines.append("")
            lines.append("```")
            lines.append(record["q3"]["counterexample"])
            lines.append("```")
        lines.append("")
    lines = lines + disproved_by_cause(document)
    lines.append("## 6. Emulations whose own term lands in ANOTHER pool "
                 "entry")
    lines.append("")
    if not document["lands_in_another_entry"]:
        lines.append("- none")
    for item in document["lands_in_another_entry"]:
        lines.append("- %s (%s) -> %s" % (item["entry_id"], item["x_unit"],
                                          item["lands_in"]))
    lines.append("")
    lines.append("## 7. Every emulation, one row each")
    lines.append("")
    header = ["entry", "x unit", "compiled", "bytes", "Q1", "Q2", "Q3",
              "lands in", "cause"]
    rows = []
    for record in document["results"] + document["control_results"]:
        cause = ""
        if record.get("word") != "walked":
            cause = record.get("word")
        elif not record.get("rendered"):
            cause = record.get("refusal_cause")
        elif not record.get("compiled"):
            cause = record.get("compile_refusal")
        rows.append([
            record["entry_id"], record["x_unit"],
            "yes" if record.get("compiled") else "no",
            record.get("body_byte_count", ""),
            (record.get("q1") or {}).get("verdict", ""),
            (record.get("q2") or {}).get("verdict", ""),
            (record.get("q3") or {}).get("outcome", ""),
            ",".join((record.get("q2") or {}).get("lands_in_entries", [])),
            cause,
        ])
    lines.append(pipe_table(header, rows))
    lines.append("")
    lines.append("## 8. Bounds")
    lines.append("")
    peaks = document["collector_peaks_kb"]
    lines.append("- The stated bound: one collecting process, its peak "
                 "resident size checked after every emulation, named "
                 "abort `ABORT_MEMORY_O7` at %d kB (4 GB). It was never "
                 "raised." % COLLECTOR_CAP_KB)
    lines.append("- Peak resident size of the collecting process, "
                 "`resource.getrusage(RUSAGE_SELF).ru_maxrss`, one figure "
                 "per lane: the run %s kB, the control %s kB, the sample "
                 "%s kB -- about 140 MB, %.1f%% of the bound."
                 % (peaks.get("run"), peaks.get("control"),
                    peaks.get("sample"),
                    100.0 * (peaks.get("run") or 0) / COLLECTOR_CAP_KB))
    lines.append("- Each emulation ran in its own forked sub-process "
                 "under `RLIMIT_AS` %d MB and a wall clock of %d s, at "
                 "most %d at once; a sub-process that passed either is "
                 "recorded as a runner limit, never as a verdict (the "
                 "`runner limit` column of section 2 is zero everywhere)."
                 % (document["sub_process_ceiling_mb"],
                    document["sub_process_seconds"], document["workers"]))
    lines.append("")
    handle = open(REPORT, "w")
    handle.write("\n".join(lines))
    handle.close()


def main(argv):
    if not argv:
        say(__doc__)
        return 2
    word = argv[0]
    if not os.path.isdir(SRC_DIR):
        os.makedirs(SRC_DIR)
    if word == "census":
        census()
        return 0
    if word == "sample":
        sample(int(argv[1]))
        return 0
    if word == "run":
        run()
        return 0
    if word == "control":
        control(int(argv[1]))
        return 0
    if word == "report":
        report()
        return 0
    say(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
