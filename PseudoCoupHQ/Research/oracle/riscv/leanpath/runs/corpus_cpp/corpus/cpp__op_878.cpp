// probe 878 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_878(float a, uint64_t b)
{
    return a bitor b;
}
