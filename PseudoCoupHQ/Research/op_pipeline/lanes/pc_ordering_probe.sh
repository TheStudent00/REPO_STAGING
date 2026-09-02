#!/bin/sh
# pc_ordering_probe -- what IS a std::partial_ordering, in bits?
#
# Why this lane exists.  dominance.py's projection table names a bit
# width per result type, and refuses to invent one:
#
#   "A result type this table does not name gets NO projection.  ...
#    Reading, say, `partial_ordering` as "some number of bits" would be
#    human interpretation of stated design, the weakest evidence class,
#    and this file does not do it."
#
# 156 class pairs are stuck behind exactly that refusal (140 on
# partial_ordering, 16 on strong_ordering).  This lane replaces the
# interpretation with a measurement, in two independent readings:
#
#   READING A -- the object representation, at run time.  Each named
#   constant is memcpy'd into an unsigned char array and every byte is
#   printed, with sizeof.  This is the compiler's own layout, executed.
#
#   READING B -- the emitted code.  A function per constant, returning
#   it, compiled at -O0 and at -O2 and disassembled.  The immediate the
#   compiler moves into the result register IS the value, forced by
#   construction: nothing else explains that byte.
#
# Both readings are printed raw.  Nothing here assumes -1/0/1.
set -u
echo "=== pc_ordering_probe ==="
date -u +%Y-%m-%dT%H:%M:%SZ

W=/work/ordering
rm -rf "$W"; mkdir -p "$W"
cd "$W" || exit 4
O=/out/ordering
rm -rf "$O"; mkdir -p "$O"

if ! /usr/bin/clang++ --version >/dev/null 2>&1; then
  echo "!! REFUSING TO START: /usr/bin/clang++ is not runnable."
  exit 4
fi
echo "--- the compiler, named on the record ---"
/usr/bin/clang++ --version 2>&1 | head -3 | tee "$O/compiler.txt"
objdump --version 2>&1 | head -1 | tee -a "$O/compiler.txt"

# ---------------------------------------------------------------- A
cat > rep.cpp <<'EOF'
#include <compare>
#include <cstddef>
#include <cstdio>
#include <cstring>

template <class T>
static void show(const char *family, const char *name, T value)
{
    unsigned char raw[sizeof(T)];
    std::memcpy(raw, &value, sizeof(T));
    std::printf("%s %s sizeof=%zu bytes=", family, name, sizeof(T));
    for (std::size_t i = 0; i < sizeof(T); i = i + 1) {
        std::printf(" %02x", raw[i]);
    }
    std::printf("  as_signed_char=%d\n", (int)(signed char)raw[0]);
}

int main()
{
    show("partial_ordering", "less", std::partial_ordering::less);
    show("partial_ordering", "equivalent",
         std::partial_ordering::equivalent);
    show("partial_ordering", "greater", std::partial_ordering::greater);
    show("partial_ordering", "unordered",
         std::partial_ordering::unordered);
    show("weak_ordering", "less", std::weak_ordering::less);
    show("weak_ordering", "equivalent", std::weak_ordering::equivalent);
    show("weak_ordering", "greater", std::weak_ordering::greater);
    show("strong_ordering", "less", std::strong_ordering::less);
    show("strong_ordering", "equal", std::strong_ordering::equal);
    show("strong_ordering", "equivalent",
         std::strong_ordering::equivalent);
    show("strong_ordering", "greater", std::strong_ordering::greater);
    return 0;
}
EOF

echo ""
echo "--- READING A: the object representation, executed ---"
/usr/bin/clang++ -std=c++20 -O0 -o rep rep.cpp 2>&1 | head -20
if [ ! -x ./rep ]; then
  echo "!! REFUSING: the representation probe did not build."
  exit 5
fi
./rep | tee "$O/representation.txt"

# ---------------------------------------------------------------- B
cat > emit.cpp <<'EOF'
#include <compare>

extern "C" std::partial_ordering p_less()
{
    return std::partial_ordering::less;
}
extern "C" std::partial_ordering p_equivalent()
{
    return std::partial_ordering::equivalent;
}
extern "C" std::partial_ordering p_greater()
{
    return std::partial_ordering::greater;
}
extern "C" std::partial_ordering p_unordered()
{
    return std::partial_ordering::unordered;
}
extern "C" std::strong_ordering s_less()
{
    return std::strong_ordering::less;
}
extern "C" std::strong_ordering s_equal()
{
    return std::strong_ordering::equal;
}
extern "C" std::strong_ordering s_greater()
{
    return std::strong_ordering::greater;
}
EOF

echo ""
echo "--- READING B: the emitted code, -O2 (SHIP) ---"
/usr/bin/clang++ -std=c++20 -O2 -c -o emit_ship.o emit.cpp 2>&1 | head -20
objdump -d --no-show-raw-insn emit_ship.o | tee "$O/emit_ship.txt"

echo ""
echo "--- READING B: the emitted code, -O0 (ANCHOR) ---"
/usr/bin/clang++ -std=c++20 -O0 -c -o emit_anchor.o emit.cpp 2>&1 | head -20
objdump -d --no-show-raw-insn emit_anchor.o | tee "$O/emit_anchor.txt"

# ------------------------------------------- what a <=> actually is
cat > spaceship.cpp <<'EOF'
#include <compare>
#include <cstdint>

extern "C" auto sp_i32(int32_t a, int32_t b)
{
    return a <=> b;
}
extern "C" auto sp_f64(double a, double b)
{
    return a <=> b;
}
EOF

echo ""
echo "--- the three-way comparison itself, -O2 ---"
/usr/bin/clang++ -std=c++20 -O2 -c -o sp.o spaceship.cpp 2>&1 | head -20
objdump -d --no-show-raw-insn sp.o | tee "$O/spaceship.txt"

echo ""
ls -la "$O"
date -u +%Y-%m-%dT%H:%M:%SZ
echo "=== pc_ordering_probe done ==="
exit 0
