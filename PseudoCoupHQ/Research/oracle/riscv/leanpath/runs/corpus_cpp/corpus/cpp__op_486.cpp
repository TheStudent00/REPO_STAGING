// probe 486 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_486(double a, int32_t b)
{
    return a == b;
}
