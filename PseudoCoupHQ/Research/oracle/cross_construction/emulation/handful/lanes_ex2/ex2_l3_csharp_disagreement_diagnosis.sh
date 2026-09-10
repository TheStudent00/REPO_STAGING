#!/usr/bin/env bash
# ex2_l3_csharp_disagreement_diagnosis.sh -- task ex2: THE LOOP'S OWN
# RUN FOUND 11 DISAGREEMENTS, every one on csharp, scattered across
# unrelated cells (`cmp`, `push`, `ucomisd`, `punpckldq`, `andpd`,
# `andps`, `orpd`, `orps`, `punpcklqdq`, `pxor`, `pand`). Before any of
# that is reported as a language-level finding, this lane asks whether
# it is instead an artifact of the c# runner's own project-folder reuse
# and `dotnet build`'s incremental cache -- re-render and re-run ONE
# failing cell twice in a row, in isolation, and print the build's own
# output both times.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly

python3 - <<'PYEOF'
import sys, os, subprocess
sys.path.insert(0, "../handful")
sys.path.insert(0, "../interp")
import expand2 as X
X.use_task_ex2()
import interp_check as IC

cells = X.read_json(X.CELLS)
shared = IC.build_shared()

asked = ("cmp", "gpr_gpr", 64)

print("== first isolated run ==")
r1 = IC.one_run(shared, cells, asked, "csharp")
print("agreements", r1.get("agreements"), "disagreements",
      r1.get("disagreements"), "first_disagreement",
      r1.get("first_disagreement"))

print("")
print("== second isolated run, same cell, same folder ==")
r2 = IC.one_run(shared, cells, asked, "csharp")
print("agreements", r2.get("agreements"), "disagreements",
      r2.get("disagreements"), "first_disagreement",
      r2.get("first_disagreement"))

print("")
print("== the rendered source, LITERAL ==")
folder = IC.run_folder("csharp")
path = os.path.join(folder, "Program.cs")
print(open(path).read())

print("")
print("== the build, run BY HAND, verbose, over the CURRENT Program.cs ==")
env = dict(os.environ)
env["HOME"] = folder
env["DOTNET_CLI_TELEMETRY_OPTOUT"] = "1"
env["DOTNET_NOLOGO"] = "1"
done = subprocess.run(
    ["/persist/dotnet/dotnet", "build", "-c", "Release", "--nologo",
     "-v", "normal"],
    cwd=folder, capture_output=True, text=True, env=env, timeout=1800)
print("returncode", done.returncode)
print(done.stdout[-4000:])
print("STDERR", done.stderr[-2000:])

dll = os.path.join(folder, "bin", "Release", "net10.0", "emu.dll")
print("")
print("dll mtime:", os.path.getmtime(dll))
print("Program.cs mtime:", os.path.getmtime(path))

print("")
print("== running the dll directly on point [1] ==")
r = subprocess.run(["/persist/dotnet/dotnet", "exec", dll],
                    input="1\n", capture_output=True, text=True,
                    cwd=folder, env=env, timeout=60)
print("stdout:", repr(r.stdout))
print("stderr:", repr(r.stderr))
PYEOF
echo "done"
