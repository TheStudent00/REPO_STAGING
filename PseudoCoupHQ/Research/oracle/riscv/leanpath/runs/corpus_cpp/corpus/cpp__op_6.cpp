// probe 6 -- unary ~
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_6(int32_t a)
{
    return ~a;
}
