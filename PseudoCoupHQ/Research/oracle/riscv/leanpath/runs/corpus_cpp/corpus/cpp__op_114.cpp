// probe 114 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_114(uint64_t a, int32_t b)
{
    return a + b;
}
