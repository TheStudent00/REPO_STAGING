// probe 55 -- unary --
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_lea_mem_gpr_64__primitive__cpp(int64_t a)
{
    return --a;
}
