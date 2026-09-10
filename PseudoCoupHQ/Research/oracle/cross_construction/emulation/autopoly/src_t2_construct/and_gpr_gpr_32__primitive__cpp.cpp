// probe 426 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_and_gpr_gpr_32__primitive__cpp(int32_t a, int32_t b)
{
    return a & b;
}
