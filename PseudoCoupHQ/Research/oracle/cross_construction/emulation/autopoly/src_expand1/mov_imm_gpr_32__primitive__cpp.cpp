// probe 61 -- unary sizeof
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
emu_mov_imm_gpr_32__primitive__cpp(int64_t a)
{
    return sizeof a;
}
