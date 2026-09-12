#!/usr/bin/env python3
"""render_general.py -- THE GENERAL RENDER: any term written in a target
as a SEQUENCE OF NAMED INTERMEDIATES, one variable per node, the
language's own operator where it has one and the construction where it
does not.

Node: hq.research.arch_unit_oracle.cross_construction.autopoly.
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_t4_brief.md`.

THE ALGORITHM, which is the brief's own, restated exactly:

    render_general(term, lang):
        for node in term, leaves first:
            if lang has node.kind at node.width:      # whoever gets there first
                emit the language's operator          # tier 1, unchanged
            else:
                emit construction[node.kind](width, W)
                over the node's children's names
        return the source

THE OBJECTS, one sentence each, in relation.
  * A NAMED INTERMEDIATE is one local variable of the rendered source
    holding one node's value: `uint64_t v17 = v16 ^ v9;` in c, `let
    v17: u64 = ...` in rust, `var v17 uint64 = ...` in go, `let v17:
    UInt64 = ...` in swift.  Every node of the term gets one, so a node
    read three times is WRITTEN ONCE -- which is the whole difference
    between this render and the one before it, where a term whose steps
    read their own previous step three times was written out 3^width
    times (task t2's log_257 section 6.2).
  * THE TEST "does the language have this kind at this width" is
    MACHINE FORM and is the target's own renderer: the node is offered
    to it with its children already bound to names, and the answer is
    whether it refuses.  There is no table of operator tokens anywhere
    in this file, and none is possible -- the renderer is asked about a
    z3 node, not about a spelling.
  * A CONSTRUCTED NODE is one the target's renderer refused: `build.py`
    gives the same mapping as a term over the primitive set at the
    target's word, and THAT term is then walked by this same loop, so
    its own nodes become named intermediates too.  The composition is
    one loop and not two.
  * THE POLICY says which of the two is tried first.  `native_first` is
    the brief's own rule and the route of record.  `all_constructed`
    offers the construction at EVERY node whose kind has one, and is
    the GUARANTEE's own measurement: it says what the primitive set
    reaches when the language's own operator is not allowed to answer.
  * A TRAPPING NODE is a node whose operator, in THIS target, can stop
    the program instead of answering: division and remainder on go and
    on swift (the zero divisor, and on swift the signed extreme too),
    and the float-to-integer conversion on swift.  Each one is a node
    kind the target's OWN renderer already marks as an edge region, and
    the set is read off those renderers and named by z3's own
    declaration kinds below; there is no source token in it.
  * A REGION is one nested scope of the rendered body: region 0 is the
    function body, and a conditional written as control flow opens one
    region per arm, whose super-region is the region the conditional
    itself is written in.

THE ONE RULE ADDED BY TASK rd1, which is that task's brief restated:

    when a conditional's branch (transitively) contains a trapping
    node, the conditional is written as CONTROL FLOW --
    `if cond { <the then arm's nodes> } else { <the else arm's
    nodes> }`, each arm's nodes computed INSIDE its arm -- so the guard
    DOMINATES the operation.  Otherwise the conditional stays a select
    over values already computed.  A node whose readers are not all
    inside one arm stays hoisted above the conditional.

WHY.  Every node used to be evaluated eagerly and a conditional printed
as a select over values already computed, so a division the term GUARDS
ran unguarded: `v0 = b / a` was written BEFORE `sel64(a == 0, ...)` in
`emulations_riscv64/div_gpr_gpr_gpr_64__reg_a0__go__native_first.go`,
and on go that traps at a = 0 where the cell answers all ones.  THE TERM
IS UNCHANGED and only the printed ORDER is, so the Lean statement
(`lean_general.py`) is untouched: it states the term, not the order.

MEMORY: this file holds the term, the statements and one memo; it forks
nothing and reads no store.  The caller states the bound.

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

HOW THIS FILE OBEYS IT.  Which route a node takes is decided by whether
the TARGET'S OWN RENDERER raises, which is a property of the z3 node and
the target, and by nothing that is written anywhere as a token.

Coding discipline: no compound one-liner statements.
"""

import os
import re

import z3

import build as B


CAUSE_TOO_LARGE = ("the constructed source is larger than the ceiling "
                   "this task states: one statement per node, measured "
                   "before anything is written")
CAUSE_ANSWER_WIDE = ("the answer home is wider than the target's widest "
                     "holder, so the value cannot be answered with at "
                     "all -- a question about the answer contract and "
                     "not about the operation")
CAUSE_NO_ROUTE = ("neither the target's own operator nor a construction "
                  "answers this node")


# ==================================================================
# section 0: the trapping node, and the regions a guard opens
# ==================================================================

def declaration_kinds(*names):
    """z3's own declaration-kind constants, by z3's own names, skipping
    any this z3 build does not carry."""
    out = []
    for name in names:
        got = getattr(z3, name, None)
        if got is None:
            continue
        out.append(got)
        continue
    return tuple(out)


DIVIDING_KINDS = declaration_kinds(
    "Z3_OP_BUDIV", "Z3_OP_BUDIV_I", "Z3_OP_BUREM", "Z3_OP_BUREM_I",
    "Z3_OP_BSDIV", "Z3_OP_BSDIV_I", "Z3_OP_BSREM", "Z3_OP_BSREM_I",
    "Z3_OP_BSMOD", "Z3_OP_BSMOD_I")

FLOAT_TO_INTEGER_KINDS = declaration_kinds("Z3_OP_FPA_TO_SBV",
                                           "Z3_OP_FPA_TO_UBV")

TRAPPING_KINDS = {
    "go": DIVIDING_KINDS,
    "swift": DIVIDING_KINDS + FLOAT_TO_INTEGER_KINDS,
}
"""which node kinds the TARGET'S OWN RENDERER writes with an operator
that can stop the program instead of answering.  Read off those
renderers, and off nothing else:

  * go (`go_render.emit_division`, measured): the plain operator, and
    "go checks the zero divisor and branches into runtime.panicdivide
    -- the EDGE REGION, rendered rather than hidden".
  * swift (`swift_render.emit_division`): the plain operator, and
    "swift's `/` and `%` on a fixed-width integer trap on a zero
    divisor and on the signed extreme by the language's own
    definition".
  * swift (`swift_render.emit_fp`, the float-to-integer conversion):
    "swift's `Int64(_: Double)` TRAPS when the value does not fit ...
    That is an edge region like division's, recorded, not hidden."
  * swift's PLAIN ARITHMETIC is not in the set because that renderer
    never writes it: `swift_render.emit_arith` writes `&+ &- &*`, the
    wrapping forms, for the three arithmetic kinds, and those do not
    trap.  The row is here so the absence is a reading of the file and
    not an omission.
  * rust is NOT in the set: `rust_render.emit_division` writes the
    divide under `core::hint::unreachable_unchecked` at exactly the
    conditions the machine's own divide leaves undefined, which it
    measured (lanes o11_l1, o11_l3, o11_l4) removes both of rust's
    checks and the panic route with them.
  * c and c++ are NOT in the set: neither renderer marks an edge region
    and neither language defines a trap for the divide -- clang emits
    the bare instruction."""


def traps_here(lang, policy, node):
    """whether THIS node will be written with a trapping operator.  It
    is a question about the node's KIND and the target, and under
    `all_constructed` also about whether a construction answers the
    kind -- a constructed divide is `& | ^ ~` and a conditional and
    traps nowhere."""
    kinds = TRAPPING_KINDS.get(lang)
    if not kinds:
        return False
    if node.decl().kind() not in kinds:
        return False
    if policy == "native_first":
        return True
    return B.kind_of(node) is None


def leaves_first(term):
    """every distinct node of the term, each after the nodes it reads.
    The same walk `bind` and `walk` do, without their memos, so the
    plan below can be made before either runs."""
    order = []
    seen = set()
    stack = [(term, False)]
    while stack:
        node, expanded = stack.pop()
        key = node.get_id()
        if expanded:
            order.append(node)
            continue
        if key in seen:
            continue
        seen.add(key)
        stack.append((node, True))
        for index in range(node.num_args()):
            stack.append((node.arg(index), False))
            continue
        continue
    return order


class Regions(object):
    """the nested scopes of one rendered body.  Region 0 is the function
    body; every other region is one arm of one conditional written as
    control flow, and `above` says which region it is written inside."""

    def __init__(self):
        self.above = [None]
        self.depth = [0]

    def open(self, inside):
        self.above.append(inside)
        self.depth.append(self.depth[inside] + 1)
        return len(self.above) - 1

    def move(self, region, inside):
        self.above[region] = inside
        self.settle()
        return

    def settle(self):
        for region in range(len(self.above)):
            above = self.above[region]
            if above is None:
                self.depth[region] = 0
                continue
            self.depth[region] = self.depth[above] + 1
            continue
        return

    def encloses(self, outer, inner):
        while inner is not None:
            if inner == outer:
                return True
            inner = self.above[inner]
            continue
        return False

    def join(self, one, other):
        """the innermost region that encloses both -- where a value read
        in both of them must be written."""
        while self.depth[one] > self.depth[other]:
            one = self.above[one]
            continue
        while self.depth[other] > self.depth[one]:
            other = self.above[other]
            continue
        while one != other:
            one = self.above[one]
            other = self.above[other]
            continue
        return one


def plan_the_regions(term, lang, policy):
    """-> (regions, region per node, the conditionals written as control
    flow, their two arm regions).

    A node is written in the INNERMOST region that encloses every place
    it is read, which is why "nodes shared by both arms and by the rest
    stay hoisted" needs no rule of its own: the join of two arms IS the
    region the conditional itself is written in."""
    order = leaves_first(term)
    readers = {}
    for node in order:
        for index in range(node.num_args()):
            key = node.arg(index).get_id()
            readers.setdefault(key, [])
            readers[key].append((node, index))
            continue
        continue
    traps_below = {}
    for node in order:
        got = traps_here(lang, policy, node)
        for index in range(node.num_args()):
            if traps_below.get(node.arg(index).get_id()):
                got = True
            continue
        traps_below[node.get_id()] = got
        continue
    branching = set()
    for node in order:
        if node.decl().kind() != z3.Z3_OP_ITE:
            continue
        if node.num_args() != 3:
            continue
        if not traps_below.get(node.arg(1).get_id()):
            if not traps_below.get(node.arg(2).get_id()):
                continue
        branching.add(node.get_id())
        continue
    regions = Regions()
    region_of = {}
    arms = {}
    for node in reversed(order):
        demands = []
        if node.get_id() == term.get_id():
            demands.append(0)
        for reader, index in readers.get(node.get_id(), []):
            held = arms.get(reader.get_id())
            if held is not None and index in (1, 2):
                demands.append(held[index - 1])
                continue
            demands.append(region_of.get(reader.get_id(), 0))
            continue
        where = 0
        for demand in demands:
            where = demand
            break
        for demand in demands:
            where = regions.join(where, demand)
            continue
        region_of[node.get_id()] = where
        if node.get_id() in branching:
            arms[node.get_id()] = (regions.open(where), regions.open(where))
        continue
    return regions, region_of, branching, arms

STATEMENT_CEILING = 400000
"""how many named intermediates a rendered source may carry.  It is a
MEASURED ceiling on the thing that is actually written -- one statement
per distinct node -- and not a rule about which operation is allowed."""

RESIDENT_CEILING_KB = 4 * 1024 * 1024
"""how much RESIDENT memory ONE render may hold while it is building.

WHY IT IS CURRENT RESIDENT AND NOT THE PEAK.  `resource.getrusage`
answers the peak, which never falls, so a bound read off it would refuse
every render after the first costly one.  `/proc/self/statm` answers
what is resident NOW, which is the quantity a bound on ONE render is
about.

WHY IT IS HERE AT ALL, measured: task t4's lane `t4_l6` step [2/6] --
`div gpr_one 64` on c, a divide at 128 bits over a word of 128 -- was
stopped by the operating system with no language-level error (`Killed`,
exit 137) and left no row.  The ceiling below is UNDER the task's own
6 GB bound so the refusal is this file's, by name and with the round it
reached, and the named abort ABORT_MEMORY_T4 stays where it is as the
bound on the pass."""

PAGE_BYTES = os.sysconf("SC_PAGE_SIZE")


def resident_kb():
    """what is resident NOW, off `/proc/self/statm` field 2 (resident
    pages).  `/usr/bin/time` is absent from the image and `getrusage`
    answers the peak, so this is the reading."""
    handle = open("/proc/self/statm")
    text = handle.read()
    handle.close()
    pages = int(text.split()[1])
    return (pages * PAGE_BYTES) // 1024


def install_the_watch(record):
    """the construction's per-round watch, set to refuse at this file's
    stated ceiling.  `record` is filled in with where it got to, so a
    refusal carries the round and the reading."""

    def watch(where):
        resident = resident_kb()
        record["where"] = where
        record["resident_kb"] = resident
        if resident < RESIDENT_CEILING_KB:
            return
        raise B.Refused(B.CAUSE_TOO_COSTLY,
                        "%s: %d kB resident, at or above the %d kB this "
                        "render is bounded at"
                        % (where, resident, RESIDENT_CEILING_KB))

    B.WATCH = watch
    return watch


def clear_the_watch():
    B.WATCH = None
    return


# ==================================================================
# section 1: the target's renderer, taught to read the memo
# ==================================================================

def bounded(base):
    """the target's own renderer class with ONE method added: `emit`
    answers from the memo where the node is already bound to a variable,
    and otherwise is the target's own `emit` unchanged.

    This is what makes "the language's own operator over the children's
    NAMES" the same call as "the language's own operator over the
    children's expressions": the renderer is not modified, it is asked
    the same question in a state where the children already have
    names."""

    class Bounded(base):

        def emit(self, node):
            got = self.bound.get(node.get_id())
            if got is not None:
                return got
            return base.emit(self, node)

    Bounded.__name__ = "Bounded" + base.__name__
    return Bounded


BOUND_CLASSES = {}


def renderer_for(lang, families, family, bits, label):
    import emulate as E
    import handful as H
    base = type(H.renderer_for(lang, families, family, bits, label))
    if base not in BOUND_CLASSES:
        BOUND_CLASSES[base] = bounded(base)
    made = BOUND_CLASSES[base](families, family, bits, label)
    made.bound = {}
    return made


SNAPSHOT_FIELDS = ("helpers", "needs_math", "needs_unsafe", "selectors",
                   "blocks")


def snapshot(renderer):
    """the renderer's own accumulators, kept so that a REFUSED attempt
    at the native route leaves nothing behind: a helper it half-added
    would become an unused import, which go refuses to compile."""
    out = {}
    for field in SNAPSHOT_FIELDS:
        if not hasattr(renderer, field):
            continue
        value = getattr(renderer, field)
        if isinstance(value, set):
            out[field] = set(value)
        elif isinstance(value, list):
            out[field] = list(value)
        else:
            out[field] = value
        continue
    return out


def restore(renderer, kept):
    for field in kept:
        setattr(renderer, field, kept[field])
        continue
    return


# ==================================================================
# section 2: the declaration, per target
# ==================================================================

def declaration(lang, renderer, name, kind, width, text):
    """one named intermediate, in the target's own spelling.  A width
    the target has no holder for raises the target's own refusal, which
    is exactly the test this file wants."""
    import emulate as E
    if kind == "bool":
        return truth_declaration(lang, name, text)
    if kind == "fp":
        return float_declaration(lang, name, width, text)
    bits = E.promoted_bits(width)
    if lang == "rust":
        import rust_render as RR
        if bits not in RR.RU:
            raise E.Refused(E.CAUSE_WIDTH, "%d bits" % bits)
        return "let %s: %s = %s;" % (name, RR.RU[bits], text)
    if lang == "go":
        import go_render as GR
        return "var %s %s = %s" % (name, GR.gu(bits), text)
    if lang == "swift":
        import swift_render as SR
        return "let %s: %s = %s" % (name, SR.su(bits), text)
    if bits not in E.UNSIGNED:
        raise E.Refused(E.CAUSE_WIDTH, "%d bits" % bits)
    return "%s %s = %s;" % (E.UNSIGNED[bits], name, text)


def truth_declaration(lang, name, text):
    if lang == "rust":
        return "let %s: bool = %s;" % (name, text)
    if lang == "go":
        return "var %s bool = %s" % (name, text)
    if lang == "swift":
        return "let %s: Bool = %s" % (name, text)
    return "int %s = (%s) ? 1 : 0;" % (name, text)


def zero_text(lang, kind, width):
    """the target's own zero for one holder, which is what a named
    intermediate two arms ASSIGN holds until an arm writes it."""
    if kind == "bool":
        if lang in ("rust", "go", "swift"):
            return "false"
        return "0"
    if kind == "fp":
        if lang == "rust":
            return "0.0"
        return "0"
    return "0"


def assigned_declaration(lang, renderer, name, kind, width):
    """one named intermediate DECLARED before an `if` and assigned
    inside both of its arms.  A width the target has no holder for
    raises the target's own refusal here, exactly as `declaration`
    does, so the conditional falls back to the select."""
    if kind == "bool":
        if lang not in ("rust", "go", "swift"):
            return "int %s = 0;" % name
    line = declaration(lang, renderer, name, kind, width,
                       zero_text(lang, kind, width))
    if lang == "rust":
        return "let mut %s" % line[len("let "):]
    return line


def assignment(lang, name, kind, text):
    """one arm's write of the value the conditional answers with."""
    if kind == "bool":
        if lang not in ("rust", "go", "swift"):
            return "%s = (%s) ? 1 : 0;" % (name, text)
    if lang in ("rust", "c", "cpp"):
        return "%s = %s;" % (name, text)
    return "%s = %s" % (name, text)


def guard_opening(lang, condition):
    if lang in ("rust", "go", "swift"):
        return "if %s {" % condition
    return "if (%s) {" % condition


def guard_middle(lang):
    return "} else {"


def guard_closing(lang):
    return "}"


def float_declaration(lang, name, width, text):
    import emulate as E
    if lang == "rust":
        import rust_render as RR
        if width not in RR.RF:
            raise E.Refused(E.CAUSE_WIDTH, RR.NO_F16 % width)
        return "let %s: %s = %s;" % (name, RR.RF[width], text)
    if lang == "go":
        import go_render as GR
        return "var %s %s = %s" % (name, GR.gf(width), text)
    if lang == "swift":
        import swift_render as SR
        return "let %s: %s = %s" % (name, SR.sf(width), text)
    if width not in E.FLOAT:
        raise E.Refused(E.CAUSE_WIDTH, "float of %d bits" % width)
    return "%s %s = %s;" % (E.FLOAT[width], name, text)


# ==================================================================
# section 3: the walk
# ==================================================================

class General(object):
    """one term rendered into one target: the statements, the memo, and
    the record of which nodes took which route."""

    def __init__(self, lang, renderer, word, policy):
        self.lang = lang
        self.renderer = renderer
        self.word = word
        self.policy = policy
        self.statements = []
        self.counter = 0
        self.values = {}
        self.constructed_kinds = {}
        self.native_nodes = 0
        self.constructed_nodes = 0
        self.widths_of_kind = {}
        self.regions = Regions()
        self.region_of = {}
        self.branching = set()
        self.arms = {}
        self.current_region = 0
        self.guards_written = 0

    def fresh(self):
        name = "v%d" % self.counter
        self.counter = self.counter + 1
        return name

    # -- one node of the FINAL term, bound to a variable ------------

    def bind(self, term):
        """one term of the target's own width, every node of it bound to
        a named intermediate, leaves first.  Returns the memo entry of
        the term itself."""
        order = []
        seen = set()
        stack = [(term, False)]
        while stack:
            node, expanded = stack.pop()
            key = node.get_id()
            if key in self.renderer.bound:
                continue
            if expanded:
                order.append(node)
                continue
            if key in seen:
                continue
            seen.add(key)
            stack.append((node, True))
            for index in range(node.num_args()):
                stack.append((node.arg(index), False))
                continue
            continue
        for node in order:
            self.bind_one(node)
            continue
        return self.renderer.bound.get(term.get_id())

    def bind_one(self, node):
        """one node bound, where a name is worth having.

        A LEAF IS NOT BOUND.  An arrival is already a parameter, a
        numeral is already a literal, and a rounding mode has no holder
        in any target; naming those would add a statement and no
        sharing."""
        if not worth_naming(node):
            return None
        if len(self.statements) >= STATEMENT_CEILING:
            raise B.Refused(CAUSE_TOO_LARGE,
                            "at or above %d statements"
                            % STATEMENT_CEILING)
        if len(self.statements) % 256 == 0:
            # THE SAME BOUND AS THE CONSTRUCTION'S, read here because
            # the statements are the second place a render grows: one
            # string and one memo entry per distinct node.
            resident = resident_kb()
            if resident >= RESIDENT_CEILING_KB:
                raise B.Refused(B.CAUSE_TOO_COSTLY,
                                "naming statement %d: %d kB resident, "
                                "at or above the %d kB this render is "
                                "bounded at"
                                % (len(self.statements), resident,
                                   RESIDENT_CEILING_KB))
        text, kind, width = self.renderer.emit(node)
        name = self.fresh()
        line = declaration(self.lang, self.renderer, name, kind, width,
                           text)
        self.statements.append({"what": "statement", "name": name,
                                "line": line, "key": node.get_id(),
                                "region": self.current_region})
        self.renderer.bound[node.get_id()] = (name, kind, width)
        return self.renderer.bound[node.get_id()]

    # -- one node of the ORIGINAL term, routed ---------------------

    def walk(self, term):
        """the original term, leaves first: each node either kept as the
        target's own operator or replaced by its construction.  Returns
        the root's Value.

        THE REGIONS ARE PLANNED FIRST, before one statement is written:
        which conditionals are written as control flow, and which region
        every node is written in, are properties of the TERM and the
        target, so they are settled once and then only read."""
        self.regions, self.region_of, self.branching, self.arms = \
            plan_the_regions(term, self.lang, self.policy)
        order = []
        seen = set()
        stack = [(term, False)]
        while stack:
            node, expanded = stack.pop()
            key = node.get_id()
            if key in self.values:
                continue
            if expanded:
                order.append(node)
                continue
            if key in seen:
                continue
            seen.add(key)
            stack.append((node, True))
            for index in range(node.num_args()):
                stack.append((node.arg(index), False))
                continue
            continue
        for node in order:
            self.current_region = self.region_of.get(node.get_id(), 0)
            self.values[node.get_id()] = self.one_node(node)
            continue
        self.current_region = 0
        return self.values[term.get_id()]

    def one_node(self, node):
        children = []
        for index in range(node.num_args()):
            children.append(self.values[node.arg(index).get_id()])
            continue
        if is_a_leaf(node):
            return self.leaf_value(node)
        kind = B.kind_of(node)
        native = None
        if self.policy == "native_first" or kind is None:
            guarded = self.try_the_guard(node, children)
            if guarded is not None:
                self.native_nodes = self.native_nodes + 1
                return guarded
            native = self.try_native(node, children)
        if native is not None:
            self.native_nodes = self.native_nodes + 1
            return native
        if kind is None:
            raise B.Refused(CAUSE_NO_ROUTE,
                            "%s at %s" % (node.decl().name(),
                                          node.sort()))
        made = B.build(node, children, self.word)
        self.record(kind, node)
        self.constructed_nodes = self.constructed_nodes + 1
        return self.bound_value(made)

    def leaf_value(self, node):
        """an arrival, a numeral, a truth constant or a rounding mode,
        as the Value it is.  Nothing is bound and nothing is built."""
        if node.sort().kind() == z3.Z3_BOOL_SORT:
            return B.Value("bool", truth=node)
        if z3.is_fp(node) or z3.is_fprm(node):
            return B.Value("other", passthrough=node)
        width = node.size()
        if width > self.word:
            raise B.Refused(B.CAUSE_ARRIVAL,
                            "%d bits against a word of %d"
                            % (width, self.word))
        return B.Value("bv", width=width, unit=width, limbs=[node])

    def try_native(self, node, children):
        """the node offered to the TARGET'S OWN renderer with its
        children already named.  Returns the Value where the target
        answers, and None where it refuses."""
        rebuilt = self.rebuilt(node, children)
        if rebuilt is None:
            return None
        kept = snapshot(self.renderer)
        before = len(self.statements)
        try:
            self.bind(rebuilt)
        except Exception as problem:
            if not is_a_refusal(problem):
                raise
            restore(self.renderer, kept)
            self.roll_back(before)
            return None
        return self.value_of_term(rebuilt)

    def roll_back(self, before):
        """every item appended since `before` removed, and the memo with
        them, so a REFUSED attempt leaves nothing behind."""
        while len(self.statements) > before:
            item = self.statements.pop()
            if item["key"] in self.renderer.bound:
                del self.renderer.bound[item["key"]]
            continue
        return

    def try_the_guard(self, node, children):
        """the conditional whose arm holds a trapping node, offered to
        the target as CONTROL FLOW rather than as a select.  Returns the
        Value where the target answers, and None where it refuses --
        exactly `try_native`'s contract, and the same fall-back on a
        refusal, so a target with no holder for the arms' width keeps
        the select it had."""
        if node.get_id() not in self.branching:
            return None
        arms = self.arms.get(node.get_id())
        if arms is None:
            return None
        rebuilt = self.rebuilt(node, children)
        if rebuilt is None:
            return None
        if rebuilt.num_args() != 3:
            return None
        kept = snapshot(self.renderer)
        before = len(self.statements)
        try:
            made = self.the_guarded_block(rebuilt, arms)
        except Exception as problem:
            if not is_a_refusal(problem):
                raise
            restore(self.renderer, kept)
            self.roll_back(before)
            return None
        if made is None:
            restore(self.renderer, kept)
            self.roll_back(before)
            return None
        return made

    def the_guarded_block(self, rebuilt, arms):
        """the three texts of one conditional -- its condition and its
        two arms -- written as a declaration, an `if`, and one
        assignment inside each arm.

        Each arm's own nodes were already written INTO that arm: the
        plan gave every node the innermost region that encloses its
        readers, and `walk` tagged each statement with the region of
        the node it was written for.  So nothing is moved here; this
        method writes the three lines that hold the arms."""
        condition, ckind, _cwidth = self.renderer.emit(rebuilt.arg(0))
        if ckind != "bool":
            return None
        then_text, then_kind, then_width = \
            self.renderer.emit(rebuilt.arg(1))
        else_text, else_kind, else_width = \
            self.renderer.emit(rebuilt.arg(2))
        if then_kind != else_kind:
            return None
        if then_width != else_width:
            return None
        if then_kind not in ("bv", "fp", "bool"):
            return None
        if len(self.statements) >= STATEMENT_CEILING:
            raise B.Refused(CAUSE_TOO_LARGE,
                            "at or above %d statements"
                            % STATEMENT_CEILING)
        name = self.fresh()
        opening = assigned_declaration(self.lang, self.renderer, name,
                                       then_kind, then_width)
        self.statements.append({
            "what": "guard",
            "name": name,
            "key": rebuilt.get_id(),
            "region": self.current_region,
            "opening": opening,
            "condition": condition,
            "then_region": arms[0],
            "else_region": arms[1],
            "then_line": assignment(self.lang, name, then_kind,
                                    then_text),
            "else_line": assignment(self.lang, name, then_kind,
                                    else_text),
        })
        self.renderer.bound[rebuilt.get_id()] = (name, then_kind,
                                                 then_width)
        self.guards_written = self.guards_written + 1
        return self.value_of_term(rebuilt)

    def rebuilt(self, node, children):
        """the node over its children's own terms, where every child is
        ONE term the target can hold.  A child held as limbs has no
        single term, so there is no native node to offer."""
        arguments = []
        for child in children:
            single = child.native()
            if single is None:
                return None
            arguments.append(single)
            continue
        if not arguments:
            return node
        same = True
        for index in range(node.num_args()):
            if node.arg(index).get_id() != arguments[index].get_id():
                same = False
                break
            continue
        if same:
            return node
        try:
            return rebuild(node, arguments)
        except Exception:
            return None

    def value_of_term(self, term):
        if term.sort().kind() == z3.Z3_BOOL_SORT:
            return B.Value("bool", truth=term)
        if z3.is_fp(term):
            return B.Value("fp", width=fp_width(term.sort()),
                           unit=0, limbs=[term],
                           ebits=term.sort().ebits(),
                           sbits=term.sort().sbits())
        return B.Value("bv", width=term.size(), unit=term.size(),
                       limbs=[term])

    def bound_value(self, made):
        """every term of a constructed Value bound to a name, so the
        construction's own nodes are named intermediates too."""
        if made.sort == "bool":
            self.bind(made.truth)
            return made
        if made.sort == "other":
            return made
        for limb in made.limbs:
            self.bind(limb)
            continue
        return made

    def record(self, kind, node):
        self.constructed_kinds[kind] = \
            self.constructed_kinds.get(kind, 0) + 1
        try:
            width = B.node_width(node)
        except Exception:
            width = 0
        self.widths_of_kind.setdefault(kind, {})
        key = "%d" % width
        self.widths_of_kind[kind][key] = \
            self.widths_of_kind[kind].get(key, 0) + 1
        return


def fp_width(sort):
    return sort.ebits() + sort.sbits()


def is_a_refusal(problem):
    import emulate as E
    if isinstance(problem, E.Refused):
        return True
    if isinstance(problem, B.Refused):
        return True
    return False


def worth_naming(node):
    """whether a node earns a variable of its own.  An arrival, a
    numeral, a truth constant and a rounding mode do not: each is
    already one token in the target's own spelling."""
    decl = node.decl()
    kind = decl.kind()
    if z3.is_const(node) and kind == z3.Z3_OP_UNINTERPRETED:
        return False
    if kind in (z3.Z3_OP_BNUM, z3.Z3_OP_TRUE, z3.Z3_OP_FALSE):
        return False
    if z3.is_fprm(node):
        return False
    if node.sort().kind() == z3.Z3_ROUNDING_MODE_SORT:
        return False
    if kind == z3.Z3_OP_EXTRACT:
        child = node.arg(0)
        if z3.is_const(child) and \
                child.decl().kind() == z3.Z3_OP_UNINTERPRETED:
            # THE ARRIVAL'S OWN LANE.  `emulate.Renderer.emit_extract`
            # reads an extract OF A SEED through `emit_symbol`, which is
            # how a parameter narrower than the register is planned; a
            # name here would not change that and the node is still
            # worth one.
            return True
    return True


def is_a_leaf(node):
    decl = node.decl()
    kind = decl.kind()
    if z3.is_const(node) and kind == z3.Z3_OP_UNINTERPRETED:
        return True
    if kind in (z3.Z3_OP_BNUM, z3.Z3_OP_TRUE, z3.Z3_OP_FALSE):
        return True
    if z3.is_fprm(node):
        return True
    return False


def rebuild(node, arguments):
    """the node's own operation applied to new arguments of the same
    sorts.  `z3.substitute` is used where the declaration takes
    parameters of its own (an extract, an extension, a rotate), because
    those cannot be re-applied through `decl()`."""
    decl = node.decl()
    if decl.num_params() > 0:
        pairs = []
        for index in range(node.num_args()):
            pairs.append((node.arg(index), arguments[index]))
            continue
        return z3.substitute(node, *pairs)
    return decl(*arguments)


# ==================================================================
# section 4: the source
# ==================================================================

NAME_PATTERN = re.compile(r"\bv(\d+)\b")


def right_of(line):
    """what one written line READS: everything right of its first `=`,
    which is the assignment in every target's own spelling."""
    body = line.split("=", 1)
    if len(body) > 1:
        return body[1]
    return ""


def reads_of(item):
    """(name, the region the read happens in) for every name one item
    reads.  A conditional written as control flow reads its condition
    OUTSIDE the `if` and each arm's value INSIDE that arm, which is
    what makes a value used by one arm alone belong to that arm."""
    out = []
    if item["what"] == "statement":
        for found in NAME_PATTERN.findall(right_of(item["line"])):
            out.append((found, item["region"]))
            continue
        return out
    for found in NAME_PATTERN.findall(item["condition"]):
        out.append((found, item["region"]))
        continue
    for found in NAME_PATTERN.findall(right_of(item["then_line"])):
        out.append((found, item["then_region"]))
        continue
    for found in NAME_PATTERN.findall(right_of(item["else_line"])):
        out.append((found, item["else_region"]))
        continue
    return out


def settle_the_regions(items, regions):
    """a value written inside an arm but READ outside it is moved out to
    the innermost region that encloses every read.

    WHY IT IS NEEDED AT ALL, and it is a small number: the plan gives
    each node of the ORIGINAL term its region, and the statements a node
    is written as are that node's -- but two nodes' CONSTRUCTIONS can
    build the same sub-term, z3 hands back the same node for it, and the
    memo then has one name written in the first node's region and read
    from the second's.  The pass below is one walk in reverse: every
    reader of a name is met before the line that writes it, so one pass
    settles the whole chain."""
    read_at = {}
    for item in reversed(items):
        where = item["region"]
        seen = read_at.get(item["name"])
        if seen is not None:
            where = regions.join(where, seen)
        if where != item["region"]:
            if item["what"] == "guard":
                regions.move(item["then_region"], where)
                regions.move(item["else_region"], where)
            item["region"] = where
        for found, region in reads_of(item):
            held = read_at.get(found)
            if held is None:
                read_at[found] = region
                continue
            read_at[found] = regions.join(held, region)
            continue
        continue
    return


def live_items(items, answer_text):
    """the items the answer actually reads, in order.

    A node bound and then not used is DEAD -- it happens where the
    native route was tried, refused, and the construction took a
    different shape -- and go refuses to compile a source with an unused
    variable, so the dead ones are dropped rather than declared."""
    live = set(NAME_PATTERN.findall(answer_text))
    kept = []
    for item in reversed(items):
        number = item["name"][1:]
        if number not in live:
            continue
        kept.append(item)
        for found, _region in reads_of(item):
            live.add(found)
            continue
        continue
    kept.reverse()
    return kept


def written_lines(lang, kept, regions):
    """(depth, line) for every line of the function body, in order: the
    region 0 items, and inside each conditional written as control flow
    its declaration, its `if`, its two arms' own items, and the two
    assignments."""
    by_region = {}
    for item in kept:
        by_region.setdefault(item["region"], [])
        by_region[item["region"]].append(item)
        continue
    return region_lines(lang, by_region, 0, 0)


def region_lines(lang, by_region, region, depth):
    out = []
    for item in by_region.get(region, []):
        if item["what"] == "statement":
            out.append((depth, item["line"]))
            continue
        out.append((depth, item["opening"]))
        out.append((depth, guard_opening(lang, item["condition"])))
        out.extend(region_lines(lang, by_region, item["then_region"],
                                depth + 1))
        out.append((depth + 1, item["then_line"]))
        out.append((depth, guard_middle(lang)))
        out.extend(region_lines(lang, by_region, item["else_region"],
                                depth + 1))
        out.append((depth + 1, item["else_line"]))
        out.append((depth, guard_closing(lang)))
        continue
    return out


def indented(lang, depth, line):
    """the target's own indentation: go is written with tabs by its own
    tool and every other target here with four spaces."""
    if lang == "go":
        return "\t" * (depth + 1) + line
    return "    " * (depth + 1) + line


def render(term, lang, families, home, bits, label, word, policy,
           text=""):
    """the WHOLE of this file's work: one term, one target, one source.

    Returns a record carrying the source, the symbol, the statements'
    count, the nodes that took each route and the kinds constructed."""
    import emulate as E
    renderer = renderer_for(lang, families, home, bits, label)
    renderer.plan_parameters(term)
    renderer.check_symbols(term)
    walker = General(lang, renderer, word, policy)
    reached = {}
    install_the_watch(reached)
    try:
        root = walker.walk(term)
    finally:
        clear_the_watch()
    single = root.native()
    if single is None:
        raise B.Refused(CAUSE_ANSWER_WIDE,
                        "%d bits over a word of %d" % (root.width,
                                                       word))
    entry = renderer.bound.get(single.get_id())
    if entry is None:
        root_text, root_kind, root_width = renderer.emit(single)
    else:
        root_text, root_kind, root_width = entry
    made = renderer.answer(root_text, root_kind, root_width)
    return_type = made[0]
    body = made[1]
    if isinstance(body, list):
        answer_text = "\n".join(body)
        answer_lines = list(body)
    else:
        answer_text = body
        answer_lines = None
    settle_the_regions(walker.statements, walker.regions)
    kept = live_items(walker.statements, answer_text)
    body_lines = written_lines(lang, kept, walker.regions)
    source, symbol = assemble(lang, renderer, label, return_type,
                              body_lines, answer_lines, body, text)
    return {
        "written_term": B.joined(root),
        "source": source,
        "symbol": symbol,
        "renderer": renderer,
        "params": renderer.params,
        "statements": len(kept),
        "statements_before_the_dead_were_dropped":
            len(walker.statements),
        "native_nodes": walker.native_nodes,
        "constructed_nodes": walker.constructed_nodes,
        "guards": walker.guards_written,
        "constructed_kinds": dict(walker.constructed_kinds),
        "constructed_widths": dict(walker.widths_of_kind),
        "policy": policy,
        "resident_kb_at_the_last_round": reached.get("resident_kb"),
        "the_last_round_reached": reached.get("where"),
    }


def assemble(lang, renderer, label, return_type, statements,
             answer_lines, body, text):
    """the target's own program shape, with the named intermediates in
    the function body.  Every shape below is the one that target's own
    renderer writes; only the body between the signature and the answer
    is this file's.

    `statements` is (depth, line) per written line, the depth being how
    many conditionals written as control flow the line sits inside."""
    import emulate as E
    symbol = "emu_%s" % label
    lines = []
    if lang == "rust":
        import rust_render as RR
        params = []
        for param in renderer.params:
            params.append("%s: %s" % (param["name"], param["holder"]))
            continue
        lines.append(RR.RUST_PRELUDE)
        lines.append("#![allow(unused_variables, unused_mut)]")
        lines.append("")
        lines.append("// task t4 emulation -- rendered by "
                     "render_general.py, one named")
        lines.append("// intermediate per node of the term of %s."
                     % label)
        lines.append("//   %s" % " ".join(text.split())[:900])
        lines.append("#[no_mangle]")
        lines.append("pub extern \"C\" fn %s(%s) -> %s"
                     % (symbol, ", ".join(params), return_type))
        lines.append("{")
        for depth, line in statements:
            lines.append(indented(lang, depth, line))
            continue
        lines.append("    %s" % body)
        lines.append("}")
        lines.append("")
        return "\n".join(lines), symbol
    if lang == "go":
        params = []
        for param in renderer.params:
            params.append("%s %s" % (param["name"], param["holder"]))
            continue
        lines.append("// task t4 emulation -- rendered by "
                     "render_general.py, one named")
        lines.append("// intermediate per node of the term of %s."
                     % label)
        lines.append("//   %s" % " ".join(text.split())[:900])
        lines.append("package main")
        lines.append("")
        if renderer.needs_math:
            lines.append("import \"math\"")
        if renderer.needs_unsafe:
            lines.append("import \"unsafe\"")
        if renderer.needs_math or renderer.needs_unsafe:
            lines.append("")
        for helper in renderer.selector_texts():
            lines.append(helper)
            lines.append("")
            continue
        lines.append("//go:noinline")
        lines.append("func %s(%s) %s {" % (symbol, ", ".join(params),
                                           return_type))
        for depth, line in statements:
            lines.append(indented(lang, depth, line))
            continue
        for line in (answer_lines or [body]):
            lines.append("\t%s" % line)
            continue
        lines.append("}")
        lines.append("")
        names = []
        for index, param in enumerate(renderer.params):
            lines.append("var g%d %s" % (index, param["holder"]))
            names.append("g%d" % index)
            continue
        lines.append("var sink interface{}")
        lines.append("")
        lines.append("func main() {")
        lines.append("\tsink = %s(%s)" % (symbol, ", ".join(names)))
        lines.append("\t_ = sink")
        lines.append("}")
        lines.append("")
        # THE CARVE ASKS objdump FOR THE SYMBOL BY NAME, and go's
        # linked executable spells a package function `main.<name>`.
        # `go_render.render` returns that spelling and this file
        # returned the bare one, so every go source this render wrote
        # BUILT and then carved to nothing: task t4's lane `t4_l7`
        # step [1/4], "objdump found no symbol emu_adc_gpr_gpr_64__
        # reg_rdi__go__all_constructed".  Every other target's own
        # renderer returns the bare name and keeps it.
        return "\n".join(lines), "main.%s" % symbol
    if lang == "swift":
        params = []
        for param in renderer.params:
            params.append("_ %s: %s" % (param["name"], param["holder"]))
            continue
        lines.append("// task t4 emulation -- rendered by "
                     "render_general.py, one named")
        lines.append("// intermediate per node of the term of %s."
                     % label)
        lines.append("//   %s" % " ".join(text.split())[:900])
        lines.append("@_cdecl(\"%s\")" % symbol)
        lines.append("public func %s(%s) -> %s"
                     % (symbol, ", ".join(params), return_type))
        lines.append("{")
        for depth, line in statements:
            lines.append(indented(lang, depth, line))
            continue
        lines.append("    return %s" % body)
        lines.append("}")
        lines.append("")
        return "\n".join(lines), symbol
    fixed = "#include <stdint.h>"
    memcpy_header = "#include <string.h>"
    linkage = None
    if lang == "cpp":
        import cpp_render as CPR
        fixed = CPR.HEADER_FIXED_WIDTH
        memcpy_header = CPR.HEADER_MEMCPY
        linkage = CPR.LINKAGE
    lines.append("/* task t4 emulation -- rendered by "
                 "render_general.py, one named")
    lines.append("   intermediate per node of the term of %s.  The "
                 "term's text, LITERAL:" % label)
    lines.append("   %s */" % " ".join(text.split())[:900])
    lines.append(fixed)
    if renderer.helpers:
        lines.append(memcpy_header)
    for helper in sorted(renderer.helpers):
        lines.append(renderer.helper_text(helper))
        continue
    params = []
    for param in renderer.params:
        params.append("%s %s" % (param["holder"], param["name"]))
        continue
    if not params:
        params.append("void")
    lines.append("")
    if linkage is not None:
        lines.append(linkage)
    lines.append("%s" % return_type)
    lines.append("%s(%s)" % (symbol, ", ".join(params)))
    lines.append("{")
    for depth, line in statements:
        lines.append(indented(lang, depth, line))
        continue
    lines.append("    return %s;" % body)
    lines.append("}")
    lines.append("")
    return "\n".join(lines), symbol
