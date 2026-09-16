// probe 864 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_864(int64_t a, int32_t b)
{
    return a bitor b;
}
