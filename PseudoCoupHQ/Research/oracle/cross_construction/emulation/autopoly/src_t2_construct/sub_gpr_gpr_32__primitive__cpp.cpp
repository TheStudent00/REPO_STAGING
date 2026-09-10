// probe 138 -- binary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_sub_gpr_gpr_32__primitive__cpp(int32_t a, int32_t b)
{
    return a - b;
}
