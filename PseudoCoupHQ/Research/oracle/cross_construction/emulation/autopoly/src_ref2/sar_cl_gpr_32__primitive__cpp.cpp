// probe 714 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_sar_cl_gpr_32__primitive__cpp(int32_t a, int32_t b)
{
    return a >> b;
}
