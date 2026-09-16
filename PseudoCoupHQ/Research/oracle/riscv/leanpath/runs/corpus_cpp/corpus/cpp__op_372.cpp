// probe 372 -- binary |
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_372(float a, int32_t b)
{
    return a | b;
}
