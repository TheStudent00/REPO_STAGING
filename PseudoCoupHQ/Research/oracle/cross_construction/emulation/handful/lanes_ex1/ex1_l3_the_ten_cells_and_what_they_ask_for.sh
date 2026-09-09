#!/usr/bin/env bash
# ex1_l3_the_ten_cells_and_what_they_ask_for.sh -- task ex1, step 2:
# WHAT AN INTERPRETED RENDERER MUST BE ABLE TO SPELL, read off the ten
# cells themselves rather than guessed.
#
# The handful's ten cells are rebuilt exactly as the driver rebuilds
# them (`handful.cell_input`), and for every written place this lane
# prints: the place, its width, the arrival families it reads and the
# holder width the ONE renderer plans for each, the term LITERAL, and
# the multiset of z3 declaration kinds the term is built from.  The
# last is the list an interpreted renderer must cover; anything outside
# it is a refusal by cause and not a silent gap.
#
# It also asks php the one question its value model raises -- whether a
# 64-bit sum stays an integer -- and asks dart and csharp, whose runners
# are in the persist volume, the same value-model questions lane
# ex1_l2 asked the other five.
#
# MEMORY: one collecting process, bound 6 GB, named abort
# ABORT_MEMORY_EX1.  It reads the cells file (2 MB) and builds the
# pipeline's walk once.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful

echo "[1/4] the ten cells, place by place"
python3 - <<'PYEOF'
import collections
import os
import resource
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "..")
sys.path.insert(0, "../../../../op_pipeline")

import handful as H
import z3

H.use_task_ap4()
shared = H.build_shared()
cells = H.read_json(H.CELLS)
kinds = collections.Counter()
for asked in H.ASKED:
    held = H.cell_input(cells, asked)
    print("")
    print("== `%s` %s %d   row %s   line %r"
          % (asked[0], asked[1], asked[2], held.get("row_id"),
             held.get("line")))
    if held.get("refusal_cause") is not None:
        print("   REFUSED at the input: %s: %s"
              % (held["refusal_cause"], held.get("refusal_detail")))
        continue
    for place in held["places"]:
        print("   -- place %r   bits %s   families %s"
              % (place["writes"], place["bits"], place.get("families")))
        print("      term, LITERAL: %s" % place["text"])
        term = place.get("term")
        if term is None:
            continue
        here = collections.Counter()

        def walk(node):
            declaration = node.decl()
            here[declaration.name()] += 1
            for index in range(node.num_args()):
                walk(node.arg(index))

        walk(term)
        for name in sorted(here):
            kinds[name] += here[name]
        print("      the declarations it is built from: %s"
              % ", ".join("%s x%d" % (n, here[n]) for n in sorted(here)))
        if place.get("families") is None:
            continue
        planner = H.E.Renderer(place["families"], place["home"]["family"],
                               place["bits"], "probe")
        try:
            planner.plan_parameters(term)
        except H.E.Refused as refusal:
            print("      the ONE renderer refuses to plan it: %s: %s"
                  % (refusal.cause, refusal.detail))
            continue
        for param in planner.params:
            print("      arrival %s  family %-10s holder %-12s kind %-4s "
                  "bits %d" % (param["name"], param["family"],
                               param["holder"], param["kind"],
                               param["bits"]))
print("")
print("THE WHOLE VOCABULARY the ten cells ask for, over every place:")
for name in sorted(kinds):
    print("   %-24s x%d" % (name, kinds[name]))
print("")
print("   peak resident: %d kB"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PYEOF

echo ""
echo "[2/4] php's one question: does a 64-bit sum stay an integer?"
php -r '
function row($l, $s, $v) { printf("   %-40s %-46s -> %s\n", $l, $s, var_export($v, true)); }
$a = 0x7FFFFFFFFFFFFFFF; $b = 0x7FFFFFFFFFFFFFFF;
row("two 64-bit values added", "0x7FFF... + 0x7FFF...", $a + $b);
row("its type", "gettype(...)", gettype($a + $b));
$s = $a + $b;
row("masked back", "($a + $b) & -1", $s & -1);
row("the same add in two 32-bit halves", "see the source", (function($x, $y) {
    $lo = ($x & 0xFFFFFFFF) + ($y & 0xFFFFFFFF);
    $hi = (($x >> 32) & 0xFFFFFFFF) + (($y >> 32) & 0xFFFFFFFF) + (($lo >> 32) & 1);
    return (($hi & 0xFFFFFFFF) << 32) | ($lo & 0xFFFFFFFF);
})($a, $b));
row("gmp loaded", "extension_loaded(\"gmp\")", extension_loaded("gmp"));
row("bcmath loaded", "extension_loaded(\"bcmath\")", extension_loaded("bcmath"));
row("a 64-bit multiply", "0x123456789 * 0x123456789", 0x123456789 * 0x123456789);
row("its type", "gettype(...)", gettype(0x123456789 * 0x123456789));
row("a float32 round trip", "unpack(\"g\", pack(\"g\", 0.1))[1]", unpack("g", pack("g", 0.1))[1]);
' 2>&1 | head -20

echo ""
echo "[3/4] dart, its own value model"
cat > /tmp/probe.dart <<'DARTEOF'
import 'dart:typed_data';
void row(String label, String source, Object answer) {
  print("   ${label.padRight(34)} ${source.padRight(46)} -> $answer");
}
void main() {
  row("int wraps at 64", "0x7FFFFFFFFFFFFFFF + 1", 0x7FFFFFFFFFFFFFFF + 1);
  row("the mask to 32 bits", "-1 & 0xFFFFFFFF", -1 & 0xFFFFFFFF);
  row("arithmetic right shift", "-1 >> 1", -1 >> 1);
  row("unsigned right shift", "-1 >>> 1", -1 >>> 1);
  row("a shift count at the width", "1 << 64", 1 << 64);
  row("truncating division", "-7 ~/ 2", -7 ~/ 2);
  row("the remainder sign", "-7.remainder(2)", -7.remainder(2));
  row("the modulo", "-7 % 2", -7 % 2);
  var bytes = ByteData(8);
  bytes.setFloat32(0, 1.5, Endian.little);
  row("a float's bits", "ByteData setFloat32 / getUint32", bytes.getUint32(0, Endian.little));
  bytes.setFloat64(0, 1.5, Endian.little);
  row("a double's bits", "ByteData setFloat64 / getUint64", bytes.getUint64(0, Endian.little));
  try { print("   ${(7 ~/ 0)}"); } catch (problem) {
    row("division by zero", "7 ~/ 0", "raises ${problem.runtimeType}"); }
}
DARTEOF
/persist/dart-sdk/bin/dart run /tmp/probe.dart 2>&1 | head -15 || echo "   the runner's own answer is above"

echo ""
echo "[4/4] csharp, its own value model"
work=/work/ex1_l3_cs
rm -rf "$work"; mkdir -p "$work"
cat > "$work/probe.csx" <<'CSEOF'
CSEOF
mkdir -p "$work/proj"
cat > "$work/proj/proj.csproj" <<'CSPROJEOF'
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>disable</Nullable>
    <AssemblyName>probe</AssemblyName>
  </PropertyGroup>
</Project>
CSPROJEOF
cat > "$work/proj/Program.cs" <<'CSEOF'
using System;
class Program {
    static void Row(string label, string source, object answer) {
        Console.WriteLine("   " + label.PadRight(34) + " " +
                          source.PadRight(46) + " -> " + answer);
    }
    static void Main() {
        Row("int wraps", "unchecked(int.MaxValue + 1)", unchecked(int.MaxValue + 1));
        Row("long wraps", "unchecked(long.MaxValue + 1)", unchecked(long.MaxValue + 1));
        Row("the mask to 32 bits", "-1L & 0xFFFFFFFFL", -1L & 0xFFFFFFFFL);
        Row("arithmetic right shift", "-1 >> 1", -1 >> 1);
        Row("unsigned right shift", "-1 >>> 1", -1 >>> 1);
        Row("a shift count at the width", "1 << 32", 1 << 32);
        Row("truncating division", "-7 / 2", -7 / 2);
        Row("the remainder sign", "-7 % 2", -7 % 2);
        Row("unsigned division", "ulong.MaxValue / 3UL", ulong.MaxValue / 3UL);
        Row("a float's bits", "BitConverter.SingleToUInt32Bits(1.5f)", BitConverter.SingleToUInt32Bits(1.5f));
        Row("a double's bits", "BitConverter.DoubleToUInt64Bits(1.5)", BitConverter.DoubleToUInt64Bits(1.5));
        try { int q = 7; int z = 0; Row("division by zero", "7 / 0", q / z); }
        catch (Exception problem) { Row("division by zero", "7 / 0", "raises " + problem.GetType().Name); }
    }
}
CSEOF
export DOTNET_CLI_TELEMETRY_OPTOUT=1
export DOTNET_NOLOGO=1
export HOME=/work
( cd "$work/proj" && /persist/dotnet/dotnet run --no-restore 2>&1 | head -20 ) \
  || ( cd "$work/proj" && /persist/dotnet/dotnet run 2>&1 | head -20 ) \
  || echo "   the runner's own answer is above"
echo "done"
