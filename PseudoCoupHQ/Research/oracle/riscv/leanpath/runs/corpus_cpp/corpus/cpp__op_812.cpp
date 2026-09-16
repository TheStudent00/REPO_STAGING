// probe 812 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_812(double a, uint64_t b)
{
    return a or b;
}
