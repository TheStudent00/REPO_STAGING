#!/bin/sh
# lap 5 smoke -- is the daemon alive, and which toolchains does the
# container hold for jobs 2 (C++ ordering probe) and 4 (compound
# assignment for c/cpp/go/rust/swift)?
set -u
echo "=== lap5_smoke ==="
date -u +%Y-%m-%dT%H:%M:%SZ
O=/out/lap5_smoke
rm -rf "$O"; mkdir -p "$O"

for t in clang clang++ gcc g++ go rustc swiftc objdump java python3; do
    printf '%-10s ' "$t"
    if command -v "$t" >/dev/null 2>&1; then
        "$t" --version 2>&1 | head -1
    else
        echo MISSING
    fi
done | tee "$O/toolchains.txt"

echo ""
echo "--- does this clang++ have <compare> at C++20? ---"
cat > /work/cmp_probe_smoke.cpp <<'EOF'
#include <compare>
int main() { return 0; }
EOF
clang++ -std=c++20 -c /work/cmp_probe_smoke.cpp -o /work/cmp_probe_smoke.o \
    2>&1 | head -20
echo "compare_header_exit=$?"
echo done
