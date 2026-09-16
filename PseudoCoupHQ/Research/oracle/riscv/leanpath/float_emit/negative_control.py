#!/usr/bin/env python3
"""negative_control.py -- a certificate that passes must be able to fail.

Inside lp3-runner, over the working copy /work/proof_float: one effects-rule
certificate as written, with `#print axioms` of its theorem (no `sorryAx` may
appear), and the same file with the two register reads handed to the pure form
in swapped order (a false statement for a subtraction: it must NOT prove).
Reads the certificate written by the strip check under /work/strip_float_check.
"""
import os
import signal
import subprocess
import sys

SRC = sys.argv[1] if len(sys.argv) > 1 else "/work/strip_float_check/Strip_F_BIN_RM_TYPE_D.lean"
W = "/work/strip_negative_control"
os.makedirs(W, exist_ok=True)
text = open(SRC).read()
theorem = [ln.split()[1] for ln in text.split("\n") if ln.startswith("theorem strip_")][0]
call = [ln.strip() for ln in text.split("\n") if ":= pure_" in ln][0]          # `let (out_0, out_1) := pure_X r1 r2 ...`
head, _, args = call.partition(":= ")
parts = args.split()
swapped = " ".join([parts[0], parts[2], parts[1]] + parts[3:])
neg = text.replace(args, swapped)
assert neg != text, "nothing to swap"
pos = text.replace("\nend Functions", "\n#print axioms %s\nend Functions" % theorem, 1)
open(os.path.join(W, "Pos.lean"), "w").write(pos)
open(os.path.join(W, "Neg.lean"), "w").write(neg)
env = dict(os.environ)
env["ELAN_HOME"] = "/persist/lp1/elan"
env["PATH"] = "/persist/lp1/elan/bin:/opt/elan/bin:" + env.get("PATH", "")
print("certificate:", SRC)
print("the swap:   ", args, " ->  ", swapped)
BOUND_S = 300          # a false certificate over defined float operations may unfold them; bounded
for f in ("Pos.lean", "Neg.lean"):
    # its own process group, so that stopping it at the bound stops `lake` AND its `lean`
    p = subprocess.Popen(["lake", "env", "lean", os.path.join(W, f)], cwd="/work/proof_float",
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env,
                         start_new_session=True)
    try:
        text_out, _ = p.communicate(timeout=BOUND_S)
        rc = p.returncode
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        text_out, _ = p.communicate()
        rc = None
    out = (text_out or "").strip().split("\n")
    if rc is None:
        print("== %s stopped at the %d s bound (lake and lean both stopped); not proved" % (f, BOUND_S))
    else:
        print("== %s rc=%d, error lines %d" % (f, rc, sum("error" in ln for ln in out)))
    for ln in out[:12]:
        print("   " + ln[:220])
