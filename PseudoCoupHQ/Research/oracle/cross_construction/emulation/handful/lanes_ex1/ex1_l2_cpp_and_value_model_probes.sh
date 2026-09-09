#!/usr/bin/env bash
# ex1_l2_cpp_and_value_model_probes.sh -- task ex1, step 1: MEASUREMENT
# BEFORE A SPELLING IS WRITTEN, task o11 section 3.1's rule, applied to
# the two expansions this task makes.
#
# PART A, cpp: what cpp spells differently from c at the holders the
# renderer uses.  The strongest measurement available is the corpus's
# own: every c source task ap4's loop rendered (309 of them under
# `autopoly/src4/`) handed to clang++ at the corpus's own cpp ship
# flags, verbatim and then with one line changed, and the failures
# counted and named.  Beside it, one probe per holder that could differ
# (`unsigned __int128`, `_Float16`, `long double`, the `UINT32_C`
# macros, `static_cast`).
#
# PART B, the interpreted languages: each one's own VALUE MODEL, asked
# of the runner rather than read out of a manual.  Whether the integer
# is unbounded, what happens at the width boundary, which way division
# rounds, what a shift count above the width does, and how a float's
# bits are reached.  Every probe prints its own source and the answer
# the runner gave.
#
# MEMORY: this lane allocates nothing of its own; every probe is a
# separate short-lived process.  Bound 6 GB, named abort
# ABORT_MEMORY_EX1.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation
work=/work/ex1_l2
rm -rf "$work"; mkdir -p "$work"

echo "[1/9] PART A -- the corpus's own c sources handed to clang++, verbatim"
python3 - <<'PYEOF'
import os
import re
import subprocess

SRC = ("PseudoCoupHQ/Research/oracle/cross_construction/"
       "emulation/autopoly/src4")
WORK = "/work/ex1_l2/cpp_verbatim"
os.makedirs(WORK, exist_ok=True)
names = sorted(name for name in os.listdir(SRC) if name.endswith(".c"))
print("   c sources task ap4's loop rendered: %d" % len(names))
ok = 0
bad = {}
symbols_mangled = 0
for name in names:
    source = open(os.path.join(SRC, name)).read()
    path = os.path.join(WORK, name + "pp")
    handle = open(path, "w")
    handle.write(source)
    handle.close()
    obj = path + ".o"
    done = subprocess.run(
        ["/usr/bin/clang++", "-std=c++20", "-O1", "-c", path, "-o", obj],
        capture_output=True, text=True, timeout=180)
    if done.returncode != 0:
        first = "(no diagnostic)"
        for line in (done.stderr or done.stdout).splitlines():
            if "error" in line:
                first = line.strip()
                break
        key = re.sub(r"^[^ ]*:\d+:\d+: ", "", first)
        bad.setdefault(key, []).append(name)
        continue
    ok = ok + 1
    match = re.search(r"^emu_(\w+)$", "", re.M)
    symbol = None
    for line in source.splitlines():
        found = re.match(r"^(emu_\w+)\(", line)
        if found:
            symbol = found.group(1)
    table = subprocess.run(["objdump", "-t", obj], capture_output=True,
                           text=True, timeout=180)
    if symbol is not None and symbol not in table.stdout:
        symbols_mangled = symbols_mangled + 1
print("   compiled by clang++ VERBATIM: %d of %d" % (ok, len(names)))
print("   of those, whose c symbol name is ABSENT from the object's "
      "symbol table (the name was mangled): %d" % symbols_mangled)
print("   refused, by the compiler's own first error line:")
for key in sorted(bad, key=lambda k: -len(bad[k])):
    print("      %4d  %s" % (len(bad[key]), key))
    print("            first: %s" % bad[key][0])
PYEOF

echo ""
echo "[2/9] PART A -- the same sources with the one line an unmangled symbol needs"
python3 - <<'PYEOF'
import os
import re
import subprocess

SRC = ("PseudoCoupHQ/Research/oracle/cross_construction/"
       "emulation/autopoly/src4")
WORK = "/work/ex1_l2/cpp_externc"
os.makedirs(WORK, exist_ok=True)
names = sorted(name for name in os.listdir(SRC) if name.endswith(".c"))
ok = 0
carved = 0
bad = {}
first_shown = False
for name in names:
    source = open(os.path.join(SRC, name)).read()
    symbol = None
    lines = source.splitlines()
    for index, line in enumerate(lines):
        found = re.match(r"^(emu_\w+)\(", line)
        if found:
            symbol = found.group(1)
            lines.insert(index - 1, 'extern "C"')
            break
    text = "\n".join(lines) + "\n"
    if not first_shown:
        print("   THE ONE LINE, on the first source, LITERAL:")
        for line in text.splitlines()[:12]:
            print("      %s" % line)
        first_shown = True
    path = os.path.join(WORK, name + "pp")
    handle = open(path, "w")
    handle.write(text)
    handle.close()
    obj = path + ".o"
    done = subprocess.run(
        ["/usr/bin/clang++", "-std=c++20", "-O1", "-c", path, "-o", obj],
        capture_output=True, text=True, timeout=180)
    if done.returncode != 0:
        first = "(no diagnostic)"
        for line in (done.stderr or done.stdout).splitlines():
            if "error" in line:
                first = line.strip()
                break
        key = re.sub(r"^[^ ]*:\d+:\d+: ", "", first)
        bad.setdefault(key, []).append(name)
        continue
    ok = ok + 1
    table = subprocess.run(["objdump", "-t", obj], capture_output=True,
                           text=True, timeout=180)
    if symbol is not None and symbol in table.stdout:
        carved = carved + 1
print("   compiled by clang++ with `extern \"C\"`: %d of %d"
      % (ok, len(names)))
print("   whose c symbol name IS in the object's symbol table: %d"
      % carved)
print("   refused, by the compiler's own first error line:")
for key in sorted(bad, key=lambda k: -len(bad[k])):
    print("      %4d  %s" % (len(bad[key]), key))
    print("            first: %s" % bad[key][0])
PYEOF

echo ""
echo "[3/9] PART A -- one probe per holder that could differ"
run_cpp() {   # $1 = a label, then the source on stdin
    name="$1"
    cat > "$work/$name.cpp"
    echo "--- $name, LITERAL:"
    sed 's/^/      /' "$work/$name.cpp"
    echo "    \$ /usr/bin/clang++ -std=c++20 -O1 -c $name.cpp"
    if /usr/bin/clang++ -std=c++20 -O1 -c "$work/$name.cpp" \
            -o "$work/$name.o" 2>"$work/$name.err"; then
        echo "      ACCEPTED"
        objdump -dr --disassemble=probe "$work/$name.o" 2>/dev/null \
            | sed -n '/>:/,$p' | sed -n '2,12p' | sed 's/^/      /' || true
    else
        echo "      REFUSED, the compiler's own words:"
        head -3 "$work/$name.err" | sed 's/^/      /'
    fi
}

run_cpp holder_u128 <<'CPPEOF'
#include <cstdint>
extern "C" unsigned __int128 probe(unsigned __int128 a) { return a + 1; }
CPPEOF

run_cpp holder_f16 <<'CPPEOF'
#include <cstdint>
extern "C" _Float16 probe(_Float16 a) { return (_Float16)(a + a); }
CPPEOF

run_cpp holder_long_double <<'CPPEOF'
#include <cstdint>
extern "C" long double probe(long double a, long double b) { return a + b; }
CPPEOF

run_cpp macro_uint32_c <<'CPPEOF'
#include <cstdint>
extern "C" uint32_t probe(uint32_t a) { return a & UINT32_C(0xffffffff); }
CPPEOF

run_cpp cstdint_unqualified <<'CPPEOF'
#include <cstdint>
extern "C" uint64_t probe(uint64_t a, int64_t b) { return a + (uint64_t)b; }
CPPEOF

run_cpp memcpy_helper <<'CPPEOF'
#include <cstdint>
#include <cstring>
static inline uint32_t f32_to_bits(float f) { uint32_t b; memcpy(&b, &f, 4); return b; }
extern "C" uint32_t probe(float a) { return f32_to_bits(a); }
CPPEOF

run_cpp c_style_cast_chain <<'CPPEOF'
#include <cstdint>
extern "C" uint32_t probe(uint32_t a, uint32_t b)
{ return (uint32_t)(((int32_t)((uint32_t)a << 0) >> 0) + (int32_t)b); }
CPPEOF

echo ""
echo "[4/9] PART B -- python3, its own value model"
python3 - <<'PYEOF'
import struct
rows = [
    ("the integer is unbounded", "2 ** 64", 2 ** 64),
    ("the mask to 32 bits", "(2**64 - 1) & 0xFFFFFFFF",
     (2 ** 64 - 1) & 0xFFFFFFFF),
    ("a right shift of a negative", "(-1) >> 1", (-1) >> 1),
    ("a shift count at the width", "1 << 64", 1 << 64),
    ("a shift count above the width", "1 << 65", 1 << 65),
    ("division rounds", "(-7) // 2", (-7) // 2),
    ("the remainder's sign", "(-7) % 2", (-7) % 2),
    ("truncating division, spelled", "-(7 // 2)", -(7 // 2)),
    ("a float's bits", "struct.unpack('<I', struct.pack('<f', 1.5))[0]",
     struct.unpack("<I", struct.pack("<f", 1.5))[0]),
    ("a double's bits", "struct.unpack('<Q', struct.pack('<d', 1.5))[0]",
     struct.unpack("<Q", struct.pack("<d", 1.5))[0]),
    ("bits back to a float", "struct.unpack('<f', struct.pack('<I', 1069547520))[0]",
     struct.unpack("<f", struct.pack("<I", 1069547520))[0]),
]
for label, source, answer in rows:
    print("   %-34s %-52s -> %s" % (label, source, answer))
try:
    7 // 0
except Exception as problem:
    print("   %-34s %-52s -> raises %s"
          % ("division by zero", "7 // 0", type(problem).__name__))
PYEOF

echo ""
echo "[5/9] PART B -- php, its own value model"
php -r '
$rows = array(
  array("the integer width", "PHP_INT_SIZE", PHP_INT_SIZE),
  array("at the width boundary", "PHP_INT_MAX + 1", PHP_INT_MAX + 1),
  array("its type there", "gettype(PHP_INT_MAX + 1)", gettype(PHP_INT_MAX + 1)),
  array("the mask to 32 bits", "-1 & 0xFFFFFFFF", -1 & 0xFFFFFFFF),
  array("a right shift of a negative", "-1 >> 1", -1 >> 1),
  array("a shift count at the width", "1 << 64", 1 << 64),
  array("division rounds", "intdiv(-7, 2)", intdiv(-7, 2)),
  array("the / operator", "-7 / 2", -7 / 2),
  array("its type", "gettype(-7 / 2)", gettype(-7 / 2)),
  array("the remainder sign", "-7 % 2", -7 % 2),
  array("a float bits", "unpack(\"V\", pack(\"g\", 1.5))[1]", unpack("V", pack("g", 1.5))[1]),
  array("a double bits", "unpack(\"P\", pack(\"e\", 1.5))[1]", unpack("P", pack("e", 1.5))[1]),
  array("bits back to a float", "unpack(\"g\", pack(\"V\", 1069547520))[1]", unpack("g", pack("V", 1069547520))[1]),
  array("multiply at the boundary", "PHP_INT_MAX * 2", PHP_INT_MAX * 2),
);
foreach ($rows as $r) { printf("   %-34s %-52s -> %s\n", $r[0], $r[1], var_export($r[2], true)); }
try { intdiv(7, 0); } catch (Throwable $t) { printf("   %-34s %-52s -> raises %s\n", "division by zero", "intdiv(7, 0)", get_class($t)); }
' 2>&1 | head -30

echo ""
echo "[6/9] PART B -- ruby, its own value model"
ruby -e '
rows = [
  ["the integer is unbounded", "2 ** 64", 2 ** 64],
  ["the mask to 32 bits", "-1 & 0xFFFFFFFF", -1 & 0xFFFFFFFF],
  ["a right shift of a negative", "-1 >> 1", -1 >> 1],
  ["a shift count at the width", "1 << 64", 1 << 64],
  ["division rounds", "-7 / 2", -7 / 2],
  ["the remainder sign", "-7 % 2", -7 % 2],
  ["truncating division, spelled", "-7.fdiv(2).truncate", -7.fdiv(2).truncate],
  ["a float bits", "[1.5].pack(\"e\").unpack1(\"V\")", [1.5].pack("e").unpack1("V")],
  ["a double bits", "[1.5].pack(\"E\").unpack1(\"Q<\")", [1.5].pack("E").unpack1("Q<")],
  ["bits back to a float", "[1069547520].pack(\"V\").unpack1(\"e\")", [1069547520].pack("V").unpack1("e")],
]
rows.each { |r| printf("   %-34s %-52s -> %s\n", r[0], r[1], r[2].inspect) }
begin; 7 / 0; rescue => e; printf("   %-34s %-52s -> raises %s\n", "division by zero", "7 / 0", e.class); end
' 2>&1 | head -20

echo ""
echo "[7/9] PART B -- java, its own value model"
mkdir -p "$work/java"
cat > "$work/java/Probe.java" <<'JAVAEOF'
public class Probe {
    static void row(String label, String source, Object answer) {
        System.out.printf("   %-34s %-52s -> %s%n", label, source, answer);
    }
    public static void main(String[] args) {
        row("int wraps", "Integer.MAX_VALUE + 1", Integer.MAX_VALUE + 1);
        row("long wraps", "Long.MAX_VALUE + 1L", Long.MAX_VALUE + 1L);
        row("the mask to 32 bits", "-1L & 0xFFFFFFFFL", -1L & 0xFFFFFFFFL);
        row("arithmetic right shift", "-1 >> 1", -1 >> 1);
        row("logical right shift", "-1 >>> 1", -1 >>> 1);
        row("a shift count at the width", "1 << 32", 1 << 32);
        row("a long shift count at 64", "1L << 64", 1L << 64);
        row("division truncates", "-7 / 2", -7 / 2);
        row("the remainder sign", "-7 % 2", -7 % 2);
        row("signed overflow of division", "Integer.MIN_VALUE / -1", Integer.MIN_VALUE / -1);
        row("unsigned division", "Long.divideUnsigned(-1L, 3L)", Long.divideUnsigned(-1L, 3L));
        row("unsigned remainder", "Long.remainderUnsigned(-1L, 3L)", Long.remainderUnsigned(-1L, 3L));
        row("unsigned compare", "Long.compareUnsigned(-1L, 1L)", Long.compareUnsigned(-1L, 1L));
        row("a float's bits", "Float.floatToRawIntBits(1.5f)", Float.floatToRawIntBits(1.5f));
        row("a double's bits", "Double.doubleToRawLongBits(1.5)", Double.doubleToRawLongBits(1.5));
        row("bits back to a float", "Float.intBitsToFloat(1069547520)", Float.intBitsToFloat(1069547520));
        try { int q = 7 / 0; row("division by zero", "7 / 0", q); }
        catch (Throwable t) { row("division by zero", "7 / 0", "raises " + t.getClass().getName()); }
    }
}
JAVAEOF
echo "   \$ java Probe.java   (the single-file source launcher)"
( cd "$work/java" && java Probe.java 2>&1 | head -20 ) || echo "   the runner's own answer is above"

echo ""
echo "[8/9] PART B -- node (javascript), its own value model"
cat > "$work/probe.js" <<'JSEOF'
function row(label, source, answer) {
    console.log("   " + label.padEnd(34) + " " + source.padEnd(52) +
                " -> " + String(answer));
}
row("BigInt is unbounded", "2n ** 64n", 2n ** 64n);
row("the mask to 32 bits", "BigInt.asUintN(32, -1n)", BigInt.asUintN(32, -1n));
row("the signed reading", "BigInt.asIntN(32, 0xFFFFFFFFn)", BigInt.asIntN(32, 0xFFFFFFFFn));
row("a right shift of a negative", "(-1n) >> 1n", (-1n) >> 1n);
row("a shift count at the width", "1n << 64n", 1n << 64n);
row("division truncates", "(-7n) / 2n", (-7n) / 2n);
row("the remainder sign", "(-7n) % 2n", (-7n) % 2n);
const view = new DataView(new ArrayBuffer(8));
view.setFloat32(0, 1.5, true);
row("a float's bits", "DataView setFloat32 / getUint32", view.getUint32(0, true));
view.setFloat64(0, 1.5, true);
row("a double's bits", "DataView setFloat64 / getBigUint64", view.getBigUint64(0, true));
view.setUint32(0, 1069547520, true);
row("bits back to a float", "DataView setUint32 / getFloat32", view.getFloat32(0, true));
try { const q = 1n / 0n; row("division by zero", "1n / 0n", q); }
catch (problem) { row("division by zero", "1n / 0n", "raises " + problem.name); }
JSEOF
node "$work/probe.js" 2>&1 | head -20 || echo "   the runner's own answer is above"

echo ""
echo "[9/9] the two runners that are not on PATH: are they in the persist volume?"
for probe in "/persist/dart-sdk/bin/dart --version" \
             "/persist/dotnet/dotnet --version" \
             "/persist/kotlinc/bin/kotlinc -version"; do
    echo "--- \$ $probe"
    ( eval "$probe" 2>&1 | head -2 ) || echo "   the machine's own answer is above"
done
ls /persist/dart-sdk/bin 2>&1 | head -5 || true
ls /persist/dotnet 2>&1 | head -5 || true
echo "done"
