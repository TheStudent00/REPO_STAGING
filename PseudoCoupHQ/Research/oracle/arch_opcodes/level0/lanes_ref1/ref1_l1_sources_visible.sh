#!/usr/bin/env bash
# ref1 lane 1 -- confirm the third-party K semantics are visible inside the
# lane at /sources, print the licence, count the rule files by folder, and
# show two whole rule files so the grammar can be written from the objects.
set -euo pipefail
total=6

echo "[1/$total] the mount"
ls -la /sources/ | head -20
echo "--- X86-64-semantics:"
ls /sources/X86-64-semantics/

echo "[2/$total] the licence, whole"
cat /sources/X86-64-semantics/LICENSE.md

echo "[3/$total] the rule files, by folder"
S=/sources/X86-64-semantics/semantics
for d in registerInstructions immediateInstructions memoryInstructions mmx pseudoTestInstructions systemInstructions extras common; do
    printf '%-26s %6d files\n' "$d" "$(ls $S/$d 2>/dev/null | wc -l)"
done
echo "total .k under semantics/: $(find $S -name '*.k' | wc -l)"

echo "[4/$total] one register rule file whole"
cat $S/registerInstructions/subl_r32_r32.k

echo "[5/$total] one shift rule file whole"
cat $S/registerInstructions/shrq_cl_r64.k

echo "[6/$total] the python and z3 the instance has"
python3 -c "import z3, sys; print(sys.version.split()[0], 'z3', z3.get_version_string())"
