// probe 65 -- unary sizeof
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_65(bool a)
{
    return sizeof a;
}
