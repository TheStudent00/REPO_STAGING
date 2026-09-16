#!/usr/bin/env bash
# lp1 lane 1d -- lane 1 again (lane 1c named the asset with a stray `v` and the image has no zstd, so the .zip asset is taken and python unpacks it), with the toolchain taken from the host the
# brief names. FLAG carried from lanes l1/l1b: elan 4.2.4 downloads every
# toolchain from https://release.lean-lang.org and the proxy refuses that
# host (LITERAL, lp1-proxy: `TCP_DENIED/403 3368 CONNECT
# release.lean-lang.org:443`); elan has no switch for another source. The
# same release archive is published on github.com, an allowlisted host,
# so this lane takes it from there with curl and places it where elan
# keeps toolchains; no host is added to the allowlist. Then `lake update`
# fetches lean-sail rev v4 from github.com and the model's Lean is built
# once into /persist. Sample first (LeanIM.Defs), then LeanIM.InstsEnd,
# then everything. Wall time and peak resident per step.
set -u
export PATH=/opt/elan/bin:/opt/opam/default/bin:$PATH
CACHE=PseudoCoupHQ/Research/oracle/riscv/leanpath/cache/sail-riscv_3243f93_I_insts_M_insts_postlude_main
PERSIST=/persist/lp1
PROJ=$PERSIST/Lean_IM
export ELAN_HOME=$PERSIST/elan
export HOME=/work
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

step "the hosts this lane reaches: github.com and objects.githubusercontent.com (the release asset); nothing else"
echo "  http_proxy=${http_proxy:-unset}"
TC="$(cat $CACHE/lean-toolchain)"; VER="${TC#leanprover/lean4:}"
echo "  toolchain the cache pins: $TC  (version $VER)"
mkdir -p "$ELAN_HOME/toolchains" "$PERSIST/dl"
export PATH=$ELAN_HOME/bin:$PATH
elan --version

step "the release archive from github.com, by curl, LITERAL headers and size"
NUM="${VER#v}"
URL="https://github.com/leanprover/lean4/releases/download/$VER/lean-$NUM-linux.zip"
echo "  $URL"
ARCH="$PERSIST/dl/lean-$NUM-linux.zip"
if [ ! -s "$ARCH" ] || [ "$(stat -c %s "$ARCH")" -lt 1000000 ]; then rm -f "$ARCH"; timed curl -sSL -o "$ARCH" "$URL"; fi
ls -la "$ARCH"; sha256sum "$ARCH"
python3 -c "import zipfile,sys; z=zipfile.ZipFile(sys.argv[1]); n=z.namelist(); print('  entries:', len(n)); print('  first:', n[:3])" "$ARCH"

step "unpack into elan's toolchain directory (elan's own naming: leanprover--lean4---$VER)"
DEST="$ELAN_HOME/toolchains/leanprover--lean4---$VER"
if [ ! -x "$DEST/bin/lean" ]; then
  rm -rf "$DEST"; mkdir -p "$DEST"
  python3 - "$ARCH" "$DEST" <<'PY2'
import zipfile, sys, os, stat
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
print("  unpacked %d files under %s (top-level entry %r stripped)" % (count, dest, top))
PY2
fi
ls "$DEST" | head; ls "$DEST/bin" | head -20
elan toolchain list
"$DEST/bin/lean" --version

step "the working copy of the cached project (the cache itself is never written)"
if [ ! -d "$PROJ/LeanIM" ]; then mkdir -p "$PROJ"; cp -r "$CACHE"/. "$PROJ"/; fi
cd "$PROJ"
echo "  lean --version through elan, from lean-toolchain:"; lean --version; lake --version

step "lake update: fetch lean-sail rev v4 (the require in lakefile.toml) from github.com"
timed lake update 2>&1 | tail -30
echo "  --- lake-manifest.json after the fetch ---"; cat lake-manifest.json
echo "  --- the library's own commit and toolchain ---"; git -C .lake/packages/Sail log -1 --format='%H %ci %s' 2>&1; cat .lake/packages/Sail/lean-toolchain 2>&1
ls .lake/packages/Sail; ls .lake/packages/Sail/Sail 2>/dev/null
peak

step "the library's state and register machinery, LITERAL (what the harness will unfold)"
grep -rn 'PreSailM\b\|structure SequentialState\|def readReg\|def writeReg\|def get_slice_int\|abbrev PreSailM\|def PreSailM' .lake/packages/Sail/Sail/*.lean | head -40
for f in .lake/packages/Sail/Sail/State.lean; do
  if [ -f "$f" ]; then echo "  --- $f (first 260 lines) ---"; sed -n '1,260p' "$f"; fi
done
echo "  --- BitVec helpers ---"
grep -rn 'def get_slice_int\|def extractLsb\|def toNatInt\|≥b\|+i\b' .lake/packages/Sail/Sail/BitVec.lean .lake/packages/Sail/Sail/Int.lean .lake/packages/Sail/Sail/Sail.lean 2>/dev/null | head -30

step "lake build Sail (the library alone), timed"
timed lake build Sail 2>&1 | tail -15
peak

step "sample: lake build LeanIM.Defs (one module), timed"
timed lake build LeanIM.Defs 2>&1 | tail -15
peak

step "lake build LeanIM.InstsEnd (the module the proofs import, with everything it imports), timed, -j 4"
timed lake build -j 4 LeanIM.InstsEnd 2>&1 | tail -40
peak
echo "  oleans so far: $(ls .lake/build/lib/lean/LeanIM/*.olean 2>/dev/null | wc -l)"

step "lake build (the whole library, default target), timed, -j 4"
timed lake build -j 4 2>&1 | tail -40
peak
echo "  oleans built: $(ls .lake/build/lib/lean/LeanIM/*.olean 2>/dev/null | wc -l) of $(ls $PROJ/LeanIM/*.lean | wc -l) modules"
du -sh "$PROJ/.lake" "$ELAN_HOME" 2>/dev/null
df -h /persist | tail -1
echo "lane lp1_l1d done at $(date -u +%FT%TZ)"
