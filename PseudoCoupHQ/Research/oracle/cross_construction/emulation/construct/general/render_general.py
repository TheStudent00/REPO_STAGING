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
        self.statements.append((name, line, node.get_id()))
        self.renderer.bound[node.get_id()] = (name, kind, width)
        return self.renderer.bound[node.get_id()]

    # -- one node of the ORIGINAL term, routed ---------------------

    def walk(self, term):
        """the original term, leaves first: each node either kept as the
        target's own operator or replaced by its construction.  Returns
        the root's Value."""
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
            self.values[node.get_id()] = self.one_node(node)
            continue
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
            while len(self.statements) > before:
                _name, _line, key = self.statements.pop()
                if key in self.renderer.bound:
                    del self.renderer.bound[key]
                continue
            return None
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


def live_statements(statements, answer_text):
    """the statements the answer actually reads, in order.

    A node bound and then not used is DEAD -- it happens where the
    native route was tried, refused, and the construction took a
    different shape -- and go refuses to compile a source with an unused
    variable, so the dead ones are dropped rather than declared."""
    live = set(NAME_PATTERN.findall(answer_text))
    kept = []
    for name, line, _key in reversed(statements):
        number = name[1:]
        if number not in live:
            continue
        kept.append((name, line))
        body = line.split("=", 1)
        if len(body) > 1:
            for found in NAME_PATTERN.findall(body[1]):
                live.add(found)
                continue
        continue
    kept.reverse()
    return kept


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
    kept = live_statements(walker.statements, answer_text)
    source, symbol = assemble(lang, renderer, label, return_type, kept,
                              answer_lines, body, text)
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
    is this file's."""
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
        for _name, line in statements:
            lines.append("    %s" % line)
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
        for _name, line in statements:
            lines.append("\t%s" % line)
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
        for _name, line in statements:
            lines.append("    %s" % line)
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
    for _name, line in statements:
        lines.append("    %s" % line)
        continue
    lines.append("    return %s;" % body)
    lines.append("}")
    lines.append("")
    return "\n".join(lines), symbol
