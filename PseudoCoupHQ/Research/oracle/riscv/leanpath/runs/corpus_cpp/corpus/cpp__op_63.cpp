// probe 63 -- unary sizeof
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_63(float a)
{
    return sizeof a;
}
