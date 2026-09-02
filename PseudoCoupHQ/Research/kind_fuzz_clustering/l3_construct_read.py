#!/usr/bin/env python3
"""l3_construct_read.py -- the FOLD for the construct pass.

Reads the raw lane output, runs the COMPLETENESS GATE against each
lane's own frozen manifest, and writes the artifacts:

  construct_index.json      the gate, per language
  construct_answers_<l>.json  per construct: the domain accepted and
                            the answer or trace per cell
  truthiness_table.md       the if-condition slot, read across the
                            languages measured so far
  trace_compare.md          the first cross-language trace comparisons

Standing rule, and it is why the gate exists at all: exit 0 is not
evidence that a lane finished.
"""

import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
sys.path.insert(0, HERE)
from l3_accept import holders                        # noqa: E402

# language -> (raw file, grain).  'value' means the row carries a value
# class; 'holder' means the row is the acceptance grain and carries the
# holder's base value only.
LANES = {
    "python": ("kc_python.txt", "value"),
    "ruby":   ("kc_ruby.txt", "value"),
    "php":    ("kc_php_recovered.txt", "value"),
    "go":     ("kg_go.txt", "holder"),
    "typescript": ("kb_typescript.txt", "holder"),
    "csharp":     ("kb_csharp.txt", "holder"),
    "rust":       ("kb_rust.txt", "holder"),
    "cpp":        ("kb_cpp.txt", "holder"),
    "dart":       ("kb_dart.txt", "holder"),
    "java":       ("kb_java.txt", "holder"),
    "swift":      ("kb_swift.txt", "holder"),
    "kotlin":     ("kb_kotlin.txt", "holder"),
}
# log 038 raised the nine checked languages to the VALUE grain.  Where
# `raw/vb_<lang>.txt` exists it REPLACES the holder-grain file, because
# it measures the same constructs over every value class rather than
# over one value each.  The holder-grain file is left on disk exactly as
# log 037 wrote it, and `l3_value_fold.py` reads both to say what moved.
for _l in ("go", "typescript", "csharp", "rust", "cpp", "dart", "java",
           "swift", "kotlin"):
    if os.path.exists(os.path.join(RAW, "vb_%s.txt" % _l)):
        LANES[_l] = ("vb_%s.txt" % _l, "value")
# the eight lanes of log 037 come back in TWO files: kx_<lang>.txt, the
# acceptance verdict per probe, and ky_<lang>.txt, the answer or trace of
# every probe acceptance scored ACCEPT.  merge() folds them into one row
# per probe, which is the shape the gate and the signatures already read.
MERGED = ["typescript", "csharp", "rust", "cpp", "dart", "java",
          "swift", "kotlin"]

# a refusal whose message names the RECORDER is the harness refusing,
# not the language refusing the construct.  rust's `db()` trait is the
# case in hand: a holder whose type the encoder has no impl for cannot
# be recorded, so the probe never reaches a verdict about the construct.
# Counted apart and never read as a language finding.
# NARROWED 2026-08-19 by log 038.  The bare token "trait bound" was too
# wide: rust says "the trait bound `String: Borrow<[i64]>` is not
# satisfied" when IT refuses to index a string-keyed map with a slice of
# whole numbers, and `Borrow` is rust's own trait and not the recorder.
# Two of log 037's four rust harness refusals were that message, so they
# were findings about rust wrongly counted as the instrument refusing.
# A token now has to NAME the recorder: its trait `DB`, its method `db`,
# or one of its functions.
HARNESS_TOKENS = ("method `db", "no method named `db`", "_emit", "_dump",
                  "`DB` is not satisfied", "DB` is not satisfied",
                  "the trait `DB`")


def harness_refusal(msg):
    return any(t in msg for t in HARNESS_TOKENS)


def merge():
    """kx_<lang>.txt + ky_<lang>.txt -> kb_<lang>.txt, one row per probe."""
    for lang in MERGED:
        ax = os.path.join(RAW, "kx_%s.txt" % lang)
        ay = os.path.join(RAW, "ky_%s.txt" % lang)
        if not os.path.exists(ax):
            continue
        ans = {}
        if os.path.exists(ay):
            for line in open(ay, encoding="utf-8", errors="replace"):
                if line.startswith("__SUMMARY__"):
                    continue
                p = line.rstrip("\n").split("|", 2)
                if len(p) == 3:
                    ans[p[0]] = "%s|%s" % (p[1], p[2])
        out, nh = [], 0
        for line in open(ax, encoding="utf-8", errors="replace"):
            if line.startswith("__SUMMARY__"):
                continue
            p = line.rstrip("\n").split("|", 2)
            if len(p) != 3:
                continue
            pid, verdict, msg = p
            if pid in ans:
                out.append("%s|%s" % (pid, ans[pid]))
            elif verdict == "ACCEPT":
                out.append("%s|-|MISSING:accepted but no answer row" % pid)
            elif harness_refusal(msg):
                nh += 1
                out.append("%s|-|HARNESS_REFUSE:%s" % (pid, msg))
            else:
                out.append("%s|-|REFUSE:%s" % (pid, msg))
        open(os.path.join(RAW, "kb_%s.txt" % lang), "w").write(
            "\n".join(out) + "\n")
        if nh:
            print("  %-11s %d refusals named the recorder, not the "
                  "construct" % (lang, nh))
FORMS = ["nothing", "truth", "whole", "fractional", "text",
         "sequence", "keyed", "nesting"]
ALL12 = ["go", "rust", "cpp", "swift", "dart", "csharp", "kotlin",
         "java", "typescript", "python", "ruby", "php"]


def parse(path):
    rows, summaries = {}, []
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        if line.startswith("__SUMMARY__"):
            summaries.append(line)
            continue
        parts = line.split("|", 2)
        if len(parts) != 3:
            continue
        rows[parts[0]] = (parts[1], parts[2])
    return rows, summaries


def split_id(pid):
    """K<family>.<role>[<op>]_<positions...>"""
    m = re.match(r"^K([a-z]+\.[a-z]+)([^_]*)_(.*)$", pid)
    if not m:
        return None, None, []
    return m.group(1), m.group(2), m.group(3).split("_")


def gate():
    idx = {}
    for lang, (fn, grain) in LANES.items():
        p = os.path.join(RAW, fn)
        if not os.path.exists(p):
            idx[lang] = dict(present=False)
            continue
        rows, sums = parse(p)
        # The PLAN comes from the lane's own opening line, not from the
        # closing summary.  php restarts past a fatal, so only its LAST
        # run writes a summary and summing summaries would score a
        # complete lane as short.  Fault found and fixed 2026-08-19.
        planned = 0
        lg = os.path.join(RAW, fn.replace(".txt", ".lane.log"))
        if os.path.exists(lg):
            for line in open(lg, errors="replace"):
                m = re.search(r"CONSTRUCTS %s: .*?(\d+) (?:acceptance )?"
                              r"probes" % lang, line)
                if m:
                    planned = int(m.group(1))
                    break
        if not planned:
            for s in sums:
                planned += int(s.split("|")[1])
        kinds = collections.Counter()
        for ty, payload in rows.values():
            head = payload.split(":", 1)[0].split("[")[0]
            kinds[head if head in ("TRACE", "RAISE", "REFUSE", "BUDGET",
                                   "DEATH", "HARNESS_REFUSE", "MISSING",
                                   "CODEGEN_REFUSE")
                  else "ANSWER"] += 1
        idx[lang] = dict(
            present=True, grain=grain, rows=len(rows),
            summary_probes=planned,
            missing=max(0, planned - len(rows)),
            complete=(planned == len(rows)),
            answers=kinds["ANSWER"], traces=kinds["TRACE"],
            raises=kinds["RAISE"], refusals=kinds["REFUSE"],
            budget=kinds["BUDGET"], deaths=kinds["DEATH"],
            harness_refusals=kinds["HARNESS_REFUSE"],
            codegen_refusals=kinds["CODEGEN_REFUSE"],
            missing_rows=kinds["MISSING"],
            shards=len(sums))
    for lang in ALL12:
        idx.setdefault(lang, dict(present=False,
                                  note="lane not yet run"))
    json.dump(idx, open(os.path.join(HERE, "construct_index.json"), "w"),
              indent=1, sort_keys=True)
    return idx


def signatures():
    """per construct, the domain accepted and the answer or trace per
    cell -- the construct's counterpart to an operator signature."""
    out = {}
    for lang, (fn, grain) in LANES.items():
        p = os.path.join(RAW, fn)
        if not os.path.exists(p):
            continue
        hs, _ = holders(lang)
        rows, _ = parse(p)
        sig = collections.defaultdict(
            lambda: dict(domain=0, refused=0, raised=0, cells={}))
        for pid, (ty, payload) in rows.items():
            cons, op, pos = split_id(pid)
            if cons is None:
                continue
            key = cons + op
            s = sig[key]
            if payload.startswith("HARNESS_REFUSE"):
                s.setdefault("harness", 0)
                s["harness"] = s.get("harness", 0) + 1
            elif payload.startswith(("REFUSE", "CODEGEN_REFUSE",
                                     "MISSING")):
                s["refused"] += 1
            elif payload.startswith(("RAISE", "BUDGET", "DEATH")):
                s["raised"] += 1
            else:
                s["domain"] += 1
                s["cells"]["_".join(pos)] = [ty, payload]
        out[lang] = {k: dict(domain=v["domain"], refused=v["refused"],
                             harness_refused=v.get("harness", 0),
                             raised=v["raised"],
                             cells=v["cells"]) for k, v in sig.items()}
        json.dump(out[lang], open(os.path.join(
            HERE, "construct_answers_%s.json" % lang), "w"), indent=1)
    return out


def truthiness():
    """the if-condition slot, one operand, over every form."""
    tab = {}
    for lang, (fn, grain) in LANES.items():
        p = os.path.join(RAW, fn)
        if not os.path.exists(p):
            continue
        hs, _ = holders(lang)
        rows, _ = parse(p)
        per = collections.defaultdict(collections.Counter)
        for pid, (ty, payload) in rows.items():
            cons, op, pos = split_id(pid)
            if cons != "flow.if":
                continue
            i = int(pos[0])
            form = hs[i]["form"]
            if payload.startswith("HARNESS_REFUSE"):
                per[form]["HARNESS"] += 1
            elif payload.startswith(("REFUSE", "CODEGEN_REFUSE")):
                per[form]["REFUSE"] += 1
            elif payload.startswith(("RAISE", "DEATH")):
                per[form]["RAISE"] += 1
            elif "BR=then" in payload:
                per[form]["then"] += 1
            elif "BR=else" in payload:
                per[form]["else"] += 1
            else:
                per[form]["?"] += 1
        tab[lang] = {f: dict(per[f]) for f in FORMS if f in per}
    json.dump(tab, open(os.path.join(HERE, "truthiness.json"), "w"),
              indent=1, sort_keys=True)
    return tab


def word(counter):
    """a form's truthiness verdict, in words rather than a count."""
    if not counter:
        return "not probed"
    if counter.get("HARNESS") and len(counter) == 1:
        return "recorder refused"
    if counter.get("REFUSE"):
        if len(counter) == 1:
            return "refused"
        return "part refused"
    t, e = counter.get("then", 0), counter.get("else", 0)
    if t and not e:
        return "always then"
    if e and not t:
        return "always else"
    if t and e:
        return "splits %d then %d else" % (t, e)
    if counter.get("RAISE"):
        return "raised"
    return "?"


def write_truthiness_md(tab, idx):
    L = []
    L.append("# truthiness_table.md")
    L.append("")
    L.append("The if-condition slot, run over every holder and every")
    L.append("value class, in every language measured so far. This is")
    L.append("the one-operand table the owner asked for: eight forms, not a")
    L.append("64-cell grid.")
    L.append("")
    L.append("Read a cell like this. **always then** means every value")
    L.append("of that form drove the condition into the then arm.")
    L.append("**refused** means the compiler would not accept a value of")
    L.append("that form in a condition at all. **splits** means the form")
    L.append("divides, and the count says how.")
    L.append("")
    L.append("Generated by l3_construct_read.py from the raw lane output.")
    L.append("")
    for lang in ALL12:
        L.append("")
        L.append("## %s" % lang)
        if lang not in tab:
            n = idx.get(lang, {})
            L.append("")
            L.append("```")
            L.append("NOT YET MEASURED -- the construct lane for this")
            L.append("language has not run.  See HARVEST.md.")
            L.append("```")
            continue
        L.append("")
        if LANES[lang][1] == "holder":
            L.append("Grain: HOLDER. This language is statically")
            L.append("checked, so its verdict is a function of the")
            L.append("holder and not of the value; each holder was")
            L.append("probed at its base value only. A form that reads")
            L.append("**always then** here was accepted, not proved")
            L.append("uniform over its values.")
            L.append("")
        L.append("```")
        for f in FORMS:
            c = collections.Counter(tab[lang].get(f, {}))
            L.append("%-11s %s" % (f, word(c)))
        L.append("```")
    open(os.path.join(HERE, "truthiness_table.md"), "w").write(
        "\n".join(L) + "\n")


def write_trace_compare():
    """the two comparisons the report asks for by name."""
    L = []
    L.append("# trace_compare.md -- the first cross-language traces")
    L.append("")
    L.append("Two comparisons, both read straight off the raw lane")
    L.append("output, both in the answers_encoding.md encoding.")
    L.append("")
    L.append("## a for over the sequence 1, 2, 3")
    L.append("")
    L.append("The `base` value class of each language's canonical")
    L.append("sequence holder is the same three whole numbers.")
    L.append("")
    seq = {}
    for lang, (fn, grain) in LANES.items():
        p = os.path.join(RAW, fn)
        if not os.path.exists(p):
            continue
        hs, _ = holders(lang)
        i = next((n for n, h in enumerate(hs)
                  if h["form"] == "sequence"), None)
        rows, _ = parse(p)
        pid = ("Kflow.for_%d" % i if grain == "holder"
               else "Kflow.for_%d_base" % i)
        if pid in rows:
            seq[lang] = rows[pid][1]
    L.append("```")
    for lang in ALL12:
        if lang in seq:
            L.append("%s" % lang)
            for chunk in re.findall(r".{1,50}", seq[lang]):
                L.append("    " + chunk)
        else:
            L.append("%s" % lang)
            L.append("    NOT YET MEASURED")
    L.append("```")
    L.append("")
    L.append("## a break at k")
    L.append("")
    L.append("The loop is the fixed sequence 1 through 5 in every")
    L.append("language, so the only thing that varies is the language.")
    L.append("")
    for k in (2, 5):
        L.append("break at k = %d" % k)
        L.append("")
        L.append("```")
        for lang, (fn, grain) in sorted(LANES.items()):
            p = os.path.join(RAW, fn)
            if not os.path.exists(p):
                continue
            rows, _ = parse(p)
            r = rows.get("Kflow.break_%d" % k)
            # ABSENT is not MISSING.  kotlin's grammar declares no
            # break kind at all (catalogue, decision 2), so kotlin has
            # no row here BY DESIGN and a reader must not read the gap
            # as a lost probe.
            cat = json.load(open(os.path.join(HERE,
                                              "construct_catalogue.json")))
            absent = not cat[lang]["flow"]["break"]["present"]
            txt = (r[1] if r else
                   ("ABSENT -- the grammar declares no break kind"
                    if absent else "MISSING"))
            L.append("%s" % lang)
            for chunk in re.findall(r".{1,50}", txt):
                L.append("    " + chunk)
        L.append("```")
        L.append("")
    open(os.path.join(HERE, "trace_compare.md"), "w").write(
        "\n".join(L) + "\n")


def php_recover():
    """php's twenty fatals, re-run one process each by l3_php_recover.py.
    The recovered rows are folded BESIDE the original file, never over
    it: kc_php.txt is left exactly as the first run wrote it."""
    base = os.path.join(RAW, "kc_php.txt")
    extra = os.path.join(RAW, "kz_php.txt")
    dest = os.path.join(RAW, "kc_php_recovered.txt")
    if not os.path.exists(base):
        return
    rows = open(base, encoding="utf-8", errors="replace").read()
    n = 0
    add = []
    if os.path.exists(extra):
        for line in open(extra, encoding="utf-8", errors="replace"):
            if line.count("|") >= 2 and not line.startswith("__"):
                add.append(line.rstrip("\n"))
                n += 1
    open(dest, "w").write(rows.rstrip("\n") + "\n"
                          + ("\n".join(add) + "\n" if add else ""))
    lg = os.path.join(RAW, "kc_php.lane.log")
    if os.path.exists(lg):
        open(os.path.join(RAW, "kc_php_recovered.lane.log"), "w").write(
            open(lg, errors="replace").read())
    print("php recovery folded: %d rows recovered" % n)


def main():
    merge()
    php_recover()
    idx = gate()
    print("completeness gate")
    for lang in ALL12:
        d = idx[lang]
        if not d.get("present"):
            print("  %-11s NOT RUN" % lang)
            continue
        print("  %-11s %s  rows %d / planned %d  missing %d  "
              "(answers %d, traces %d, raises %d, refusals %d)"
              % (lang, "COMPLETE" if d["complete"] else "INCOMPLETE",
                 d["rows"], d["summary_probes"], d["missing"],
                 d["answers"], d["traces"], d["raises"], d["refusals"]))
    sig = signatures()
    print("")
    print("construct signatures written for %d languages" % len(sig))
    tab = truthiness()
    write_truthiness_md(tab, idx)
    write_trace_compare()
    print("wrote truthiness_table.md and trace_compare.md")


if __name__ == "__main__":
    main()
