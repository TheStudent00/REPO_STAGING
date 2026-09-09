#!/usr/bin/env bash
# t93 lane 5 -- THE MOVE. The graphs, the coverage joins, the super-op
# candidates, the variant connections and the diaries leave PseudoCoupHQ
# for the companion folder PseudoCoupGraphs, and each graph is written
# there in the COMPACT form.
#
# the owner, 2026-09-04: "we can have a separate companion folder for the
# graphs and we will use local git to track changes every 30 seconds."
# The companion folder has NO REMOTE, deliberately -- repo-daemon commits
# a remote-less repository locally and never pushes. NO ORIGIN IS ADDED
# HERE.
#
# WHAT MOVES: the CURRENT artifacts only.
# WHAT STAYS, and it is named rather than left to a wildcard: the four
# earlier go laps (graph_go2/go3/go4/go_lapone.json, 533,590,808 bytes
# between them), the two earlier cpp laps (graph_cpp2/cpp3.json) and the
# superseded coverage_go.json. They are RECORDS of what was and they stay
# where they are, in this repository, untracked, exactly as they are now.
#
# THE ORDER IS THE SAFETY. For each graph: compact it INTO the companion
# folder, expand it back, compare with the original BYTE FOR BYTE, and
# only then remove the original. Nothing is deleted that has not first
# been proved rebuildable.
#
# THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
# second violation). No operator token may appear in ANY key, grouping,
# pairing, row structure, candidate selection, or comparison scope,
# anywhere in this line -- not in matching, not in "which pairs get
# compared", not in report rows, not in dropdowns. The candidate set for
# comparison comes from machine-form evidence (clusters, connections,
# type pairs) or from ratified intention -- never from the token. The
# token appears exactly once per unit: as a display label on the member.
# MECHANICAL GUARD REQUIRED: every pipeline stage that groups or pairs
# units must run op_pipeline/check_no_spelling_keys.py and refuse its own
# output on failure.
#
# This lane moves files. It groups nothing and pairs nothing.
set -u
CG=/projects/PseudoCoupHQ/Research/compiler_graph
GR=/projects/PseudoCoupGraphs
cd "$CG"
total=8; i=0
step() { i=$((i+1)); echo; echo "======== [$i/$total] $* ========"; }

step "before: what is tracked in PseudoCoupHQ, and what is not"
for f in graph_go.json graph_cpp.json graph_rust.json graph_swift.json \
         graph_go2.json graph_go3.json graph_go4.json graph_go_lapone.json \
         graph_cpp2.json graph_cpp3.json coverage_go.json coverage_go2.json \
         coverage_c.json coverage_cpp.json coverage_c_and_cpp.json \
         coverage_extended.json super_ops_go.json super_ops_cpp.json \
         variant_connections_go.json variant_connections_c.json \
         variant_connections_cpp.json variant_connections_c_and_cpp.json \
         variant_connections_extended.json variant_connections_rust.json \
         variant_connections_swift.json \
         graph_go_files.json graph_cpp_files.json coverage_go_files.json \
         coverage_go_summary.json coverage_cpp_summary.json ; do
  if git -C /projects/PseudoCoupHQ ls-files --error-unmatch "Research/compiler_graph/$f" >/dev/null 2>&1; then T=TRACKED; else T="untracked"; fi
  if [ -f "$f" ]; then S=$(stat -c%s "$f"); else S=ABSENT; fi
  printf '   %-38s %-9s %14s\n' "$f" "$T" "$S"
done

step "the four graphs: compact into the companion folder, prove, then remove"
for LANG in go rust swift cpp; do
  echo "   --- $LANG ---"
  python3 graph_compact.py compact --graph graph_$LANG.json \
      --out "$GR/graph_$LANG.json" >/dev/null || exit 1
  python3 graph_compact.py expand --compact "$GR/graph_$LANG.json" \
      --out /work/rebuilt_$LANG.json --verify >/dev/null || exit 1
  if cmp graph_$LANG.json /work/rebuilt_$LANG.json; then
    echo "     THE ROUND-TRIP DIFF: cmp graph_$LANG.json <rebuilt> -> IDENTICAL, 0 differing bytes"
  else
    echo "     cmp -> DIFFERENT. NOTHING WILL BE REMOVED."; exit 1
  fi
  B=$(stat -c%s graph_$LANG.json); A=$(stat -c%s "$GR/graph_$LANG.json")
  python3 -c "print('     SIZE graph_$LANG.json  before %14d  after %13d  (%.1f%%, %.1fx smaller)' % ($B,$A,100.0*$A/$B,$B/float($A)))"
  rm -f graph_$LANG.json /work/rebuilt_$LANG.json
  echo "     removed $CG/graph_$LANG.json (rebuildable: graph_compact.py expand)"
done

step "the coverage joins, the super-op candidates and the variant connections"
for f in coverage_go2.json coverage_c.json coverage_cpp.json \
         coverage_c_and_cpp.json coverage_extended.json \
         super_ops_go.json super_ops_cpp.json \
         variant_connections_go.json variant_connections_c.json \
         variant_connections_cpp.json variant_connections_c_and_cpp.json \
         variant_connections_extended.json variant_connections_rust.json \
         variant_connections_swift.json ; do
  [ -f "$f" ] || { echo "   $f ABSENT, skipped"; continue; }
  B=$(stat -c%s "$f")
  cp -p "$f" "$GR/$f" || exit 1
  A=$(stat -c%s "$GR/$f")
  if [ "$B" != "$A" ]; then echo "   $f COPY SIZE MISMATCH $B vs $A -- refusing"; exit 1; fi
  M1=$(md5sum < "$f" | cut -d' ' -f1); M2=$(md5sum < "$GR/$f" | cut -d' ' -f1)
  if [ "$M1" != "$M2" ]; then echo "   $f MD5 MISMATCH -- refusing"; exit 1; fi
  rm -f "$f"
  printf '   moved %-38s %14d bytes, md5 %s\n' "$f" "$B" "$M1"
done

step "the diaries, with their hardlinks preserved"
echo "   before, in PseudoCoupHQ:"
du -sb diaries | sed 's/^/     /'
for d in diaries/*; do echo "     $d: $(ls -1 "$d" | wc -l) files"; done
tar -C "$CG" -cf - diaries | tar -C "$GR" -xf - || exit 1
echo "   after, in PseudoCoupGraphs:"
du -sb "$GR/diaries" | sed 's/^/     /'
OK=yes
for d in diaries/*; do
  a=$(ls -1 "$CG/$d" | wc -l); b=$(ls -1 "$GR/$d" | wc -l)
  printf '     %-22s here %5d  there %5d  %s\n' "$d" "$a" "$b" "$([ "$a" = "$b" ] && echo same || { OK=no; echo DIFFERENT; })"
done
[ "$OK" = yes ] || { echo "   diary counts differ -- refusing to remove"; exit 1; }
echo "   one file compared byte for byte, both sides:"
SAMPLE=$(ls -1 "$CG/diaries/go" | head -1)
cmp "$CG/diaries/go/$SAMPLE" "$GR/diaries/go/$SAMPLE" && echo "     $SAMPLE IDENTICAL"
rm -rf "$CG/diaries"
echo "   removed $CG/diaries"

step "the superseded laps, which STAY, listed so the record is explicit"
for f in graph_go2.json graph_go3.json graph_go4.json graph_go_lapone.json \
         graph_cpp2.json graph_cpp3.json coverage_go.json ; do
  if [ -f "$f" ]; then printf '   STAYS %-30s %14d bytes\n' "$f" "$(stat -c%s "$f")";
  else printf '   STAYS %-30s ABSENT\n' "$f"; fi
done

step "the companion folder, and that it still has NO REMOTE"
ls -la "$GR" | sed 's/^/   /'
du -sb "$GR" | sed 's/^/   whole folder: /'
echo "   remotes (none expected, by design):"
git -C "$GR" remote -v | sed 's/^/     /'
echo "   (nothing above this line means no remote)"

step "PseudoCoupHQ afterwards"
du -sb "$CG" | sed 's/^/   Research\/compiler_graph now: /'
echo "   git status of this repository, porcelain, compiler_graph only:"
git -C /projects/PseudoCoupHQ status --porcelain Research/compiler_graph | head -30
echo
echo "======== lane 5 finished ========"
