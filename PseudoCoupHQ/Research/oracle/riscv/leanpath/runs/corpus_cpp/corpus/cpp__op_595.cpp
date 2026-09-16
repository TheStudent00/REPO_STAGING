// probe 595 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_595(double a, int64_t b)
{
    return a >= b;
}
