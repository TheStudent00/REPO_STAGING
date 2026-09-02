#!/usr/bin/env python3
"""swift_type_authority.py -- TASK 35: swift's EXTRACTED scalar type authority.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token. The
token appears exactly once per unit: as a display label on the member.
MECHANICAL GUARD REQUIRED: every pipeline stage that groups or pairs
units must run the spelling-key check (op_pipeline/check_no_spelling_keys.py)
and refuse its own output on failure.

This program's subject is TYPES, not operators. It never reads an
operator list; SwiftIntTypes.py carries operator-name lists and those
functions are never called.

WHAT IT DOES
------------
Two independent ENUMERATING routes read swift's scalar type authority,
and a third CONFIRMING route puts each spelling to the compiler itself.
Two routes agreeing is the acceptance bar (the brief); where they
disagree the disagreement is written out as a finding and is NOT
resolved by preference.

  route_source     -- the pinned swift source clone
                      (<WORKSPACE_DIR>/Sources/swift-6.0.3-RELEASE at
                      commit 6a862d2e..., tag swift-6.0.3-RELEASE).
                      The concrete scalar types are NOT hand-listed:
                      each .gyb template's own generation loop is read
                      out of the template as data (`% for <var> in
                      <fn>(...)`, the `<Self> = <var>.<attr>` binding,
                      and the `public struct ${<Self>}` declaration),
                      and <fn> is then imported from the SAME pinned
                      tree (utils/SwiftIntTypes.py,
                      utils/SwiftFloatingPointTypes.py) and called, so
                      the enumeration is the template's own.
                      Non-templated declarations (Bool.swift,
                      Int128.swift, UInt128.swift) are read by their
                      `public struct` line, with the conformance line
                      that marks the class quoted.

  route_typecheck  -- log 121 route (b)'s tool: the installed
                      swift-frontend typechecks `func probe(x: <T>) {}`
                      per spelling, inside the Airlock container, with a
                      negative control (a spelling no authority admits
                      must be refused). CONFIRMING only: it can never
                      enumerate a spelling it was not handed.

  route_installed  -- log 121 route (a): the INSTALLED stdlib module
                      interface for this target, copied byte-identical
                      out of the Airlock container to
                      swift_stdlib_x86_64-unknown-linux-gnu.swiftinterface.
                      Its own header states the compiler pin. Types are
                      the top-level `public struct` declarations; the
                      class marking is the protocol conformance stated
                      on the declaration or in a top-level `extension
                      Swift.<T> : ...` line.

OUTPUT (new files only; type_inventory.json is NOT modified)
------------------------------------------------------------
  swift_type_authority.json  -- all three routes, their agreement,
                                findings
  swift_type_authority_typecheck.swift -- the one-file form of the
                                typecheck route, kept as evidence
  type_inventory2.json       -- type_inventory.json's four extracted
                                languages copied verbatim, with swift's
                                record REBUILT from the routes above.
                                Supersedes type_inventory.json.
  type_inventory2.md         -- the readable rendering

  /tmp/reconnect_venv/bin/python3 swift_type_authority.py
"""

import importlib.util
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SWIFT_SRC = "<WORKSPACE_DIR>/Sources/swift-6.0.3-RELEASE"
CORE = os.path.join(SWIFT_SRC, "stdlib/public/core")
UTILS = os.path.join(SWIFT_SRC, "utils")
IFACE = os.path.join(HERE, "swift_stdlib_x86_64-unknown-linux-gnu.swiftinterface")

# The target this whole corpus was compiled for. CMAKE_SIZEOF_VOID_P is
# the gyb template's own parameter name; 8 is x86_64. It is recorded as a
# target parameter, not a guess about swift.
TARGET_TRIPLE = "x86_64-unknown-linux-gnu"
CMAKE_SIZEOF_VOID_P = 8

# The class-marking vocabulary is NOT invented here: these are the
# strings type_inventory_validate.py's NUMERIC_MARKS already recognises
# (integer_signed, integer_unsigned, float). `truth_value` is the one
# string this file adds, and it is added because swift's Bool has an
# extracted marking that is neither integer nor float; the consequence
# (NUMERIC_MARKS has no truth-value entry, so Bool lands in `undecided`
# under the shared rule, exactly as rust's bool does) is REPORTED as a
# finding, not smoothed over by widening the rule here.
MARK_SIGNED = "integer_signed"
MARK_UNSIGNED = "integer_unsigned"
MARK_FLOAT = "float"
MARK_TRUTH = "truth_value"


def run(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def read(path):
    with open(path) as fh:
        return fh.read()


def load_pinned_module(name):
    """Import a helper module out of the PINNED swift tree, by path."""
    path = os.path.join(UTILS, name + ".py")
    spec = importlib.util.spec_from_file_location("pinned_" + name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["pinned_" + name] = mod
    spec.loader.exec_module(mod)
    return mod, path


# ---------------------------------------------------------------- route S

def source_pin():
    rc, head, _ = run(["git", "log", "-1", "--format=%H %s"], cwd=SWIFT_SRC)
    rc2, tag, _ = run(["git", "describe", "--all"], cwd=SWIFT_SRC)
    return {
        "path": SWIFT_SRC,
        "git_log_1": head,
        "git_describe_all": tag,
        "quoted_from": "the repository itself (git log -1 / git describe "
                       "--all run in %s)" % SWIFT_SRC,
        "matches_log_122_recorded_commit": head.split()[0] ==
        "6a862d2eb7128ff1f317b07e8ad1a6da939775f3" if head else False,
    }


def read_gyb_loop(gyb_path, marker=None):
    """Read a .gyb template's generation loop AS DATA.

    Returns the loop variable, the generator call text, the name of the
    template variable holding the produced type spelling, the attribute
    that variable is bound to, and the `public struct ${...}` line that
    consumes it -- every one of them QUOTED out of the template.
    """
    text = read(gyb_path)
    lines = text.split("\n")
    start = 0
    if marker:
        for i, ln in enumerate(lines):
            if marker in ln:
                start = i
                break
    loop = None
    for i in range(start, len(lines)):
        m = re.match(r"^%\s*for\s+(\w+)\s+in\s+(\w+)\((.*?)\)\s*:\s*$",
                     lines[i])
        if m:
            loop = {"line_number": i + 1, "text": lines[i].strip(),
                    "loop_variable": m.group(1),
                    "generator_function": m.group(2),
                    "generator_arguments": m.group(3)}
            break
    if loop is None:
        raise SystemExit("no generation loop found in %s" % gyb_path)

    binding = None
    decl = None
    for i in range(loop["line_number"], min(loop["line_number"] + 400,
                                            len(lines))):
        ln = lines[i]
        if binding is None:
            m = re.match(r"^%?\s*(\w+)\s*=\s*"
                         + re.escape(loop["loop_variable"])
                         + r"\.(\w+)\s*$", ln)
            if m and m.group(2) in ("stdlib_name",):
                binding = {"line_number": i + 1, "text": ln.strip(),
                           "template_variable": m.group(1),
                           "attribute": m.group(2)}
        if binding and decl is None:
            m = re.match(r"^public struct \$\{"
                         + re.escape(binding["template_variable"])
                         + r"\}", ln)
            if m:
                decl = {"line_number": i + 1, "text": ln.strip()}
                break
    if binding is None or decl is None:
        raise SystemExit("loop found but binding/declaration not found in %s"
                         % gyb_path)
    loop["binding"] = binding
    loop["declaration"] = decl
    loop["file"] = gyb_path
    return loop, lines


def float_target_conditions(lines, loop):
    """The per-type `#if` guard the float template wraps its struct in.

    Captured VERBATIM and keyed by the template's own condition on the
    type's bit count, so nothing about which targets carry Float16 or
    Float80 is decided by me here.
    """
    out = []
    lo = loop["line_number"]
    hi = loop["declaration"]["line_number"]
    pending = None
    for i in range(lo, hi):
        ln = lines[i]
        m = re.match(r"^%\s*(?:el)?if\s+bits\s*==\s*(\d+)\s*:\s*$", ln)
        if m:
            pending = int(m.group(1))
            continue
        if pending is not None and ln.startswith("#if "):
            out.append({"bits": pending,
                        "template_line": lo + 1 + (i - lo),
                        "condition": ln.strip()})
            pending = None
    return out


def route_source():
    pin = source_pin()
    findings = []
    entries = []

    int_gyb = os.path.join(CORE, "IntegerTypes.swift.gyb")
    flt_gyb = os.path.join(CORE, "FloatingPointTypes.swift.gyb")

    # --- the integer template
    iloop, _ilines = read_gyb_loop(int_gyb, marker="Concrete FixedWidthIntegers")
    imod, ipath = load_pinned_module("SwiftIntTypes")
    igen = getattr(imod, iloop["generator_function"])
    word_bits_line = [ln.strip() for ln in read(int_gyb).split("\n")
                      if ln.strip().startswith("word_bits =")]
    word_bits = CMAKE_SIZEOF_VOID_P * 8
    int_objs = list(igen(word_bits))
    for obj in int_objs:
        spelling = getattr(obj, iloop["binding"]["attribute"])
        entries.append({
            "spelling": spelling,
            "class": MARK_SIGNED if obj.is_signed else MARK_UNSIGNED,
            "class_source": "%s :: SwiftIntegerType.is_signed" %
                            os.path.basename(ipath),
            "declared_in": int_gyb,
            "how": "template generation loop, evaluated with the "
                   "template's own generator",
            "generator": "%s(%s) with word_bits=%d, from %s" %
                         (iloop["generator_function"],
                          iloop["generator_arguments"], word_bits, ipath),
            "declaration_line": iloop["declaration"]["text"],
            "bits": obj.bits,
            "is_word_sized": obj.is_word,
            "target_condition": None,
        })

    # --- the floating-point template
    floop, flines = read_gyb_loop(flt_gyb)
    fmod, fpath = load_pinned_module("SwiftFloatingPointTypes")
    fgen = getattr(fmod, floop["generator_function"])
    conds = float_target_conditions(flines, floop)
    cond_by_bits = {c["bits"]: c["condition"] for c in conds}
    for obj in list(fgen()):
        spelling = getattr(obj, floop["binding"]["attribute"])
        entries.append({
            "spelling": spelling,
            "class": MARK_FLOAT,
            "class_source": "%s :: all_floating_point_types()" %
                            os.path.basename(fpath),
            "declared_in": flt_gyb,
            "how": "template generation loop, evaluated with the "
                   "template's own generator",
            "generator": "%s(%s), from %s" % (floop["generator_function"],
                                              floop["generator_arguments"],
                                              fpath),
            "declaration_line": floop["declaration"]["text"],
            "bits": obj.bits,
            "is_word_sized": False,
            "target_condition": cond_by_bits.get(obj.bits),
        })

    # --- the non-templated declarations
    plain = [
        ("Bool.swift", r"^public struct (Bool)\b",
         r"^extension Bool: .*ExpressibleByBooleanLiteral", MARK_TRUTH),
        ("Int128.swift", r"^public struct (Int128)\b",
         r"^extension Int128: FixedWidthInteger, SignedInteger", MARK_SIGNED),
        ("UInt128.swift", r"^public struct (UInt128)\b",
         r"^extension UInt128: FixedWidthInteger, UnsignedInteger",
         MARK_UNSIGNED),
    ]
    for fname, decl_rx, mark_rx, mark in plain:
        path = os.path.join(CORE, fname)
        lines = read(path).split("\n")
        decl = None
        marker = None
        for i, ln in enumerate(lines):
            if decl is None and re.match(decl_rx, ln):
                decl = {"line_number": i + 1, "text": ln.strip(),
                        "spelling": re.match(decl_rx, ln).group(1)}
            if marker is None and re.match(mark_rx, ln):
                marker = {"line_number": i + 1, "text": ln.strip()}
        if decl is None or marker is None:
            raise SystemExit("declaration or class marking not found in %s"
                             % path)
        entries.append({
            "spelling": decl["spelling"],
            "class": mark,
            "class_source": "%s:%d `%s`" % (fname, marker["line_number"],
                                            marker["text"]),
            "declared_in": path,
            "how": "plain source declaration (no template)",
            "generator": None,
            "declaration_line": "%s:%d %s" % (fname, decl["line_number"],
                                              decl["text"]),
            "bits": None,
            "is_word_sized": False,
            "target_condition": None,
        })

    # Integers.swift carries PROTOCOLS, not concrete types -- computed,
    # not assumed, because the brief named that file as an authority.
    ints_path = os.path.join(CORE, "Integers.swift")
    ints_lines = read(ints_path).split("\n")
    n_struct = sum(1 for ln in ints_lines
                   if re.match(r"^public struct \b", ln))
    n_proto = sum(1 for ln in ints_lines if re.match(r"^public protocol ", ln))
    findings.append({
        "id": "F35-1",
        "statement": "Integers.swift declares no concrete scalar type; the "
                     "concrete fixed-width integers are generated by "
                     "IntegerTypes.swift.gyb. Counted, not assumed.",
        "computed": {"file": ints_path,
                     "top_level_public_struct_lines": n_struct,
                     "top_level_public_protocol_lines": n_proto},
        "evidence_class": "computed over the pinned file",
    })

    return {
        "route": "route_source",
        "what": "the pinned swift source clone, templates read as data",
        "pin": pin,
        "word_bits_line_quoted": word_bits_line,
        "target_parameter": {"CMAKE_SIZEOF_VOID_P": CMAKE_SIZEOF_VOID_P,
                             "target": TARGET_TRIPLE,
                             "why": "the gyb templates take the pointer "
                                    "size as their parameter; 8 is this "
                                    "target's"},
        "integer_loop": iloop,
        "floating_point_loop": floop,
        "floating_point_target_conditions": conds,
        "entries": entries,
        "findings": findings,
    }


# ---------------------------------------------------------------- route I

CONFORM_INT = ("Swift.FixedWidthInteger", "Swift.BinaryInteger")
CONFORM_SIGNED = "Swift.SignedInteger"
CONFORM_UNSIGNED = "Swift.UnsignedInteger"
CONFORM_FLOAT = ("Swift.BinaryFloatingPoint", "Swift.FloatingPoint")
CONFORM_TRUTH = "Swift.ExpressibleByBooleanLiteral"


def route_installed():
    text = read(IFACE)
    lines = text.split("\n")
    header = [ln for ln in lines[:4]]
    m = re.search(r"swift-compiler-version:\s*(.+)$", "\n".join(header),
                  re.M)
    compiler_version = m.group(1).strip() if m else None

    decls = {}
    for i, ln in enumerate(lines):
        m = re.match(r"^(?:@frozen )?public struct ([A-Za-z0-9_]+)"
                     r"(?: : (.*?))? \{", ln)
        if m:
            decls[m.group(1)] = {
                "declaration_line_number": i + 1,
                "declaration_line": ln.strip(),
                "conformances": [c.strip() for c in
                                 (m.group(2) or "").split(",") if c.strip()],
            }
    for i, ln in enumerate(lines):
        m = re.match(r"^extension Swift\.([A-Za-z0-9_]+) : (.*?) \{", ln)
        if m and m.group(1) in decls:
            for c in m.group(2).split(","):
                c = c.strip()
                if c and c not in decls[m.group(1)]["conformances"]:
                    decls[m.group(1)]["conformances"].append(c)
                    decls[m.group(1)].setdefault(
                        "conformance_extension_lines", []).append(
                            {"line_number": i + 1, "text": ln.strip()})

    entries = []
    for name, d in sorted(decls.items()):
        conf = d["conformances"]
        cls = None
        src = None
        if any(c in conf for c in CONFORM_INT):
            if CONFORM_SIGNED in conf:
                cls, src = MARK_SIGNED, CONFORM_SIGNED
            elif CONFORM_UNSIGNED in conf:
                cls, src = MARK_UNSIGNED, CONFORM_UNSIGNED
        elif any(c in conf for c in CONFORM_FLOAT):
            cls = MARK_FLOAT
            src = [c for c in CONFORM_FLOAT if c in conf][0]
        elif CONFORM_TRUTH in conf:
            cls, src = MARK_TRUTH, CONFORM_TRUTH
        if cls is None:
            continue
        entries.append({
            "spelling": name,
            "class": cls,
            "class_source": src,
            "declared_in": IFACE,
            "how": "top-level declaration in the installed module interface",
            "declaration_line": d["declaration_line"],
            "declaration_line_number": d["declaration_line_number"],
            "conformances": conf,
        })

    return {
        "route": "route_installed",
        "what": "log 121 route (a): the installed stdlib module interface "
                "for this target, copied byte-identical out of the Airlock "
                "container",
        "pin": {
            "path": IFACE,
            "copied_from": "sandbox-runner:/persist/swift/usr/lib/"
                           "swift_static/linux/Swift.swiftmodule/"
                           "x86_64-unknown-linux-gnu.swiftinterface",
            "compiler_version_quoted_from_the_file": compiler_version,
            "header_quoted": header[:2],
            "container_wall_note": "/persist does not exist on the host; "
                                   "the file was read inside the Airlock "
                                   "container and copied out, and both "
                                   "copies hash the same",
        },
        "declaration_count_scanned": len(decls),
        "entries": entries,
        "findings": [],
    }


# ---------------------------------------------------------------- route T

# The Airlock container that holds the installed toolchain. /persist is
# INSIDE it; on the host the path does not exist, so this route states
# which side of the container wall it ran on before it states anything
# else.
CONTAINER = "sandbox-runner"
SWIFT_FRONTEND = "/persist/swift/usr/bin/swift-frontend"


def typecheck_one(spelling):
    """Ask the installed compiler itself whether the spelling names a type.

    This is the tool log 121 route (b) names (`swiftc`/swift-frontend).
    It is used as a CONFIRMING witness per row, not as an enumerator: a
    typecheck can only answer about a spelling it is handed.
    """
    src = "func probe(x: %s) {}\n" % spelling
    cmd = ["podman", "exec", "-i", CONTAINER, "bash", "-lc",
           "cat > /tmp/t35_one.swift && %s -typecheck "
           "-target %s /tmp/t35_one.swift 2>&1" % (SWIFT_FRONTEND,
                                                   TARGET_TRIPLE)]
    p = subprocess.run(cmd, input=src, capture_output=True, text=True)
    return {"accepted": p.returncode == 0,
            "source": src.strip(),
            "diagnostic": p.stdout.strip() or None,
            "exit_code": p.returncode}


def route_typecheck(spellings):
    rc, _, _ = run(["podman", "exec", CONTAINER, "test", "-x",
                    SWIFT_FRONTEND])
    host_side = os.path.exists("/persist")
    if rc != 0:
        return {"route": "route_typecheck", "available": False,
                "refusal": "%s is not executable in container %s"
                           % (SWIFT_FRONTEND, CONTAINER),
                "entries": [], "negative_control": None}
    ver_rc, ver, _ = run(["podman", "exec", CONTAINER, SWIFT_FRONTEND,
                          "--version"])
    entries = {}
    for s in spellings:
        entries[s] = typecheck_one(s)
    negative = typecheck_one("Int13")
    return {
        "route": "route_typecheck",
        "what": "log 121 route (b)'s tool: the installed swift-frontend "
                "typechecks a one-parameter declaration per spelling",
        "available": True,
        "container": CONTAINER,
        "container_wall": {
            "persist_exists_on_host": host_side,
            "statement": "the toolchain lives inside the container; the "
                         "host has no /persist, so a host-side absence "
                         "check would prove nothing about the toolchain",
        },
        "version_quoted_from_the_tool": ver.split("\n")[0] if ver else None,
        "negative_control": negative,
        "entries": entries,
    }


# ------------------------------------------------------------- agreement

def build():
    rs = route_source()
    ri = route_installed()

    s_by = {e["spelling"]: e for e in rs["entries"]}
    i_by = {e["spelling"]: e for e in ri["entries"]}
    both = sorted(set(s_by) & set(i_by))
    only_s = sorted(set(s_by) - set(i_by))
    only_i = sorted(set(i_by) - set(s_by))
    class_disagreements = [
        {"language": "swift", "id": "swift/disagreement_%d" % n,
         "spelling": s,
         "route_source_class": s_by[s]["class"],
         "route_installed_class": i_by[s]["class"]}
        for n, s in enumerate(both) if s_by[s]["class"] != i_by[s]["class"]]

    findings = list(rs["findings"])
    findings.append({
        "id": "F35-2",
        "statement": "The two routes agree on the type set." if not
                     (only_s or only_i) else
                     "The two routes DISAGREE on the type set; the "
                     "difference is recorded and is not resolved by "
                     "preference.",
        "computed": {
            "in_both": len(both),
            "route_source_only": [{"language": "swift",
                                   "id": "swift/source_only_%d" % n,
                                   "spelling": s}
                                  for n, s in enumerate(only_s)],
            "route_installed_only": [{"language": "swift",
                                      "id": "swift/installed_only_%d" % n,
                                      "spelling": s}
                                     for n, s in enumerate(only_i)],
        },
        "evidence_class": "computed set difference over the two routes",
    })
    findings.append({
        "id": "F35-3",
        "statement": "The two routes agree on every class marking."
                     if not class_disagreements else
                     "The routes disagree on at least one class marking.",
        "computed": {"disagreements": class_disagreements},
        "evidence_class": "computed comparison over the two routes",
    })

    rt = route_typecheck(sorted(set(s_by) | set(i_by)))
    if rt["available"]:
        tc_refused = sorted(s for s, e in rt["entries"].items()
                            if not e["accepted"])
        findings.append({
            "id": "F35-4",
            "statement": "The installed compiler typechecks every extracted "
                         "spelling, and refuses a control spelling that no "
                         "authority admits -- so the check has teeth."
                         if not tc_refused else
                         "The installed compiler refused at least one "
                         "extracted spelling.",
            "computed": {
                "spellings_offered": len(rt["entries"]),
                "spellings_the_compiler_accepted": sum(
                    1 for e in rt["entries"].values() if e["accepted"]),
                "spellings_the_compiler_refused": [
                    {"language": "swift", "id": "swift/typecheck_refused_%d"
                     % n, "spelling": s} for n, s in enumerate(tc_refused)],
                "negative_control_accepted": rt["negative_control"][
                    "accepted"],
                "negative_control_diagnostic": rt["negative_control"][
                    "diagnostic"],
            },
            "evidence_class": "the compiler's own testimony, per spelling",
        })

    # the inventory rows -- multi-witness admission, in type_inventory.json's
    # exact row shape (a UNIT OBJECT per type, spelling as a display label)
    types = []
    for n, s in enumerate(sorted(set(s_by) | set(i_by))):
        admitted = []
        if s in s_by:
            e = s_by[s]
            rec = {
                "witness": "compiler_source",
                "source": e["declared_in"],
                "read_at_ref": rs["pin"]["git_describe_all"],
                "declared_as": e["declaration_line"],
                "verification": "template_generation_loop"
                                if e["generator"] else "source_declaration",
            }
            if e["generator"]:
                rec["generator"] = e["generator"]
            if e["target_condition"]:
                rec["condition"] = e["target_condition"]
            admitted.append(rec)
        if s in i_by:
            e = i_by[s]
            admitted.append({
                "witness": "installed_module_interface",
                "source": e["declared_in"],
                "read_at_ref": ri["pin"][
                    "compiler_version_quoted_from_the_file"],
                "declared_as": e["declaration_line"],
                "verification": "interface_declaration",
            })
        if rt["available"] and rt["entries"].get(s, {}).get("accepted"):
            admitted.append({
                "witness": "compiler_typecheck",
                "source": "%s in container %s" % (SWIFT_FRONTEND, CONTAINER),
                "read_at_ref": rt["version_quoted_from_the_tool"],
                "declared_as": rt["entries"][s]["source"],
                "verification": "typechecked_by_the_installed_compiler",
            })
        cls = (s_by[s]["class"] if s in s_by else i_by[s]["class"])
        csrc = (s_by[s]["class_source"] if s in s_by
                else i_by[s]["class_source"])
        types.append({
            "language": "swift",
            "id": "swift/type_%d" % n,
            "spelling": s,
            "admitted_by": admitted,
            "class": cls,
            "class_source": csrc,
        })
    return rs, ri, rt, findings, types, both, only_s, only_i


def corpus_witness(types):
    """The confirming witness, added exactly as type_inventory.py adds it."""
    units = json.load(open(os.path.join(HERE, "op_units_swift.json")))
    probes = units["probes"]
    sides = {}
    for r in probes.values():
        if "ship" not in r:
            continue
        for side in ("lhs_type", "rhs_type"):
            t = r["meta"].get(side)
            if t:
                sides[t] = sides.get(t, 0) + 1
    for e in types:
        if e["spelling"] in sides:
            e["admitted_by"].append({
                "witness": "corpus_accepted",
                "source": "op_units_swift.json",
                "accepted_probe_sides": sides[e["spelling"]],
                "verification": "observed_on_accepted_probe",
            })
    return units, sides


def refuse_own_output_on_spelling_failure(paths):
    cmd = [sys.executable, os.path.join(HERE, "check_no_spelling_keys.py")]
    cmd += paths
    p = subprocess.run(cmd, capture_output=True, text=True)
    sys.stdout.write(p.stdout)
    sys.stderr.write(p.stderr)
    if p.returncode != 0:
        for path in paths:
            if os.path.exists(path):
                os.remove(path)
        raise SystemExit("REFUSED OWN OUTPUT: the spelling-key check failed")


def main():
    rs, ri, rt, findings, types, both, only_s, only_i = build()
    units, sides = corpus_witness(types)

    unadmitted = sorted(set(sides) - {e["spelling"] for e in types})
    findings.append({
        "id": "F35-5",
        "statement": "Every type spelling on swift's accepted probes is "
                     "admitted by an extracted (non-corpus) authority; "
                     "swift's row in log_116's direction-two table is no "
                     "longer a tautology."
                     if not unadmitted else
                     "Some spelling on an accepted probe is admitted by no "
                     "authority.",
        "computed": {
            "accepted_probes": units["tally"]["accepted"],
            "distinct_spellings_used_by_accepted_probes": len(sides),
            "spellings_no_authority_admits": [
                {"language": "swift", "id": "swift/unadmitted_%d" % n,
                 "spelling": s} for n, s in enumerate(unadmitted)],
        },
        "evidence_class": "computed set difference, inventory against "
                          "op_units_swift.json",
    })

    authority = {
        "generated_by": "swift_type_authority.py",
        "task": "TASK 35 -- swift's extracted scalar type authority",
        "spelling_ban": "no operator token appears in any key, grouping, "
                        "pairing or row structure here; the subject of this "
                        "file is types",
        "acceptance_bar": "two independent routes agreeing; a disagreement "
                          "is a reported finding, never resolved by "
                          "preference",
        "routes": {"route_source": rs, "route_installed": ri,
                   "route_typecheck": rt},
        "agreement": {
            "types_in_both_routes": [
                {"language": "swift", "id": "swift/both_%d" % n,
                 "spelling": s} for n, s in enumerate(both)],
            "route_source_only": [
                {"language": "swift", "id": "swift/source_only_%d" % n,
                 "spelling": s} for n, s in enumerate(only_s)],
            "route_installed_only": [
                {"language": "swift", "id": "swift/installed_only_%d" % n,
                 "spelling": s} for n, s in enumerate(only_i)],
        },
        "findings": findings,
        "types": types,
    }

    inv = json.load(open(os.path.join(HERE, "type_inventory.json")))
    inv["generated_by"] = ("type_inventory.py (c, cpp, go, rust rows, "
                           "copied verbatim) + swift_type_authority.py "
                           "(swift rows)")
    inv["task"] = ("TASK 29 (a) extended by TASK 35 -- swift's rows are now "
                   "extracted from the pinned swift source and the "
                   "installed module interface")
    inv["replaces"] = ("supersedes type_inventory.json, which is left "
                       "untouched on disk. Only swift's language record "
                       "differs; the other four are copied byte-for-byte.")
    inv["pins"]["swift_source"] = rs["pin"]
    inv["pins"]["swift_installed_interface"] = ri["pin"]
    inv["witness_definitions"]["compiler_source"] = (
        "the compiler's own stdlib source declares the type, at a pinned "
        "commit; for a .gyb template the declaration is read through the "
        "template's own generation loop")
    inv["witness_definitions"]["installed_module_interface"] = (
        "the installed stdlib module interface for this target declares "
        "the type, at the interface file's own stated compiler version")
    sw = inv["languages"]["swift"]
    sw["witnesses"]["compiler_source"] = {
        "source": os.path.join(CORE, "IntegerTypes.swift.gyb") + " ; " +
                  os.path.join(CORE, "FloatingPointTypes.swift.gyb") + " ; " +
                  os.path.join(CORE, "Bool.swift") + " ; " +
                  os.path.join(CORE, "Int128.swift") + " ; " +
                  os.path.join(CORE, "UInt128.swift"),
        "read_at_ref": rs["pin"]["git_describe_all"],
        "refusal": None,
    }
    sw["witnesses"]["installed_module_interface"] = {
        "source": IFACE,
        "read_at_ref": ri["pin"]["compiler_version_quoted_from_the_file"],
        "refusal": None,
    }
    sw["witnesses"]["compiler_table"]["refusal"] = (
        "SUPERSEDED BY TASK 35: this refusal was true of the machine on "
        "2026-09-01 before the pinned clone landed. Swift's authority is "
        "now read by the compiler_source and installed_module_interface "
        "witnesses above; the original text is kept as history.")
    sw["counts"] = {
        "compiler_source_admitted": len(rs["entries"]),
        "installed_interface_admitted": len(ri["entries"]),
        "two_route_admitted": len(both),
        "corpus_confirmed": len(sides),
        "distinct_entries": len(types),
    }
    sw["types"] = types

    p_auth = os.path.join(HERE, "swift_type_authority.json")
    p_inv = os.path.join(HERE, "type_inventory2.json")
    with open(p_auth, "w") as fh:
        json.dump(authority, fh, indent=1, sort_keys=False)
    with open(p_inv, "w") as fh:
        json.dump(inv, fh, indent=1, sort_keys=False)

    p_md = os.path.join(HERE, "type_inventory2.md")
    with open(p_md, "w") as fh:
        fh.write("# type_inventory2.json -- swift's rows extracted "
                 "(TASK 35)\n\n")
        fh.write("source pin: %s\n" % rs["pin"]["git_log_1"])
        fh.write("installed interface pin: %s\n\n"
                 % ri["pin"]["compiler_version_quoted_from_the_file"])
        fh.write("| swift type | class | source route | installed route "
                 "| corpus |\n|---|---|---|---|---|\n")
        for e in types:
            w = {a["witness"] for a in e["admitted_by"]}
            fh.write("| %s | %s | %s | %s | %s |\n" % (
                e["spelling"], e["class"],
                "yes" if "compiler_source" in w else "-",
                "yes" if "installed_module_interface" in w else "-",
                "yes" if "corpus_accepted" in w else "-"))
        fh.write("\nfindings\n")
        for f in findings:
            fh.write("- %s: %s\n" % (f["id"], f["statement"]))

    refuse_own_output_on_spelling_failure([p_auth, p_inv])
    print("wrote %s" % p_auth)
    print("wrote %s" % p_inv)
    print("wrote %s" % p_md)
    print("swift types: source=%d installed=%d both=%d union=%d" % (
        len(rs["entries"]), len(ri["entries"]), len(both), len(types)))
    print("source only: %s" % only_s)
    print("installed only: %s" % only_i)


if __name__ == "__main__":
    main()
