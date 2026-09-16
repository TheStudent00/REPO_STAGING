// probe 549 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_549(uint64_t a, float b)
{
    return a > b;
}
