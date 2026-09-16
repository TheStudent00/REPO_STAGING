// probe 8 -- unary ~
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_8(uint64_t a)
{
    return ~a;
}
