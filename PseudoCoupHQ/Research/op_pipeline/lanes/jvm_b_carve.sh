#!/bin/sh
# JIT track -- JVM pilot, LANE B: repair of lane A's carver.
#
# Lane A captured the JVM's annotations correctly but produced an EMPTY
# objdump listing.  Cause, found by reading the printed line back:
#   0x00007e6f08eab880: 4881 ec18 | 0000 0048 | 896c 2410 | ...
# the bar-separated groups are each FOUR hex digits with a SPACE in the
# middle ("4881 ec18"), and lane A's pattern required each group to be
# an unbroken hex run.  Nothing matched, so no bytes, so no blob, so no
# disassembly.  This lane takes every hex token after the colon instead.
#
# It also prints the FULL raw dump into the log, so the af2 block is
# visible in full rather than only in its first lines.
set -u
echo "=== jvm_b_carve ==="
date -u +%Y-%m-%dT%H:%M:%SZ

W=/work/jvmb
rm -rf "$W"; mkdir -p "$W"
cd "$W" || exit 4
O=/out/jvm_b
rm -rf "$O"; mkdir -p "$O"

cp /out/jvm_a/Probe.java .
javac Probe.java 2>&1
echo "javac exit=$?"

echo ""
echo "######## the dump: C2 only, -Xbatch, dontinline, print af + af2 ########"
java -Xbatch -XX:-TieredCompilation \
  -XX:+UnlockDiagnosticVMOptions \
  -XX:CompileCommand=print,Probe::af \
  -XX:CompileCommand=print,Probe::af2 \
  -XX:CompileCommand=dontinline,Probe::af \
  -XX:CompileCommand=dontinline,Probe::af2 \
  Probe 200000 > "$O/dump_raw.txt" 2>&1
echo "dump exit=$?  lines=`wc -l < "$O/dump_raw.txt"`"

echo ""
echo "######## THE RAW DUMP, IN FULL ########"
cat "$O/dump_raw.txt"

cat > carve.py <<'PYEOF'
import json
import re
import subprocess
import sys

path = sys.argv[1]
outjson = sys.argv[2]

lines = open(path, errors="replace").read().split("\n")

start_re = re.compile(r"^Compiled method \((\w+)\)\s+(.*)$")
addr_re = re.compile(r"^\s*(0x[0-9a-f]+):\s*(.*)$")
hex_re = re.compile(r"^[0-9a-f]+$")
sect_re = re.compile(r"^\s*\[([^\]]+)\]\s*$")
comment_re = re.compile(r"^\s*#\s+\S")

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
        blocks.append(cur)
        continue
    if cur is None:
        continue
    m = sect_re.match(ln)
    if m is not None:
        cur["sections"].append(m.group(1))
        continue
    if comment_re.match(ln) is not None:
        cur["comments"].append(ln.strip())
        continue
    m = addr_re.match(ln)
    if m is None:
        continue
    addr = int(m.group(1), 16)
    rest = m.group(2).strip()
    if rest.startswith(";"):
        cur["notes"].append([m.group(1), rest.lstrip("; ").strip()])
        continue
    toks = []
    for t in rest.replace("|", " ").split():
        if hex_re.match(t) is not None:
            toks.append(t)
    if not toks:
        continue
    hexs = "".join(toks)
    if len(hexs) % 2 != 0:
        continue
    cur["bytes"].append([addr, hexs])


def assemble(blk):
    seen = {}
    for addr, hexs in blk["bytes"]:
        n = 0
        while n * 2 < len(hexs):
            b = hexs[n * 2:n * 2 + 2]
            seen[addr + n] = b
            n = n + 1
    return seen


def contiguous_runs(seen):
    keys = sorted(seen.keys())
    runs = []
    cur = None
    prev = None
    for k in keys:
        if cur is None or k != prev + 1:
            cur = [k, bytearray()]
            runs.append(cur)
        cur[1].append(int(seen[k], 16))
        prev = k
    return runs


def disasm(base, raw):
    open("blob.bin", "wb").write(bytes(raw))
    cmd = ["objdump", "-D", "-b", "binary", "-m", "i386:x86-64",
           "-M", "att", "--adjust-vma=0x%x" % base, "blob.bin"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    out = []
    for ln in p.stdout.split("\n"):
        if ":\t" in ln:
            out.append(ln.rstrip())
    if not out:
        out.append("!! objdump produced nothing; stderr: %s"
                   % p.stderr.strip()[:400])
    return out


out = {}
out["blocks"] = []
for blk in blocks:
    seen = assemble(blk)
    runs = contiguous_runs(seen)
    rec = {}
    rec["compiler"] = blk["compiler"]
    rec["header"] = blk["header"]
    rec["sections"] = blk["sections"]
    rec["comments"] = blk["comments"]
    rec["annotations"] = blk["notes"]
    rec["byte_lines"] = blk["bytes"]
    rec["total_bytes"] = len(seen)
    rec["runs"] = []
    for base, raw in runs:
        r = {}
        r["base"] = "0x%x" % base
        r["length"] = len(raw)
        r["hex"] = raw.hex()
        r["objdump"] = disasm(base, raw)
        rec["runs"].append(r)
    out["blocks"].append(rec)

json.dump(out, open(outjson, "w"), indent=1)

for blk in out["blocks"]:
    print("")
    print("################ %s ################" % blk["header"])
    print("compiler=%s  bytes_recovered=%d  runs=%d"
          % (blk["compiler"], blk["total_bytes"], len(blk["runs"])))
    print("sections: %s" % ", ".join(blk["sections"]))
    for c in blk["comments"]:
        print("  %s" % c)
    print("  --- the JVM's own annotations (its testimony) ---")
    for a, t in blk["annotations"]:
        print("    %s  %s" % (a, t))
    for r in blk["runs"]:
        print("  --- objdump reading of run at %s (%d bytes) ---"
              % (r["base"], r["length"]))
        for ln in r["objdump"]:
            print("    %s" % ln)
PYEOF

echo ""
echo "######## carve ########"
python3 carve.py "$O/dump_raw.txt" "$O/nmethods.json" \
  > "$O/carved.txt" 2>&1
echo "carve exit=$?"
cat "$O/carved.txt"

echo "=== jvm_b_carve done ==="
date -u +%Y-%m-%dT%H:%M:%SZ
