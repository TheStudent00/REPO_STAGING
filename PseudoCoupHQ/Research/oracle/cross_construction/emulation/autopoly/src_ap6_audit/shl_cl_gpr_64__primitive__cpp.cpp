// probe 684 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_shl_cl_gpr_64__primitive__cpp(int64_t a, int32_t b)
{
    return a << b;
}
