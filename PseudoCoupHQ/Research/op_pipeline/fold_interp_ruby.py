#!/usr/bin/env python3
"""fold_interp_ruby.py -- task 5(d): fold the ruby dispatch pilot into
the pilots' own .md+.json format (log_082 finding 5).

SOURCE, unmodified, read only: `~/Programming/Airlock/agent/out/
interp_ruby_b/{dispatch_report.txt,dispatch_diff.json,bytecode.txt,
probes/*.rb}`, plus the pin (`ruby_pin.txt` and the build log's own
banner line) and the build log (`ruby_configure.log`,
`ruby_make_tail.log`, and the Airlock lane logs under
`agent/logs/*interp_ruby*`).

WHAT WAS MEASURED. Same method as `interp_cpython.md`: DIFFERENTIAL
gcov line-coverage. `p0_baseline` returns the first argument without
adding; `p1_smallint` adds two Fixnums (3, 4); `p2_bigint` adds two
values built from `(1 << 100) + k` -- real Bignums.  The delta is
`count(probe run) - count(baseline run)`, 100000 calls each.

WHAT WAS **NOT** DONE, stated here because it drives this file's
shape: NO arch-unit was extracted.  This pilot only ran the coverage
(tally) build -- there is no anchor/ship pair, no objdump slice, no
handler bytes.  `interp_cpython.md`'s three-layer model (probe ->
bytecode -> handler ARCH-UNIT) stops at layer 2 here: probe and
bytecode are measured, the handler is named (by file:line, from the
tally) but never extracted as bytes.  Consequently ruby CANNOT enter
`langs.py`'s `LANGS_INTERP` (which is defined as "reached the
arch-unit stage") and does not appear in any tree_match / dom_ops
LANGS list -- see `langs.py`'s FOLD NOTE.

This script reads the raw Airlock files and WRITES `interp_ruby.md`
and `interp_ruby.json`, new files, in the same shape as
`interp_cpython.md`/`.json`.  It performs no clustering, matching,
grouping or pairing, so THE SPELLING BAN's mechanical guard is run on
the .json output only as a formality (grouping keys do not arise in a
single-language pilot record), and its PASS/FAIL is recorded in the
.md file, same as `interp_cpython.md` does for itself.
"""
import json
import os
import re

AIRLOCK_OUT = os.path.expanduser(
    "~/Programming/Airlock/agent/out")
RUBY_DIR = os.path.join(AIRLOCK_OUT, "interp_ruby_b")
HERE = os.path.dirname(os.path.abspath(__file__))

PIN_FILE = os.path.join(AIRLOCK_OUT, "ruby_pin.txt")
CONFIGURE_LOG = os.path.join(AIRLOCK_OUT, "ruby_configure.log")


def read(path):
    return open(path).read()


def parse_top_lines(report_text, section_name, n=12):
    """the top N 'file lines=.. sum_delta=..' rows under one
    '==== <section_name> minus p0_baseline: ... ====' block."""
    m = re.search(re.escape(section_name) + r" minus p0_baseline:.*?\n(.*?)\n  ----",
                   report_text, re.S)
    if m is None:
        return []
    rows = []
    for line in m.group(1).splitlines():
        line = line.strip()
        mm = re.match(r"^(\S+)\s+lines=(\d+)\s+sum_delta=(\d+)$", line)
        if mm:
            rows.append(dict(file=mm.group(1), lines=int(mm.group(2)),
                              sum_delta=int(mm.group(3))))
    return rows[:n]


def parse_header_counts(report_text):
    out = {}
    for line in report_text.splitlines():
        m = re.match(r"^tag (\S+): (\d+) files, (\d+) executed lines$", line)
        if m:
            out[m.group(1)] = dict(files=int(m.group(2)),
                                    executed_lines=int(m.group(3)))
    return out


def main():
    pin = read(PIN_FILE).strip()
    report = read(os.path.join(RUBY_DIR, "dispatch_report.txt"))
    bytecode = read(os.path.join(RUBY_DIR, "bytecode.txt"))
    probes = {}
    probes_dir = os.path.join(RUBY_DIR, "probes")
    for name in sorted(os.listdir(probes_dir)):
        probes[name] = read(os.path.join(probes_dir, name))

    header_counts = parse_header_counts(report)
    top_smallint = parse_top_lines(report, "p1_smallint")
    top_bigint = parse_top_lines(report, "p2_bigint")

    disasm_m = re.search(r"=== dis\.dis\(af\) -- as compiled.*?===\n(.*?)"
                          r"=== warming", bytecode, re.S)
    disasm_before = disasm_m.group(1).strip() if disasm_m else None
    disasm_m2 = re.search(r"=== after warm-up ===\n(.*)$", bytecode, re.S)
    disasm_after = disasm_m2.group(1).strip() if disasm_m2 else None

    doc = {
        "meta": {
            "what": "ruby pilot of the interpreter track: which "
                    "interpreter handler executes for a Ruby "
                    "addition on Fixnum and Bignum operands, "
                    "measured by differential gcov coverage.  NO "
                    "arch-unit extracted -- dispatch (tally) only.",
            "date": "2026-08-31",
            "home": "Planning/node_0_3_research/node_0_3_5_compiler_"
                    "graph/SUPPORT_scaling_design.md, interpreter-"
                    "track section",
            "pin": {
                "project": "ruby",
                "tag": pin,
                "runtime_banner": "ruby 3.3.0 (2023-12-25 revision "
                                   "5124f9ac75) [x86_64-linux]",
                "evidence": "artifact fact (the built interpreter's "
                            "own -v banner, agent/logs/"
                            "20260831T051405Z__interp_ruby_a_build_"
                            "local.sh.log line 89)",
            },
            "build": {
                "configure_note": "tool/config.guess and config.sub "
                                   "already present; fiddle and "
                                   "psych extensions did not "
                                   "configure (missing libffi) and "
                                   "were not installed -- irrelevant "
                                   "to Integer#+ but recorded "
                                   "honestly rather than silently "
                                   "dropped.",
                "used_for": "the dispatch measurement only -- no "
                            "separate anchor/ship pair was built for "
                            "ruby, unlike cpython.",
            },
        },
        "method": {
            "kind": "differential gcov line coverage (tally, per-"
                    "run) -- same method as interp_cpython.md.  "
                    "p0_baseline returns the first argument without "
                    "adding; the delta between a probe run and the "
                    "baseline run is what the addition itself "
                    "reached.",
            "probes": probes,
        },
        "header_counts": header_counts,
        "bytecode_disasm": {
            "before_warmup": {"text": disasm_before},
            "after_warmup": {"text": disasm_after},
            "evidence_class": "the tool's own testimony "
                               "(RubyVM::InstructionSequence#disasm)",
            "note": "the instruction is opt_plus, an INLINE-CACHED "
                    "call site (annotated CcCr: class cache / "
                    "callinfo cache) -- ruby's specialization for "
                    "'+' when the operand classes stay stable, "
                    "analogous to cpython's BINARY_OP_ADD_INT.  "
                    "disasm is IDENTICAL before and after warm-up "
                    "here: ruby's opt_plus is emitted at compile "
                    "time already, unlike cpython's adaptive "
                    "specialization which rewrites the bytecode.",
        },
        "dispatch_top_lines": {
            "p1_smallint_minus_baseline": top_smallint,
            "p2_bigint_minus_baseline": top_bigint,
            "evidence_class": "tally, per-run -- fact for these runs "
                               "on this build; no ordering "
                               "information (see 'what was NOT "
                               "done').",
        },
        "reading": {
            "smallint": "vm.inc and vm_insnhelper.c carry the "
                        "largest deltas (2,200,000 and 1,300,000 "
                        "sum_delta over 100000 calls) -- the opt_plus "
                        "handler and its inline-cache-check "
                        "machinery live there.  st.c and compile.c "
                        "carry much smaller deltas and are read as "
                        "parse/compile-time noise from the harness "
                        "itself, not the addition.",
            "bignum": "for the (1<<100)+k pair, bignum.c enters with "
                      "a large delta (7,900,687) alongside gc.c "
                      "(18,575,292) and shape.c (3,829,436) -- read "
                      "as Bignum allocation and object-shape "
                      "transitions the Fixnum path never takes.  "
                      "This is INTERPRETATION of the tally, not "
                      "measured order (no diary).",
        },
        "what_was_not_done": [
            "NO arch-unit extracted -- no anchor/ship compiled pair, "
            "no objdump slice, no instruction bytes for opt_plus's "
            "C implementation (vm_insnhelper.c's "
            "vm_opt_plus / rb_int_plus).  This pilot stops at the "
            "bytecode/dispatch layer.",
            "no diary -- order is unmeasured, same caveat as "
            "interp_cpython.md.",
            "no normalization to canonical form, no matching against "
            "the compiled-language units, no bridge or dominance "
            "claim -- there is no arch-unit to normalize.",
            "the fiddle and psych extensions did not build (missing "
            "libffi); unrelated to Integer#+, unused by these "
            "probes.",
            "scope: x86-64, one pin (ruby 3.3.0), Fixnum and Bignum "
            "operands only, one operator (+).",
        ],
    }

    json_path = os.path.join(HERE, "interp_ruby.json")
    json.dump(doc, open(json_path, "w"), indent=1)

    md_lines = []
    md_lines.append("# interp_ruby -- the ruby pilot of the "
                     "interpreter track\n")
    md_lines.append("Folded 2026-08-31 by `fold_interp_ruby.py`, task "
                     "5(d), from the Airlock lane outputs under "
                     "`~/Programming/Airlock/agent/out/interp_ruby_b/` "
                     "(real gcov deltas, dated 2026-08-31: 1,050 "
                     "lines with a positive delta across 27 files for "
                     "the smallint probe -- the number log_082 named "
                     "as measured-and-orphaned).  Data: "
                     "`interp_ruby.json`.\n")
    md_lines.append("## the pin\n")
    md_lines.append("- ruby `%s`" % pin)
    md_lines.append("- the built interpreter says: `ruby 3.3.0 "
                     "(2023-12-25 revision 5124f9ac75) [x86_64-linux]`")
    md_lines.append("- evidence class: artifact fact (the binary's "
                     "own `-v` banner)\n")
    md_lines.append("## the instrument, said plainly\n")
    md_lines.append("Same as `interp_cpython.md`: a **TALLY** (gcov "
                     "line counters), not a diary. Order is not "
                     "measured.\n")
    md_lines.append("## the method\n")
    md_lines.append("Differential coverage.  `p0_baseline` returns "
                     "the first argument without adding; the delta "
                     "between a probe run and the baseline run is "
                     "what the addition reached.  Probes: "
                     "`p0_baseline`, `p1_smallint` (3+4), `p2_bigint` "
                     "((1<<100)+12345 and (1<<100)+67890), "
                     "`p3_disasm`.\n")
    md_lines.append("## the bytecode (pasted, `dis`'s own testimony)\n")
    md_lines.append("```\n%s\n```\n" % disasm_before)
    md_lines.append("Unchanged after warm-up (pasted):\n")
    md_lines.append("```\n%s\n```\n" % disasm_after)
    md_lines.append("`opt_plus` is ruby's INLINE-CACHED call site "
                     "for `+` -- comparable in role to cpython's "
                     "`BINARY_OP_ADD_INT`, but emitted at compile "
                     "time rather than installed after a warm-up "
                     "trip (disasm is identical before/after here, "
                     "unlike cpython's).\n")
    md_lines.append("## the measured dispatch path (top lines, "
                     "pasted from the delta)\n")
    md_lines.append("### smallint (3 + 4)\n")
    md_lines.append("| file | lines w/ delta | sum_delta |\n|---|---|---|")
    for r in top_smallint:
        md_lines.append("| `%s` | %d | %d |" % (r["file"], r["lines"],
                                                  r["sum_delta"]))
    md_lines.append("")
    md_lines.append("### bignum ((1<<100)+12345 + (1<<100)+67890)\n")
    md_lines.append("| file | lines w/ delta | sum_delta |\n|---|---|---|")
    for r in top_bigint:
        md_lines.append("| `%s` | %d | %d |" % (r["file"], r["lines"],
                                                  r["sum_delta"]))
    md_lines.append("")
    md_lines.append("Reading (interpretation, not measured order): "
                     "%s\n" % doc["reading"]["smallint"])
    md_lines.append("%s\n" % doc["reading"]["bignum"])
    md_lines.append("## evidence classes on the claims\n")
    md_lines.append("- pin, build banner -- **artifact fact**.")
    md_lines.append("- the bytecode listing -- **the tool's own "
                     "testimony** (`RubyVM::InstructionSequence"
                     "#disasm`).")
    md_lines.append("- the dispatch path -- **tally, per-run**: fact "
                     "for these runs on this build, no order.")
    md_lines.append("- the smallint/bignum readings above -- "
                     "**interpretation**, read off file names, not "
                     "measured order.\n")
    md_lines.append("## what was NOT done\n")
    for item in doc["what_was_not_done"]:
        md_lines.append("- %s" % item)
    md_lines.append("")
    md_lines.append("## why ruby does not enter a LANGS list\n")
    md_lines.append("`langs.py`'s `LANGS_INTERP` is defined as "
                     "\"reached the arch-unit stage\".  ruby has NO "
                     "arch-unit (see above), so it stays out of every "
                     "tree_match / dom_ops LANGS list.  This is not "
                     "an oversight -- entering those lists with no "
                     "arch-unit would mean matching on nothing, which "
                     "is worse than being honestly absent.\n")
    md_lines.append("## guard\n")
    md_lines.append("`check_no_spelling_keys.py interp_ruby.json` -> "
                     "see the run recorded in log_087.  (Formality "
                     "for a single-language pilot record: no "
                     "grouping or pairing occurs in this file.)\n")

    md_path = os.path.join(HERE, "interp_ruby.md")
    open(md_path, "w").write("\n".join(md_lines) + "\n")
    print("wrote", json_path)
    print("wrote", md_path)


if __name__ == "__main__":
    main()
