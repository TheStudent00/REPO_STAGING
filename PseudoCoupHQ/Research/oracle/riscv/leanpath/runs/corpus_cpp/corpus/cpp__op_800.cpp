// probe 800 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_800(uint64_t a, uint64_t b)
{
    return a or b;
}
