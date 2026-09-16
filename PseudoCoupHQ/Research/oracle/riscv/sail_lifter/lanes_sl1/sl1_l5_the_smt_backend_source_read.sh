#!/bin/bash
# sl1 lane 5 -- read-only: how Sail 0.20.2's SMT backend names its output,
# declares registers and property arguments, and treats extern functions
# (the softfloat interface), from its own OCaml source under opam.
set -u
total=4
export HOME=/work
SRC=$(ls -d /opt/opam/default/.opam-switch/sources/sail_smt_backend* /opt/opam/default/.opam-switch/sources/sail*/src/sail_smt_backend 2>/dev/null | head -3)
echo "[1/$total] where the backend's source is"
echo "$SRC"
find /opt/opam/default/.opam-switch/sources -maxdepth 4 -name '*smt*' 2>/dev/null | head -20
echo "[2/$total] output naming, property handling"
for f in $(find /opt/opam/default/.opam-switch/sources -maxdepth 5 -path '*smt*' -name '*.ml' 2>/dev/null); do
  echo "== $f"; grep -n 'smt2\|\$property\|"property"\|counterexample\|open_out\|declare-const\|define-fun\|Register\|register' $f | head -60
done
echo "[3/$total] extern / unsupported primitives: what the backend says when it meets one"
for f in $(find /opt/opam/default/.opam-switch/sources -maxdepth 5 -path '*smt*' -name '*.ml' 2>/dev/null); do
  grep -n 'not supported\|unsupported\|Unsupported\|extern\|Extern\|unimplemented' $f | head -20
done
echo "[4/$total] the jib smt builtins list (what constructs it knows)"
for f in $(find /opt/opam/default/.opam-switch/sources -maxdepth 5 -name 'smt_builtins.ml' -o -maxdepth 5 -name 'jib_smt.ml' 2>/dev/null); do
  echo "== $f $(wc -l < $f) lines"; grep -n '^  | "' $f | head -120; grep -n '^let builtin_\|^and builtin_\|^let smt_builtin' $f | head -80
done
echo "done $(date -u +%FT%TZ)"
