#!/bin/sh
# JIT track -- JVM pilot, LANE A: the warm-up recipe and the dump.
#
# What the smoke lane established, and why this lane is shaped as it is:
#   * no hsdis ships with this JDK, and no dis-asm.h / autoconf exist
#     in the container, so Plan B (build hsdis) has no ingredients.
#   * BUT: -XX:CompileCommand=print,Class::method still prints the
#     nmethod's MACHINE CODE BYTES in hex, with the JVM's own
#     annotations ({poll_return}, {runtime_call ...}), plus the
#     parameter-register comments.  Only the mnemonics are missing.
#   * so this lane takes those bytes and disassembles them with
#     objdump (-b binary -m i386:x86-64).  Bytes are the JVM's own
#     testimony; mnemonics are objdump's reading of those bytes.
#     Both facts are recorded separately, never merged.
#
# Configuration choice for the RECORDED unit: -XX:-TieredCompilation,
# i.e. C2 only, final tier, no C1 profiling stub in the way.
set -u
echo "=== jvm_a_dump ==="
date -u +%Y-%m-%dT%H:%M:%SZ

W=/work/jvm
rm -rf "$W"; mkdir -p "$W"
cd "$W" || exit 4
O=/out/jvm_a
rm -rf "$O"; mkdir -p "$O"

echo "--- pin ---"
java -version 2>&1
java -XshowSettings:properties -version 2>&1 | grep -Ei \
  'java.vendor =|java.version =|java.vm.name|java.vm.version|os.arch'

echo ""
echo "--- the thresholds this JVM reports about itself ---"
java -XX:+PrintFlagsFinal -version 2>&1 | grep -Ei \
  'CompileThreshold|Tier[0-9]+InvocationThreshold|TieredCompilation|BackEdgeThreshold' \
  | sed 's/  */ /g'

echo ""
echo "--- is PrintOptoAssembly (Plan C) available in this product build? ---"
java -XX:+UnlockDiagnosticVMOptions -XX:+PrintOptoAssembly -version 2>&1 | head -5
echo "(exit above tells whether the flag exists)"

# ---------------------------------------------------------------- probes
cat > Probe.java <<'EOF'
public class Probe {
    static int af(int a, int b) {
        return a + b;
    }
    static int af2(int a, int b) {
        return a / b;
    }
    static int sink;
    public static void main(String[] args) {
        int n = Integer.parseInt(args[0]);
        long t0 = System.nanoTime();
        int acc = 0;
        int i = 0;
        while (i < n) {
            acc = af(acc, 1);
            i = i + 1;
        }
        int acc2 = 0;
        int j = 1;
        while (j < n) {
            acc2 = af2(j, 3);
            j = j + 1;
        }
        long t1 = System.nanoTime();
        sink = acc + acc2;
        long ms = (t1 - t0) / 1000000L;
        System.out.println("WARMED n=" + n + " acc=" + acc
                           + " acc2=" + acc2 + " ms=" + ms);
    }
}
EOF
javac Probe.java 2>&1
echo "javac exit=$?"
cp Probe.java "$O/Probe.java"

echo ""
echo "--- javap -c -p Probe (bytecode middle form) ---"
javap -c -p Probe 2>&1 | tee "$O/javap_c.txt"

# ------------------------------------------------- the warm-up sweep
echo ""
echo "######## warm-up sweep : how many calls until C2 takes af? ########"
echo "# configuration: -XX:-TieredCompilation (C2 only)"
: > "$O/warmup_sweep.txt"
for N in 1 10 100 500 1000 2000 5000 10000 20000 50000 200000; do
  T0=`date +%s.%N`
  OUT=`java -XX:-TieredCompilation -XX:+PrintCompilation Probe $N 2>&1`
  T1=`date +%s.%N`
  WALL=`echo "$T1 $T0" | awk '{printf "%.2f", $1-$2}'`
  HITAF=`echo "$OUT" | grep -c 'Probe::af (4 bytes)'`
  HITAF2=`echo "$OUT" | grep -c 'Probe::af2 (4 bytes)'`
  HITOSR=`echo "$OUT" | grep -c 'Probe::main @'`
  LINE="n=$N wall=${WALL}s  af_compiled=$HITAF  af2_compiled=$HITAF2  main_osr=$HITOSR"
  echo "$LINE"
  echo "$LINE" >> "$O/warmup_sweep.txt"
  echo "$OUT" | grep -E 'Probe::' >> "$O/warmup_sweep.txt"
  echo "$OUT" | grep -E '^WARMED' >> "$O/warmup_sweep.txt"
  echo "" >> "$O/warmup_sweep.txt"
done

echo ""
echo "--- the Probe:: tier-transition lines, default tiers, n=200000 ---"
java -XX:+PrintCompilation Probe 200000 2>&1 | grep -E 'Probe::' \
  | tee "$O/tiers_default.txt"

echo ""
echo "--- the Probe:: tier-transition lines, -XX:-TieredCompilation, n=200000 ---"
java -XX:-TieredCompilation -XX:+PrintCompilation Probe 200000 2>&1 \
  | grep -E 'Probe::' | tee "$O/tiers_c2only.txt"

# ------------------------------------------------------- the dump run
echo ""
echo "######## the dump: C2-only, -Xbatch, print af and af2 ########"
T0=`date +%s.%N`
java -Xbatch -XX:-TieredCompilation \
  -XX:+UnlockDiagnosticVMOptions \
  -XX:CompileCommand=print,Probe::af \
  -XX:CompileCommand=print,Probe::af2 \
  -XX:CompileCommand=dontinline,Probe::af \
  -XX:CompileCommand=dontinline,Probe::af2 \
  Probe 200000 > "$O/dump_raw.txt" 2>&1
T1=`date +%s.%N`
echo "dump exit=$?  wall=`echo "$T1 $T0" | awk '{printf "%.2f", $1-$2}'`s"
echo "dump_raw.txt lines: `wc -l < "$O/dump_raw.txt"`"
echo "--- head of dump_raw.txt ---"
head -60 "$O/dump_raw.txt"

# ------------------------------------------- bytes -> objdump mnemonics
cat > carve.py <<'PYEOF'
import json
import re
import subprocess
import sys

path = sys.argv[1]
outjson = sys.argv[2]

text = open(path, errors="replace").read()
lines = text.split("\n")

# an nmethod block starts at the "Compiled method (cN) ... Class::name" line
start_re = re.compile(r"^Compiled method \((\w+)\)\s+(.*)$")
byte_re = re.compile(r"^\s*(0x[0-9a-f]+):\s+([0-9a-f]{2,8}(?:\s*\|\s*[0-9a-f]{2,8})*)\s*$")
note_re = re.compile(r"^\s*(0x[0-9a-f]+):\s*;\s*(.*?)\s*$")
sect_re = re.compile(r"^\s*\[([^\]]+)\]\s*$")
parm_re = re.compile(r"^\s*#\s+(parm\d+|\[sp.*|\{method\}.*)")

blocks = []
cur = None
for ln in lines:
    m = start_re.match(ln)
    if m is not None:
        cur = {}
        cur["compiler"] = m.group(1)
        cur["header"] = m.group(2).strip()
        cur["bytes"] = []
        cur["notes"] = []
        cur["sections"] = []
        cur["comments"] = []
        cur["raw"] = []
        blocks.append(cur)
        continue
    if cur is None:
        continue
    cur["raw"].append(ln)
    m = sect_re.match(ln)
    if m is not None:
        cur["sections"].append(m.group(1))
    m = parm_re.match(ln)
    if m is not None:
        cur["comments"].append(ln.strip())
    m = note_re.match(ln)
    if m is not None:
        cur["notes"].append([m.group(1), m.group(2)])
        continue
    m = byte_re.match(ln)
    if m is not None:
        addr = int(m.group(1), 16)
        groups = m.group(2).split("|")
        hexs = ""
        for g in groups:
            hexs = hexs + g.strip()
        cur["bytes"].append([addr, hexs])
        continue

def assemble(blk):
    """the byte stream in address order, deduped."""
    seen = {}
    for addr, hexs in blk["bytes"]:
        n = 0
        while n * 2 < len(hexs):
            b = hexs[n * 2:n * 2 + 2]
            seen[addr + n] = b
            n = n + 1
    keys = sorted(seen.keys())
    return keys, seen

def disasm(blk):
    keys, seen = assemble(blk)
    if not keys:
        return None, []
    base = keys[0]
    raw = bytearray()
    prev = None
    for k in keys:
        if prev is not None and k != prev + 1:
            # a hole; stop at the first discontinuity, honestly
            break
        raw.append(int(seen[k], 16))
        prev = k
    open("/work/jvm/blob.bin", "wb").write(bytes(raw))
    cmd = ["objdump", "-D", "-b", "binary", "-m", "i386:x86-64",
           "-M", "att", "--adjust-vma=0x%x" % base, "/work/jvm/blob.bin"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return base, p.stdout.split("\n")

out = {}
out["blocks"] = []
for blk in blocks:
    base, dis = disasm(blk)
    rec = {}
    rec["compiler"] = blk["compiler"]
    rec["header"] = blk["header"]
    rec["sections"] = blk["sections"]
    rec["comments"] = blk["comments"]
    rec["annotations"] = blk["notes"]
    rec["byte_lines"] = blk["bytes"]
    rec["objdump"] = dis
    out["blocks"].append(rec)

json.dump(out, open(outjson, "w"), indent=1)

for blk in out["blocks"]:
    print("")
    print("################ %s ################" % blk["header"])
    print("compiler=%s sections=%s" % (blk["compiler"], blk["sections"]))
    for c in blk["comments"]:
        print("  %s" % c)
    print("  --- the JVM's own annotations ---")
    for a, t in blk["annotations"]:
        print("    %s  %s" % (a, t))
    print("  --- objdump's reading of the printed bytes ---")
    for ln in blk["objdump"]:
        if ln.strip():
            print("    %s" % ln)
PYEOF

echo ""
echo "######## carving the printed bytes and disassembling ########"
python3 carve.py "$O/dump_raw.txt" "$O/nmethods.json" \
  > "$O/carved.txt" 2>&1
echo "carve exit=$?"
cat "$O/carved.txt"

echo ""
echo "--- deopt / uncommon-trap mentions anywhere in the dump ---"
grep -nEi 'uncommon|deopt|trap|implicit|exception' "$O/dump_raw.txt" \
  | head -60 | tee "$O/deopt_mentions.txt"

echo "=== jvm_a_dump done ==="
date -u +%Y-%m-%dT%H:%M:%SZ
