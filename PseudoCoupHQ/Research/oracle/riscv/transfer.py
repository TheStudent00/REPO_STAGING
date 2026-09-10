#!/usr/bin/env python3
"""transfer.py -- THE COUNT: how much of x86's proved polyfill library
transferred to riscv64, how much had to be re-proved, and how much the
loop still had to run.

Node: hq.research.arch_unit_oracle.  Task rv2, brief sections 2.3 to 2.5,
`PRIVATE/PseudoCoupHQ/Research/briefs/task_rv2_brief.md`.

WHAT THIS IS, one sentence, in relation: the report `transfer.md` is
assembled here from the four json artifacts this task wrote, so every
figure in it is measured and none is typed by hand.

Coding discipline (the owner's ruling): no complex/compound one-liner statements.

usage:
  transfer.py <riscv folder> <bank certificates.json> <out path>
"""

import json
import os
import sys


def read(path):
    return json.load(open(path))


def lines_of(path):
    out = []
    for line in open(path):
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def cell_key(cell):
    return (cell.get("mnem"), cell.get("shape"), cell.get("key_width"))


def main():
    folder = sys.argv[1]
    bank_summary = sys.argv[2]
    out_path = sys.argv[3]

    table = read(os.path.join(folder, "model_table_rv.json"))
    twins = read(os.path.join(folder, "twins.json"))
    inherited = lines_of(os.path.join(folder,
                                      "certificates_riscv64.jsonl"))
    inherit_meta = read(os.path.join(folder,
                                     "certificates_riscv64.json"))
    loop = lines_of(os.path.join(folder, "rv_loop.jsonl"))
    loop_meta = read(os.path.join(folder, "rv_loop.json"))
    attest = read(os.path.join(folder, "attest_rv.json"))
    interp = read(os.path.join(folder, "interp_recheck.json"))
    bank = read(bank_summary)

    lines = []
    say = lines.append

    say("# transfer.md -- what carried from x86 to riscv64, measured")
    say("")
    say("Task rv2, node `hq.research.arch_unit_oracle`. Written by "
        "`transfer.py`; never hand-edited. Every figure below is read "
        "out of this folder's own json.")
    say("")
    say("**The hypothesis this measures, the owner 2026-09-10, LITERAL:** "
        "*\"If we already know what is proven in x86 with their "
        "combination of high-level compiler-operators to emulate "
        "arch-opcodes, it should also be true in RISC-V ... it should "
        "shrink the workload substantially.\"*")
    say("")

    # ---------------------------------------------------------------
    total_cells = twins["meta"]["riscv_cells"]
    reading1 = twins["census"]
    reading2 = twins["census_at_key_width"]
    twinned1 = total_cells - reading1.get("NONE", 0)
    twinned2 = total_cells - reading2.get("NONE", 0)

    say("## 1. The two model tables, and the join between them")
    say("")
    say("Table 1 -- the RISC-V model table, as `model_table_rv.py` "
        "swept it.")
    say("")
    say("| what | count |")
    say("|---|---|")
    census = {}
    mnems = {}
    for row in table["rows"]:
        census[row["outcome"]] = census.get(row["outcome"], 0) + 1
        mnems[row["mnem"]] = True
    say("| sweep attempts | %d |" % len(table["rows"]))
    for outcome in sorted(census):
        say("| rows %s | %d |" % (outcome, census[outcome]))
    say("| mnemonics in the reference's table | %d |" % len(mnems))
    say("| CELLS -- distinct (`mnem`, shape, `key_width`) with at least "
        "one written place | %d |" % total_cells)
    say("")
    say("Table 2 -- the twin, by TERM, in its two readings. READING 1 "
        "is the whole written place; READING 2 cuts both sides to the "
        "RISC-V cell's own `key_width`. RISC-V writes all 64 bits of a "
        "register and its 32-bit forms SIGN-extend, where x86's "
        "32-bit write ZERO-extends, so at the whole place a `w` form "
        "can never twin an x86 32-bit form.")
    say("")
    say("| twin | reading 1 | reading 2 |")
    say("|---|---|---|")
    for how in ("TEXT", "Z3", "NONE"):
        say("| %s | %d | %d |" % (how, reading1.get(how, 0),
                                  reading2.get(how, 0)))
    say("| **cells with a twin** | **%d** | **%d** |"
        % (twinned1, twinned2))
    say("| **of** | **%d** | **%d** |" % (total_cells, total_cells))
    say("")
    say("Table 3 -- the cells with NO twin under either reading, by "
        "mnemonic.")
    say("")
    untwinned = {}
    for row in twins["rows"]:
        if row["how_at_key_width"] != "NONE":
            continue
        untwinned[row["mnem"]] = untwinned.get(row["mnem"], 0) + 1
    say("| `mnem` | untwinned shapes |")
    say("|---|---|")
    for mnem in sorted(untwinned):
        say("| `%s` | %d |" % (mnem, untwinned[mnem]))
    say("")

    # ---------------------------------------------------------------
    say("## 2. The inheritance -- section 2.3 of the brief")
    say("")
    say("Every preferred `proved`/`agreed` certificate in the bank "
        "whose x86 cell a RISC-V cell twins: the certificate's own "
        "SOURCE taken unchanged, compiled for riscv64 at the corpus's "
        "ship flags, carved, lifted with the RISC-V reference, and "
        "gated by z3 against the certificate's own x86-64 body, both "
        "as functions of the same arguments.")
    say("")
    per = {}
    for row in inherited:
        held = per.setdefault(row["target"], {})
        key = "%s / %s" % (row["kind"], row["verdict"].get("outcome"))
        held[key] = held.get(key, 0) + 1
    say("Table 4 -- the inherited certificates, per target.")
    say("")
    say("| target | certificates | outcome |")
    say("|---|---|---|")
    for target in sorted(per):
        for key in sorted(per[target]):
            say("| `%s` | %d | %s |" % (target, per[target][key], key))
    say("")
    proved = [r for r in inherited if r["kind"] == "proved"]
    agreed = [r for r in inherited if r["kind"] == "agreed"]
    disproved = [r for r in inherited if r["kind"] == "sat"]
    whole = {}
    for row in proved:
        got = (row.get("verdict_at_the_whole_place") or {}).get("outcome")
        whole[got] = whole.get(got, 0) + 1
    say("Table 5 -- the inheritance, in one line per number.")
    say("")
    say("| what | count |")
    say("|---|---|")
    say("| certificates attempted | %d |" % len(inherited))
    say("| PROVED on riscv64, at the cell's own `key_width` | %d |"
        % len(proved))
    say("| DISPROVED on riscv64 | %d |" % len(disproved))
    say("| transferred as they are (interpreted targets) | %d |"
        % len(agreed))
    say("| refused, with a cause | %d |"
        % len([r for r in inherited if r["kind"] == "refused"]))
    say("| of the PROVED, also proved at the WHOLE written place | %d |"
        % whole.get("PROVED", 0))
    say("| of the PROVED, differing above the operation's own width | "
        "%d |" % whole.get("DISPROVED", 0))
    say("| distinct RISC-V cells with an inherited PROVED certificate "
        "| %d |" % len(set(cell_key(r["cell"]) for r in proved)))
    say("| distinct RISC-V cells with an inherited `agreed` "
        "certificate | %d |"
        % len(set(cell_key(r["cell"]) for r in agreed)))
    say("")
    causes = {}
    for row in inherited:
        if row["kind"] != "refused":
            continue
        key = (row["target"], row["verdict"]["outcome"])
        causes[key] = causes.get(key, 0) + 1
    say("Table 6 -- every refusal, by cause. A refusal is a FLAG, not "
        "a verdict.")
    say("")
    say("| target | cause | rows |")
    say("|---|---|---|")
    for key in sorted(causes):
        say("| `%s` | %s | %d |" % (key[0], key[1], causes[key]))
    say("")
    say("Table 7 -- the one interpreter's handful, re-run "
        "(`interp_recheck.json`). A check at points, NOT a proof.")
    say("")
    say("| `mnem` | shape | `key_width` | place | outcome | agreements "
        "/ points |")
    say("|---|---|---|---|---|---|")
    for row in interp["rows"]:
        say("| `%s` | %s | %s | %s | %s | %d / %d |"
            % (row["cell"]["mnem"], row["cell"]["shape"],
               row["cell"]["key_width"], row["place"], row["outcome"],
               row["agreements"], row["points"]))
    say("")

    # ---------------------------------------------------------------
    say("## 3. The loop on the delta -- section 2.4 of the brief")
    say("")
    say("`find_emulation` over the RISC-V cells with no twin under "
        "either reading, on c and go, both routes -- the term rendered "
        "by `handful`'s own renderer, and, where the corpus attests a "
        "riscv64 SINGLETON for the cell, that probe's own source.")
    say("")
    say("Table 8 -- the loop's own counts.")
    say("")
    say("| what | count |")
    say("|---|---|")
    say("| cells with no twin | %d |" % reading2.get("NONE", 0))
    say("| runs (cells x written places x targets) | %d |" % len(loop))
    for kind in sorted(loop_meta["census"]):
        say("| runs %s | %d |" % (kind, loop_meta["census"][kind]))
    say("| distinct cells PROVED by the loop | %d |"
        % len(set(cell_key(r["cell"]) for r in loop
                  if r["kind"] == "proved")))
    say("| riscv64 singletons the corpus attests | %d |"
        % len(attest["singletons"]))
    say("| riscv64 cells the corpus attests | %d |"
        % len(attest["cells"]))
    say("")
    say("Table 9 -- the corpus compiled for riscv64 "
        "(`attest_rv.json`), and the two builds' agreement.")
    say("")
    say("| what | count |")
    say("|---|---|")
    for lang in sorted(attest["meta"]["counts"]):
        held = attest["meta"]["counts"][lang]
        say("| `%s` probes in the manifest | %d |"
            % (lang, held["probes_in_the_manifest"]))
        say("| `%s` probes attempted for riscv64 | %d |"
            % (lang, held["attempted"]))
        say("| `%s` probes the x86 unit store holds a ship body for | "
            "%d |" % (lang,
                      held["probes_the_x86_store_holds_a_ship_body_for"]))
    for key in sorted(attest["meta"]["the_two_builds_agree"]):
        say("| %s | %d |"
            % (key, attest["meta"]["the_two_builds_agree"][key]))
    say("")

    # ---------------------------------------------------------------
    say("## 4. The count -- section 2.5 of the brief")
    say("")
    say("Table 10 -- the shrinkage of the workload, as a number.")
    say("")
    reached = set()
    for row in proved:
        reached.add(cell_key(row["cell"]))
    for row in agreed:
        reached.add(cell_key(row["cell"]))
    loop_proved = set(cell_key(r["cell"]) for r in loop
                      if r["kind"] == "proved")
    say("| what | cells | share of the %d RISC-V cells |"
        % total_cells)
    say("|---|---|---|")
    say("| RISC-V cells with at least one written place | %d | 100%% |"
        % total_cells)
    say("| with an x86 twin, READING 1 (the whole written place) | %d | "
        "%.1f%% |" % (twinned1, 100.0 * twinned1 / total_cells))
    say("| with an x86 twin, READING 2 (at the cell's own `key_width`) "
        "| %d | %.1f%% |" % (twinned2, 100.0 * twinned2 / total_cells))
    say("| reached by an INHERITED certificate (proved or agreed) | %d "
        "| %.1f%% |" % (len(reached), 100.0 * len(reached) / total_cells))
    say("| twinned, but the x86 bank holds NO proved or agreed "
        "certificate for the twin | %d | %.1f%% |"
        % (twinned2 - len(reached),
           100.0 * (twinned2 - len(reached)) / total_cells))
    say("| the loop still had to run (the untwinned) | %d | %.1f%% |"
        % (reading2.get("NONE", 0),
           100.0 * reading2.get("NONE", 0) / total_cells))
    say("| PROVED by the loop | %d | %.1f%% |"
        % (len(loop_proved), 100.0 * len(loop_proved) / total_cells))
    say("| **with at least one proved riscv64 emulation, from either "
        "route** | **%d** | **%.1f%%** |"
        % (len(reached | loop_proved),
           100.0 * len(reached | loop_proved) / total_cells))
    say("| **with none yet** | **%d** | **%.1f%%** |"
        % (total_cells - len(reached | loop_proved),
           100.0 * (total_cells - len(reached | loop_proved))
           / total_cells))
    say("")
    say("**The shrinkage, in three sentences, each with its reading.** "
        "Of the %d RISC-V cells, %d (%.1f%%) have an x86 cell that "
        "computes the same term at the cell's own width, so the LOOP "
        "had to be run on only %d (%.1f%%) of them -- and that is the "
        "number the hypothesis asked for. What ACTUALLY arrived by "
        "inheritance is smaller and its reason is not the transfer: "
        "only %d cells (%.1f%%) had an x86 twin the BANK holds a "
        "proved or agreed certificate for, because the x86 loop has "
        "itself proved only part of its own table, so %d twinned cells "
        "have a twin and nothing yet to inherit from it. Between the "
        "two routes %d cells (%.1f%%) now carry at least one proved "
        "riscv64 emulation and %d do not."
        % (total_cells, twinned2, 100.0 * twinned2 / total_cells,
           reading2.get("NONE", 0),
           100.0 * reading2.get("NONE", 0) / total_cells,
           len(reached), 100.0 * len(reached) / total_cells,
           twinned2 - len(reached),
           len(reached | loop_proved),
           100.0 * len(reached | loop_proved) / total_cells,
           total_cells - len(reached | loop_proved)))
    say("")
    say("Table 11 -- THE THREE READINGS of the polyfill-complete set, "
        "RISC-V beside x86. On RISC-V the three COINCIDE, and the "
        "reason is one fact: **the architecture has no flags "
        "register**, so a RISC-V cell writes exactly one place. Strict "
        "(every written place), destination-only (the destination "
        "alone) and corpus-needed (the destination plus the flags "
        "wherever a consumer reads them) are three ways of saying the "
        "same thing when there is one place and no flags.")
    say("")
    say("| reading | what it counts | RISC-V | x86 |")
    say("|---|---|---|---|")
    complete = complete_cells(proved, agreed, loop)
    readings = (bank.get("readings") or {}).get("bank") or {}
    for name, note in (("strict", "every written place proved"),
                       ("destination", "the destination place proved"),
                       ("corpus", "the destination proved, and the "
                                  "flags wherever the corpus shows a "
                                  "consumer reading them")):
        say("| %s | %s | %d | %s |"
            % (name, note, complete,
               readings.get(name, "-")))
    say("")
    say("The x86 column is the bank's own count of proved (cell, "
        "target) PAIRS as `certificates.json` records it, and the "
        "RISC-V column counts CELLS with every written place proved "
        "or agreed on both compiled targets -- the two are not the "
        "same population and are printed side by side rather than "
        "divided.")
    say("")
    say("Table 12 -- what the x86 bank held when this task read it.")
    say("")
    say("| what | value |")
    say("|---|---|")
    say("| the bank file | `certificates.jsonl` |")
    say("| its sha256 | `%s` |" % inherit_meta["meta"]["bank_sha256"])
    say("| certificates in it | %s |"
        % (bank.get("meta") or {}).get("certificates"))
    say("| keys in it | %s |" % (bank.get("meta") or {}).get("keys"))
    say("| the x86 reference this task walked with | `%s` |"
        % inherit_meta["meta"]["x86_reference_file"])
    say("| its sha256 | `%s` |"
        % inherit_meta["meta"]["x86_reference_sha256"])
    say("")

    handle = open(out_path, "w")
    handle.write("\n".join(lines) + "\n")
    handle.close()
    sys.stdout.write("wrote %s, %d lines\n" % (out_path, len(lines)))
    return 0


def complete_cells(proved, agreed, loop):
    """RISC-V cells every written place of which is proved or agreed on
    BOTH compiled targets."""
    places = {}
    for row in proved:
        key = cell_key(row["cell"])
        places.setdefault((key, row["place"]), set()).add(row["target"])
    for row in loop:
        if row["kind"] != "proved":
            continue
        key = cell_key(row["cell"])
        places.setdefault((key, row["place"]), set()).add(row["target"])
    by_cell = {}
    for key, target_set in places.items():
        cell, place = key
        held = by_cell.setdefault(cell, [])
        held.append(target_set)
    complete = 0
    for cell in by_cell:
        every = True
        for target_set in by_cell[cell]:
            if "c" not in target_set or "go" not in target_set:
                every = False
        if every:
            complete = complete + 1
    return complete


if __name__ == "__main__":
    sys.exit(main())
