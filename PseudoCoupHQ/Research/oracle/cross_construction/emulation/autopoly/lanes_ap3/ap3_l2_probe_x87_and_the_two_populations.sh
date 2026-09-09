#!/usr/bin/env bash
# ap3_l2_probe_x87_and_the_two_populations.sh -- task ap3: the PROBE the
# brief puts before fix 2, and what the two populations the driver
# fixes actually hold, asked of the objects rather than reasoned about.
#
#  [1] THE PROBE.  `long double` is c's 80-bit holder on x86-64.  The
#      brief's rule: probe it FIRST -- a `long double` add compiled at
#      the corpus's own ship flags, its carved body pasted -- and only
#      if clang emits the x87 opcode does the fix go in.
#  [2] THE 32 x87 CELLS, task ap2's 128 runs of `no setter row to
#      compose the flag pair from`: what their chosen row is, which of
#      their written places read the arriving flag state, what the
#      places' homes and widths are.  The question the fix turns on is
#      whether ANY place of these rows reads `seed_FLAG_L` /
#      `seed_FLAG_R`: a row that reads neither is not a flag consumer
#      and has nothing to compose.
#  [3] THE 40 RUNS OF `vector arrival used beyond its low lane`: which
#      cells, which places, which arrival symbol is read above bit 63,
#      and whether the read is a whole read or an Extract.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP3.  This lane
# reads `autopoly2_cells.json` (2 MB) and task ap2's store (5 MB) and
# runs no gate call; the peak is printed at the end.
set -euo pipefail
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 - <<'PY'
import os
import resource
import sys

HERE = "/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation"
sys.path.insert(0, os.path.join(HERE, "handful"))
sys.path.insert(0, os.path.join(HERE, "autopoly"))
sys.path.insert(0, HERE)
import z3
import emulate as E
import handful as H
import autopoly2 as A

ABORT_KB = 6 * 1024 * 1024


def peak():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def guard(where):
    got = peak()
    if got > ABORT_KB:
        raise SystemExit("ABORT_MEMORY_AP3: %d kB at %s" % (got, where))
    return got


print("[1/3] THE PROBE: does clang emit the x87 opcode for a "
      "`long double` add at the corpus's own ship flags?")
print("   the compiler: %s" % E.CLANG)
print("   the ship flags, LITERAL: %s" % " ".join(E.SHIP_FLAGS))
print("   the flags' source, LITERAL: %s" % E.SHIP_FLAGS_SOURCE)
SOURCES = [
    ("add", "long double emu_probe_ld_add(long double a, long double b)\n"
            "{\n    return a + b;\n}\n"),
    ("mul", "long double emu_probe_ld_mul(long double a, long double b)\n"
            "{\n    return a * b;\n}\n"),
    ("bits_in_and_out",
     "#include <stdint.h>\n"
     "#include <string.h>\n"
     "static inline long double bits_to_f80(unsigned __int128 b)\n"
     "{ long double f; memcpy(&f, &b, 10); return f; }\n"
     "static inline unsigned __int128 f80_to_bits(long double f)\n"
     "{ unsigned __int128 b = 0; memcpy(&b, &f, 10); return b; }\n"
     "unsigned __int128 emu_probe_ld_bits(unsigned __int128 a,\n"
     "                                    unsigned __int128 b)\n"
     "{\n    return f80_to_bits(bits_to_f80(a) + bits_to_f80(b));\n}\n"),
]
for name, source in SOURCES:
    symbol = "emu_probe_ld_%s" % ("bits" if name == "bits_in_and_out"
                                  else name)
    print("")
    print("   -- probe %r, the source LITERAL:" % name)
    for line in source.rstrip("\n").split("\n"):
        print("      %s" % line)
    got, refusal = E.compile_and_carve(source, symbol)
    if got is None:
        print("      COMPILE OR CARVE REFUSED: %s" % refusal)
        continue
    raw_bytes, mnem = got
    print("      the carved body, LITERAL: %s" % "; ".join(mnem))
    names = []
    for line in mnem:
        names.append(line.split()[0])
    x87 = []
    for one in names:
        if one.startswith("f"):
            x87.append(one)
    print("      instructions: %d; the mnemonics whose spelling begins "
          "with f: %s" % (len(mnem), sorted(set(x87)) or "none"))

print("")
print("   the holder tables the c renderer carries, LITERAL:")
print("      emulate.FLOAT    = %r" % (E.FLOAT,))
print("      emulate.UNSIGNED = %r" % (E.UNSIGNED,))
guard("after the probe")

print("")
print("[2/3] THE 32 x87 CELLS of task ap2's `no setter row to compose`")
A.use_task_ap2()
cells = A.read_json(A.CELLS)
wanted = {}
for run in A.read_runs(A.RUNS):
    cause = A.cause_of(run)
    if cause is None or "no setter row to compose" not in cause:
        continue
    wanted[(run["mnem"], run["shape"], run["key_width"])] = run
print("   task ap2's runs with that cause: %d"
      % sum(1 for r in A.read_runs(A.RUNS)
            if (A.cause_of(r) or "").startswith("no setter row")))
print("   distinct cells: %d" % len(wanted))
print("")
print("| cell | the chosen row | preseeded | flags_in | the places the "
      "row writes, with their homes and widths | any place reading the "
      "arriving flag state |")
print("|---|---|---|---|---|---|")
readers = 0
for key in sorted(wanted):
    held = {"mnem": key[0], "shape": key[1], "key_width": key[2]}
    row = H.chosen_row(cells, key, held)
    if row is None:
        print("| `%s` %s %s | -- no row -- | | | | |" % key)
        continue
    places, flags = H.terms_of_row(row)
    described = []
    reads = []
    if places is not None:
        for name in sorted(places):
            term = places[name]
            described.append("`%s` %s bits, home %s"
                             % (name, term.size(),
                                H.home_of(name)["family"]))
            for symbol in z3.z3util.get_vars(term):
                if symbol.decl().name().startswith("seed_FLAG"):
                    reads.append(name)
    if flags is not None:
        pair = z3.Concat(H.MT.as_bits(flags[1]), H.MT.as_bits(flags[2]))
        described.append("`flags` %d bits, arriving state: %s"
                         % (pair.size(), H.is_the_arriving_flag_state(pair)))
    if reads:
        readers = readers + 1
    print("| `%s` %s %s | %s | %s | %s | %s | %s |"
          % (key[0], key[1], key[2], row.get("row_id"),
             row.get("preseeded"), (row.get("flags_in") or {}).get("mnem"),
             "; ".join(described), sorted(set(reads)) or "none"))
print("")
print("   cells with at least one DESTINATION place reading the "
      "arriving flag state: %d of %d" % (readers, len(wanted)))
guard("after the x87 cells")

print("")
print("[3/3] THE 40 RUNS of `vector arrival used beyond its low lane`")
lane = []
for run in A.read_runs(A.RUNS):
    cause = A.cause_of(run)
    if cause is None or "beyond its low lane" not in cause:
        continue
    lane.append(run)
print("   runs: %d" % len(lane))
seen = {}
for run in lane:
    seen.setdefault((run["mnem"], run["shape"], run["key_width"]),
                    []).append(run["lang"])
print("   distinct cells: %d" % len(seen))
print("")
print("| cell | targets | the place | bits | the arrival read beyond "
      "bit 63 | how it is read |")
print("|---|---|---|---|---|---|")
for key in sorted(seen):
    held = {"mnem": key[0], "shape": key[1], "key_width": key[2]}
    row = H.chosen_row(cells, key, held)
    if row is None:
        print("| `%s` %s %s | %s | -- no row -- | | | |"
              % (key[0], key[1], key[2], ",".join(sorted(seen[key]))))
        continue
    places, flags = H.terms_of_row(row)
    records = H.in_halves_where_it_must_be(
        H.places_as_records(row, places, flags, []), key[2])
    for record in records:
        detail = record.get("not_rendered_detail")
        if record.get("not_rendered") is None and detail is None:
            holder = E.Renderer([], None, 0, "probe")
            holder.collect_uses(record["term"], None)
            wide = []
            for name in sorted(holder.uses):
                family = name[len("seed_"):]
                if family not in H.R.XMM_NAMES:
                    continue
                for use in holder.uses[name]:
                    if use is None:
                        wide.append("%s whole" % name)
                    elif use[0] > 63:
                        wide.append("%s Extract(%d, %d)"
                                    % (name, use[0], use[1]))
            if not wide:
                continue
            print("| `%s` %s %s | %s | `%s` | %s | %s | %s |"
                  % (key[0], key[1], key[2],
                     ",".join(sorted(seen[key])), record["writes"],
                     record["bits"], "; ".join(sorted(set(wide))),
                     "collect_uses"))
        else:
            print("| `%s` %s %s | %s | `%s` | %s | %s | %s |"
                  % (key[0], key[1], key[2],
                     ",".join(sorted(seen[key])), record["writes"],
                     record["bits"], record.get("not_rendered"),
                     detail))
print("")
print("peak resident: %d kB" % guard("end"))
PY
echo "done"
