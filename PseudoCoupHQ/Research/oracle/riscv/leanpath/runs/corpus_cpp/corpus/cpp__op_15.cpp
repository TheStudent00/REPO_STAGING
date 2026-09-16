// probe 15 -- unary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_15(float a)
{
    return -a;
}
