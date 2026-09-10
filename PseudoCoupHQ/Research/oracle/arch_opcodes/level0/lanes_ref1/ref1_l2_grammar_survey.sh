#!/usr/bin/env bash
# ref1 lane 2 -- the survey the parser's grammar must cover: every identifier
# that appears in an application position across all 3,098 rule files, every
# left-hand place a rule writes, every operand-list suffix a file name spells,
# and the sort annotations the rule heads carry.  Nothing is copied out of
# /sources; only counts and identifier names are printed.
set -euo pipefail
S=/sources/X86-64-semantics/semantics
total=8

echo "[1/$total] every identifier followed by '(' -- the function vocabulary, with counts"
grep -ho '[A-Za-z#][A-Za-z0-9_#]*[[:space:]]*(' $S/*/*.k \
  | tr -d ' (' | sort | uniq -c | sort -rn

echo "[2/$total] every infix word operator"
grep -ho '\b[a-zA-Z]*Bool\b\|==Bool\|=/=Bool\|#then\|#else\|#fi\|#ifMInt\|#ifBool' $S/*/*.k \
  | sort | uniq -c | sort -rn

echo "[3/$total] the places a rule writes: the left of |->"
grep -ho '[^ ,(]*[[:space:]]*|->' $S/*/*.k | sed 's/[[:space:]]*|->//' | sort | uniq -c | sort -rn | head -40

echo "[4/$total] the cells a rule updates"
grep -ho '<[a-zA-Z]*>' $S/*/*.k | sort | uniq -c | sort -rn | head -30

echo "[5/$total] the operand-list suffixes the file names spell, by folder"
for d in registerInstructions immediateInstructions memoryInstructions mmx systemInstructions pseudoTestInstructions extras; do
  echo "--- $d"
  ls $S/$d 2>/dev/null | sed 's/\.k$//' | sed 's/^[a-z0-9]*_//' | sort | uniq -c | sort -rn | head -40
done

echo "[6/$total] the sort annotations on rule-head variables"
grep -ho ':[A-Za-z][A-Za-z0-9]*' $S/*/*.k | sort | uniq -c | sort -rn | head -40

echo "[7/$total] the execinstr head shapes, deduplicated"
grep -ho 'execinstr *([^)]*)' $S/*/*.k | sed 's/[A-Z][0-9]*:/V:/g' | sed 's/execinstr *(//' | sort | uniq -c | sort -rn | head -60

echo "[8/$total] files whose body mentions undefMInt or undefBool"
echo "undefMInt files: $(grep -l 'undefMInt' $S/*/*.k | wc -l)"
echo "undefBool files: $(grep -l 'undefBool' $S/*/*.k | wc -l)"
echo "files with more than one rule: $(for f in $S/*/*.k; do n=$(grep -c '^  rule' $f); [ "$n" -gt 1 ] && echo $f; done | wc -l)"
