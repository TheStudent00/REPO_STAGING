// probe 433 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_and_gpr_gpr_64__primitive__cpp(int64_t a, int64_t b)
{
    return a & b;
}
