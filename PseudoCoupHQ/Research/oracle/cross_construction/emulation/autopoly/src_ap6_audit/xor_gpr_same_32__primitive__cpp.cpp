// probe 251 -- binary %
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_xor_gpr_same_32__primitive__cpp(int32_t a, bool b)
{
    return a % b;
}
