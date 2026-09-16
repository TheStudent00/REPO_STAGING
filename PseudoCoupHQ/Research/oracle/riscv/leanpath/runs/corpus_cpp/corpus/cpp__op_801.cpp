// probe 801 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_801(uint64_t a, float b)
{
    return a or b;
}
