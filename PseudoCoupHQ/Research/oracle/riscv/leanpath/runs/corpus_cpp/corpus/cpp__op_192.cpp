// probe 192 -- binary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_192(float a, int32_t b)
{
    return a * b;
}
