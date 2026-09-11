// probe 727 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_shr_cl_gpr_64__primitive__cpp(uint64_t a, int64_t b)
{
    return a >> b;
}
