// probe 662 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_662(float a, uint64_t b)
{
    return a < b;
}
