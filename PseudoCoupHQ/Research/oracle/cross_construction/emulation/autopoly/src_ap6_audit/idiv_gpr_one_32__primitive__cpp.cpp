// probe 246 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_idiv_gpr_one_32__primitive__cpp(int32_t a, int32_t b)
{
    return a % b;
}
