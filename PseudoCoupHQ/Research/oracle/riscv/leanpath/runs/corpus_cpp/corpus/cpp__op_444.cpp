// probe 444 -- binary &
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_444(float a, int32_t b)
{
    return a & b;
}
