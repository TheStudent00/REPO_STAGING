#!/bin/sh
# JIT track -- JVM pilot, LANE SMOKE.
# Proves: java runs; the probe compiles; and reports whether the JDK
# ships an hsdis disassembler plugin (Plan A) before any long lane.
set -u
echo "=== jvm_smoke ==="
date -u +%Y-%m-%dT%H:%M:%SZ

echo "--- which java/javac ---"
command -v java
command -v javac
echo "--- java -version ---"
java -version 2>&1
echo "--- javac -version ---"
javac -version 2>&1
echo "--- java -XshowSettings:properties (vendor/home/vm) ---"
java -XshowSettings:properties -version 2>&1 | grep -Ei \
  'java.vendor|java.version|java.home|java.vm.name|java.vm.version|os.arch'

JH=`java -XshowSettings:properties -version 2>&1 | \
    grep -E 'java.home' | head -1 | sed 's/.*= *//'`
echo "JAVA_HOME detected = $JH"

echo "--- hsdis present in the JDK? (Plan A probe) ---"
find "$JH" -name 'hsdis*' 2>/dev/null
echo "(end of hsdis find; empty means none shipped)"
echo "--- JDK lib dir listing ---"
ls "$JH/lib" 2>/dev/null | head -40

echo "--- toolchain for a possible Plan B (hsdis build) ---"
for t in gcc make binutils-version objdump nm ar autoconf git; do
  printf '  %s : ' "$t"
  command -v "$t" || echo MISSING
done
echo "  objdump -v:"
objdump -v 2>&1 | head -2
echo "  binutils dev headers (dis-asm.h):"
find / -name 'dis-asm.h' -not -path '*/proc/*' 2>/dev/null | head -5
echo "(end dis-asm.h find)"

echo "--- the probe source ---"
W=/work/jvmsmoke
rm -rf "$W"; mkdir -p "$W"
cd "$W" || exit 4
cat > Probe.java <<'EOF'
public class Probe {
    static int af(int a, int b) {
        return a + b;
    }
    static int af2(int a, int b) {
        return a / b;
    }
    public static void main(String[] args) {
        int n = 200000;
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
        System.out.println("acc=" + acc + " acc2=" + acc2);
    }
}
EOF
cat Probe.java
echo "--- javac ---"
javac Probe.java 2>&1
echo "javac exit=$?"
ls -la

echo "--- javap -c (the bytecode middle form) ---"
javap -c -p Probe 2>&1

echo "--- run, plain ---"
java Probe 2>&1

echo "--- PrintCompilation, first 30 lines (does it tier?) ---"
java -XX:+PrintCompilation Probe 2>&1 | head -30

echo "--- PrintAssembly attempt WITHOUT hsdis (what does it actually say?) ---"
java -XX:+UnlockDiagnosticVMOptions -XX:+PrintAssembly Probe 2>&1 | head -25

echo "--- PrintOptoAssembly attempt (Plan C probe) ---"
java -XX:+UnlockDiagnosticVMOptions -XX:-TieredCompilation \
  -XX:CompileCommand=print,Probe::af Probe 2>&1 | head -40

echo "=== jvm_smoke done ==="
date -u +%Y-%m-%dT%H:%M:%SZ
