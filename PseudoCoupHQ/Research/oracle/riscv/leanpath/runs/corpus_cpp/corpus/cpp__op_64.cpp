// probe 64 -- unary sizeof
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_64(double a)
{
    return sizeof a;
}
