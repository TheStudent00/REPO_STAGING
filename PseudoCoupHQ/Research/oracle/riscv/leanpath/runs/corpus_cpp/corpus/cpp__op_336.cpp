// probe 336 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_336(float a, int32_t b)
{
    return a && b;
}
