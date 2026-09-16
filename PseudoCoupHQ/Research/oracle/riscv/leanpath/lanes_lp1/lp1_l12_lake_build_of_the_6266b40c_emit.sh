#!/usr/bin/env bash
# lp1 lane 12 -- THIRD launch, brief §5 lane 12: `lake build` of the emit
# lane 11 cached (model 6266b40c1c, sail 8eb1fb6b5b), as lanes 1d and 8
# did: a working copy of the cache under /persist (the cache itself is never
# written), the toolchain the cache pins taken from /persist/lp1/elan if it
# is already there (the 4.29.0 from the github route, first launch) and
# FETCHED from github.com (the .zip release asset, python unpacks it: the
# image has no zstd) only if absent, said so; the lean-sail rev it pins
# copied in from the earlier working copies if one of them holds that rev
# (v4 in Lean_IM, v5 in Lean_IM_5745ea9e) and FETCHED with `lake update`
# from github.com only if neither does, said so. Sample first (`lake build
# Sail`, then `LeanIM.Defs`, the module the two earlier emits failed at),
# then the whole library. Bounded by the instance (20g); the lake jobs are
# capped at 4 (8 parallel elaborations of a 63k-line model could pass 20g);
# wall time, the largest descendant's peak resident and the cgroup peak are
# printed; the count of modules built "of N". A build error is a FLAG: the
# first twelve error lines LITERAL, and the task stops at it. A build that
# passes is the first measured fact of this path.
set -u
export HOME=/work
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/venv/bin:$PATH
P=PseudoCoupHQ
LP=$P/Research/oracle/riscv/leanpath
CACHE=$LP/cache/sail-riscv_6266b40c_sail_8eb1fb6b_I_insts_M_insts_postlude_main
PROJ=/persist/lp1/Lean_IM_6266b40c
OLD4=/persist/lp1/Lean_IM
OLD5=/persist/lp1/Lean_IM_5745ea9e
total=10
i=1
step() { echo "[$i/$total] $1"; i=$((i+1)); echo "  at $(date -u +%FT%TZ)"; }
peak() { echo "  cgroup memory.peak: $(cat /sys/fs/cgroup/memory.peak 2>/dev/null || echo unreadable) bytes; memory.current: $(cat /sys/fs/cgroup/memory.current 2>/dev/null || echo unreadable)"; }
timed() {
python3 - "$@" <<'PY'
import resource, subprocess, sys, time
cmd = sys.argv[1:]
t0 = time.time()
p = subprocess.run(cmd)
t1 = time.time()
ru = resource.getrusage(resource.RUSAGE_CHILDREN)
print("  rc=%d wall=%.1fs largest-descendant peak resident=%d kB" % (p.returncode, t1 - t0, ru.ru_maxrss))
sys.exit(p.returncode)
PY
}

step "the new cache and what it pins (LITERAL); the earlier working copies' pins beside it"
ls "$CACHE" | tr '\n' ' '; echo
echo "  lakefile.toml:"; sed 's/^/    /' "$CACHE/lakefile.toml"
TC="$(cat $CACHE/lean-toolchain)"; VER="${TC#leanprover/lean4:}"
echo "  lean-toolchain: $TC (version $VER)"
NEWREV="$(grep -E '^rev' "$CACHE/lakefile.toml" | head -1 | sed 's/.*= *"//; s/".*//')"
REV4="$(grep -E '^rev' "$OLD4/lakefile.toml" 2>/dev/null | head -1 | sed 's/.*= *"//; s/".*//')"
REV5="$(grep -E '^rev' "$OLD5/lakefile.toml" 2>/dev/null | head -1 | sed 's/.*= *"//; s/".*//')"
echo "  lean-sail rev pinned: new='$NEWREV'; Lean_IM holds '$REV4' ($(git -C $OLD4/.lake/packages/Sail rev-parse --short HEAD 2>&1)); Lean_IM_5745ea9e holds '$REV5' ($(git -C $OLD5/.lake/packages/Sail rev-parse --short HEAD 2>&1))"
echo "  toolchains under /persist/lp1/elan: $(ls $ELAN_HOME/toolchains 2>&1 | tr '\n' ' ')"

step "the toolchain the cache pins: from /persist if present, else fetched from github.com (the .zip release asset), said so"
DEST="$ELAN_HOME/toolchains/leanprover--lean4---$VER"
if [ -x "$DEST/bin/lean" ]; then
  echo "  PRESENT: $DEST (nothing fetched for the toolchain)"
else
  echo "  ABSENT: $DEST; this lane FETCHES the release asset from github.com (authorised by brief §5 for this lane, said so here); http_proxy=${http_proxy:-unset}"
  NUM="${VER#v}"
  URL="https://github.com/leanprover/lean4/releases/download/$VER/lean-$NUM-linux.zip"
  ARCH="/persist/lp1/dl/lean-$NUM-linux.zip"; mkdir -p /persist/lp1/dl
  echo "  $URL"
  if [ ! -s "$ARCH" ] || [ "$(stat -c %s "$ARCH")" -lt 1000000 ]; then rm -f "$ARCH"; timed curl -sSL -o "$ARCH" "$URL"; fi
  ls -la "$ARCH"; sha256sum "$ARCH"
  rm -rf "$DEST"; mkdir -p "$DEST"
  python3 - "$ARCH" "$DEST" <<'PY2'
import zipfile, sys, os
arch, dest = sys.argv[1], sys.argv[2]
z = zipfile.ZipFile(arch)
names = z.namelist()
top = names[0].split("/")[0]
count = 0
for info in z.infolist():
    rel = info.filename[len(top) + 1:] if info.filename.startswith(top + "/") else info.filename
    if not rel or info.is_dir():
        continue
    out = os.path.join(dest, rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with z.open(info) as src, open(out, "wb") as dst:
        dst.write(src.read())
    mode = (info.external_attr >> 16) & 0o777
    if mode:
        os.chmod(out, mode)
    count += 1
print("  unpacked %d files under %s" % (count, dest))
PY2
fi
"$DEST/bin/lean" --version

step "the working copy of the new cache (the cache itself is never written), with the pinned lean-sail copied in if an earlier working copy holds that rev, else fetched, said so"
rm -rf "$PROJ"; mkdir -p "$PROJ"; cp -r "$CACHE"/. "$PROJ"/; rm -f "$PROJ/emit_lane.log" "$PROJ/MANIFEST.md"
SRCPROJ=""
if [ "$NEWREV" = "$REV5" ] && [ -d "$OLD5/.lake/packages/Sail" ]; then SRCPROJ=$OLD5; fi
if [ -z "$SRCPROJ" ] && [ "$NEWREV" = "$REV4" ] && [ -d "$OLD4/.lake/packages/Sail" ]; then SRCPROJ=$OLD4; fi
cd "$PROJ"
if [ -n "$SRCPROJ" ]; then
  mkdir -p "$PROJ/.lake"; cp -a "$SRCPROJ/.lake/packages" "$PROJ/.lake/"; cp "$SRCPROJ/lake-manifest.json" "$PROJ/lake-manifest.json"
  unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
  echo "  same rev '$NEWREV' as $SRCPROJ: its built lean-sail (commit $(git -C $PROJ/.lake/packages/Sail rev-parse HEAD 2>&1)) copied in; THIS LANE FETCHES NOTHING for the library (proxy variables unset)"
else
  echo "  DIFFERENT rev '$NEWREV' (neither earlier working copy holds it): this lane FETCHES it with lake update from github.com (authorised by brief §5 for this lane, said so here); http_proxy=${http_proxy:-unset}"
  timed lake update 2>&1 | tail -20
fi
echo "  --- lake-manifest.json (LITERAL) ---"; sed 's/^/    /' lake-manifest.json
echo "  --- the library's own commit and toolchain (LITERAL) ---"
git -C .lake/packages/Sail log -1 --format='  %H %ci %s' 2>&1; echo "    lean-toolchain: $(cat .lake/packages/Sail/lean-toolchain 2>&1)"
ls .lake/packages/Sail/Sail 2>/dev/null | tr '\n' ' '; echo
echo "  lean: $(lean --version 2>&1)"; echo "  lake: $(lake --version 2>&1)"
JOBS=""; if lake build --help 2>&1 | grep -q -- '--jobs'; then JOBS="--jobs=4"; fi
echo "  lake's jobs option (from lake build --help): '$JOBS'"
lake build --help 2>&1 | grep -i 'jobs' | head -3 | sed 's/^/    /'
du -sh "$PROJ" 2>&1 | sed 's/^/    /'

step "lake build Sail (the library), timed"
timed lake build $JOBS Sail 2>&1 | tail -8
peak

step "SAMPLE: lake build LeanIM.Defs (the module the two earlier emits failed at), timed"
timed lake build $JOBS LeanIM.Defs > /work/defs_build.txt 2>&1
rc=$?
tail -12 /work/defs_build.txt | sed 's/^/    /'
echo "  LeanIM.Defs rc=$rc; error lines: $(grep -c 'error' /work/defs_build.txt)"
if [ $rc -ne 0 ]; then echo "  FLAG: the first twelve error lines, LITERAL:"; grep -n 'error' /work/defs_build.txt | head -12 | sed 's/^/    /'; fi
peak

step "lake build LeanIM.InstsEnd (the module the proofs import, with everything it imports), timed"
timed lake build $JOBS LeanIM.InstsEnd > /work/instsend_build.txt 2>&1
rc=$?
tail -12 /work/instsend_build.txt | sed 's/^/    /'
echo "  LeanIM.InstsEnd rc=$rc; error lines: $(grep -c 'error' /work/instsend_build.txt)"
if [ $rc -ne 0 ]; then echo "  FLAG: the first twelve error lines, LITERAL:"; grep -n 'error' /work/instsend_build.txt | head -12 | sed 's/^/    /'; fi
echo "  oleans so far: $(ls .lake/build/lib/lean/LeanIM/*.olean 2>/dev/null | wc -l)"
peak

step "lake build (the whole library, default target), timed"
timed lake build $JOBS > /work/all_build.txt 2>&1
rc=$?
tail -12 /work/all_build.txt | sed 's/^/    /'
echo "  whole build rc=$rc; error lines: $(grep -c 'error' /work/all_build.txt); warning lines: $(grep -c 'warning' /work/all_build.txt)"
if [ $rc -ne 0 ]; then echo "  FLAG: the first twelve error lines, LITERAL:"; grep -n 'error' /work/all_build.txt | head -12 | sed 's/^/    /'; fi
peak

step "the count of modules built, of N"
NMOD=$(( $(ls LeanIM/*.lean | wc -l) + 1 ))
NOLE=$(( $(ls .lake/build/lib/lean/LeanIM/*.olean 2>/dev/null | wc -l) + $(ls .lake/build/lib/lean/LeanIM.olean 2>/dev/null | wc -l) ))
echo "  modules built: $NOLE of $NMOD (LeanIM/*.lean plus LeanIM.lean)"
du -sh "$PROJ/.lake" "$PROJ" 2>&1 | sed 's/^/    /'
df -h /persist | tail -1 | sed 's/^/    /'

step "a one-file smoke test of the built model: import it, check the names the harness composes, timed (the harness's first move)"
mkdir -p /work/smoke
cat > /work/smoke/Smoke.lean <<'EOF2'
import LeanIM
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIM LeanIM.Functions
set_option maxHeartbeats 2000000
#check @execute
#check @encdec_backwards
#check @encdec_compressed_backwards
#check @rX_bits
#check @wX_bits
#check @readReg
#check @writeReg
#print SailM
#check (default : SequentialState RegisterType trivialChoiceSource)
#check @sail_model_init
#check @reset
#check @Std.ExtDHashMap.get?_insert
#check @Std.ExtDHashMap.get?_insert_self
#check @Std.ExtDHashMap.get?_empty
#check @EStateM.bind
#check @EStateM.run
example : (2 : Int) * 3 = 6 := by grind
example (a b : Int) : (a + b) * (a + b) = a*a + 2*a*b + b*b := by grind
example (a b : BitVec 8) : a + b = b + a := by bv_decide
EOF2
cd "$PROJ"
timed lake env lean /work/smoke/Smoke.lean 2>&1 | head -80 | sed 's/^/    /'
peak

step "the namespace and the names of the register-file machinery as the harness will spell them (LITERAL grep of the emit)"
grep -n '^namespace\|^open\|^end ' LeanIM/Regs.lean | head -12 | sed 's/^/    /'
grep -n 'def rX_bits\|def wX_bits\|def rX \|def wX \|def execute \|def encdec_backwards \|def encdec_compressed_backwards \|def sail_model_init\|def reset \|def reset_misa\|def currentlyEnabled \|def hartSupports ' LeanIM/*.lean LeanIM.lean | sed 's/^/    /'
grep -n 'abbrev SailM\|inductive Register : Type\|deriving DecidableEq, Hashable' LeanIM/Defs.lean | head -4 | sed 's/^/    /'
echo "lane lp1_l12 done at $(date -u +%FT%TZ)"
