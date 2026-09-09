#!/usr/bin/env python3
"""runtime_callee_swift_lane.py -- the swift half of TASK 63, run
INSIDE the `trickle` Airlock instance, which is where swift's
toolchain lives.

Node: `hq.research.compiler_graph.arch_unit.runtime_callee`
CORE: Planning/node_0_3_research/node_0_3_5_compiler_graph/
      node_0_3_5_1_arch_unit/node_0_3_5_1_8_runtime_callee/
      CORE_0_3_5_1_8_runtime_callee.md

WHY A LANE AND NOT A HOST RUN.  Task 59 asked `swiftc` on the host,
got no answer, and recorded swift's callers as not attached.  The
audit of round 12 (log_165 §3) found the reason: swift is installed in
the `sandbox-persist` volume at `/persist/swift`, which only a
sandbox instance mounts.  The CORE's rule is unchanged -- the callee
must come from the compiler that built the caller -- so the
extraction runs where that compiler is.

WHAT IT DOES, and every path in it is READ BACK from a toolchain
rather than typed:

  1. `swiftc --version` and `swiftc -print-target-info`, printed.
  2. the builtins archive located by asking the clang that ships
     INSIDE the swift toolchain:
     `<swift>/usr/bin/clang -print-file-name=libclang_rt.builtins-x86_64.a`
  3. every callee name this program is given, extracted from that
     archive with `runtime_callee.RuntimeCallee.extract_closure` --
     the same code the host half runs, relocation-aware, cycle
     guarded.
  4. the units written to /out as JSON, for the host half to merge.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation).  No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns.  The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token.  The token appears exactly once per unit: as a display label
on the member.  HISTORY OF VIOLATIONS, so the pattern is visible: (1)
the arch campaign's cross-language matrix (caught by the owner
2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25
-- the fix brief itself reintroduced it as "same-operator pairs").
MECHANICAL GUARD REQUIRED: every pipeline stage that groups or pairs
units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure.  A brief handed to any subagent for this line MUST paste
this paragraph verbatim."

Coding discipline: no compound one-liner statements.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import runtime_callee as RC                                      # noqa: E402


SWIFTC = "/persist/swift/usr/bin/swiftc"
SWIFT_CLANG = "/persist/swift/usr/bin/clang"
BUILTINS = "libclang_rt.builtins-x86_64.a"

# The callee names swift's own call-bearing units spell, computed on
# the host from canon39 and from the recorded 308-unit list, and
# handed in as data rather than believed in here.
DEFAULT_WANTED = (
    "__extendhfsf2",
    "__truncsfhf2",
    "__divti3",
    "__udivti3",
    "__modti3",
    "__umodti3",
)


def say(transcript, text):
    print(text)
    sys.stdout.flush()
    transcript.append(text)


def locate(transcript):
    """(archive path, the record of how it was found)."""
    record = {"probes": []}
    for argv in ([SWIFTC, "--version"],
                 [SWIFTC, "-print-target-info"]):
        probe = RC.Probe("swiftc", argv)
        record["probes"].append(probe.as_record())
        say(transcript, "$ %s" % " ".join(argv))
        if probe.stdout:
            for line in probe.stdout.splitlines()[:6]:
                say(transcript, "  %s" % line)
        if probe.exit_code != 0:
            say(transcript, "  exit %d  %s"
                % (probe.exit_code, probe.stderr.splitlines()[0]
                   if probe.stderr else ""))
    argv = [SWIFT_CLANG, "-print-file-name=%s" % BUILTINS]
    probe = RC.Probe("swift's own clang", argv)
    record["probes"].append(probe.as_record())
    say(transcript, "$ %s" % " ".join(argv))
    say(transcript, "  %s" % probe.stdout)
    archive = probe.path()
    if archive is None:
        record["not_located"] = probe.as_record()
        return None, record
    if not archive.endswith(".a"):
        record["not_located"] = probe.as_record()
        return None, record
    record["archive"] = archive
    return archive, record


def main():
    transcript = []
    wanted = list(DEFAULT_WANTED)
    if len(sys.argv) > 1:
        wanted = list(sys.argv[1:])

    say(transcript, "== WHICH SIDE OF THE CONTAINER WALL IS THIS? ==")
    for path in (SWIFTC, "/persist/swift/usr/bin", "/out", "/work"):
        say(transcript, "  %-34s exists: %s"
            % (path, os.path.exists(path)))
    say(transcript, "")

    say(transcript, "== SWIFT'S TOOLCHAIN, ASKED WHERE ITS OWN "
                    "BUILTINS ARCHIVE IS ==")
    archive, record = locate(transcript)
    say(transcript, "")
    if archive is None:
        say(transcript, "REFUSING: swift's builtins archive was not "
                        "located from the toolchain's own output.")
        out = {
            "meta": {
                "generator": "runtime_callee_swift_lane.py",
                "toolchain": "swiftc",
                "located": False,
                "location_record": record,
            },
            "units": {},
            "could_not_extract": {},
            "transcript": transcript,
        }
        json.dump(out, open("/out/runtime_callee_swift.json", "w"),
                  indent=1, sort_keys=True)
        return 4

    engine = RC.RuntimeCallee.__new__(RC.RuntimeCallee)
    engine.probes = []
    engine.archive_paths = {"swiftc": archive}
    engine.not_located = {}
    engine.family_of = None
    table, trouble = RC.defined_symbols(archive)
    engine.symbol_tables = {"swiftc": table}
    say(transcript, "the archive's own symbol index names %d defined "
                    "symbols  (nm --print-armap)" % len(table))
    if trouble:
        say(transcript, "  nm trouble: %s" % trouble)
    say(transcript, "")

    say(transcript, "== IS EACH NAME A ROUTINE OF SWIFT'S OWN "
                    "RUNTIME? ==")
    for callee in wanted:
        yes, where = engine.is_runtime_routine(callee, "swiftc")
        say(transcript, "  %-16s %s" % (callee, "yes" if yes else "no"))
    say(transcript, "")

    say(transcript, "== THE BODIES, EXTRACTED (nested callees "
                    "followed) ==")
    units = {}
    troubles = {}
    seen = set()
    for callee in wanted:
        got, bad = engine.extract_closure(callee, "swiftc", seen)
        units.update(got)
        troubles.update(bad)
    for key in sorted(units):
        one = units[key]
        say(transcript, "  %-28s %4d instructions   nested: %s"
            % (key, one["instruction_count"],
               ",".join(one["nested_callees"]) or "-"))
    for key in sorted(troubles):
        say(transcript, "  %-28s NOT EXTRACTED: %s"
            % (key, troubles[key]))
    say(transcript, "")

    literal = units.get("swiftc/__extendhfsf2")
    if literal is not None:
        say(transcript, "== LITERAL -- swiftc/__extendhfsf2, the body "
                        "as objdump printed it ==")
        say(transcript, "archive: %s" % literal["archive"])
        say(transcript, "member:  %s" % literal["archive_member"])
        for index, line in enumerate(literal["body_as_read"]):
            say(transcript, "  %3d  %s" % (index, line))
        say(transcript, "")

    out = {
        "meta": {
            "generator": "runtime_callee_swift_lane.py",
            "node": "hq.research.compiler_graph.arch_unit."
                    "runtime_callee",
            "toolchain": "swiftc",
            "located": True,
            "archive": archive,
            "location_record": record,
            "wanted": wanted,
            "ran_inside": "the trickle Airlock instance, where "
                          "/persist/swift is mounted",
        },
        "units": units,
        "could_not_extract": troubles,
        "transcript": transcript,
    }
    json.dump(out, open("/out/runtime_callee_swift.json", "w"),
              indent=1, sort_keys=True)
    print("done: %d callee units written to "
          "/out/runtime_callee_swift.json" % len(units))
    return 0


sys.exit(main())
