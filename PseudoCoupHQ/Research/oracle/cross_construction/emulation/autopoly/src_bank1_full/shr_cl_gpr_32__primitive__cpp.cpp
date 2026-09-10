// probe 744 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_shr_cl_gpr_32__primitive__cpp(bool a, int32_t b)
{
    return a >> b;
}
