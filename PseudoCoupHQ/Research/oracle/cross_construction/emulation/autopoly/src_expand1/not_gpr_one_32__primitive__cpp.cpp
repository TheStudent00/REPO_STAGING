// probe 11 -- unary ~
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_not_gpr_one_32__primitive__cpp(bool a)
{
    return ~a;
}
