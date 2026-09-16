#!/usr/bin/env bash
# lp1 lane 6 -- the SECOND and LAST fetch lane (brief §4, lane 6): build
# the sail compiler from source at commit 5745ea9e53 (branch sail2,
# 2026-08-26, the head before the model's own commit of 2026-09-09), by
# the model's own CI recipe (.github/actions/sail-setup, sail-version
# "latest"): git clone; opam install sail --deps-only --yes; make install.
# The opam root is a COPY of the image's (/opt/opam -> /persist/opam) so
# that the built sail survives `down`. Hosts this lane reaches:
# github.com (the clone), opam.ocaml.org / ocaml.org (opam's index and
# any dependency source). A host the proxy refuses is a FLAG with the
# literal line; nothing is worked around. Sample first: the three hosts
# one request each, then the copy, then the clone, then the build.
# Wall time and peak resident per step; cgroup peak at the end.
set -u
export HOME=/work
total=9
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

step "what the persistent volume holds from the first launch (LITERAL), and this lane's proxy"
echo "  http_proxy=${http_proxy:-unset} https_proxy=${https_proxy:-unset}"
ls -la /persist /persist/lp1 2>&1 | sed 's/^/    /'
du -sh /persist/lp1/elan /persist/lp1/Lean_IM/.lake /persist/lp1/dl 2>&1 | sed 's/^/    /'
df -h /persist | tail -1 | sed 's/^/    /'
echo "  the image's sail: $(/opt/opam/default/bin/sail --version 2>&1)"
echo "  the image's opam: $(/opt/opam/default/bin/opam --version 2>&1 || opam --version 2>&1)"
echo "  which opam: $(command -v opam || echo ABSENT); which git: $(command -v git || echo ABSENT); which z3: $(command -v z3 || echo ABSENT); which make: $(command -v make || echo ABSENT)"

step "SAMPLE: one request to each host this lane needs, LITERAL status or refusal"
for u in https://github.com/rems-project/sail.git/info/refs?service=git-upload-pack https://opam.ocaml.org/index.tar.gz https://ocaml.org/ ; do
  echo "  --- $u"
  curl -sS -I -m 40 -o /dev/null -w "    HTTP %{http_code} in %{time_total}s\n" "$u" 2>&1 | sed 's/^/  /'
done

step "copy the image's opam root to /persist/opam (once; a copy so the build survives down)"
if [ ! -d /persist/opam/default ]; then
  timed cp -a /opt/opam /persist/opam
else
  echo "  /persist/opam already present (from an earlier attempt); kept"
fi
du -sh /persist/opam 2>&1 | sed 's/^/    /'
export OPAMROOT=/persist/opam
export OPAMYES=1
export OPAMSWITCH=default
export PATH=/persist/opam/default/bin:$PATH
eval "$(opam env --root=/persist/opam --switch=default --set-root --set-switch 2>&1 | grep -v '^\[' )" || true
echo "  opam var prefix: $(opam var prefix 2>&1)"
echo "  opam switch list:"; opam switch list 2>&1 | sed 's/^/    /'
echo "  ocaml: $(ocaml -version 2>&1); which ocamlfind: $(command -v ocamlfind || echo ABSENT); which dune: $(command -v dune || echo ABSENT)"
CONF=/persist/opam/default/lib/findlib.conf
if [ -f "$CONF" ]; then
  echo "  findlib.conf BEFORE relocation (LITERAL):"; sed 's/^/    /' "$CONF"
  if grep -q '/opt/opam' "$CONF"; then sed -i 's#/opt/opam#/persist/opam#g' "$CONF"; fi
  export OCAMLFIND_CONF=$CONF
  echo "  findlib.conf AFTER relocation (LITERAL):"; sed 's/^/    /' "$CONF"
fi
echo "  ocamlfind printconf destdir: $(ocamlfind printconf destdir 2>&1)"
echo "  sail (the copy, before the build): $(sail --version 2>&1); which sail: $(command -v sail)"
echo "  opam list, the sail-related packages installed in the copy:"; opam list 2>&1 | grep -iE '^(sail|lem|linksem|ott|libsail|dune |menhir|yojson|z3|zarith|omd|pprint|linenoise|base64|logs|fmt|cmdliner|sedlex|alcotest|ocaml )' | sed 's/^/    /'

step "git clone https://github.com/rems-project/sail.git into /persist/sail-src; checkout 5745ea9e53 (LITERAL commit line)"
cd /persist
if [ ! -d /persist/sail-src/.git ]; then
  timed git clone https://github.com/rems-project/sail.git /persist/sail-src 2>&1 | tail -5
else
  echo "  clone already present; fetching"; git -C /persist/sail-src fetch --all 2>&1 | tail -3
fi
cd /persist/sail-src
git checkout --quiet 5745ea9e53 2>&1 | tail -3
git log -1 --format='  %H %ci %s' 2>&1
echo "  branch containing it: $(git branch -r --contains 5745ea9e53 2>/dev/null | head -3 | tr '\n' ' ')"
ls /persist/sail-src | head -40 | tr '\n' ' '; echo
echo "  the opam file's version line and its depends (LITERAL, first 60 lines of sail.opam):"
sed -n '1,60p' sail.opam | sed 's/^/    /'

step "opam install sail --deps-only --yes, inside the clone (the CI recipe), timed; on failure, opam update then retry"
cd /persist/sail-src
timed opam install . --deps-only --yes 2>&1 | tail -40
rc=$?
if [ $rc -ne 0 ]; then
  echo "  first attempt rc=$rc; running opam update (fetches the index from opam.ocaml.org), then retrying"
  timed opam update --yes 2>&1 | tail -15
  timed opam install . --deps-only --yes 2>&1 | tail -60
  rc=$?
fi
echo "  deps-only rc=$rc"
peak

step "make install (dune build --release; dune install into the switch prefix), timed"
cd /persist/sail-src
export OPAMROOT=/persist/opam
eval "$(opam env --root=/persist/opam --switch=default --set-root --set-switch 2>&1 | grep -v '^\[' )" || true
echo "  OPAM_SWITCH_PREFIX=${OPAM_SWITCH_PREFIX:-unset}"
timed make install 2>&1 | tail -40
echo "  make install rc=$?"
peak

step "the built sail, LITERAL: sail --version, which sail, sail --dir"
export PATH=/persist/opam/default/bin:$PATH
hash -r
echo "  which sail: $(command -v sail)"
echo "  sail --version: $(sail --version 2>&1)"
echo "  sail --dir: $(sail --dir 2>&1)"
ls -la /persist/opam/default/bin/sail 2>&1 | sed 's/^/    /'
ls "$(sail --dir 2>/dev/null)/lib" 2>/dev/null | head -5 | sed 's/^/    /'
echo "  the Lean backend is present in the built sail (LITERAL grep of --help):"
sail --help 2>&1 | grep -E '^\s*-+lean' | head -30 | sed 's/^/    /'

step "SAMPLE the built sail on the model: sail --list-files I_insts M_insts postlude main (seconds), and the lean flags of the emit invocation are accepted"
cd /opt/sail-riscv-src/model
timed sail --list-files I_insts M_insts postlude main riscv.sail_project 2>&1 | tail -3
echo "  files resolved: $(sail --list-files I_insts M_insts postlude main riscv.sail_project 2>/dev/null | wc -l); base_insts/mext_insts among them: $(sail --list-files I_insts M_insts postlude main riscv.sail_project 2>/dev/null | grep -cE 'base_insts.sail|mext_insts.sail')"
for f in --lean --lean-output-dir --lean-force-output --lean-non-beq-type --lean-noncomputable --lean-noncomputable-function --lean-import-file --memo-z3 --memo-z3-path --strict-var --strict-bitvector --strict-exponentials; do
  if sail --help 2>&1 | grep -qE -- "^\s*$f\b"; then echo "    $f: accepted"; else echo "    $f: NOT IN --help"; fi
done

step "sizes and the persistent state left for lane 7 (which fetches nothing)"
du -sh /persist/opam /persist/sail-src 2>&1 | sed 's/^/    /'
df -h /persist | tail -1 | sed 's/^/    /'
peak
echo "lane lp1_l6 done at $(date -u +%FT%TZ)"
