// probe 788 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_788(int32_t a, uint64_t b)
{
    return a or b;
}
