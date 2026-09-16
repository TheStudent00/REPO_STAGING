// probe 550 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_550(uint64_t a, double b)
{
    return a > b;
}
