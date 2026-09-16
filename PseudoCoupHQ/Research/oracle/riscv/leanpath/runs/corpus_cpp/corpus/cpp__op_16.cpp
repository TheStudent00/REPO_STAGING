// probe 16 -- unary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_16(double a)
{
    return -a;
}
