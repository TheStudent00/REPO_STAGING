// probe 630 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_630(double a, int32_t b)
{
    return a <= b;
}
