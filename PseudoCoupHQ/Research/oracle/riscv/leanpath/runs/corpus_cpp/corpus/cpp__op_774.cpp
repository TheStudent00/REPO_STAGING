// probe 774 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_774(double a, int32_t b)
{
    return a <=> b;
}
