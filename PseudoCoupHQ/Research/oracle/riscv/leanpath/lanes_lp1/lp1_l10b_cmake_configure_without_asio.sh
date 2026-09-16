#!/usr/bin/env bash
# lp1 lane 10b -- lane 10's step 7 again. Lane 10's `cmake -S . -B build
# -DCMAKE_BUILD_TYPE=Release -DFIRST_PARTY_TESTS=OFF` in the model clone at
# 6266b40c1c stopped at dependencies/asio: FetchContent downloads asio from
# https://downloads.sourceforge.net/..., and the proxy refused that host
# (LITERAL: `TCP_DENIED/403 3376 CONNECT downloads.sourceforge.net:443`) --
# a FLAG, recorded, not worked around: the host is NOT added and nothing is
# fetched from it. The model's OWN dependencies/asio/CMakeLists.txt carries
# `option(DOWNLOAD_ASIO "Download asio" ON)` with the comment "Allow
# downloads to be turned off (in particular, for targets that don't need
# it)"; the Lean emit needs no asio (the C emulator does); and the config
# json this lane exists for is produced by config/CMakeLists.txt's
# `configure_file(config.json.in ...)` from cmake variables alone, with no
# network in it (both files are printed LITERAL below). So this lane runs
# the same configure with the model's own switch -DDOWNLOAD_ASIO=OFF. The
# only other fetch the configure makes is CLI11 from github (allowlisted).
# Sample first: the option line and the config recipe, LITERAL; then the
# configure; then the json, diffed against the image's 3243f93 one.
set -u
export HOME=/work
P=PseudoCoupHQ
LP=$P/Research/oracle/riscv/leanpath
MODEL=/persist/sail-riscv-6266b40c
OLDCFG=/opt/sail-riscv-src/build/config/rv64d_v256_e64.json
export OPAMROOT=/persist/opam
export OPAMSWITCH=default
export OCAMLFIND_CONF=/persist/opam/default/lib/findlib.conf
export PATH=/persist/opam/default/bin:$PATH
total=6
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

step "the model's own switch and the config recipe at 6266b40c1c, LITERAL (dependencies/asio/CMakeLists.txt lines 1-14; config/CMakeLists.txt's configure_file line; dependencies/CMakeLists.txt whole)"
cd "$MODEL"
git log -1 --format='  model %H %ci' 2>&1
sed -n '1,14p' dependencies/asio/CMakeLists.txt | sed 's/^/    /'
echo "  ---- config/CMakeLists.txt, the lines that write the json ----"
grep -n 'configure_file\|config_filename "' config/CMakeLists.txt | sed 's/^/    /'
echo "  ---- dependencies/CMakeLists.txt (every fetch the configure makes) ----"
sed 's/^/    /' dependencies/CMakeLists.txt
echo "  ---- every FetchContent URL under the tree ----"
grep -rn 'URL \|GIT_REPOSITORY' --include=CMakeLists.txt . 2>/dev/null | grep -v '^./build' | sed 's/^/    /'
echo "  http_proxy=${http_proxy:-unset} (this lane fetches CLI11 from github if the configure asks; nothing from sourceforge)"

step "cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DFIRST_PARTY_TESTS=OFF -DDOWNLOAD_ASIO=OFF (the model's own option), timed"
cd "$MODEL"
rm -rf build
timed cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DFIRST_PARTY_TESTS=OFF -DDOWNLOAD_ASIO=OFF > /work/cmake_configure.txt 2>&1
rc=$?
echo "  cmake rc=$rc; the whole output (LITERAL):"
sed 's/^/    /' /work/cmake_configure.txt
if [ $rc -ne 0 ]; then echo "  FLAG: cmake configure failed again; every line with 'error' (LITERAL):"; grep -n -i 'error' /work/cmake_configure.txt | head -20 | sed 's/^/    /'; fi
peak

step "build/config: the json this lane exists for (LITERAL listing, size, sha256)"
ls -la build/config 2>&1 | sed 's/^/    /'
sha256sum build/config/rv64d_v256_e64.json 2>&1 | sed 's/^/    /'
echo "  lines: $(wc -l < build/config/rv64d_v256_e64.json 2>/dev/null)"

step "diff against the image's 3243f93 config (the one lanes 5/7b emitted with), LITERAL"
diff "$OLDCFG" build/config/rv64d_v256_e64.json > /work/cfg.diff 2>&1; drc=$?
echo "  diff rc=$drc (0 = identical); lines: $(wc -l < /work/cfg.diff)"
sed 's/^/    /' /work/cfg.diff | head -80

step "the sail this lane leaves in place for lane 11 (LITERAL), and sail --list-files once more with the config present"
echo "  sail --version: $(sail --version 2>&1)"
cd "$MODEL/model"
timed sail --list-files I_insts M_insts postlude main riscv.sail_project > /work/listfiles.txt 2>&1
echo "  files resolved: $(tr ' ' '\n' < /work/listfiles.txt | grep -c '\.sail$')"

step "sizes, the cgroup peak"
du -sh "$MODEL/build" 2>&1 | sed 's/^/    /'
df -h /persist | tail -1 | sed 's/^/    /'
peak
echo "lane lp1_l10b done at $(date -u +%FT%TZ)"
