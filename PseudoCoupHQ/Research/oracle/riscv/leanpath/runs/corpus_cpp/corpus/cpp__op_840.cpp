// probe 840 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_840(float a, int32_t b)
{
    return a and b;
}
