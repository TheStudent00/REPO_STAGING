// probe 151 -- binary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_151(uint64_t a, int64_t b)
{
    return a - b;
}
