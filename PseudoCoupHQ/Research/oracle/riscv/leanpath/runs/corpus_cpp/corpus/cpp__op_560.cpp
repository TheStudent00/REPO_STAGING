// probe 560 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_560(double a, uint64_t b)
{
    return a > b;
}
