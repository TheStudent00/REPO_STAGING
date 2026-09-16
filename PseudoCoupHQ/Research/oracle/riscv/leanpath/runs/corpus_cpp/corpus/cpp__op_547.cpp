// probe 547 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_547(uint64_t a, int64_t b)
{
    return a > b;
}
