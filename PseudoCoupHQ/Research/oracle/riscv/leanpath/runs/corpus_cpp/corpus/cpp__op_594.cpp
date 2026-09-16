// probe 594 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_594(double a, int32_t b)
{
    return a >= b;
}
