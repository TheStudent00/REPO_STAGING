// probe 29 -- unary not
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_xor_imm_gpr_8__primitive__cpp(bool a)
{
    return not a;
}
