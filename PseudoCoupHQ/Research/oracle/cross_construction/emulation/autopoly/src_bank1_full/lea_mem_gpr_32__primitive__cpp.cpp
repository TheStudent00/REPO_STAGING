// probe 54 -- unary --
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_lea_mem_gpr_32__primitive__cpp(int32_t a)
{
    return --a;
}
