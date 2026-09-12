// probe 30 -- unary compl
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_not_gpr_one_32__primitive__cpp(int32_t a)
{
    return compl a;
}
