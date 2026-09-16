// probe 477 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_477(uint64_t a, float b)
{
    return a == b;
}
