// probe 811 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_811(double a, int64_t b)
{
    return a or b;
}
