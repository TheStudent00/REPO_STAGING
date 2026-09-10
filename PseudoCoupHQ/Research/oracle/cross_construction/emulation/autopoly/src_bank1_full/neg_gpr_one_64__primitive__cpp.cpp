// probe 13 -- unary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_neg_gpr_one_64__primitive__cpp(int64_t a)
{
    return -a;
}
