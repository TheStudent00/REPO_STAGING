// probe 12 -- unary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_neg_gpr_one_32__primitive__cpp(int32_t a)
{
    return -a;
}
