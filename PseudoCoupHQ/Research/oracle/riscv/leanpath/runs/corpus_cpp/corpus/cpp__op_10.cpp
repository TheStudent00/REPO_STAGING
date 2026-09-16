// probe 10 -- unary ~
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_10(double a)
{
    return ~a;
}
