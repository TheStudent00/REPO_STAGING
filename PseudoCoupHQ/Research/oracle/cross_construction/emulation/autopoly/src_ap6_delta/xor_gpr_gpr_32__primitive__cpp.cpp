// probe 390 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_xor_gpr_gpr_32__primitive__cpp(int32_t a, int32_t b)
{
    return a ^ b;
}
