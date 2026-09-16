#!/usr/bin/env bash
# lp1 lane 23 -- CONTAINERS: the universal container (a dict-list) built and
# checked against the REAL lean-sail package, not against a transcription.
#
# `leanpath_src/Containers.lean` was written and checked on the laptop, where
# the lean-sail package does not exist, so its three Sail primitives
# (`vectorUpdate`, `vectorInit`, `Vector.length`) are TRANSCRIBED from their
# uses in the emit (header note 4 of that file). This lane is the one thing
# the laptop could not do:
#
#   1. PRINT the package's own definitions, literal, so the transcription can
#      be read against them by eye;
#   2. PROVE the transcription equals them, by `rfl` in separate one-line
#      files -- each file's rc printed on its own, so one wrong transcription
#      cannot hide the others;
#   3. BUILD Universal.lean + Containers.lean under the emit's own toolchain
#      (leanprover/lean4:v4.29.0; the laptop has v4.30.0), and print the 24
#      self-checks and the axiom audit the file carries.
#
# Never the cache and never /work/proof: /work/proof is only READ (its built
# lean-sail package is copied). This lane writes only /work/containers.
# FETCHES NOTHING (proxy variables unset). One process, no pool, no clock.
set -uo pipefail
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
export HOME=/work
P=PseudoCoupHQ
LP=$P/Research/oracle/riscv/leanpath
KS=$LP/lp1_harness/leanpath_src
CACHE=$LP/cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules
SRC=/work/proof
W=/work/containers
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
total=7
t0=$(date +%s)

echo "[1/$total] this lane fetches nothing: http_proxy=${http_proxy:-unset}"
df -h /work | tail -1 | awk '{print "  /work: "$4" free of "$2}'
echo "  source read: $KS/Universal.lean ($(wc -l < $KS/Universal.lean) lines), $KS/Containers.lean ($(wc -l < $KS/Containers.lean) lines)"
[ -d "$SRC/.lake/packages/Sail" ] || { echo "FLAG: no built lean-sail package at $SRC/.lake/packages/Sail -- this lane needs the instance whose /work/proof holds the built emit"; exit 3; }
echo "  package read (never written): $SRC/.lake/packages/Sail"
du -sh $SRC/.lake/packages/Sail | awk '{print "  its size: "$1}'
cat $CACHE/lean-toolchain | sed 's/^/  emit toolchain: /'

echo "[2/$total] the package's OWN definitions of the three container primitives, LITERAL"
SAILSRC=$SRC/.lake/packages/Sail
echo "  --- files ---"
find $SAILSRC -name '*.lean' -not -path '*/.lake/*' | sed 's/^/    /'
for name in vectorUpdate vectorInit "Vector.length" "def Vector" "abbrev Vector" "GetElem"; do
  echo "  --- $name ---"
  grep -rn -B2 -A6 -- "$name" $SAILSRC --include='*.lean' 2>/dev/null \
    | grep -v '^.*/\.lake/' | head -60 | sed 's/^/    /'
done

echo "[3/$total] the project at $W (the built package copied in; nothing fetched, nothing built twice)"
rm -rf $W; mkdir -p $W/src $W/probe
cp $KS/Universal.lean $KS/Containers.lean $W/src/
cp $CACHE/lean-toolchain $W/
cp $SRC/lake-manifest.json $W/ 2>/dev/null || true
mkdir -p $W/.lake/packages
cp -a $SRC/.lake/packages/Sail $W/.lake/packages/Sail
cat > $W/lakefile.toml <<'EOF'
name = "Containers_lane"
defaultTargets = ["ContainersLib"]

[[lean_lib]]
name = "ContainersLib"
srcDir = "src"
roots = ["Universal", "Containers"]

[[require]]
name = "Sail"
git = "https://github.com/rems-project/lean-sail"
rev = "v5"
EOF
echo "  wrote $W/lakefile.toml, src/Universal.lean, src/Containers.lean"

echo "[4/$total] BUILD: Universal + Containers under the emit's own toolchain -- the 24 self-checks and the axiom audit are this build's output"
cd $W
lake build ContainersLib 2>&1 | sed 's/^/    /'
brc=${PIPESTATUS[0]}
echo "  lake rc=$brc"

echo "[5/$total] the transcription, one claim per file, each rc on its own line"
mk () { # mk <name> <body>
  printf '%s\n' "$2" > $W/probe/$1.lean
  ( cd $W && env LEAN_PATH="$W/.lake/build/lib/lean:$W/.lake/packages/Sail/.lake/build/lib/lean" \
      lake env lean $W/probe/$1.lean ) > $W/probe/$1.out 2>&1
  rc=$?
  echo "  rc=$rc  $1"
  sed 's/^/      /' $W/probe/$1.out
}
mk length_is_the_type "import Sail
import Containers
open Containers
example {α : Type} {n : Nat} (v : Vector α n) : sailVectorLength v = Vector.length v := rfl"
mk init_is_replicate "import Sail
import Containers
open Containers
example {α : Type} {n : Nat} (a : α) : (sailVectorInit a : Vector α n) = vectorInit a := rfl"
mk update_nat_index "import Sail
import Containers
open Containers
example {α : Type} {n : Nat} (v : Vector α n) (i : Nat) (x : α) :
    sailVectorUpdate v i x = vectorUpdate v i x := rfl"
mk update_int_index "import Sail
import Containers
open Containers
example {α : Type} {n : Nat} (v : Vector α n) (i : Int) (x : α) :
    sailVectorUpdateI v i x = vectorUpdate v i x := rfl"
mk read_is_getElem "import Sail
import Containers
open Containers
example {α : Type} [Inhabited α] {n : Nat} (v : Vector α n) (i : Nat) :
    sailVectorRead v i = GetElem?.getElem! v i := rfl"
mk what_the_package_says "import Sail
#check @vectorUpdate
#check @vectorInit
#check @Vector.length
#print vectorUpdate
#print vectorInit
#print Vector.length"

echo "[6/$total] the bridge theorems restated over the package's own names -- this file is the actual claim of the lane"
mk bridge_over_the_package "import Sail
import Containers
open Containers
open Containers.Dict
-- Vector.length equals length
example {α : Type} {n : Nat} (v : Vector α n) : Vector.length v = (ofVector v).length := by
  simpa using (sailVectorLength_eq_length v)
-- vectorInit equals a dict-list of one repeated value
example {α : Type} {n : Nat} (a : α) : ofVector (vectorInit (n := n) a) = repeatVal n a := by
  simpa using (ofVector_sailVectorInit (n := n) a)
-- vectorUpdate equals set, in bounds
example {α : Type} {n : Nat} (v : Vector α n) (i : Nat) (x : α) (h : i < n) :
    ofVector (vectorUpdate v i x) = (ofVector v).set (key i) x := by
  simpa using (ofVector_sailVectorUpdate v i x h)
-- the round trip
example {α : Type} {n : Nat} (v : Vector α n) (dflt : α) : toVector n (ofVector v) dflt = v :=
  toVector_ofVector v dflt"

echo "[7/$total] what this lane proved, and what it did not"
echo "  if [5] and [6] are all rc=0, the transcription in Containers.lean IS the package's, and every bridge theorem holds over the package's own names."
echo "  if any is nonzero, its output above names the difference; the file's header note 4 is then the thing to correct, not the proofs."
echo "  NOT attempted here, deliberately: the memory bridge. The model's vmem_read / vmem_write bottom out in"
echo "  Sail/ConcurrencyInterfaceV1.lean (readReg / writeReg / writeByte), a monadic machine; no read-after-write"
echo "  lemma of the package has been seen, so Containers.lean states the read-back law on the CONTAINER only."
echo "  grep -c exempt over the files this lane touches (0 expected on every deliverable):"
for f in $KS/Containers.lean $LP/lanes_lp1/lp1_l23_containers_against_the_real_lean_sail.sh; do
  echo "    $(grep -c exempt "$f") $(basename "$f")"
done
echo "lane lp1_l23 done in $(( $(date +%s) - t0 ))s at $(date -u +%FT%TZ)"
