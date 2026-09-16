"""retired 2026-09-15 (plan node the_run.retire_drifted_code, after the audit of log 281): the commands
that walked printed emulations (`corpus`, its CORPUS_FLAGS) and the handful of 2026-09-13 (`harness`,
`handful`, `pass_a`) built on the old-shape Language/System stubs. Kept for the record, never run."""

def cmd_harness(argv):
    cache_root, project, out = argv
    doc = {"steps": []}
    names, axioms, hyps, hyp_names, src = harness_setup(cache_root, project)
    say("  names listed for the unfold set: %d (defs and value-abbrevs of the emitted tree)" % len(names))
    earlier = []
    if os.path.exists(out):
        try:
            earlier = json.load(open(out)).get("names_pruned", [])
        except ValueError:
            earlier = []
    if earlier:
        names = [n for n in names if n not in earlier]
        say("  names an earlier build of this harness refused, dropped before building (LITERAL): %s" % earlier)
    say("  axioms of the support library of type ... -> SailM Unit (each theorem assumes it leaves the state as it is), LITERAL:")
    for ax in axioms:
        say("    %s:%s" % (ax["file"], ax["line"]))
    say("  the hypotheses text: %s" % hyps)
    doc["names_count"] = len(names)
    doc["axioms"] = axioms
    doc["hyps"] = hyps
    # 1. build Leanpath, pruning the attribute lines Lean refuses (each refusal LITERAL)
    pruned = []
    for attempt in range(4):
        write_harness(src, names, cache_root)
        rc, secs, text = sh(["lake", "build", "LeanpathAttr", "Leanpath"], cwd=project)
        errs = [l for l in text.splitlines() if "error" in l]
        say("  [build Leanpath, attempt %d] rc=%d wall=%.1fs error lines=%d" % (attempt + 1, rc, secs, len(errs)))
        doc["steps"].append({"step": "build Leanpath", "attempt": attempt + 1, "rc": rc, "seconds": secs, "errors": errs[:20]})
        if rc == 0:
            break
        lines = open(os.path.join(src, "Leanpath.lean")).read().splitlines()
        bad = set()
        for l in errs:
            m = re.search(r'Leanpath\.lean:(\d+):\d+:', l)
            if m:
                bad.add(int(m.group(1)))
        removed = []
        for ln in sorted(bad):
            line = lines[ln - 1] if ln - 1 < len(lines) else ""
            m = re.match(r'attribute \[leanpath_model\] (\S+)', line)
            if m and m.group(1) in names:
                names.remove(m.group(1))
                removed.append(m.group(1))
        pruned.extend(removed)
        doc["names_pruned"] = sorted(set(pruned) | set(earlier))
        say("    attribute lines Lean refused, dropped from the set (LITERAL names): %s" % removed)
        for l in errs[:6]:
            say("      %s" % l[:220])
        if not removed:
            say("  FLAG: the harness does not build and no attribute line is the cause; the first errors are above")
            doc["flag"] = "harness build failed: " + " | ".join(errs[:6])
            write_json(out, doc)
            return 1
    doc["names_pruned"] = sorted(set(pruned) | set(earlier))
    doc["names_used"] = len(names)
    say("  names used: %d; pruned: %d" % (len(names), len(pruned)))
    # 1b. the simp set's own names (Lean core's monad and map lemmas): every name checked, an unknown one dropped and printed
    work = os.path.join(project, "leanpath_work")
    os.makedirs(work, exist_ok=True)
    all_names = [n.strip() for n in LE.SIMP_SET.split(",") if n.strip()]
    attrs = ("leanpath_model", "leanpath_run", "leanpath_base", "simp_sail")
    probe_names = [n for n in all_names if n not in attrs]
    pfile = HEADER_NOBASE + "".join("#check @%s\n" % n for n in probe_names)
    ppath = os.path.join(work, "SimpSetProbe.lean")
    open(ppath, "w").write(pfile)
    rc, secs, lines = LeanExpr._run_lean(project, ppath, timeout_s=600)
    bad_lines = set()
    for l in lines:
        mm = re.search(r'SimpSetProbe\.lean:(\d+):\d+: error', l)
        if mm:
            bad_lines.add(int(mm.group(1)))
    nheader = HEADER_NOBASE.count("\n")
    unknown = [probe_names[ln - nheader - 1] for ln in sorted(bad_lines) if 0 <= ln - nheader - 1 < len(probe_names)]
    LE.SIMP_SET = ", ".join(n for n in all_names if n not in unknown)
    say("  [simp-set probe] rc=%d wall=%.1fs; names of Lean's own this toolchain lacks, dropped (LITERAL): %s" % (rc, secs, unknown))
    doc["simp_set_unknown"] = unknown
    doc["simp_set"] = LE.SIMP_SET
    # 2. the base state: the model's own init and reset, run in Lean on the empty state, printed
    probe = HEADER_NOBASE + "theorem base_probe %s : initState = initState := by\n" % hyps
    probe += "  conv => lhs; simp (config := {decide := true}) only [%s, initState, init, %s]\n" % (LE.simp_set(), ", ".join(hyp_names))
    probe += "  leanpath_show_lhs\n  rfl\n"
    ppath = os.path.join(work, "BaseProbe.lean")
    open(ppath, "w").write(probe)
    rc, secs, lines = LeanExpr._run_lean(project, ppath, timeout_s=3600)
    forms = LeanExpr._blocks(lines, "LHS")
    errs = LeanExpr._errors(lines)
    say("  [base probe] rc=%d wall=%.1fs printed forms=%d error lines=%d" % (rc, secs, len(forms), len(errs)))
    for l in errs[:6]:
        say("    %s" % l[:240])
    doc["steps"].append({"step": "base probe", "rc": rc, "seconds": secs, "errors": errs[:10], "printed_chars": len(forms[-1]) if forms else 0})
    state_text = forms[-1] if forms else ""
    residual = None
    for h in ("match ", "forIn", "EStateM.bind", "Leanpath.init", "sail_model_init", "reset "):
        if h in state_text:
            residual = h
    say("  the printed base state: %d chars; residual head: %s" % (len(state_text), residual))
    say("  the first 1500 chars (LITERAL):")
    for l in state_text[:1500].splitlines():
        say("    " + l)
    doc["base_state_chars"] = len(state_text)
    doc["base_state_head"] = state_text[:4000]
    doc["base_residual"] = residual
    open(os.path.join(work, "base_state.txt"), "w").write(state_text)
    # 3. LeanpathBase: S0 as the printed term (the round trip), checked against the run once
    base_src = "import Leanpath\nopen Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIM LeanIM.Functions\n"
    base_src += "set_option maxHeartbeats 1000000000\nset_option maxRecDepth 100000\nnoncomputable section\nnamespace Leanpath\n"
    mode = None
    if state_text and residual is None:
        base_src_a = base_src + "def S0 : St :=\n  %s\n" % state_text
        base_src_a += "theorem S0_eq %s : initState = S0 := by\n" % hyps
        base_src_a += "  simp (config := {decide := true}) only [%s, initState, init, %s, S0]\n" % (LE.simp_set(), ", ".join(hyp_names))
        base_src_a += "attribute [leanpath_base] S0\nend Leanpath\nend\n"
        open(os.path.join(src, "LeanpathBase.lean"), "w").write(base_src_a)
        rc, secs, text = sh(["lake", "build", "LeanpathBase"], cwd=project)
        errs = [l for l in text.splitlines() if "error" in l]
        say("  [build LeanpathBase, S0 as the printed term] rc=%d wall=%.1fs error lines=%d" % (rc, secs, len(errs)))
        for l in errs[:6]:
            say("    %s" % l[:240])
        doc["steps"].append({"step": "build LeanpathBase (printed S0)", "rc": rc, "seconds": secs, "errors": errs[:10]})
        if rc == 0:
            mode = "S0 is the printed state, checked equal to the model's own init and reset (S0_eq)"
    if mode is None:
        base_src_b = base_src + "def S0 : St := initState\nattribute [leanpath_base] S0 initState init\nend Leanpath\nend\n"
        open(os.path.join(src, "LeanpathBase.lean"), "w").write(base_src_b)
        rc, secs, text = sh(["lake", "build", "LeanpathBase"], cwd=project)
        errs = [l for l in text.splitlines() if "error" in l]
        say("  [build LeanpathBase, S0 := stateOf (init default), unfolded per theorem] rc=%d wall=%.1fs error lines=%d" % (rc, secs, len(errs)))
        doc["steps"].append({"step": "build LeanpathBase (S0 unfolded per theorem)", "rc": rc, "seconds": secs, "errors": errs[:10]})
        mode = "S0 := stateOf (init default), unfolded in every theorem (the printed state did not round-trip; FLAG)"
        doc["flag_base"] = "the printed base state did not round-trip; S0 is unfolded per theorem; residual head %s" % residual
    doc["base_mode"] = mode
    say("  base mode: %s" % mode)
    # 4. what the base holds, for a few registers (LITERAL), by the same machinery
    regs = SailModel.registers(os.path.join(cache_root, "LeanIM"))
    doc["register_count"] = len(regs)
    sample = [r for r in ("cur_privilege", "misa", "mstatus", "PC", "nextPC", "x10", "mseccfg", "menvcfg") if r in regs]
    peek = HEADER
    for r in sample:
        peek += "theorem peek_%s %s : S0.regs.get? Register.%s = S0.regs.get? Register.%s := by\n  conv => lhs; simp (config := {decide := true}) only [%s, S0, initState, init, %s]\n  leanpath_show_lhs\n  rfl\n" % (r, hyps, r, r, LE.simp_set(), ", ".join(hyp_names))
    kpath = os.path.join(work, "BasePeek.lean")
    open(kpath, "w").write(peek)
    rc, secs, lines = LeanExpr._run_lean(project, kpath, timeout_s=1800)
    forms = LeanExpr._blocks(lines, "LHS")
    say("  [base peek] rc=%d wall=%.1fs; the registers, LITERAL:" % (rc, secs))
    doc["base_peek"] = {}
    for r, f in zip(sample, forms):
        say("    %-14s %s" % (r, f[:200]))
        doc["base_peek"][r] = f[:400]
    for l in LeanExpr._errors(lines)[:4]:
        say("    %s" % l[:240])
    doc["peak_resident_kB"] = check_memory("harness")
    write_json(out, doc)
    say("  wrote %s; driver peak resident %d kB" % (out, doc["peak_resident_kB"]))
    return 0


# ---------------------------------------------------------------------- #
def load_hyps(cache_root, harness_json=None):
    tree = os.path.join(cache_root, "LeanIM")
    axioms = SailModel.axioms(tree)
    hyps, hyp_names = SailModel.axiom_hyps(axioms)
    LE.EXTRA_SIMP[:] = hyp_names
    if harness_json and os.path.exists(harness_json):
        d = json.load(open(harness_json))
        if d.get("simp_set"):
            LE.SIMP_SET = d["simp_set"]
    return hyps, hyp_names


def definition_forms(cache_root, project, workdir, hyps, only=None, limit=None):
    """strip on every definition instance (no-immediate keys first);
    {key -> form result}."""
    tree = os.path.join(cache_root, "LeanIM")
    inst = SailModel.instances(tree)
    out = {}
    n = 0
    for key in sorted(inst):
        if only and key not in only:
            continue
        d = inst[key]
        if d.get("refusal"):
            out[key] = {"refusal": "instance: " + d["refusal"], "term": d["term"]}
            continue
        if limit is not None and n >= limit:
            break
        n += 1
        name = "def_%s_%s" % (re.sub(r'[^A-Za-z0-9]', '_', key[0]), key[1])
        r = SailModel.strip(d, project, workdir, name, hyps)
        r["term"] = d["term"]
        r["unknowns"] = d["unknowns"]
        out[key] = r
        say("    strip %-22s %-8s %s" % ("%s/%s" % key, "%.1fs" % r.get("seconds", 0), (r.get("answer") or r.get("refusal") or "")[:150]))
    return out


def rv1_units():
    rv = "PseudoCoupHQ/Research/oracle/riscv"
    carved = json.load(open(os.path.join(rv, "carved.json")))["rows"]
    srcs = {r.get("unit"): r for r in json.load(open(os.path.join(rv, "units.json")))["rows"]}
    units = []
    for r in carved:
        if r.get("outcome") != "CARVED":
            continue
        u = ArchUnit(r["lang"], srcs.get(r["unit"], {}).get("source", ""), srcs.get(r["unit"], {}).get("symbol", ""), r["bytes"])
        units.append({"label": r["unit"], "language": r["lang"], "unit": u, "body": r["body"], "cell": "%s %s %d" % (r["mnem"], r["shape"], r["key_width"]), "source_expr": srcs.get(r["unit"], {}).get("expression", "")})
    return units


MULH_C = '''#include <stdint.h>
int64_t op_mulh(int64_t a, int64_t b)
{
    return (__int128)a * b >> 64;
}
'''




def cmd_handful(argv):
    cache_root, project, workdir, out = argv[:4]
    max_units = int(argv[4]) if len(argv) > 4 else 99
    os.makedirs(workdir, exist_ok=True)
    hyps, hyp_names = load_hyps(cache_root, os.path.join(os.path.dirname(out), "lp1_harness.json"))
    doc = {"units": [], "definitions": {}}
    say("[handful] the definition instances, strip through the model's own execute (no-immediate keys):")
    dforms = definition_forms(cache_root, project, workdir, hyps)
    doc["definitions"] = {"%s/%s" % k: {kk: vv for kk, vv in v.items() if kk != "expr"} for k, v in dforms.items()}
    units = rv1_units()[:max_units]
    # mulh on c, the headline: the plain source, and the corpus's rendered one
    cw = os.path.join(workdir, "mulh_c_plain")
    r = Language.compile("c", MULH_C, cw, symbol="op_mulh")
    if "unit" in r:
        units.append({"label": "c/mulh_plain", "language": "c", "unit": r["unit"], "body": r["body"], "cell": "mulh gpr_gpr_gpr 64", "source_expr": "(__int128)a * b >> 64", "compile": r["command"]})
    else:
        doc["mulh_plain_refusal"] = r
    gen = "PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/emulations_riscv64"
    p = os.path.join(gen, "mulh_gpr_gpr_gpr_64__reg_a0__c__native_first.c")
    if os.path.exists(p):
        r = Language.compile("c", open(p).read(), os.path.join(workdir, "mulh_c_rv6"))
        if "unit" in r:
            units.append({"label": "c/mulh_rv6_native_first", "language": "c", "unit": r["unit"], "body": r["body"], "cell": "mulh gpr_gpr_gpr 64", "source_expr": "rv6's rendered emulation (t4 render)", "compile": r["command"]})
        else:
            doc["mulh_rv6_refusal"] = r
    say("[handful] %d units; meaning on each (decode, compose in Lean):" % len(units))
    for i, u in enumerate(units):
        tag = "u%02d_%s" % (i, re.sub(r'[^A-Za-z0-9]', '_', u["label"]))
        dd = ArchUnit.decoded_display(u["unit"], project, workdir, tag + "_decode", hyps)
        m = ArchUnit.meaning(u["unit"], project, workdir, tag + "_meaning", hyps)
        u["meaning"] = m
        say("  [%d/%d] %-26s body: %s" % (i + 1, len(units), u["label"], " ; ".join(u["body"])))
        say("      decode %.1fs: %s" % (dd["seconds"], (dd["text"] or "|".join(dd["lean_errors"]))[:300]))
        say("      meaning %.1fs: %s" % (m["seconds"], (m.get("answer") or m.get("refusal") or "")[:300]))
        row = {"label": u["label"], "language": u["language"], "body": u["body"], "words": u["unit"].instructions, "cell": u["cell"], "source_expr": u["source_expr"],
               "decode": {"seconds": dd["seconds"], "text": dd["text"][:2000], "errors": dd["lean_errors"]},
               "meaning": {k: v for k, v in m.items() if k != "expr"}, "equals": []}
        if "expr" in m:
            for key in System.candidates(m["answer"], dforms):
                d = dforms[key]
                if "expr" not in d:
                    continue
                name = "%s_vs_%s_%s" % (tag, re.sub(r'[^A-Za-z0-9]', '_', key[0]), key[1])
                v = LeanExpr.equals(m["expr"], d["expr"], 30, project, workdir, name)
                v["key"] = "%s/%s" % key
                v["identical_text"] = (d["answer"] == m["answer"])
                row["equals"].append({k2: v2 for k2, v2 in v.items()})
                say("      equals vs %-22s %-10s %5.1fs %s" % (v["key"], v["outcome"], v.get("seconds", 0), (v.get("stage") or "")[:90]))
                if v["outcome"] == "Proof":
                    break
        doc["units"].append(row)
        check_memory("handful")
        write_json(out, doc)
    doc["peak_resident_kB"] = check_memory("handful end")
    write_json(out, doc)
    say("  wrote %s; driver peak resident %d kB" % (out, doc["peak_resident_kB"]))
    return 0




def cmd_pass_a(argv):
    cache_root, project, workdir, srcdir, out, lang, route, count, seconds = argv[:9]
    count, seconds = int(count), int(seconds)
    os.makedirs(workdir, exist_ok=True)
    hyps, hyp_names = load_hyps(cache_root, os.path.join(os.path.dirname(out), "lp1_harness.json"))
    t0 = time.time()
    doc = {"language": lang, "route": route, "count_asked": count, "seconds_bound": seconds, "units": [], "rows": []}
    say("[pass A] definition instances (no-immediate keys):")
    dforms = definition_forms(cache_root, project, workdir, hyps)
    doc["definitions"] = {"%s/%s" % k: {kk: vv for kk, vv in v.items() if kk != "expr"} for k, v in dforms.items()}
    ext = {"c": ".c", "cpp": ".cpp", "rust": ".rs", "go": ".go"}[lang]
    files = sorted(f for f in os.listdir(srcdir) if f.endswith("__%s__%s%s" % (lang, route, ext)))
    doc["population"] = len(files)
    files = files[:count]
    say("[pass A] %d sources of %d for %s/%s; compile (rv3's route), meaning, equals:" % (len(files), doc["population"], lang, route))
    units = []
    for i, f in enumerate(files):
        if time.time() - t0 > seconds:
            doc["rows"].append({"unit": f, "outcome": "not reached", "stage": "the lane's time bound"})
            continue
        label = f.rsplit(".", 1)[0]
        r = Language.compile(lang, open(os.path.join(srcdir, f)).read(), os.path.join(workdir, "cc_%04d" % i))
        if "unit" not in r:
            doc["rows"].append({"unit": label, "outcome": "Refused", "stage": "compile: " + r.get("refusal", ""), "diagnostic": r.get("diagnostic", "")[:300]})
            continue
        tag = "p%04d" % i
        m = ArchUnit.meaning(r["unit"], project, workdir, tag + "_meaning", hyps)
        u = {"label": label, "language": lang, "unit": r["unit"], "body": r["body"], "meaning": m}
        say("  [%d/%d] %-60s %2d words, meaning %.1fs: %s" % (i + 1, len(files), label, len(r["unit"].instructions), m["seconds"], (m.get("answer") or m.get("refusal") or "")[:120]))
        doc["units"].append({"label": label, "body": r["body"], "meaning": {k: v for k, v in m.items() if k != "expr"}})
        rows, found = System.pass_a_find([u], dforms, project, workdir, hyps, 30, tag, stop_at=None)
        for row in rows:
            if "key" in row:
                row["key"] = "%s/%s" % row["key"]
            say("      %-12s %-22s %s" % (row["outcome"], row.get("key", ""), (row.get("stage") or "")[:80]))
        doc["rows"].extend(rows)
        check_memory("pass_a")
        write_json(out, doc)
    doc["seconds"] = time.time() - t0
    doc["peak_resident_kB"] = check_memory("pass_a end")
    write_json(out, doc)
    say("  wrote %s; %.1fs; driver peak resident %d kB" % (out, doc["seconds"], doc["peak_resident_kB"]))
    return 0




def cmd_corpus(argv):
    """python3 -m leanpath corpus <srcdir> <out prefix> [shards] [langs csv] [routes csv]
    Every rendered source of the corpus as a walk unit, sharded round-robin;
    nothing is selected by a cell name."""
    srcdir, prefix = argv[:2]
    shards = int(argv[2]) if len(argv) > 2 else 1
    langs = argv[3].split(",") if len(argv) > 3 else ["c", "cpp", "rust", "go"]
    routes = argv[4].split(",") if len(argv) > 4 else ["native_first", "all_constructed"]
    units = []
    for f in sorted(os.listdir(srcdir)):
        m = re.match(r"^(.*)__(c|cpp|rust|go)__(native_first|all_constructed)\.(c|cpp|rs|go)$", f)
        if not m or m.group(2) not in langs or m.group(3) not in routes:
            continue
        stem = f.rsplit(".", 1)[0]
        units.append({"name": stem, "lang": m.group(2), "source": os.path.join(srcdir, f), "symbol": "emu_" + stem,
                      "flags": CORPUS_FLAGS[m.group(2)],
                      "cell_display": "%s (%s, %s)" % (m.group(1).split("__reg_")[0], m.group(2), m.group(3))})
    for k in range(shards):
        write_json("%s_%d.json" % (prefix, k), units[k::shards])
    say("  corpus: %d units over %d shard(s); languages %s; routes %s" % (len(units), shards, ",".join(langs), ",".join(routes)))
    return 0




CORPUS_FLAGS = {"c": "clang -std=c17 -O1 --target=riscv64-linux-gnu --gcc-toolchain=/usr",
                "cpp": "clang++ -std=c++17 -O1 --target=riscv64-linux-gnu --gcc-toolchain=/usr",
                "rust": "rustc --target riscv64gc-unknown-linux-gnu --crate-type lib --emit obj -C opt-level=1",
                "go": "GOARCH=riscv64 GOOS=linux go build"}




def harness_setup(cache_root, project):
    """the names (a listing), the axioms, the hypotheses text; the source
    dir and lakefile of the working copy prepared."""
    tree = os.path.join(cache_root, "LeanIM")
    names = SailModel.harness_names(cache_root)
    axioms = SailModel.axioms(tree)
    hyps, hyp_names = SailModel.axiom_hyps(axioms)
    LE.EXTRA_SIMP[:] = hyp_names
    src = os.path.join(project, "leanpath_src")
    os.makedirs(src, exist_ok=True)
    lf = os.path.join(project, "lakefile.toml")
    text = open(lf).read()
    if 'name = "Leanpath"' not in text:
        open(lf, "a").write(LAKE_LIB)
    open(os.path.join(src, "LeanpathAttr.lean"), "w").write(open(os.path.join(HERE, "lean", "LeanpathAttr.lean")).read())
    # the base module is rewritten by this command once the base state is
    # known; until then a stub, so a stale one from an earlier run never
    # enters the build (lane 13c stopped on exactly that)
    open(os.path.join(src, "LeanpathBase.lean"), "w").write("import Leanpath\n")
    return names, axioms, hyps, hyp_names, src


def write_harness(src, names, cache_root):
    tpl = open(os.path.join(HERE, "lean", "Leanpath.lean.in")).read()
    attrs = "\n".join("attribute [leanpath_model] %s" % n for n in names)
    # the 16-bit decoder's signature, as emitted (a listing of one line):
    # `... : SailM instruction :=` is monadic, `... : instruction :=` is pure
    sig = SailModel.signature_of(os.path.join(cache_root, "LeanIM"), "encdec_compressed_backwards")
    dec16 = "encdec_compressed_backwards h" if "SailM instruction" in (sig or "") else "pure (encdec_compressed_backwards h)"
    open(os.path.join(src, "Leanpath.lean"), "w").write(tpl.replace("@@MODEL_ATTRS@@", attrs).replace("@@DECODE16@@", dec16))


