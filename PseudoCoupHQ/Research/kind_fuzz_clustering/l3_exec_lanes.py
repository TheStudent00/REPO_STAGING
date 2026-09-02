#!/usr/bin/env python3
"""l3_exec_lanes.py -- emit the EXECUTION lanes for the nine checked nine.

One lane per language (or per chunk range).  A lane carries its own
holder table, its own accepted-row list, its own runtime, and its own
driver, because the runner cannot see this repo.

Per chunk the lane does exactly one compile and then runs the binary.
The binary takes a START INDEX, so an uncatchable death (a c++ SIGFPE,
a swift trap) costs one probe: the driver records DEATH for it and
restarts the binary at the next index.
"""

import base64
import gzip
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.join(HERE, "lanes")
sys.path.insert(0, HERE)
from l3_exec import (accepted, table, CHUNK, CATCHABLE, RT,   # noqa: E402
                     ASSEMBLE, LANGS)

CAP = 3000.0          # the daemon kills at 3600 s; stop clean before it


# --------------------------------------------------------------- source gen
SRCGEN = r'''
def _hdr_split(lines, kw):
    """(header lines, body lines) -- java/kotlin/csharp/dart imports first."""
    h, b = [], []
    for l in lines:
        (h if l.startswith(kw) else b).append(l)
    return h, b


def _dedup(seq):
    out = []
    for s in seq:
        if s not in out:
            out.append(s)
    return out


def build(lang, rt, probes, start_index):
    """probes: [(pid, fn, pres, da, db, op)] -- the whole chunk, one file."""
    pres = _dedup([l for p in probes for l in p[2]])
    ids = [p[0] for p in probes]
    n = len(probes)

    def bodies(fmt):
        # every probe carries a MARKER line.  When a compiler refuses the
        # chunk -- swift's constant folder refuses an overflow that its
        # type checker accepted -- the driver maps the error's line back
        # to a probe through these markers, drops that probe alone, and
        # rebuilds.  It is the single-file discipline with a repair step,
        # not a bisect: the compiler names the line itself.
        return "\n".join("// __PROBE__ %s\n%s" % (p[0], fmt(p))
                         for p in probes) + "\n// __PROBE__ -\n"

    if lang == "go":
        pkgs = []
        rest = []
        for l in pres:
            q = _re.findall(r'"([^"]+)"', l)
            if l.startswith("import") or (q and l.strip().startswith('"')):
                pkgs += q
            elif l.strip() in ("import (", ")", "("):
                pass
            else:
                rest.append(l)
        base = ["bufio", "fmt", "math", "os", "reflect", "sort", "strconv",
                "strings"]
        allp = _dedup(base + pkgs)
        src = "package main\n\nimport (\n"
        for p in allp:
            src += '\t"%s"\n' % p
        src += ")\n\n" + "\n".join(rest) + "\n" + rt + "\n"
        src += bodies(lambda p:
            'func %s() {\n\tdefer _guard("%s")\n\t%s\n\t%s\n\t_r := (a) %s (b)\n\t_emit("%s", _r)\n}\n'
            % (p[1], p[0], p[3], p[4], p[5], p[0]))
        src += "\nvar _P = []func(){\n"
        for p in probes:
            src += "\t%s,\n" % p[1]
        src += "}\n\nfunc main() {\n\ts := 0\n"
        src += "\tif len(os.Args) > 1 {\n\t\ts, _ = strconv.Atoi(os.Args[1])\n\t}\n"
        src += "\tfor i := s; i < len(_P); i++ {\n\t\t_P[i]()\n\t}\n"
        src += '\tfmt.Fprintln(_W, "__END__")\n\t_W.Flush()\n}\n'
        return src, "chunk.go"

    if lang == "rust":
        # unconditional_panic and arithmetic_overflow are DENY-by-default
        # lints that fire only once const propagation runs, which is after
        # the metadata emission the acceptance run stopped at.  Allowing
        # them is what makes the accepted set compile; the panic itself
        # still happens at run time and is still caught and recorded.
        src = ("#![allow(unused, non_snake_case, non_camel_case_types, "
               "unused_parens, unused_mut, unused_variables, dead_code, "
               "unconditional_panic, arithmetic_overflow)]\n")
        src += "\n".join(pres) + "\n" + rt + "\n"
        src += bodies(lambda p:
            'fn %s() {\n    %s\n    %s\n    let _r = (a) %s (b);\n    _emit("%s", &_r);\n}\n'
            % (p[1], p[3], p[4], p[5], p[0]))
        src += "\nfn main() {\n    std::panic::set_hook(Box::new(|_| {}));\n"
        src += "    let ps: Vec<(&str, fn())> = vec![\n"
        for p in probes:
            src += '        ("%s", %s),\n' % (p[0], p[1])
        src += "    ];\n"
        src += "    let av: Vec<String> = std::env::args().collect();\n"
        src += ("    let s: usize = if av.len() > 1 "
                "{ av[1].parse().unwrap_or(0) } else { 0 };\n")
        src += "    for i in s..ps.len() {\n        let (id, f) = ps[i];\n"
        src += ("        if std::panic::catch_unwind(f).is_err() "
                '{ println!("{}|-|RAISE:panic", id); }\n    }\n')
        src += '    println!("__END__");\n}\n'
        return src, "chunk.rs"

    if lang == "cpp":
        src = rt + "\n" + "\n".join(pres) + "\n"
        src += bodies(lambda p:
            'static void %s() {\n    %s\n    %s\n    auto _r = (a) %s (b);\n    _emit("%s", _r);\n}\n'
            % (p[1], p[3], p[4], p[5], p[0]))
        src += "\ntypedef void (*_FN)();\nstatic _FN _P[] = {\n"
        for p in probes:
            src += "  %s,\n" % p[1]
        src += "};\nstatic const char* _I[] = {\n"
        for p in probes:
            src += '  "%s",\n' % p[0]
        src += "};\n\nint main(int argc, char** argv) {\n"
        src += "  size_t n = %d;\n" % n
        src += "  size_t s = argc > 1 ? (size_t)atol(argv[1]) : 0;\n"
        src += ("  for (size_t i = s; i < n; i++) {\n"
                "    try { _P[i](); } catch (...) { _raise(_I[i], \"cxx\"); }\n"
                "  }\n")
        src += '  printf("__END__\\n");\n  return 0;\n}\n'
        return src, "chunk.cpp"

    if lang == "swift":
        src = rt + "\n" + "\n".join(pres) + "\n"
        src += bodies(lambda p:
            'func %s() {\n    %s\n    %s\n    let _r = (a) %s (b)\n    _emit("%s", _r)\n}\n'
            % (p[1], p[3], p[4], p[5], p[0]))
        src += "\nlet _I: [String] = [\n"
        for p in probes:
            src += '  "%s",\n' % p[0]
        src += "]\nlet _P: [() -> Void] = [\n"
        for p in probes:
            src += "  %s,\n" % p[1]
        src += "]\nsetvbuf(stdout, nil, _IONBF, 0)\nvar _s = 0\n"
        src += ("if CommandLine.arguments.count > 1 "
                "{ _s = Int(CommandLine.arguments[1]) ?? 0 }\n")
        src += "var _i = _s\nwhile _i < _P.count {\n  _P[_i]()\n  _i += 1\n}\n"
        src += 'print("__END__")\n'
        return src, "main.swift"

    if lang == "dart":
        hdr, rest = _hdr_split(pres, "import ")
        src = "\n".join(hdr) + "\n" + rt + "\n" + "\n".join(rest) + "\n"
        src += bodies(lambda p:
            "void %s() {\n  try {\n    %s\n    %s\n    var _r = (a) %s (b);\n    _emit('%s', _r);\n  } catch (e) {\n    stdout.writeln('%s|-|RAISE:' + e.runtimeType.toString());\n  }\n}\n"
            % (p[1], p[3], p[4], p[5], p[0], p[0]))
        src += "\nfinal _P = <void Function()>[\n"
        for p in probes:
            src += "  %s,\n" % p[1]
        src += "];\n\nvoid main(List<String> args) {\n"
        src += "  var s = args.isNotEmpty ? int.parse(args[0]) : 0;\n"
        src += "  for (var i = s; i < _P.length; i++) { _P[i](); }\n"
        src += "  stdout.writeln('__END__');\n}\n"
        return src, "chunk.dart"

    if lang == "typescript":
        src = "\n".join(pres) + "\n" + rt + "\n"
        src += bodies(lambda p:
            'function %s(): void {\n  try {\n    %s\n    %s\n    let _r = (a) %s (b);\n    _emit("%s", _r);\n  } catch (e: any) {\n    process.stdout.write("%s|-|RAISE:" + ((e && e.constructor && e.constructor.name) || "error") + "\\n");\n  }\n}\n'
            % (p[1], p[3], p[4], p[5], p[0], p[0]))
        src += "\nconst _P: Array<() => void> = [\n"
        for p in probes:
            src += "  %s,\n" % p[1]
        src += "];\nconst _s: number = process.argv.length > 2 ? parseInt(process.argv[2]) : 0;\n"
        src += "for (let i = _s; i < _P.length; i++) { _P[i](); }\n"
        src += 'process.stdout.write("__END__\\n");\n'
        return src, "chunk.ts"

    if lang == "java":
        rt_h, rt_b = _hdr_split(rt.splitlines(), "import ")
        pr_h, pr_b = _hdr_split(pres, "import ")
        src = "\n".join(_dedup(pr_h + rt_h)) + "\n" + "\n".join(pr_b) + "\n"
        src += "\n".join(rt_b) + "\n\nclass Chunk {\n"
        src += bodies(lambda p:
            '  static void %s() {\n    try {\n      %s\n      %s\n      var _r = (a) %s (b);\n      RT.emit("%s", _r);\n    } catch (Throwable _t) {\n      RT.raise("%s", _t);\n    }\n  }\n'
            % (p[1], p[3], p[4], p[5], p[0], p[0]))
        for g in range(0, n, 100):
            src += "  static void d%d(int i) {\n    switch (i) {\n" % (g // 100)
            for i in range(g, min(g + 100, n)):
                src += "      case %d: %s(); break;\n" % (i, probes[i][1])
            src += "    }\n  }\n"
        src += "  static void run(int i) {\n    switch (i / 100) {\n"
        for g in range(0, n, 100):
            src += "      case %d: d%d(i); break;\n" % (g // 100, g // 100)
        src += "    }\n  }\n"
        src += ("  public static void main(String[] a) {\n    int s = "
                "a.length > 0 ? Integer.parseInt(a[0]) : 0;\n"
                "    for (int i = s; i < %d; i++) run(i);\n"
                '    System.out.println("__END__");\n  }\n}\n' % n)
        return src, "Chunk.java"

    if lang == "kotlin":
        rt_h, rt_b = _hdr_split(rt.splitlines(), "import ")
        pr_h, pr_b = _hdr_split(pres, "import ")
        src = "\n".join(_dedup(pr_h + rt_h)) + "\n" + "\n".join(pr_b) + "\n"
        src += "\n".join(rt_b) + "\n\n"
        src += bodies(lambda p:
            'fun %s() {\n  try {\n    %s\n    %s\n    val _r = (a) %s (b)\n    RT.emit("%s", _r)\n  } catch (_t: Throwable) {\n    RT.raise("%s", _t)\n  }\n}\n'
            % (p[1], p[3], p[4], p[5], p[0], p[0]))
        for g in range(0, n, 100):
            src += "fun d%d(i: Int) {\n  when (i) {\n" % (g // 100)
            for i in range(g, min(g + 100, n)):
                src += "    %d -> %s()\n" % (i, probes[i][1])
            src += "  }\n}\n"
        src += "fun run(i: Int) {\n  when (i / 100) {\n"
        for g in range(0, n, 100):
            src += "    %d -> d%d(i)\n" % (g // 100, g // 100)
        src += "  }\n}\n"
        src += ("fun main(args: Array<String>) {\n  val s = if "
                "(args.isNotEmpty()) args[0].toInt() else 0\n"
                "  for (i in s until %d) run(i)\n"
                '  println("__END__")\n}\n' % n)
        return src, "Chunk.kt"

    if lang == "csharp":
        rt_h, rt_b = _hdr_split(rt.splitlines(), "using ")
        pr_h, pr_b = _hdr_split(pres, "using ")
        src = "\n".join(_dedup(pr_h + rt_h)) + "\n" + "\n".join(pr_b) + "\n"
        src += "\n".join(rt_b) + "\n\nclass Chunk {\n"
        src += bodies(lambda p:
            '  static void %s() {\n    try {\n      %s\n      %s\n      var _r = (a) %s (b);\n      RT.Emit("%s", _r);\n    } catch (System.Exception _e) {\n      RT.Raise("%s", _e.GetType().FullName);\n    }\n  }\n'
            % (p[1], p[3], p[4], p[5], p[0], p[0]))
        for g in range(0, n, 100):
            src += "  static void d%d(int i) {\n    switch (i) {\n" % (g // 100)
            for i in range(g, min(g + 100, n)):
                src += "      case %d: %s(); break;\n" % (i, probes[i][1])
            src += "    }\n  }\n"
        src += "  static void Run(int i) {\n    switch (i / 100) {\n"
        for g in range(0, n, 100):
            src += "      case %d: d%d(i); break;\n" % (g // 100, g // 100)
        src += "    }\n  }\n"
        src += ("  static void Main(string[] a) {\n    int s = a.Length > 0 "
                "? int.Parse(a[0]) : 0;\n"
                "    for (int i = s; i < %d; i++) Run(i);\n"
                '    System.Console.Out.Write("__END__\\n");\n'
                "    System.Console.Out.Flush();\n  }\n}\n" % n)
        return src, "Chunk.cs"

    raise SystemExit("no builder for " + lang)
'''

# ------------------------------------------------------------------ driver

DRIVER = r'''
import glob
import json
import os
import re as _re
import shutil
import subprocess
import sys
import threading
import time

ROOT = sys.argv[1]
LANG = "{LANG}"
CAP = {CAP}
OUT = "/out/{NAME}.txt"

T = json.load(open(os.path.join(ROOT, "table.json")))
ROWS = json.load(open(os.path.join(ROOT, "rows.json")))
RTX = open(os.path.join(ROOT, "rt.txt")).read()
CH = {CHUNK}
STALL = 90.0
LO = {LO}
HI = {HI}

{ASSEMBLE}
{SRCGEN}

def hms(x):
    if x is None or x < 0:
        return "--:--:--"
    x = int(x)
    return "%02d:%02d:%02d" % (x // 3600, (x % 3600) // 60, x % 60)


def free_mb(p="/work"):
    st = os.statvfs(p)
    return st.f_bavail * st.f_frsize // (1024 * 1024)


FREE0 = free_mb()
print("free /work before start: %d MB" % FREE0)
if FREE0 < 400:
    print("!! REFUSING TO START: %d MB free, need 400" % FREE0)
    sys.exit(3)

chunks = [ROWS[i:i + CH] for i in range(0, len(ROWS), CH)]
chunks = chunks[LO:HI]
total = sum(len(c) for c in chunks)
print("== exec lane %s: %d chunks %d..%d, %d probes, cap %.0f s"
      % (LANG, len(chunks), LO, HI, total, CAP))
sys.stdout.flush()

out = open(OUT, "w")
t0 = time.time()
done = 0
answers = raises = deaths = cgrefuse = 0
stopped_at = None

DOT = "/persist/dotnet"


def build_cmds(lang, d, fname):
    """(compile argv list, run argv factory)."""
    if lang == "go":
        return ([["go", "build", "-o", d + "/bin", d + "/" + fname]],
                lambda s: [d + "/bin", str(s)])
    if lang == "rust":
        return ([["rustc", "-C", "debug-assertions=on", "-C", "opt-level=0",
                  "-o", d + "/bin", d + "/" + fname]],
                lambda s: [d + "/bin", str(s)])
    if lang == "cpp":
        return ([["g++", "-std=c++20", "-O0", "-w", "-o", d + "/bin",
                  d + "/" + fname]],
                lambda s: [d + "/bin", str(s)])
    if lang == "swift":
        return ([["/persist/swift/usr/bin/swiftc", "-Onone", "-suppress-warnings",
                  "-o", d + "/bin", d + "/" + fname]],
                lambda s: [d + "/bin", str(s)])
    if lang == "dart":
        return ([["/persist/dart-sdk/bin/dart", "compile", "exe",
                  d + "/" + fname, "-o", d + "/bin"]],
                lambda s: [d + "/bin", str(s)])
    if lang == "java":
        return ([["javac", "-nowarn", "-d", d + "/cls", d + "/" + fname]],
                lambda s: ["java", "-cp", d + "/cls", "Chunk", str(s)])
    if lang == "kotlin":
        std = "/persist/kotlinc/lib/kotlin-stdlib.jar"
        return ([["/persist/kotlinc/bin/kotlinc", "-nowarn", "-d", d + "/cls",
                  d + "/" + fname]],
                lambda s: ["java", "-cp", d + "/cls:" + std, "ChunkKt", str(s)])
    if lang == "csharp":
        refd = sorted(glob.glob(DOT + "/packs/Microsoft.NETCore.App.Ref/*/ref/net*"))[-1]
        csc = sorted(glob.glob(DOT + "/sdk/*/Roslyn/bincore/csc.dll"))[-1]
        ver = refd.split("/")[-3]
        tfm = refd.split("/")[-1]
        open(d + "/Chunk.runtimeconfig.json", "w").write(
            '{"runtimeOptions":{"tfm":"%s","framework":{"name":'
            '"Microsoft.NETCore.App","version":"%s"}}}' % (tfm, ver))
        refs = ["-reference:" + os.path.join(refd, f)
                for f in os.listdir(refd) if f.endswith(".dll")]
        return ([[DOT + "/dotnet", "exec", csc, "-nologo", "-nowarn:CS0168",
                  "-out:" + d + "/Chunk.dll", "-target:exe"] + refs
                 + [d + "/" + fname]],
                lambda s: [DOT + "/dotnet", d + "/Chunk.dll", str(s)])
    if lang == "typescript":
        tsc = ("/persist/tv/ts5/node_modules/typescript/lib/typescript.js")
        open(d + "/tr.js", "w").write(
            "const ts=require(%r);const fs=require('fs');"
            "const src=fs.readFileSync(process.argv[2],'utf8');"
            "const o=ts.transpileModule(src,{compilerOptions:"
            "{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.CommonJS}});"
            "fs.writeFileSync(process.argv[3],o.outputText);" % tsc)
        return ([["node", d + "/tr.js", d + "/" + fname, d + "/chunk.js"]],
                lambda s: ["node", "--stack-size=4000", d + "/chunk.js", str(s)])
    raise SystemExit("no toolchain for " + lang)


for ci, rows in enumerate(chunks):
    if time.time() - t0 > CAP:
        stopped_at = LO + ci
        print("!! TIME CAP reached before chunk %d" % (LO + ci))
        break
    d = os.path.join(ROOT, "c%03d" % (LO + ci))
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    allp = assemble(T, rows)
    ids = [p[0] for p in allp]
    probes = list(allp)
    refused = {}
    ok = False
    tb = time.time()
    for attempt in range(16):
        if not probes:
            break
        src, fname = build(LANG, RTX, probes, 0)
        open(os.path.join(d, fname), "w").write(src)
        spans = probe_spans(src)
        cmds, runf = build_cmds(LANG, d, fname)
        ok = True
        msg = ""
        for c in cmds:
            r = subprocess.run(c, capture_output=True, text=True, cwd=d,
                               timeout=1800)
            if r.returncode != 0:
                ok = False
                msg = (r.stderr or "") + "\n" + (r.stdout or "")
                break
        if ok:
            break
        bad = map_errors(msg, spans)
        print("!! chunk %d compile attempt %d failed; %d probes named"
              % (LO + ci, attempt, len(bad)))
        sys.stdout.flush()
        if not bad:
            print(msg[:3000])
            open("/out/{NAME}.compilefail.%d.txt" % (LO + ci), "w").write(
                msg[:200000])
            break
        for pid in bad:
            refused[pid] = bad[pid]
        keep = set(bad)
        probes = [p for p in probes if p[0] not in keep]
    tbuild = time.time() - tb
    if not ok:
        for pid in ids:
            out.write("%s|-|BUILDFAIL\n" % pid)
        out.flush()
        done += len(ids)
        shutil.rmtree(d, ignore_errors=True)
        continue
    ids = [p[0] for p in probes]
    got = {}
    pos = dict((p, k) for k, p in enumerate(ids))
    start = 0
    restarts = 0
    while start < len(ids) and restarts < 400:
        pr = subprocess.Popen(runf(start), stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, text=True, cwd=d,
                              bufsize=1)
        last = start - 1
        ended = False
        # WATCHDOG.  A probe can hang rather than die -- kotlin's `..`
        # returns a LongRange and a LongRange walked as an iterable does
        # not come back.  Silence for STALL seconds is treated as a
        # death of the probe that was next, and the runner resumes past
        # it, so one hang costs one probe and not a lane.
        beat = [time.time()]
        stop = [False]

        def _watch():
            while not stop[0]:
                time.sleep(2.0)
                if time.time() - beat[0] > STALL:
                    try:
                        pr.kill()
                    except Exception:
                        pass
                    return

        th = threading.Thread(target=_watch)
        th.daemon = True
        th.start()
        for line in pr.stdout:
            beat[0] = time.time()
            line = line.rstrip("\n")
            if line == "__END__":
                ended = True
                continue
            if "|" not in line:
                continue
            pid = line.split("|", 1)[0]
            k = pos.get(pid)
            if k is None:
                continue
            got[pid] = line
            if k > last:
                last = k
        pr.wait()
        stop[0] = True
        if ended or last >= len(ids) - 1:
            break
        nxt = last + 1
        got[ids[nxt]] = "%s|-|DEATH:rc%s" % (ids[nxt], pr.returncode)
        start = nxt + 1
        restarts += 1
    for pid in allids(allp):
        if pid in refused:
            line = "%s|-|CODEGEN_REFUSE:%s" % (pid, refused[pid])
        else:
            line = got.get(pid, "%s|-|MISSING" % pid)
        out.write(line + "\n")
        if "|-|RAISE:" in line:
            raises += 1
        elif "|-|DEATH:" in line:
            deaths += 1
        elif "|-|CODEGEN_REFUSE:" in line:
            cgrefuse += 1
        elif "|-|MISSING" in line:
            pass
        else:
            answers += 1
    out.flush()
    done += len(allp)
    shutil.rmtree(d, ignore_errors=True)
    el = time.time() - t0
    eta = (el / done) * (total - done) if done else None
    print("[progress] %s chunk %d/%d [%d/%d] %5.1f%% build %.1fs "
          "elapsed %s ETA %s restarts %d free %d MB"
          % (LANG, LO + ci + 1, LO + len(chunks), done, total,
             100.0 * done / total, tbuild, hms(el), hms(eta), restarts,
             free_mb()))
    sys.stdout.flush()

el = time.time() - t0
out.write("__SUMMARY__|%s|%d|%d|%d|%d|%d|%.3f|%s\n"
          % (LANG, done, answers, raises, deaths, cgrefuse, el,
             "PARTIAL:%d" % stopped_at if stopped_at is not None else "ALL"))
out.close()
print("== %s: %d probes, %d answers, %d raises, %d deaths, %d codegen-refuse,"
      " %.1f s" % (LANG, done, answers, raises, deaths, cgrefuse, el))
'''

IDSET = r'''

def allids(probes):
    return [p[0] for p in probes]


_MARK = _re.compile(r"^// __PROBE__ (\S+)\s*$")
_ERL = _re.compile(r"(?:chunk|Chunk|main)\.[A-Za-z]+:(\d+)[:.]")
_ERC = _re.compile(r"(?:chunk|Chunk|main)\.[A-Za-z]+\((\d+),\d+\)")


def probe_spans(src):
    """[(first_line, last_line, pid)] over the built chunk, 1-based."""
    marks = []
    for n, line in enumerate(src.splitlines(), 1):
        m = _MARK.match(line)
        if m:
            marks.append((n, m.group(1)))
    out = []
    for k, (n, pid) in enumerate(marks):
        end = marks[k + 1][0] - 1 if k + 1 < len(marks) else 10 ** 9
        out.append((n, end, pid))
    return out


def map_errors(msg, spans):
    """which probes did the compiler NAME?  {pid: short reason}"""
    hit = {}
    for ml in msg.splitlines():
        ms = _ERL.search(ml) or _ERC.search(ml)
        if not ms:
            continue
        ln = int(ms.group(1))
        reason = ml.strip().replace("|", "/")[:120]
        for a, b, pid in spans:
            if a <= ln <= b:
                if pid != "-":
                    hit.setdefault(pid, reason)
                break
    return hit
'''

PRELUDE = r'''#!/bin/sh
# layer-3 EXECUTION lane -- {LANG} -- generated by l3_exec_lanes.py.
# Do not hand-edit.  Accepted probes only; one compile per chunk.
set -u
export HOME=/work
export GO111MODULE=off
export GOFLAGS=-mod=mod
export GOCACHE=/work/.gocache
export GOPATH=/work/.gopath
export PATH=/persist/dart-sdk/bin:/persist/dotnet:$PATH
export DOTNET_CLI_TELEMETRY_OPTOUT=1
export DOTNET_NOLOGO=1
if [ -f /usr/lib/x86_64-linux-gnu/libncursesw.so.6.6 ]; then
  ln -sf /usr/lib/x86_64-linux-gnu/libncursesw.so.6.6 \
     /usr/lib/x86_64-linux-gnu/libncurses.so.6 2>/dev/null
  ldconfig 2>/dev/null
fi
ROOT=/work/{NAME}
rm -rf "$ROOT"; mkdir -p "$ROOT"
echo "=== layer-3 EXECUTION -- {LANG} -- chunks {LO}..{HI} ==="
date -u +%Y-%m-%dT%H:%M:%SZ
df -Pm /work | awk 'NR==2{{print "free /work: " $4 " MB"}}'
base64 -d <<'T_EOF' | gunzip > "$ROOT/table.json"
{TB}
T_EOF
base64 -d <<'R_EOF' | gunzip > "$ROOT/rows.json"
{RB}
R_EOF
base64 -d <<'X_EOF' | gunzip > "$ROOT/rt.txt"
{XB}
X_EOF
python3 - "$ROOT" <<'PY_EOF'
'''

TAIL = r'''
PY_EOF
rm -rf "$ROOT"
echo "swept $ROOT; /work free: $(df -Pm /work | awk 'NR==2{print $4}') MB"
date -u +%Y-%m-%dT%H:%M:%SZ
echo "=== exec lane done ==="
'''


def b64(raw):
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as g:
        g.write(raw)
    b = base64.b64encode(buf.getvalue()).decode()
    return "\n".join(b[i:i + 76] for i in range(0, len(b), 76))


def emit(lang, lo, hi, name=None, cap=CAP, rows=None):
    rows = accepted(lang) if rows is None else rows
    tb = table(lang)
    nch = (len(rows) + CHUNK[lang] - 1) // CHUNK[lang]
    hi = min(hi, nch)
    name = name or "ex_%s_%02d" % (lang, lo)
    drv = (DRIVER.replace("{ASSEMBLE}", ASSEMBLE)
                 .replace("{SRCGEN}", SRCGEN + IDSET)
                 .replace("{LANG}", lang).replace("{NAME}", name)
                 .replace("{CHUNK}", str(CHUNK[lang]))
                 .replace("{LO}", str(lo)).replace("{HI}", str(hi))
                 .replace("{CAP}", "%.1f" % cap))
    head = (PRELUDE.replace("{{", "\x00").replace("}}", "\x01")
                   .replace("{LANG}", lang).replace("{NAME}", name)
                   .replace("{LO}", str(lo)).replace("{HI}", str(hi))
                   .replace("{TB}", b64(json.dumps(tb).encode()))
                   .replace("{RB}", b64(json.dumps(rows).encode()))
                   .replace("{XB}", b64(RT[lang].encode()))
                   .replace("\x00", "{").replace("\x01", "}"))
    p = os.path.join(LANES, name + ".sh")
    open(p, "w").write(head + drv + TAIL)
    print("wrote %s  (%d rows, chunks %d..%d of %d)"
          % (p, len(rows), lo, hi, nch))
    return p


def main():
    args = sys.argv[1:]
    if args and args[0] == "smoke":
        # a SMOKE lane per language: the first N accepted probes only,
        # one chunk, to prove the file compiles before the full run.
        n = int(args[1]) if len(args) > 1 else 120
        for lang in (args[2:] or LANGS):
            rows = accepted(lang)[:n]
            CHUNK[lang] = n
            emit(lang, 0, 1, name="xs_%s" % lang, cap=1200.0, rows=rows)
        return
    for lang in (args or LANGS):
        rows = accepted(lang)
        nch = (len(rows) + CHUNK[lang] - 1) // CHUNK[lang]
        emit(lang, 0, nch)


if __name__ == "__main__":
    main()
