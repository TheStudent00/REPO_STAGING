// probe 9 -- unary ~
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_9(float a)
{
    return ~a;
}
