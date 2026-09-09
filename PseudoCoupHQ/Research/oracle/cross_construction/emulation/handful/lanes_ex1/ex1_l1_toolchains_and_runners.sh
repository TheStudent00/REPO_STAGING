#!/usr/bin/env bash
# ex1_l1_toolchains_and_runners.sh -- task ex1, step 0: WHAT IS IN THE
# IMAGE.  Nothing is assumed about any runner: every one this task could
# use is asked for its own version string, and the literal answer -- a
# version, or the shell's own "No such file or directory" -- is the
# record.  A runner that is absent is a FLAG for the coordinator, per the
# brief; no workaround is attempted here or anywhere in this task.
#
# It also asks the cpp toolchain to compile one probe at the corpus's own
# ship flags (`lane_gen.py` compile_probe, cpp branch, LITERAL:
# `[CLANGXX, "-std=c++20"] + ["-O1"] + ["-c", src, "-o", obj]`) and
# carves it with the same objdump the pipeline uses, so the fifth
# compiled target is measured before a line of its renderer is written.
#
# MEMORY: this lane allocates nothing; it runs compilers and interpreters
# in separate short-lived processes.  Bound 6 GB, named abort
# ABORT_MEMORY_EX1, per the brief.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation

echo "[1/6] the compiled toolchains lane_gen.py names"
for probe in "/usr/bin/clang --version" "/usr/bin/clang++ --version" \
             "rustc --version" "go version" \
             "/persist/swift/usr/bin/swiftc --version"; do
    echo "--- \$ $probe"
    ( eval "$probe" 2>&1 | head -2 ) || echo "   (the command failed; the text above is the machine's own answer)"
done

echo ""
echo "[2/6] the interpreted runners this task could use"
for probe in "python3 --version" "php --version" "ruby --version" \
             "java --version" "javac --version" "node --version" \
             "dart --version" "dotnet --version" "kotlinc -version"; do
    echo "--- \$ $probe"
    ( eval "$probe" 2>&1 | head -2 ) || echo "   ABSENT: the text above is the machine's own answer"
done

echo ""
echo "[3/6] the persist volume, which is where the anchors live"
ls /persist 2>&1 | head -20 || true
echo "--- the interpreter ship builds the interp line names"
ls -d /persist/cpython_ship /persist/php_ship /persist/ruby_ship 2>&1 | head || true

echo ""
echo "[4/6] cpp at the corpus's own ship flags: one probe compiled and carved"
work=/work/ex1_l1
rm -rf "$work"; mkdir -p "$work"
cat > "$work/unit.cpp" <<'CPPEOF'
#include <cstdint>
extern "C" uint32_t emu_probe(uint32_t a, uint32_t b)
{
    return (uint32_t)(a + b);
}
CPPEOF
echo "--- the source, LITERAL:"
cat "$work/unit.cpp"
echo "--- \$ /usr/bin/clang++ -std=c++20 -O1 -c unit.cpp -o unit_ship.o"
/usr/bin/clang++ -std=c++20 -O1 -c "$work/unit.cpp" -o "$work/unit_ship.o" 2>&1 | head -5 || true
echo "--- \$ objdump -dr --disassemble=emu_probe unit_ship.o"
objdump -dr --disassemble=emu_probe "$work/unit_ship.o" 2>&1 | sed -n '1,40p' || true

echo ""
echo "[5/6] does cpp need extern \"C\"?  the name the symbol table carries, both ways"
cat > "$work/mangle.cpp" <<'CPPEOF'
#include <cstdint>
uint32_t plain_name(uint32_t a, uint32_t b) { return a + b; }
extern "C" uint32_t c_name(uint32_t a, uint32_t b) { return a + b; }
CPPEOF
/usr/bin/clang++ -std=c++20 -O1 -c "$work/mangle.cpp" -o "$work/mangle.o" 2>&1 | head -5 || true
objdump -t "$work/mangle.o" 2>&1 | grep -E "name" || true

echo ""
echo "[6/6] the corpus's own cpp rows: how many single-opcode units it holds"
python3 - <<'PYEOF'
import json
path = ("PseudoCoupHQ/Research/oracle/arch_opcodes/"
        "single_opcode_units.json")
document = json.load(open(path))
groups = document["single_opcode_groups"]
for language in sorted(groups.keys()):
    narrow = groups[language].get("narrow", {})
    print("   %-10s narrow groups %d" % (language, len(narrow)))
PYEOF
echo "done"
