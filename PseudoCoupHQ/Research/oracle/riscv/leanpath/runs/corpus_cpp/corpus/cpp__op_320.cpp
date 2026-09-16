// probe 320 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_320(int32_t a, uint64_t b)
{
    return a && b;
}
