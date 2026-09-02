#!/bin/sh
# JIT track -- JVM pilot, LANE C: the warm-up recipe, pinned.
# Lane A bracketed C2's takeover of af between 5000 and 10000 calls.
# This lane narrows the bracket, and repeats each point three times so
# the boundary is a repeated observation rather than a single run.
set -u
echo "=== jvm_c_recipe ==="
date -u +%Y-%m-%dT%H:%M:%SZ

W=/work/jvmc
rm -rf "$W"; mkdir -p "$W"
cd "$W" || exit 4
O=/out/jvm_c
rm -rf "$O"; mkdir -p "$O"
cp /out/jvm_a/Probe.java .
javac Probe.java 2>&1

echo ""
echo "### fine sweep, -XX:-TieredCompilation (C2 only), 3 reps each ###"
: > "$O/fine_sweep.txt"
for N in 5000 6000 7000 8000 9000 9500 10000 11000 12000; do
  for R in 1 2 3; do
    T0=`date +%s.%N`
    OUT=`java -XX:-TieredCompilation -XX:+PrintCompilation Probe $N 2>&1`
    T1=`date +%s.%N`
    WALL=`echo "$T1 $T0" | awk '{printf "%.3f", $1-$2}'`
    A=`echo "$OUT" | grep -c 'Probe::af (4 bytes)'`
    B=`echo "$OUT" | grep -c 'Probe::af2 (4 bytes)'`
    L="n=$N rep=$R wall=${WALL}s af=$A af2=$B"
    echo "$L"
    echo "$L" >> "$O/fine_sweep.txt"
  done
done

echo ""
echo "### same sweep, DEFAULT tiers (for contrast) ###"
: > "$O/fine_sweep_tiered.txt"
for N in 200 500 1000 2000 5000 10000; do
  OUT=`java -XX:+PrintCompilation Probe $N 2>&1`
  A3=`echo "$OUT" | grep -E 'Probe::af \(4 bytes\)' | grep -c ' 3  *Probe'`
  A4=`echo "$OUT" | grep -E 'Probe::af \(4 bytes\)' | grep -c ' 4  *Probe'`
  L="n=$N  af_at_tier3=$A3  af_at_tier4=$A4"
  echo "$L"
  echo "$L" >> "$O/fine_sweep_tiered.txt"
  echo "$OUT" | grep -E 'Probe::af \(4' >> "$O/fine_sweep_tiered.txt"
done

echo ""
echo "### total cost of the whole JVM pilot, measured here ###"
echo "one C2-only warmed run, timed 5x:"
for R in 1 2 3 4 5; do
  T0=`date +%s.%N`
  java -XX:-TieredCompilation Probe 200000 > /dev/null 2>&1
  T1=`date +%s.%N`
  echo "  rep$R `echo "$T1 $T0" | awk '{printf "%.3f", $1-$2}'`s"
done

echo "=== jvm_c_recipe done ==="
date -u +%Y-%m-%dT%H:%M:%SZ
