// probe 62 -- unary sizeof
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_62(uint64_t a)
{
    return sizeof a;
}
