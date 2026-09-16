// probe 60 -- unary sizeof
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_60(int32_t a)
{
    return sizeof a;
}
