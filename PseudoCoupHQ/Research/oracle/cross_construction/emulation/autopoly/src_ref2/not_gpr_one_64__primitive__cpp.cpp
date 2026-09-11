// probe 31 -- unary compl
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_not_gpr_one_64__primitive__cpp(int64_t a)
{
    return compl a;
}
