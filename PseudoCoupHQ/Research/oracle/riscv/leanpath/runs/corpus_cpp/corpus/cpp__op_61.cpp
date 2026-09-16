// probe 61 -- unary sizeof
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_61(int64_t a)
{
    return sizeof a;
}
