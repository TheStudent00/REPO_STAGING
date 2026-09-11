// probe 253 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_idiv_gpr_one_64__primitive__cpp(int64_t a, int64_t b)
{
    return a % b;
}
