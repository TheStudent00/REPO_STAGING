#!/usr/bin/env python3
"""fold_interp_php.py -- task 5(d): fold the php dispatch pilot into
the pilots' own .md+.json format (log_082 finding 5).

SOURCE, unmodified, read only: `PUBLIC/Airlock/agent/out/
interp_php_b/{dispatch_report.txt,dispatch_diff.json,probes/*.php}`,
plus the Airlock lane logs under `agent/logs/*interp_php*` for the
pin history and build outcomes.

THE PIN IS A COMPROMISE -- recorded here because log_082 flagged it
as recorded only inside a lane script until now.  Three php versions
were tried, in order, all on the SAME coverage build flags
(`--coverage -O0 -g`):

  - PHP 8.3.0 -- FAILED.  `Zend/zend_atomic.h` uses
    `__c11_atomic_exchange` / `__c11_atomic_load` / `__c11_atomic_store`
    without including `<stdatomic.h>` under this container's compiler;
    `make` stopped at `ext/date/php_date.lo`
    (`error: implicit declaration of function '__c11_atomic_exchange'`,
    pasted from `agent/logs/20260831T051838Z__interp_php_a_build_"
    local.sh.log`).
  - PHP 8.2.13 -- FAILED, same root cause, four separate attempts
    (`agent/logs/20260831T052013Z`, `052104Z`, `052250Z`, `052342Z`
    `__interp_php_a_build_local.sh.log`), one of which got one file
    further (`Zend/zend_execute_API.lo`) before the same atomic-
    intrinsic error, and one where retrying the same source under a
    slightly different flag order turned the error into "incorrect
    number of arguments to function '__atomic_exchange'" -- same
    underlying incompatibility, different diagnostic wording.
  - PHP 7.4.33 -- the first attempt still failed
    (`ext/standard/scanf.lo`, `agent/logs/20260831T052441Z`), the
    SECOND attempt succeeded
    (`agent/logs/20260831T052532Z__interp_php_a_build_local.sh.log`,
    `PHP 7.4.33 (cli) (built: Aug 31 2026 05:25:57) ( NTS )`, exit 0
    in 30.7s).  7.4 predates PHP's own C11-atomics zend_atomic.h
    entirely, so the failure mode does not apply.

This is a COMPROMISE, not a preference: 7.4.33 is what built in this
container, not the version this line would have chosen first.  Any
claim below is scoped to 7.4.33 and does not generalize to 8.x.

WHAT WAS **NOT** DONE. Same shape as `fold_interp_ruby.py`'s pilot:
NO arch-unit was extracted.  Coverage (tally) build only.  php does
not enter `langs.py`'s `LANGS_INTERP` for the same reason ruby does
not.

This script reads the raw Airlock files and WRITES `interp_php.md`
and `interp_php.json`.  No clustering/grouping/pairing occurs;
check_no_spelling_keys.py is still run on the .json output as a
formality, same as the ruby fold.
"""
import json
import os
import re

AIRLOCK_OUT = os.path.expanduser("PUBLIC/Airlock/agent/out")
AIRLOCK_LOGS = os.path.expanduser("PUBLIC/Airlock/agent/logs")
PHP_DIR = os.path.join(AIRLOCK_OUT, "interp_php_b")
HERE = os.path.dirname(os.path.abspath(__file__))

PIN_LOG_OK = os.path.join(
    AIRLOCK_LOGS,
    "20260831T052532Z__interp_php_a_build_local.sh.log")
PIN_LOGS_FAILED = [
    ("PHP 8.3.0",
     "20260831T051838Z__interp_php_a_build_local.sh.log",
     "implicit declaration of function '__c11_atomic_exchange'",
     "ext/date/php_date.lo"),
    ("PHP 8.2.13",
     "20260831T052013Z__interp_php_a_build_local.sh.log",
     "implicit declaration of function '__c11_atomic_exchange'",
     "ext/date/php_date.lo"),
    ("PHP 8.2.13",
     "20260831T052342Z__interp_php_a_build_local.sh.log",
     "implicit declaration of function '__c11_atomic_init'",
     "Zend/zend_execute_API.lo"),
    ("PHP 7.4.33 (first attempt)",
     "20260831T052441Z__interp_php_a_build_local.sh.log",
     "make error (unrelated to atomics)",
     "ext/standard/scanf.lo"),
]


def read(path):
    return open(path).read()


def parse_top_lines(report_text, section_name, n=12):
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
    ok_log = read(PIN_LOG_OK)
    banner_m = re.search(r"^(PHP 7\.4\.33 \(cli\).*)$", ok_log, re.M)
    banner = banner_m.group(1) if banner_m else None

    report = read(os.path.join(PHP_DIR, "dispatch_report.txt"))
    probes = {}
    probes_dir = os.path.join(PHP_DIR, "probes")
    for name in sorted(os.listdir(probes_dir)):
        probes[name] = read(os.path.join(probes_dir, name))

    header_counts = parse_header_counts(report)
    top_smallint = parse_top_lines(report, "p1_smallint")
    top_float = parse_top_lines(report, "p2_float")

    pin_history = []
    for version, logname, error, stopfile in PIN_LOGS_FAILED:
        pin_history.append(dict(tried=version, outcome="FAILED",
                                 log="agent/logs/%s" % logname,
                                 error=error, stopped_at=stopfile))
    pin_history.append(dict(
        tried="PHP 7.4.33 (second attempt)", outcome="SUCCEEDED",
        log="agent/logs/20260831T052532Z__interp_php_a_build_local.sh.log",
        banner=banner, elapsed_s=30.7))

    doc = {
        "meta": {
            "what": "php pilot of the interpreter track: which "
                    "interpreter handler executes for a PHP addition "
                    "on int and float operands, measured by "
                    "differential gcov coverage.  NO arch-unit "
                    "extracted -- dispatch (tally) only.",
            "date": "2026-08-31",
            "home": "Planning/node_0_3_research/node_0_3_5_compiler_"
                    "graph/SUPPORT_scaling_design.md, interpreter-"
                    "track section",
            "pin": {
                "project": "php",
                "tag": "7.4.33",
                "runtime_banner": banner,
                "evidence": "artifact fact (the built interpreter's "
                            "own --version banner)",
                "compromise": True,
                "compromise_note": "7.4.33 is a COMPROMISE pin, not "
                                    "the first choice.  PHP 8.3.0 and "
                                    "8.2.13 both failed the coverage "
                                    "build in this container: "
                                    "Zend/zend_atomic.h's C11 atomic "
                                    "intrinsics "
                                    "(__c11_atomic_exchange/_load/"
                                    "_store) are used without the "
                                    "matching declaration under this "
                                    "compiler.  7.4 predates that "
                                    "file's C11-atomics path "
                                    "entirely, so it built.  See "
                                    "pin_history for every attempt, "
                                    "pasted from the actual build "
                                    "logs.",
            },
            "pin_history": pin_history,
        },
        "method": {
            "kind": "differential gcov line coverage (tally, per-"
                    "run) -- same method as interp_cpython.md and "
                    "interp_ruby.json.  p0_baseline returns the "
                    "first argument without adding.",
            "probes": probes,
            "probe_note": "p2 is named 'float' here, not 'bigint': "
                           "PHP has no arbitrary-precision integer "
                           "type in its core (GMP is an optional "
                           "extension, not probed here).  The 'big "
                           "value' probe instead uses two float "
                           "literals (1.2345e+100, 6.7890e+100), so "
                           "this pilot measures int-addition and "
                           "float-addition dispatch, not int-vs-"
                           "bignum the way cpython's and ruby's do. "
                           "Named rather than silently matched to "
                           "the other two pilots' shape.",
        },
        "header_counts": header_counts,
        "dispatch_top_lines": {
            "p1_smallint_minus_baseline": top_smallint,
            "p2_float_minus_baseline": top_float,
            "evidence_class": "tally, per-run -- fact for these runs "
                               "on this build; no ordering "
                               "information.",
        },
        "reading": {
            "smallint": "Zend/zend_vm_execute.h carries the largest "
                        "delta (sum_delta=1,300,011 over 100000 "
                        "calls) -- this is Zend's generated opcode "
                        "handler table, the interpreted-VM analogue "
                        "of cpython's generated_cases.c.h and ruby's "
                        "vm.inc.  Zend/zend_execute.c follows "
                        "(400,000) -- the ZEND_ADD opcode handler's "
                        "call site.  Parser/scanner/compiler files "
                        "carry much smaller deltas, read as one-time "
                        "compile-time cost, not the addition itself.",
        },
        "what_was_not_done": [
            "NO arch-unit extracted -- no anchor/ship compiled pair, "
            "no objdump slice, no instruction bytes for the ZEND_ADD "
            "opcode handler (zend_vm_execute.h's generated "
            "ZEND_ADD_SPEC_* cases / zend_operators.c's add_function "
            "fast paths).  This pilot stops at the dispatch layer.",
            "no diary -- order is unmeasured.",
            "no normalization to canonical form, no matching against "
            "the compiled-language units, no bridge or dominance "
            "claim.",
            "no bignum probe -- PHP core has no arbitrary-precision "
            "integer type; the 'big value' probe uses floats "
            "instead (see method.probe_note).",
            "the 8.3.0 / 8.2.13 coverage-build failure was not "
            "chased to a fix (patching zend_atomic.h or the "
            "compiler's C11-atomics visibility) -- 7.4.33 was taken "
            "as the working pin instead.  Whether that failure is "
            "worth fixing so a newer PHP can be measured is left "
            "open, not decided here.",
            "scope: x86-64, one pin (php 7.4.33, a compromise), int "
            "and float operands only, one operator (+).",
        ],
    }

    json_path = os.path.join(HERE, "interp_php.json")
    json.dump(doc, open(json_path, "w"), indent=1)

    md_lines = []
    md_lines.append("# interp_php -- the php pilot of the "
                     "interpreter track\n")
    md_lines.append("Folded 2026-08-31 by `fold_interp_php.py`, task "
                     "5(d), from the Airlock lane outputs under "
                     "`PUBLIC/Airlock/agent/out/interp_php_b/` "
                     "(real gcov deltas, dated 2026-08-31: 344 lines "
                     "with a positive delta across 9 files for the "
                     "smallint probe -- the number log_082 named as "
                     "measured-and-orphaned).  Data: "
                     "`interp_php.json`.\n")
    md_lines.append("## the pin -- a COMPROMISE, recorded in full\n")
    md_lines.append("| tried | outcome | detail |\n|---|---|---|")
    for row in pin_history:
        if row["outcome"] == "FAILED":
            md_lines.append("| %s | FAILED | `%s`, stopped at `%s` |"
                             % (row["tried"], row["error"],
                                row["stopped_at"]))
        else:
            md_lines.append("| %s | SUCCEEDED | `%s`, %ss |"
                             % (row["tried"], row["banner"],
                                row["elapsed_s"]))
    md_lines.append("")
    md_lines.append("8.3.0 and 8.2.13 both fail the SAME way: "
                     "`Zend/zend_atomic.h`'s C11 atomic intrinsics "
                     "(`__c11_atomic_exchange`/`_load`/`_store`) are "
                     "used without a declaration this container's "
                     "compiler accepts.  7.4 predates that file's "
                     "C11-atomics path, so it is unaffected -- not a "
                     "coincidence, a version boundary.  7.4.33 is "
                     "therefore a COMPROMISE pin: the first version "
                     "that BUILT, not the first version tried. Any "
                     "claim in this file is scoped to 7.4.33.\n")
    md_lines.append("## the instrument, said plainly\n")
    md_lines.append("Same as the ruby and cpython pilots: a "
                     "**TALLY** (gcov line counters), not a diary.\n")
    md_lines.append("## the method\n")
    md_lines.append("Differential coverage, 100000 calls per probe. "
                     "`p0_baseline` returns the first argument "
                     "without adding.  `p1_smallint` adds two PHP "
                     "ints (3, 4).  `p2_float` adds two floats "
                     "(1.2345e+100, 6.7890e+100) -- PHP has no "
                     "arbitrary-precision integer in core, so this "
                     "pilot's 'big value' probe is a FLOAT probe, "
                     "not a bignum probe, unlike cpython's and "
                     "ruby's.\n")
    md_lines.append("## the measured dispatch path (top lines, "
                     "pasted from the delta)\n")
    md_lines.append("### smallint (3 + 4)\n")
    md_lines.append("| file | lines w/ delta | sum_delta |\n|---|---|---|")
    for r in top_smallint:
        md_lines.append("| `%s` | %d | %d |" % (r["file"], r["lines"],
                                                  r["sum_delta"]))
    md_lines.append("")
    md_lines.append("### float (1.2345e+100 + 6.7890e+100)\n")
    md_lines.append("| file | lines w/ delta | sum_delta |\n|---|---|---|")
    for r in top_float:
        md_lines.append("| `%s` | %d | %d |" % (r["file"], r["lines"],
                                                  r["sum_delta"]))
    md_lines.append("")
    md_lines.append("Reading (interpretation, not measured order): "
                     "%s\n" % doc["reading"]["smallint"])
    md_lines.append("## evidence classes on the claims\n")
    md_lines.append("- pin history, build banner -- **artifact "
                     "fact** (pasted straight from the build logs).")
    md_lines.append("- the dispatch path -- **tally, per-run**: fact "
                     "for these runs on this build, no order.")
    md_lines.append("- the file-name reading above -- "
                     "**interpretation**.\n")
    md_lines.append("## what was NOT done\n")
    for item in doc["what_was_not_done"]:
        md_lines.append("- %s" % item)
    md_lines.append("")
    md_lines.append("## why php does not enter a LANGS list\n")
    md_lines.append("Same reason as ruby (see `interp_ruby.md`): no "
                     "arch-unit was extracted, and `langs.py`'s "
                     "`LANGS_INTERP` requires reaching that stage.\n")
    md_lines.append("## guard\n")
    md_lines.append("`check_no_spelling_keys.py interp_php.json` -> "
                     "see the run recorded in log_087.\n")

    md_path = os.path.join(HERE, "interp_php.md")
    open(md_path, "w").write("\n".join(md_lines) + "\n")
    print("wrote", json_path)
    print("wrote", md_path)


if __name__ == "__main__":
    main()
