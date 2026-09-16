// probe 381 -- binary |
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_381(double a, float b)
{
    return a | b;
}
