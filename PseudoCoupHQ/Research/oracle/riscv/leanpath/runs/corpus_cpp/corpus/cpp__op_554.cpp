// probe 554 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_554(float a, uint64_t b)
{
    return a > b;
}
